"""Read Marvel Snap's local CollectionState.json (read-only) and write two
derived files: which cards the player owns, and what is in their saved decks.

Never writes to or copies the input file. Never reads or emits account
identifiers ("Id" fields, anything under "Account", etc.).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_STATE_PATH = os.path.expandvars(
    r"%USERPROFILE%\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\CollectionState.json"
)


def norm(s: str) -> str:
    """Lowercase and strip everything that isn't a-z or 0-9."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def display_name(card_def_id: str) -> str:
    """Insert a space before an uppercase letter that follows a lowercase
    letter or digit, e.g. "StarlordGuardiansOfTheGalaxy" -> "Starlord
    Guardians Of The Galaxy"."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", card_def_id)


def load_overrides(games_snap_dir: Path) -> dict[str, str]:
    overrides_path = games_snap_dir / "name_overrides.json"
    if not overrides_path.is_file():
        return {}
    try:
        with open(overrides_path, encoding="utf-8-sig") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def get_path(root: Any, path: list[str]) -> Any:
    """Walk a list of dict keys, raising KeyError(dotted path) on failure."""
    node = root
    for i, key in enumerate(path):
        if not isinstance(node, dict) or key not in node:
            raise KeyError(".".join(path[: i + 1]))
        node = node[key]
    return node


def fail(code: int, message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", default=DEFAULT_STATE_PATH, help="Path to CollectionState.json")
    args = parser.parse_args()

    state_path = Path(args.state)
    if not state_path.is_file():
        fail(
            2,
            f"State file not found: {state_path}. Open Marvel Snap on the PC once, then retry.",
        )

    mtime = state_path.stat().st_mtime
    mtime_iso = datetime.datetime.fromtimestamp(mtime).isoformat(timespec="seconds")

    try:
        with open(state_path, encoding="utf-8-sig") as f:
            root = json.load(f)
    except json.JSONDecodeError as exc:
        fail(3, f"Failed to parse {state_path} as JSON: {exc}")
        return

    try:
        ownership_rows = get_path(root, ["ServerState", "CardOwnership", "Dao", "S"])
        if not isinstance(ownership_rows, list):
            raise KeyError("ServerState.CardOwnership.Dao.S")

        copies = get_path(root, ["ServerState", "Cards"])
        if not isinstance(copies, list):
            raise KeyError("ServerState.Cards")

        decks_raw = get_path(root, ["ServerState", "Decks"])
        if not isinstance(decks_raw, list):
            raise KeyError("ServerState.Decks")
    except KeyError as exc:
        fail(3, f"Expected JSON path missing or wrong type: {exc}. The game's file layout may have changed.")
        return

    owned: dict[str, dict[str, Any]] = {}
    for row in ownership_rows:
        card_id = row["C"]
        owned[card_id] = {
            "base_owned": bool(row.get("B")),
            "variant_count": len(row.get("V", [])),
        }
    owned_ids = set(owned.keys())

    copy_ids = {c["CardDefId"] for c in copies if isinstance(c, dict) and "CardDefId" in c}

    only_in_ownership = sorted(owned_ids - copy_ids)
    only_in_copies = sorted(copy_ids - owned_ids)

    decks = []
    for deck in decks_raw:
        deck_cards = [c["CardDefId"] for c in deck.get("Cards", [])]
        missing = sorted(set(deck_cards) - owned_ids)
        decks.append(
            {
                "name": deck.get("Name"),
                "time_updated": deck.get("TimeUpdated"),
                "slot": deck.get("DeckSlotDefId"),
                "cards": deck_cards,
                "missing": missing,
            }
        )

    script_dir = Path(__file__).resolve().parent
    games_snap_dir = script_dir.parent
    overrides = load_overrides(games_snap_dir)

    def name_for(card_id: str) -> str:
        return overrides.get(card_id, display_name(card_id))

    def norm_key_for(card_id: str) -> str:
        if card_id in overrides:
            return norm(overrides[card_id])
        return norm(card_id)

    cards_out = [
        {
            "id": card_id,
            "norm_key": norm_key_for(card_id),
            "base_owned": owned[card_id]["base_owned"],
            "variant_count": owned[card_id]["variant_count"],
        }
        for card_id in sorted(owned_ids)
    ]

    collection = {
        "source_file_modified": mtime_iso,
        "card_count": len(owned_ids),
        "cards": cards_out,
        "decks": decks,
        "integrity": {
            "copies_list_count": len(copy_ids),
            "only_in_ownership": only_in_ownership,
            "only_in_copies": only_in_copies,
        },
    }

    integrity_ok = not only_in_ownership and not only_in_copies

    json_path = games_snap_dir / "collection.json"
    md_path = games_snap_dir / "collection.md"

    json_text = json.dumps(collection, indent=2, ensure_ascii=False) + "\n"

    md_lines: list[str] = []
    md_lines.append("# Marvel Snap collection")
    md_lines.append("")
    md_lines.append(f"Collection file last modified: {mtime_iso}")
    md_lines.append(f"Cards owned: {len(owned_ids)}")
    if integrity_ok:
        md_lines.append("Integrity: OK")
    else:
        md_lines.append(
            "Integrity: only_in_ownership="
            + json.dumps(only_in_ownership, ensure_ascii=False)
            + " only_in_copies="
            + json.dumps(only_in_copies, ensure_ascii=False)
        )
    md_lines.append("")
    md_lines.append("## Cards")
    for card_id in sorted(owned_ids, key=lambda cid: name_for(cid)):
        line = f"- {name_for(card_id)} (`{card_id}`)"
        variant_count = owned[card_id]["variant_count"]
        if variant_count > 0:
            line += f" — +{variant_count} variants"
        md_lines.append(line)
    md_lines.append("")
    md_lines.append("## Decks")
    for deck in decks:
        md_lines.append(f"### {deck['name']}")
        md_lines.append(f"Updated: {deck['time_updated']}")
        card_names = ", ".join(name_for(cid) for cid in deck["cards"])
        md_lines.append(card_names)
        if deck["missing"]:
            md_lines.append("Missing: " + ", ".join(deck["missing"]))
        md_lines.append("")

    md_text = "\n".join(md_lines).rstrip("\n") + "\n"

    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json_text)
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(md_text)

    age_days = (datetime.datetime.now() - datetime.datetime.fromtimestamp(mtime)).days
    print(
        f"Cards: {len(owned_ids)} | Decks: {len(decks)} | "
        f"State file modified: {mtime_iso} ({age_days} days ago) | "
        f"Integrity: {'OK' if integrity_ok else 'MISMATCH'}"
    )


if __name__ == "__main__":
    main()
