"""Match this week's ranked Marvel Snap decks against the player's owned
cards and report, per deck, how many of its cards are owned and which are
missing. Standard library only; no network access.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def norm(s: str) -> str:
    """Lowercase and strip everything but a-z / 0-9."""
    return "".join(ch for ch in s.lower() if ("a" <= ch <= "z") or ("0" <= ch <= "9"))


def suffix_match_len(a: str, b: str) -> int:
    """Length of the longest common suffix of a and b."""
    common = 0
    for x, y in zip(reversed(a), reversed(b)):
        if x != y:
            break
        common += 1
    return common


def is_near_match(owned_key: str, missing_norm: str) -> bool:
    if owned_key == missing_norm:
        return False
    if len(owned_key) < 5:
        return False
    if abs(len(owned_key) - len(missing_norm)) > 6:
        return False
    return suffix_match_len(owned_key, missing_norm) >= 6


def load_json_file(path: Path, label: str) -> Any:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Error: {label} file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except OSError as exc:
        print(f"Error: could not read {label} file {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"Error: {label} file is not valid JSON ({path}): {exc}", file=sys.stderr)
        sys.exit(3)


def validate_decks(data: Any) -> list[dict]:
    if not isinstance(data, list):
        print("Error: decks JSON must be a list", file=sys.stderr)
        sys.exit(3)
    decks = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            print(f"Error: deck #{i} is not an object", file=sys.stderr)
            sys.exit(3)
        for key in ("tier", "name", "cube", "win_rate"):
            if key not in item or not isinstance(item[key], str):
                print(f"Error: deck #{i} missing/non-string field '{key}'", file=sys.stderr)
                sys.exit(3)
        cards = item.get("cards")
        if not isinstance(cards, list) or len(cards) < 1 or not all(isinstance(c, str) for c in cards):
            print(f"Error: deck #{i} 'cards' must be a non-empty list of strings", file=sys.stderr)
            sys.exit(3)
        decks.append(item)
    return decks


def validate_collection(data: Any) -> tuple[int, Any, list[dict]]:
    if not isinstance(data, dict):
        print("Error: collection JSON must be an object", file=sys.stderr)
        sys.exit(3)
    if "card_count" not in data or not isinstance(data["card_count"], int):
        print("Error: collection missing integer field 'card_count'", file=sys.stderr)
        sys.exit(3)
    if "source_file_modified" not in data:
        print("Error: collection missing field 'source_file_modified'", file=sys.stderr)
        sys.exit(3)
    cards = data.get("cards")
    if not isinstance(cards, list):
        print("Error: collection missing list field 'cards'", file=sys.stderr)
        sys.exit(3)
    for i, c in enumerate(cards):
        if not isinstance(c, dict) or "id" not in c or "norm_key" not in c:
            print(f"Error: collection cards[{i}] missing 'id' or 'norm_key'", file=sys.stderr)
            sys.exit(3)
        if not isinstance(c["id"], str) or not isinstance(c["norm_key"], str):
            print(f"Error: collection cards[{i}] 'id'/'norm_key' must be strings", file=sys.stderr)
            sys.exit(3)
    return data["card_count"], data["source_file_modified"], cards


def main() -> None:
    parser = argparse.ArgumentParser(description="Match Marvel Snap decks against an owned-card collection.")
    parser.add_argument("decks_json", type=Path)
    parser.add_argument("--collection", type=Path, default=None)
    parser.add_argument("--out-json", type=Path, default=None)
    args = parser.parse_args()

    collection_path = args.collection
    if collection_path is None:
        collection_path = Path(__file__).resolve().parent.parent / "collection.json"

    decks = validate_decks(load_json_file(args.decks_json, "decks"))
    card_count, source_modified, coll_cards = validate_collection(load_json_file(collection_path, "collection"))

    owned_norms = {c["norm_key"] for c in coll_cards}
    owned_pairs = [(c["norm_key"], c["id"]) for c in coll_cards]

    deck_results = []
    warnings_seen: dict[tuple[str, str], None] = {}
    missing_per_deck_sets: list[set[str]] = []

    for deck in decks:
        owned_names, missing_names = [], []
        for name in deck["cards"]:
            (owned_names if norm(name) in owned_norms else missing_names).append(name)
        for m in missing_names:
            nm = norm(m)
            for key, cid in owned_pairs:
                if is_near_match(key, nm):
                    warnings_seen.setdefault((m, cid), None)
        deck_results.append({
            "tier": deck["tier"], "name": deck["name"], "cube": deck["cube"],
            "win_rate": deck["win_rate"], "owned": owned_names, "missing": missing_names,
            "total": len(deck["cards"]),
        })
        missing_per_deck_sets.append(set(missing_names))

    lines = [f"Collection file last modified: {source_modified} · Cards owned: {card_count}", ""]

    lines.append("| Tier | Deck | Cube avg | Win rate | You own |")
    lines.append("|---|---|---|---|---|")
    for d in deck_results:
        n, t = len(d["owned"]), d["total"]
        cell = f"{n} / {t}"
        if n >= t - 4:
            cell = f"**{cell}**"
        lines.append(f"| {d['tier']} | {d['name']} | {d['cube']} | {d['win_rate']} | {cell} |")
    lines.append("")

    lines.append("## Buildable now")
    buildable = [d for d in deck_results if not d["missing"]]
    lines.extend(f"- {d['name']}" for d in buildable) if buildable else lines.append("None.")
    lines.append("")

    lines.append("## Closest")
    candidates = [d for d in deck_results if d["missing"]]
    closest = sorted(candidates, key=lambda d: len(d["missing"]))[:3]
    if closest:
        for d in closest:
            missing_str = ", ".join(d["missing"])
            lines.append(f"- **{d['name']}** — {len(d['owned'])} of {d['total']}. Missing: {missing_str}.")
    else:
        lines.append("None.")
    lines.append("")

    counter: Counter[str] = Counter()
    for s in missing_per_deck_sets:
        counter.update(s)
    freq_items = sorted(((name, cnt) for name, cnt in counter.items() if cnt >= 2), key=lambda x: (-x[1], x[0]))[:10]

    lines.append("## Unowned cards that appear most")
    if freq_items:
        lines.append("| Card | In how many decks |")
        lines.append("|---|---|")
        lines.extend(f"| {name} | {cnt} |" for name, cnt in freq_items)
    else:
        lines.append("None.")
    lines.append("")

    lines.append("## Possible spelling mismatches (review by hand)")
    if warnings_seen:
        lines.extend(f"- site name '{s}' vs owned id '{o}'" for s, o in warnings_seen.keys())
    else:
        lines.append("None.")

    print("\n".join(lines))

    if args.out_json:
        out_obj = {
            "decks": [
                {
                    "tier": d["tier"], "name": d["name"], "cube": d["cube"],
                    "win_rate": d["win_rate"], "owned": d["owned"], "missing": d["missing"],
                }
                for d in deck_results
            ],
            "unowned_frequency": [{"card": name, "count": cnt} for name, cnt in freq_items],
            "spelling_warnings": [{"site_name": s, "owned_id": o} for s, o in warnings_seen.keys()],
        }
        args.out_json.write_text(json.dumps(out_obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="")

    sys.exit(0)


if __name__ == "__main__":
    main()
