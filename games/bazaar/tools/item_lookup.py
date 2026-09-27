#!/usr/bin/env python3
"""Look up items and keywords from The Bazaar (Tempo Storm) using the game's
own local cache files - no web fetch required.

Data sources (read-only):
  GameData.db   - %USERPROFILE%\\AppData\\LocalLow\\Tempo Storm\\The Bazaar\\prod\\cache\\GameData.db
                  (SQLite; tables "cards" and "tooltips", each row Id TEXT,
                  Data BLOB where Data is UTF-8 JSON. THIS IS THE DEFAULT AND
                  LIVE SOURCE - see staleness note below.)
  cards.json    - ...\\prod\\cache\\cards.json    (older flat-file cache; --cards override only)
  tooltips.json - ...\\prod\\cache\\tooltips.json (older flat-file cache; --tooltips override only)

STALENESS FINDING (checked directly against this machine's cache on the day
this tool was written): cards.json's mtime is months behind GameData.db's
mtime, and comparing the two sources' copy of "Apothecary" shows the JSON
file is missing an entire generation of the item's kit (it has 3 abilities/
tooltips where the db has 5 - no separate Burn/Poison base stats, wrong
Charge-trigger list). GameData.db is the live source; cards.json is a stale
leftover. The database is therefore the default for both items ("cards"
table) and the keyword glossary ("tooltips" table, a single row whose Data
is a dict keyed by keyword id - same fields as tooltips.json's list entries,
just a dict instead of a list, and with more entries).  --cards/--tooltips
accept an explicit override path to either a .db (read via sqlite3) or a
.json (read via the old flat-file loader) file, auto-detected by extension.

The .json flat-file caches are each a single versioned dict:
{"<version>": [ ...records... ]}. GameData.db's tables carry no such
version wrapper - each row's Data blob IS one record directly (though the
record itself still carries its own "Version" field, e.g. "5.0.0").

Schema notes discovered by inspecting the live cache (patch 5.0.0):
  - cards.json's list mixes several "Type" values (Item, Skill, EncounterStep,
    EventEncounter, CombatEncounter, PedestalEncounter, PlayerEffect,
    SocketEffect). Only Type == "Item" records are items.
  - An item has top-level "Tiers": {TierName: {"Attributes": {...},
    "AbilityIds": [...], "AuraIds": [...], "TooltipIds": [...]}, ...}.
    Tier names appear in the progression Bronze -> Silver -> Gold -> Diamond
    -> Legendary. A tier's "Attributes" dict holds only the keys that are NEW
    or CHANGED at that tier; the full attribute set at a given tier is the
    cascading merge of every present tier up to and including it, in that
    canonical order (confirmed against "Magnifying Glass", a Bronze-tier item
    whose Gold/Diamond tiers only redeclare the attributes that changed).
  - "Abilities" and "Auras" are flat dicts on the item itself (ids "0", "1",
    ... ), not per-tier; the tier's "AbilityIds"/"AuraIds"/"TooltipIds" name
    which of those apply and which Localization.Tooltips entries describe
    them. The numeric behaviour of an ability/aura at a given tier comes from
    that tier's merged Attributes, via a naming convention: an action whose
    "$type" is "TAction<Role><Effect>[Apply]" (Role in Player/Card/Game) reads
    its amount from attribute "<Effect>[Apply]Amount" and, if present, its
    target count from "<Effect>Targets". Attributes named Slow/Freeze/
    Haste/Charge (and CooldownMax) are stored in milliseconds and are
    rendered in seconds; other amounts (Regen/Heal/Shield/Poison/Burn/Damage/
    etc.) are stored and shown as plain numbers - confirmed by scanning every
    "*Amount"/"*Max" attribute key in the file for its value range.
  - "Enchantments" is a sibling of "Tiers" on the item: a flat dict keyed by
    enchant name (Golden, Heavy, Icy, Turbo, Shielded, Restorative, Toxic,
    Fiery, Shiny, Radiant, Deadly, Obsidian, Mossy, ...), each with its own
    (non-tiered) "Attributes", "Abilities", "Auras" and "Localization.
    Tooltips". Enchant tooltip placeholders of the form "{aura.<id>.mod}" (or
    "{ability.<id>.mod}") resolve to the fixed multiplier stored at
    Auras[id]["Action"]["Value"]["Modifier"]["Value"]["Value"] when that
    Value node is a "TReferenceValueCardAttribute" whose own Modifier is a
    "TFixedValue" - this is what lets "Shield equal to {aura.e2.mod} times
    this item's Regen" resolve to "5" without ever touching the attribute
    being multiplied (the multiplier is tier/attribute independent).
  - Tooltip placeholders seen across the whole file: "{ability.<id>}",
    "{aura.<id>}", "{ability.<id>.targets}" (also the rarer singular
    "target"), "{aura.<id>.mod}", and the rare "{ability.<id>.mod}". Any
    placeholder this tool cannot confidently resolve from static data (for
    example a value that depends on the player's own runtime stats, not the
    item's own attributes) is left untouched in the output, verbatim -
    never guessed.
  - tooltips.json's versioned list / GameData.db's "tooltips" row both hold
    keyword-glossary entries with fields Id, Tag, Keyword (the glossary
    text), Icon, Singleton, PostSymbol, PostWord, Version.
  - The db's item/skill/etc. JSON blobs are otherwise the same shape as the
    old JSON cache's records (Type, Tiers, Enchantments, Localization,
    Abilities, Auras, ...), plus a couple of fields the old cache didn't
    have (e.g. "SpawningEligibility", and a "Cost": null on many Action
    nodes) - none of which this tool's resolver reads, so no resolver logic
    needed to change, only the loading layer.

This file is stdlib-only, read-only, and loads each cache source once.
The SQLite connection is opened read-only and lock-free
(file:<path>?mode=ro&immutable=1) so it never blocks or is blocked by the
running game, and never writes, journals, or otherwise touches the db file.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sqlite3
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

TIER_ORDER = ["Bronze", "Silver", "Gold", "Diamond", "Legendary"]

# Attribute "effect stems" whose *Amount value is stored in milliseconds.
TIME_EFFECT_STEMS = {"Slow", "Freeze", "Haste", "Charge"}

PLACEHOLDER_RE = re.compile(r"\{(ability|aura)\.([^.{}]+)(?:\.([^{}]+))?\}")

_CACHE_DIR = os.path.join(
    os.environ.get("USERPROFILE", ""),
    "AppData", "LocalLow", "Tempo Storm", "The Bazaar", "prod", "cache",
)

# Live source (default for both --cards and --tooltips): one SQLite db with
# a "cards" table and a "tooltips" table.
DEFAULT_DB_PATH = os.path.join(_CACHE_DIR, "GameData.db")

# Older flat-file caches, kept only as documented fallback targets for an
# explicit --cards/--tooltips override.
DEFAULT_CARDS_JSON_PATH = os.path.join(_CACHE_DIR, "cards.json")
DEFAULT_TOOLTIPS_JSON_PATH = os.path.join(_CACHE_DIR, "tooltips.json")

DEFAULT_CARDS_PATH = DEFAULT_DB_PATH
DEFAULT_TOOLTIPS_PATH = DEFAULT_DB_PATH


def source_kind(path: str) -> str:
    """.db -> sqlite, anything else -> the old flat-file JSON loader."""
    return "sqlite" if path.lower().endswith(".db") else "json"


# --------------------------------------------------------------------------
# Loading + validation (fail loudly, per spec)
# --------------------------------------------------------------------------

def _pick_latest_version(keys: Iterable[str]) -> str:
    def version_tuple(v: str) -> Tuple[int, ...]:
        parts = []
        for piece in v.split("."):
            try:
                parts.append(int(piece))
            except ValueError:
                parts.append(0)
        return tuple(parts)

    keys = list(keys)
    try:
        return max(keys, key=version_tuple)
    except (ValueError, TypeError):
        return max(keys)


def load_versioned_list(path: str, label: str) -> Tuple[List[Any], str]:
    """Load a `{"<version>": [...]}` flat-file cache. Exits 2 on
    missing/unreadable file, exits 3 on any structure that isn't what's
    expected."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {label} file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except OSError as exc:
        print(f"ERROR: cannot read {label} file '{path}': {exc}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"ERROR: {label} file is not valid JSON: '{path}' ({exc})", file=sys.stderr)
        sys.exit(3)

    if not isinstance(raw, dict) or not raw:
        print(
            f"ERROR: unexpected top-level structure in {label} file '{path}' "
            "(expected a non-empty object mapping version -> list)",
            file=sys.stderr,
        )
        sys.exit(3)

    version = _pick_latest_version(raw.keys())
    data = raw.get(version)
    if not isinstance(data, list):
        print(
            f"ERROR: unexpected structure under version '{version}' in {label} "
            f"file '{path}' (expected a list, found {type(data).__name__})",
            file=sys.stderr,
        )
        sys.exit(3)
    return data, version


def _open_sqlite_readonly(path: str, label: str) -> sqlite3.Connection:
    """Open a SQLite db strictly read-only and lock-free, so this tool never
    blocks the running game and never writes/journals anything. Exits 2 if
    the file doesn't exist, exits 3 if it exists but isn't a readable db."""
    if not os.path.exists(path):
        print(f"ERROR: {label} file not found: {path}", file=sys.stderr)
        sys.exit(2)
    uri = "file:" + path.replace("\\", "/") + "?mode=ro&immutable=1"
    try:
        con = sqlite3.connect(uri, uri=True)
        con.execute("SELECT 1")  # forces the lazy open to happen now
    except sqlite3.Error as exc:
        print(f"ERROR: cannot open {label} database '{path}': {exc}", file=sys.stderr)
        sys.exit(3)
    return con


def _table_exists(con: sqlite3.Connection, table: str) -> bool:
    cur = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cur.fetchone() is not None


def load_items_sqlite(path: str) -> List[Dict[str, Any]]:
    con = _open_sqlite_readonly(path, "cards")
    try:
        if not _table_exists(con, "cards"):
            print(f"ERROR: '{path}' has no 'cards' table (schema may have changed)", file=sys.stderr)
            sys.exit(3)
        try:
            rows = con.execute("SELECT Id, Data FROM cards").fetchall()
        except sqlite3.Error as exc:
            print(f"ERROR: cannot read 'cards' table in '{path}': {exc}", file=sys.stderr)
            sys.exit(3)
    finally:
        con.close()

    items: List[Dict[str, Any]] = []
    decode_errors = 0
    for row_id, blob in rows:
        try:
            obj = json.loads(blob.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            decode_errors += 1
            continue
        if isinstance(obj, dict) and obj.get("Type") == "Item":
            items.append(obj)

    if decode_errors and decode_errors == len(rows):
        print(
            f"ERROR: none of the {len(rows)} rows in 'cards' table of '{path}' "
            "decoded as UTF-8 JSON (schema may have changed)",
            file=sys.stderr,
        )
        sys.exit(3)
    if not items:
        print(
            f"ERROR: no records with Type == 'Item' decoded from 'cards' table "
            f"in '{path}' (schema may have changed)",
            file=sys.stderr,
        )
        sys.exit(3)
    if not any("Tiers" in it for it in items):
        print(
            f"ERROR: item records in '{path}' are missing the expected 'Tiers' "
            "field (schema may have changed)",
            file=sys.stderr,
        )
        sys.exit(3)
    return items


def load_glossary_sqlite(path: str) -> List[Dict[str, Any]]:
    con = _open_sqlite_readonly(path, "tooltips")
    try:
        if not _table_exists(con, "tooltips"):
            print(f"ERROR: '{path}' has no 'tooltips' table (schema may have changed)", file=sys.stderr)
            sys.exit(3)
        try:
            row = con.execute("SELECT Data FROM tooltips LIMIT 1").fetchone()
        except sqlite3.Error as exc:
            print(f"ERROR: cannot read 'tooltips' table in '{path}': {exc}", file=sys.stderr)
            sys.exit(3)
    finally:
        con.close()

    if row is None:
        print(f"ERROR: 'tooltips' table in '{path}' is empty", file=sys.stderr)
        sys.exit(3)
    try:
        obj = json.loads(row[0].decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: 'tooltips' row in '{path}' is not valid UTF-8 JSON: {exc}", file=sys.stderr)
        sys.exit(3)

    if isinstance(obj, dict):
        entries = list(obj.values())
    elif isinstance(obj, list):
        entries = obj
    else:
        print(
            f"ERROR: unexpected 'tooltips' row structure in '{path}' "
            f"(expected a dict or list, found {type(obj).__name__})",
            file=sys.stderr,
        )
        sys.exit(3)

    if not entries or not isinstance(entries[0], dict) or "Keyword" not in entries[0]:
        print(
            f"ERROR: glossary entries in '{path}' are missing the expected "
            "'Keyword' field (schema may have changed)",
            file=sys.stderr,
        )
        sys.exit(3)
    return entries


def load_items(path: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if source_kind(path) == "sqlite":
        items = load_items_sqlite(path)
    else:
        records, _version = load_versioned_list(path, "cards")
        items = [r for r in records if isinstance(r, dict) and r.get("Type") == "Item"]
        if not items:
            print(
                f"ERROR: no records with Type == 'Item' found in cards file '{path}' "
                "(schema may have changed)",
                file=sys.stderr,
            )
            sys.exit(3)
        if not any("Tiers" in it for it in items):
            print(
                f"ERROR: item records in '{path}' are missing the expected 'Tiers' "
                "field (schema may have changed)",
                file=sys.stderr,
            )
            sys.exit(3)
    return items, source_meta(path, len(items))


def load_glossary(path: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if source_kind(path) == "sqlite":
        entries = load_glossary_sqlite(path)
    else:
        records, _version = load_versioned_list(path, "tooltips")
        if not records or not isinstance(records[0], dict) or "Keyword" not in records[0]:
            print(
                f"ERROR: glossary records in '{path}' are missing the expected "
                "'Keyword' field (schema may have changed)",
                file=sys.stderr,
            )
            sys.exit(3)
        entries = records
    return entries, source_meta(path, len(entries))


# --------------------------------------------------------------------------
# Source metadata / staleness header (spec: print on every text run)
# --------------------------------------------------------------------------

def _fmt_mtime(path: str) -> Optional[str]:
    try:
        ts = os.path.getmtime(path)
    except OSError:
        return None
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def source_meta(path: str, count: int) -> Dict[str, Any]:
    return {"path": path, "mtime": _fmt_mtime(path), "count": count, "kind": source_kind(path)}


def print_source_header(meta: Dict[str, Any], noun: str) -> None:
    mtime = meta["mtime"] or "unknown mtime"
    print(f"[source: {meta['path']} | mtime: {mtime} | {noun}: {meta['count']}]")


def warn_if_zip_newer(db_path: str) -> None:
    """GameData.db ships alongside GameData.db.zip (the last downloaded
    archive). If the zip is newer than the live db file, the db itself may
    be stale relative to what's actually been downloaded - flag it, but
    never touch/extract the zip."""
    if source_kind(db_path) != "sqlite":
        return
    zip_path = db_path + ".zip"
    if not os.path.exists(zip_path):
        return
    try:
        db_mtime = os.path.getmtime(db_path)
        zip_mtime = os.path.getmtime(zip_path)
    except OSError:
        return
    if zip_mtime > db_mtime:
        print(
            f"WARNING: '{zip_path}' is newer than '{db_path}' - the database "
            "may be stale relative to the last download.",
            file=sys.stderr,
        )


# --------------------------------------------------------------------------
# Number / attribute helpers
# --------------------------------------------------------------------------

def fmt_num(v: Any) -> str:
    if v is None:
        return "?"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, float):
        if v == int(v):
            return str(int(v))
        return f"{v:g}"
    return str(v)


def merge_tier_attributes(tiers: Dict[str, Any], upto_tier: str) -> Dict[str, Any]:
    """Cascading merge of Attributes across TIER_ORDER, stopping after
    upto_tier. Tiers absent from `tiers` are simply skipped."""
    merged: Dict[str, Any] = {}
    for t in TIER_ORDER:
        if t in tiers:
            merged.update((tiers[t] or {}).get("Attributes") or {})
        if t == upto_tier:
            break
    return merged


def present_tiers(tiers: Dict[str, Any]) -> List[str]:
    return [t for t in TIER_ORDER if t in tiers]


def action_base_name(type_name: str) -> str:
    """'TActionPlayerRegenApply' -> 'RegenApply'; 'TActionCardSlow' -> 'Slow'."""
    s = type_name or ""
    if s.startswith("TAction"):
        s = s[len("TAction"):]
    for role in ("Player", "Card", "Game"):
        if s.startswith(role):
            s = s[len(role):]
            break
    return s


def _amount_and_stem(base: str) -> Tuple[str, str]:
    stem = base[:-6] if base.endswith("Amount") else base
    amount_key = base if base.endswith("Amount") else base + "Amount"
    return amount_key, stem


# Full attribute names (as opposed to the Slow/Freeze/Haste/Charge *stems*
# above) that are also millisecond durations. Found by inspecting abilities/
# auras that hardcode a raw duration constant directly against one of these
# named attributes (e.g. Outlands Terror's "FlatCooldownReduction" aura,
# InternalDescription "reduced by 3 seconds" backed by a literal TFixedValue
# of 3000; "[DEBUG] Decharge Test"'s ability targeting bare "Cooldown" with
# InternalDescription "... {ability.0} second(s)" backed by 3000) rather
# than going through an item's own *Amount attribute.
TIME_ATTRIBUTE_NAMES = {"CooldownMax", "FlatCooldownReduction", "Cooldown"}


def _attr_is_time(attr_or_stem: str) -> bool:
    """True if a bare attribute name/stem (e.g. 'SlowAmount', 'Slow',
    'CooldownMax', 'FlatCooldownReduction') is a millisecond duration that
    should be rendered in seconds."""
    if not attr_or_stem:
        return False
    if attr_or_stem in TIME_ATTRIBUTE_NAMES:
        return True
    stem = attr_or_stem[:-6] if attr_or_stem.endswith("Amount") else attr_or_stem
    return stem in TIME_EFFECT_STEMS


def resolve_ability_plain(ability: Dict[str, Any], attrs: Dict[str, Any]) -> Optional[float]:
    action = ability.get("Action") or {}
    val = action.get("Value")

    # Generic actions ("TActionCardModifyAttribute" / "TActionPlayerModify-
    # Attribute") always carry their target attribute explicitly, exactly
    # like an aura's "AttributeType" - and are authoritative when present,
    # since the naming-convention guess below has no way to know a generic
    # action is secretly modifying, say, "FlatCooldownReduction" or bare
    # "Cooldown". Found via "[DEBUG] Decharge Test" (AttributeType
    # "Cooldown", constant 3000, InternalDescription "... {ability.0}
    # second(s)") and "Hands of Time" (AttributeType "FlatCooldownReduction",
    # constant 1000, InternalDescription "reduced by 1 second") - both were
    # rendering as raw uncoverted milliseconds before this branch existed.
    explicit_attr = action.get("AttributeType")
    if explicit_attr:
        if isinstance(val, dict) and val.get("$type") == "TFixedValue":
            v = val.get("Value")
        elif explicit_attr in attrs:
            v = attrs[explicit_attr]
        else:
            v = None
        if v is None:
            return None
        return v / 1000.0 if _attr_is_time(explicit_attr) else v

    base = action_base_name(action.get("$type") or "")
    amount_key, stem = _amount_and_stem(base) if base else (None, None)
    if isinstance(val, dict) and val.get("$type") == "TFixedValue":
        v = val.get("Value")
        if stem and _attr_is_time(stem):
            return v / 1000.0
        return v
    if amount_key and amount_key in attrs:
        v = attrs[amount_key]
        if _attr_is_time(stem):
            return v / 1000.0
        return v
    return None


def resolve_ability_targets(ability: Dict[str, Any], attrs: Dict[str, Any]) -> Optional[Any]:
    action = ability.get("Action") or {}

    # A hardcoded TargetCount (seen as a direct TFixedValue on generic
    # ModifyAttribute actions, e.g. Hands of Time's "TargetCount": {"$type":
    # "TFixedValue", "Value": 1.0}) takes precedence over any attribute
    # lookup, since it isn't backed by an item attribute at all.
    tc = action.get("TargetCount")
    if isinstance(tc, dict) and tc.get("$type") == "TFixedValue":
        return tc.get("Value")

    explicit_attr = action.get("AttributeType")
    if explicit_attr:
        return attrs.get(explicit_attr + "Targets")

    base = action_base_name(action.get("$type") or "")
    if not base:
        return None
    _, stem = _amount_and_stem(base)
    targets_key = stem + "Targets"
    return attrs.get(targets_key)


def resolve_aura_plain(aura: Dict[str, Any]) -> Optional[float]:
    action = aura.get("Action") or {}
    val = action.get("Value")
    if isinstance(val, dict) and val.get("$type") == "TFixedValue":
        v = val.get("Value")
        if _attr_is_time(action.get("AttributeType") or ""):
            return v / 1000.0
        return v
    return None


def resolve_mod_generic(node: Dict[str, Any]) -> Optional[float]:
    """Shared by ability.<id>.mod / aura.<id>.mod: find a
    TReferenceValueCardAttribute whose own Modifier.Value is a fixed
    constant, and return that constant (the multiplier), without needing
    to know or resolve the attribute it multiplies."""
    action = node.get("Action") or {}
    val = action.get("Value")
    if not isinstance(val, dict):
        rv = action.get("ReferenceValue")
        val = rv if isinstance(rv, dict) else None
    if isinstance(val, dict) and val.get("$type") == "TReferenceValueCardAttribute":
        modifier = val.get("Modifier") or {}
        mod_val = modifier.get("Value")
        if isinstance(mod_val, dict) and mod_val.get("$type") == "TFixedValue":
            return mod_val.get("Value")
    return None


# --------------------------------------------------------------------------
# Tooltip placeholder rendering
# --------------------------------------------------------------------------

def render_tooltip(
    text: str,
    resolve_fn,
    tier_names: List[str],
) -> str:
    """Replace every {ability.X[.suffix]} / {aura.X[.suffix]} placeholder.

    resolve_fn(kind, ident, suffix, tier_name) -> value or None.
    If any tier yields None for a placeholder, that placeholder is left
    untouched (raw). If all tiers agree, a single value is shown; if they
    differ, they're chained "v1 > v2 > v3" in tier order.
    """
    if not text:
        return text

    def repl(m: "re.Match[str]") -> str:
        kind, ident, suffix = m.group(1), m.group(2), m.group(3)
        values = []
        for tier in tier_names:
            v = resolve_fn(kind, ident, suffix, tier)
            if v is None:
                return m.group(0)
            values.append(v)
        strs = [fmt_num(v) for v in values]
        if all(s == strs[0] for s in strs):
            return strs[0]
        return " > ".join(strs)

    return PLACEHOLDER_RE.sub(repl, text)


def make_item_resolver(item: Dict[str, Any]):
    tiers = item.get("Tiers") or {}
    abilities = item.get("Abilities") or {}
    auras = item.get("Auras") or {}
    cache: Dict[str, Dict[str, Any]] = {}

    def attrs_for(tier: str) -> Dict[str, Any]:
        if tier not in cache:
            cache[tier] = merge_tier_attributes(tiers, tier)
        return cache[tier]

    def resolve(kind: str, ident: str, suffix: Optional[str], tier: str):
        node = (abilities if kind == "ability" else auras).get(ident)
        if node is None:
            return None
        attrs = attrs_for(tier)
        if kind == "ability":
            if suffix is None:
                return resolve_ability_plain(node, attrs)
            if suffix in ("targets", "target"):
                return resolve_ability_targets(node, attrs)
            if suffix == "mod":
                return resolve_mod_generic(node)
            return None
        else:
            if suffix is None:
                return resolve_aura_plain(node)
            if suffix == "mod":
                return resolve_mod_generic(node)
            return None

    return resolve


def make_enchant_resolver(ench: Dict[str, Any]):
    attrs = ench.get("Attributes") or {}
    abilities = ench.get("Abilities") or {}
    auras = ench.get("Auras") or {}

    def resolve(kind: str, ident: str, suffix: Optional[str], tier: str):
        node = (abilities if kind == "ability" else auras).get(ident)
        if node is None:
            return None
        if kind == "ability":
            if suffix is None:
                return resolve_ability_plain(node, attrs)
            if suffix in ("targets", "target"):
                return resolve_ability_targets(node, attrs)
            if suffix == "mod":
                return resolve_mod_generic(node)
            return None
        else:
            if suffix is None:
                return resolve_aura_plain(node)
            if suffix == "mod":
                return resolve_mod_generic(node)
            return None

    return resolve


# --------------------------------------------------------------------------
# Building display records
# --------------------------------------------------------------------------

def item_title(item: Dict[str, Any]) -> str:
    title = ((item.get("Localization") or {}).get("Title") or {}).get("Text")
    return title or item.get("InternalName") or "(untitled)"


def build_tier_data(item: Dict[str, Any], tier_list: List[str]) -> Dict[str, Dict[str, Any]]:
    tiers = item.get("Tiers") or {}
    out: Dict[str, Dict[str, Any]] = {}
    for t in tier_list:
        attrs = merge_tier_attributes(tiers, t)
        cooldown_ms = attrs.get("CooldownMax")
        out[t] = {
            "cooldown_seconds": (cooldown_ms / 1000.0) if isinstance(cooldown_ms, (int, float)) else None,
            "attributes": attrs,
        }
    return out


def build_tooltips(item: Dict[str, Any], tier_list: List[str]) -> List[Dict[str, str]]:
    tiers = item.get("Tiers") or {}
    loc_tooltips = (item.get("Localization") or {}).get("Tooltips") or []
    # Tooltip ids are consistent across tiers in every item observed; use the
    # first present tier's list to decide which localization entries apply.
    ids: List[int] = []
    for t in tier_list:
        tier_ids = (tiers.get(t) or {}).get("TooltipIds")
        if tier_ids:
            ids = tier_ids
            break
    resolver = make_item_resolver(item)
    out = []
    for idx in ids:
        if not isinstance(idx, int) or idx < 0 or idx >= len(loc_tooltips):
            continue
        entry = loc_tooltips[idx]
        raw = (entry.get("Content") or {}).get("Text") or ""
        resolved = render_tooltip(raw, resolver, tier_list)
        out.append({"raw": raw, "resolved": resolved, "type": entry.get("TooltipType")})
    return out


def build_enchantments(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    ench_dict = item.get("Enchantments") or {}
    out = []
    for name, ench in ench_dict.items():
        resolver = make_enchant_resolver(ench)
        tooltips = []
        loc_tooltips = (ench.get("Localization") or {}).get("Tooltips") or []
        for entry in loc_tooltips:
            raw = (entry.get("Content") or {}).get("Text") or ""
            resolved = render_tooltip(raw, resolver, ["_flat_"])
            tooltips.append({"raw": raw, "resolved": resolved, "type": entry.get("TooltipType")})
        out.append({
            "name": name,
            "tooltips": tooltips,
            "attributes": ench.get("Attributes") or {},
        })
    return out


def build_record(item: Dict[str, Any], include_raw: bool) -> Dict[str, Any]:
    tiers = item.get("Tiers") or {}
    tier_list = present_tiers(tiers)
    record = {
        "title": item_title(item),
        "internal_name": item.get("InternalName"),
        "heroes": item.get("Heroes") or [],
        "size": item.get("Size"),
        "starting_tier": item.get("StartingTier"),
        "tags": item.get("Tags") or [],
        "hidden_tags": item.get("HiddenTags") or [],
        "tiers": tier_list,
        "tier_data": build_tier_data(item, tier_list),
        "tooltips": build_tooltips(item, tier_list),
        "enchantments": build_enchantments(item),
    }
    if include_raw:
        record["raw_json"] = item
    return record


# --------------------------------------------------------------------------
# Filtering
# --------------------------------------------------------------------------

def name_matches(item: Dict[str, Any], query: str) -> bool:
    q = query.lower()
    title = ((item.get("Localization") or {}).get("Title") or {}).get("Text") or ""
    internal = item.get("InternalName") or ""
    return q in title.lower() or q in internal.lower()


def hero_matches(item: Dict[str, Any], query: str) -> bool:
    q = query.lower()
    return any(q == h.lower() for h in (item.get("Heroes") or []))


def size_matches(item: Dict[str, Any], query: str) -> bool:
    return (item.get("Size") or "").lower() == query.lower()


def tag_matches(item: Dict[str, Any], query: str) -> bool:
    q = query.lower()
    tags = [t.lower() for t in (item.get("Tags") or [])]
    hidden = [t.lower() for t in (item.get("HiddenTags") or [])]
    return q in tags or q in hidden


def _all_texts(item: Dict[str, Any]) -> List[str]:
    texts = []
    loc = item.get("Localization") or {}
    title = (loc.get("Title") or {}).get("Text")
    if title:
        texts.append(title)
    desc = (loc.get("Description") or {}).get("Text") if isinstance(loc.get("Description"), dict) else None
    if desc:
        texts.append(desc)
    flavor = (loc.get("FlavorText") or {}).get("Text") if isinstance(loc.get("FlavorText"), dict) else None
    if flavor:
        texts.append(flavor)
    for tt in loc.get("Tooltips") or []:
        t = (tt.get("Content") or {}).get("Text")
        if t:
            texts.append(t)
    for ench in (item.get("Enchantments") or {}).values():
        for tt in (ench.get("Localization") or {}).get("Tooltips") or []:
            t = (tt.get("Content") or {}).get("Text")
            if t:
                texts.append(t)
    return texts


def text_matches(item: Dict[str, Any], query: str) -> bool:
    q = query.lower()
    return any(q in t.lower() for t in _all_texts(item))


def filter_items(items: List[Dict[str, Any]], args: argparse.Namespace) -> List[Dict[str, Any]]:
    out = items
    if args.name:
        out = [it for it in out if name_matches(it, args.name)]
    if args.hero:
        out = [it for it in out if hero_matches(it, args.hero)]
    if args.size:
        out = [it for it in out if size_matches(it, args.size)]
    if args.tag:
        out = [it for it in out if tag_matches(it, args.tag)]
    if args.text:
        out = [it for it in out if text_matches(it, args.text)]
    return out


# --------------------------------------------------------------------------
# Text rendering
# --------------------------------------------------------------------------

def render_record_text(record: Dict[str, Any]) -> str:
    lines = []
    heroes = ", ".join(record["heroes"]) if record["heroes"] else "?"
    lines.append(
        f"{record['title']} · {heroes} · {record['size'] or '?'} · "
        f"Starting: {record['starting_tier'] or '?'}"
    )
    if record["internal_name"] and record["internal_name"] != record["title"]:
        lines.append(f"  InternalName: {record['internal_name']}")

    tags = ", ".join(record["tags"]) if record["tags"] else "(none)"
    lines.append(f"  Tags: {tags}")
    if record["hidden_tags"]:
        lines.append(f"  Hidden Tags: {', '.join(record['hidden_tags'])} [hidden]")

    for t in record["tiers"]:
        td = record["tier_data"][t]
        cd = td["cooldown_seconds"]
        cd_str = f"Cooldown {fmt_num(cd)}s" if cd is not None else "Cooldown -"
        attr_bits = []
        for k in sorted(td["attributes"]):
            if k == "CooldownMax":
                continue
            v = td["attributes"][k]
            if _attr_is_time(k) and isinstance(v, (int, float)):
                attr_bits.append(f"{k}={fmt_num(v / 1000.0)}s")
            else:
                attr_bits.append(f"{k}={fmt_num(v)}")
        attrs_str = ", ".join(attr_bits) if attr_bits else "(no attributes)"
        lines.append(f"  {t}: {cd_str} | {attrs_str}")

    if record["tooltips"]:
        lines.append("  Tooltips:")
        for tt in record["tooltips"]:
            lines.append(f"    - {tt['resolved']}")

    if record["enchantments"]:
        lines.append("  Enchantments:")
        for ench in record["enchantments"]:
            if ench["tooltips"]:
                for tt in ench["tooltips"]:
                    lines.append(f"    - {ench['name']}: {tt['resolved']}")
            elif ench["attributes"]:
                attr_bits = ", ".join(f"{k}={fmt_num(v)}" for k, v in sorted(ench["attributes"].items()))
                lines.append(f"    - {ench['name']}: [no tooltip text] {attr_bits}")
            else:
                lines.append(f"    - {ench['name']}: (no data)")

    if "raw_json" in record:
        lines.append("  --- RAW JSON ---")
        lines.append(json.dumps(record["raw_json"], indent=2, ensure_ascii=False))

    return "\n".join(lines)


# --------------------------------------------------------------------------
# Keyword glossary + hero listing
# --------------------------------------------------------------------------

def keyword_lookup(glossary: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    q = query.lower()
    matches = []
    for entry in glossary:
        ident = str(entry.get("Id") or "")
        tag = str(entry.get("Tag") or "")
        if q in ident.lower() or q in tag.lower():
            matches.append(entry)
    return matches


def list_heroes(items: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
    counts: Dict[str, int] = {}
    for it in items:
        for h in it.get("Heroes") or []:
            counts[h] = counts.get(h, 0) + 1
    return sorted(counts.items(), key=lambda kv: kv[0].lower())


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Look up items/keywords from The Bazaar's own local cache files.",
    )
    p.add_argument("--name", help="Case-insensitive substring match on item title (falls back to InternalName).")
    p.add_argument("--hero", help="Filter by hero (case-insensitive exact match, e.g. Mak, Common).")
    p.add_argument("--size", choices=["Small", "Medium", "Large", "small", "medium", "large"], help="Filter by item size.")
    p.add_argument("--tag", help="Filter by Tags or HiddenTags (case-insensitive exact match).")
    p.add_argument("--text", help="Case-insensitive substring match across tooltip/description text.")
    p.add_argument("--keyword", help="Look up a keyword in the glossary instead of items.")
    p.add_argument("--list-heroes", action="store_true", help="Print each hero and its item count.")
    p.add_argument("--raw", action="store_true", help="Also dump each matched item's full JSON.")
    p.add_argument("--json", action="store_true", help="Machine-readable JSON output instead of text.")
    p.add_argument(
        "--cards", default=DEFAULT_CARDS_PATH,
        help="Override path to the items source: GameData.db (sqlite, default) or cards.json "
             "(auto-detected by extension).",
    )
    p.add_argument(
        "--tooltips", default=DEFAULT_TOOLTIPS_PATH,
        help="Override path to the keyword-glossary source: GameData.db (sqlite, default) or "
             "tooltips.json (auto-detected by extension).",
    )
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.list_heroes:
        warn_if_zip_newer(args.cards)
        items, meta = load_items(args.cards)
        rows = list_heroes(items)
        if args.json:
            print(json.dumps(
                {"_source": meta, "heroes": [{"hero": h, "count": c} for h, c in rows]},
                indent=2, ensure_ascii=False,
            ))
        else:
            print_source_header(meta, "items")
            for h, c in rows:
                print(f"{h}: {c}")
        return 0

    if args.keyword:
        warn_if_zip_newer(args.tooltips)
        glossary, meta = load_glossary(args.tooltips)
        matches = keyword_lookup(glossary, args.keyword)
        if args.json:
            print(json.dumps({"_source": meta, "matches": matches}, indent=2, ensure_ascii=False))
        else:
            print_source_header(meta, "keywords")
            if not matches:
                print(f"No glossary entries matched '{args.keyword}'.")
            for entry in matches:
                tag = entry.get("Tag") or entry.get("Id") or "?"
                print(f"{tag}: {entry.get('Keyword') or '(no description)'}")
        return 0

    has_filter = any([args.name, args.hero, args.size, args.tag, args.text])
    if not has_filter:
        parser.print_usage(sys.stderr)
        print(
            "ERROR: at least one filter is required (--name/--hero/--size/--tag/--text), "
            "or use --keyword / --list-heroes.",
            file=sys.stderr,
        )
        return 1

    warn_if_zip_newer(args.cards)
    items, meta = load_items(args.cards)
    matched = filter_items(items, args)
    records = [build_record(it, include_raw=args.raw) for it in matched]

    if args.json:
        print(json.dumps({"_source": meta, "items": records}, indent=2, ensure_ascii=False))
    else:
        print_source_header(meta, "items")
        if not records:
            print("No items matched.")
        for i, rec in enumerate(records):
            if i:
                print()
            print(render_record_text(rec))

    return 0


if __name__ == "__main__":
    sys.exit(main())
