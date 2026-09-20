"""Build a Marvel Snap card-name -> English ability-text lookup.

How the link works (verified against the local install, not guessed):

Unity's Localization package splits each localized string table into two
pieces: a locale-independent "SharedTableData" asset that maps a human
key name (e.g. ``Card_Name_Jubilee``, ``Card_Desc_Jubilee``) to a numeric
int64 id, and a per-locale "string table" asset that maps that same id to
the localized text. For Marvel Snap the two pieces live in different
bundles:

  * ``StreamingAssets/aa/StandaloneWindows64/localization-assets-shared_
    assets_assets/data/localization/tables/card/cardshareddata.asset.bundle``
    -- the Card table's SharedTableData: key name -> int64 id.
  * ``StreamingAssets/aa/StandaloneWindows64/localization-string-tables-
    english(en)_assets_all.bundle`` -- id -> English text, for every
    localization table (Card, UI, Mission, ...), English only.

Both are ordinary UnityFS bundles; ``read_card_text.py`` in this folder
already implements a pure-Python UnityFS/LZ4 reader. This module reuses
that reader, then recovers the (id, text) records that Unity's string
serialization leaves in the decompressed asset: an 8-byte little-endian
int64 id immediately followed by a 4-byte length-prefixed UTF-8 string.
Matching ``Card_Name_<Key>``/``Card_Desc_<Key>`` ids between the two
bundles gives a verified key -> (display name, ability text) mapping --
confirmed by hand for Jubilee, Wong, Taskmaster and Cassandra Nova.

Card cost and power are NOT part of this localization data and were not
located elsewhere in the local files by this script, so they are always
reported as ``null``. Ability text may still contain unresolved
placeholders such as ``{card.AddedPower}`` -- their numeric values are
not available locally, so they are left as-is rather than invented.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_card_text import (  # noqa: E402
    BundleFormatError,
    _clean_text,
    _looks_like_text,
    parse_bundle,
)

_GAME_DATA = Path(
    r"D:\SteamLibrary\steamapps\common\MARVEL SNAP\SNAP_Data"
)
_AA = _GAME_DATA / "StreamingAssets" / "aa" / "StandaloneWindows64"

DEFAULT_SHARED_TABLE_BUNDLE = (
    _AA
    / "localization-assets-shared_assets_assets"
    / "data"
    / "localization"
    / "tables"
    / "card"
    / "cardshareddata.asset.bundle"
)
DEFAULT_ENGLISH_BUNDLE = (
    _AA / "localization-string-tables-english(en)_assets_all.bundle"
)

_MAX_STRING_LEN = 4096
_NAME_PREFIX = "Card_Name_"
_DESC_PREFIX = "Card_Desc_"


def _scan_id_text_records(blob: bytes) -> list[tuple[Optional[int], str]]:
    """Recover (id, text) records from a decompressed Unity asset blob.

    Unity serializes each localization entry as an 8-byte little-endian
    int64 id followed immediately by a 4-byte length-prefixed UTF-8
    string (itself 4-byte aligned). This walks the blob the same way
    ``read_card_text.extract_strings`` does, but also captures the 8
    bytes preceding each accepted string as that entry's id when they
    are available.
    """
    records: list[tuple[Optional[int], str]] = []
    n = len(blob)
    i = 0
    while i + 4 <= n:
        length = struct.unpack_from("<I", blob, i)[0]
        end = i + 4 + length
        if 1 <= length <= _MAX_STRING_LEN and end <= n:
            raw = blob[i + 4 : end]
            try:
                s = raw.decode("utf-8")
            except UnicodeDecodeError:
                s = None
            if s is not None and _looks_like_text(s):
                idval = struct.unpack_from("<q", blob, i - 8)[0] if i - 8 >= 0 else None
                records.append((idval, _clean_text(s)))
                i = end + ((-end) % 4)
                continue
        i += 4
    return records


def _load_blob(path: Path) -> bytes:
    if not path.is_file():
        print(f"game file not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    return parse_bundle(path.read_bytes())


def build_lookup(
    shared_bundle: Path = DEFAULT_SHARED_TABLE_BUNDLE,
    english_bundle: Path = DEFAULT_ENGLISH_BUNDLE,
) -> dict[str, dict]:
    """Build {card display name -> {key, ability, cost, power}}.

    Raises SystemExit(2) if a required game file is missing, and
    SystemExit(3) if the expected key layout (Card_Name_*/Card_Desc_*)
    is not found in the shared-table bundle.
    """
    try:
        shared_blob = _load_blob(shared_bundle)
        english_blob = _load_blob(english_bundle)
    except BundleFormatError as exc:
        print(f"unexpected bundle format: {exc}", file=sys.stderr)
        raise SystemExit(3)

    shared_records = _scan_id_text_records(shared_blob)
    name_keys = {
        t[len(_NAME_PREFIX) :]: idv
        for idv, t in shared_records
        if idv is not None and t.startswith(_NAME_PREFIX)
    }
    desc_keys = {
        t[len(_DESC_PREFIX) :]: idv
        for idv, t in shared_records
        if idv is not None and t.startswith(_DESC_PREFIX)
    }
    if not name_keys:
        print(
            f"no {_NAME_PREFIX}* keys found in {shared_bundle}; "
            "SharedTableData layout may have changed",
            file=sys.stderr,
        )
        raise SystemExit(3)

    id_to_text: dict[int, str] = {}
    for idv, text in _scan_id_text_records(english_blob):
        if idv is not None and idv not in id_to_text:
            id_to_text[idv] = text

    result: dict[str, dict] = {}
    for suffix, name_id in name_keys.items():
        display_name = id_to_text.get(name_id)
        if display_name is None:
            # The id from SharedTableData has no matching English string;
            # skip rather than invent a name.
            continue
        desc_id = desc_keys.get(suffix)
        ability = id_to_text.get(desc_id) if desc_id is not None else None
        result[display_name] = {
            "key": suffix,
            "ability": ability,
            "cost": None,
            "power": None,
        }
    return result


def _normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


DEFAULT_STATS_PATH = Path(__file__).resolve().parent.parent / "card_stats.json"


def _load_stats(stats_path: Path) -> tuple[Optional[dict], Optional[str], Optional[str]]:
    """Load the optional card_stats.json file.

    Returns (name -> {cost, power} keyed by normalized stats name, source, fetched).
    Returns (None, None, None) if the file is missing. Prints a one-line error
    to stderr and returns (None, None, None) if the file exists but is
    malformed or has an unexpected shape -- a bad stats file must never break
    text lookup.
    """
    if not stats_path.is_file():
        return None, None, None
    try:
        with stats_path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        cards = data["cards"]
        by_name: dict[str, dict] = {}
        for card in cards:
            by_name[_normalize(card["name"])] = {
                "cost": int(card["cost"]),
                "power": int(card["power"]),
            }
        source = data.get("source")
        fetched = data.get("fetched")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"malformed stats file {stats_path}: {exc}", file=sys.stderr)
        return None, None, None
    return by_name, source, fetched


def _apply_stats(
    lookup: dict[str, dict], stats_by_name: Optional[dict]
) -> int:
    """Fill cost/power in-place from stats_by_name. Returns matched count."""
    matched = 0
    if not stats_by_name:
        return matched
    for name, entry in lookup.items():
        stat = stats_by_name.get(_normalize(name))
        if stat is None:
            stat = stats_by_name.get(_normalize(entry["key"]))
        if stat is not None:
            entry["cost"] = stat["cost"]
            entry["power"] = stat["power"]
            matched += 1
    return matched


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shared-bundle",
        type=Path,
        default=DEFAULT_SHARED_TABLE_BUNDLE,
        help="Path to cardshareddata.asset.bundle.",
    )
    parser.add_argument(
        "--english-bundle",
        type=Path,
        default=DEFAULT_ENGLISH_BUNDLE,
        help="Path to the English localization string-tables bundle.",
    )
    parser.add_argument("--name", default=None, help="Print cards whose name contains NAME and exit.")
    parser.add_argument("--out", default=None, help="Output JSON path.")
    parser.add_argument(
        "--stats",
        type=Path,
        default=DEFAULT_STATS_PATH,
        help="Path to card_stats.json (optional; cost/power source).",
    )
    args = parser.parse_args(argv)

    try:
        lookup = build_lookup(args.shared_bundle, args.english_bundle)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1

    stats_by_name, stats_source, stats_fetched = _load_stats(args.stats)
    matched = _apply_stats(lookup, stats_by_name)

    if args.name:
        needle = _normalize(args.name)
        matches = {
            name: entry for name, entry in lookup.items() if needle in _normalize(name)
        }
        for name, entry in sorted(matches.items()):
            print(json.dumps({"name": name, **entry}, ensure_ascii=False))
        print(f"# {len(matches)} match(es) for {args.name!r}", file=sys.stderr)
        if stats_by_name is None:
            print(
                "note: no card_stats.json found; cost/power unavailable",
                file=sys.stderr,
            )
        return 0

    if args.out:
        out_path = Path(args.out)
    else:
        out_path = Path(__file__).resolve().parent.parent / "local" / "card_lookup.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    ordered = {name: lookup[name] for name in sorted(lookup)}
    output = {
        "stats_source": stats_source,
        "stats_fetched": stats_fetched,
        "stats_matched": matched,
        **ordered,
    }
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {len(ordered)} cards to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
