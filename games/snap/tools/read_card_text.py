"""Extract English localization string entries from the Marvel Snap
UnityFS localization string-table bundle.

The bundle is a UnityFS archive (signature "UnityFS", version 8) whose
"blocks info" (and, here, directory info) is stored immediately after the
header and is itself LZ4/LZ4HC-compressed. The archive's single serialized
asset ("CAB-...") is reassembled from a handful of LZ4/LZ4HC-compressed
data blocks. Inside that reassembled asset, individual localized strings
are stored Unity-style: a 4-byte little-endian length prefix followed by
that many UTF-8 bytes, aligned to a 4-byte boundary.

This script never modifies the bundle (opened "rb" only) and does not
depend on any third-party package -- the LZ4 block decompressor below is
a small pure-Python implementation of the standard LZ4 block format
(shared by both the LZ4 and LZ4HC compressors; only the compressor
differs, not the bitstream).

Key names for each string (Unity's "shared table data") are not present
in this bundle, so every extracted entry is emitted with ``key: null``.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import struct
import sys
from pathlib import Path

DEFAULT_BUNDLE = (
    r"D:\SteamLibrary\steamapps\common\MARVEL SNAP\SNAP_Data\StreamingAssets"
    r"\aa\StandaloneWindows64\localization-string-tables-english(en)_assets_all.bundle"
)

# Compression type mask used both at the archive level and per data block.
_COMPRESSION_MASK = 0x3F
_COMPRESSION_NAMES = {0: "none", 1: "lzma", 2: "lz4", 3: "lz4hc"}


class BundleFormatError(Exception):
    """Raised when the bundle does not match the expected UnityFS layout."""


def _align16(offset: int) -> int:
    return (offset + 15) // 16 * 16


def _read_cstring(data: bytes, pos: int) -> tuple[str, int]:
    end = data.index(b"\x00", pos)
    return data[pos:end].decode("ascii", errors="replace"), end + 1


def lz4_decompress_block(data: bytes, uncompressed_size: int) -> bytes:
    """Decompress one LZ4/LZ4HC block (the standard LZ4 block bitstream).

    Both the LZ4 and LZ4HC compressors of Unity's bundle format produce the
    same bitstream; only the encoder differs, so one decoder handles both.
    """
    out = bytearray()
    i = 0
    n = len(data)
    try:
        while len(out) < uncompressed_size:
            token = data[i]
            i += 1
            lit_len = token >> 4
            if lit_len == 15:
                while True:
                    b = data[i]
                    i += 1
                    lit_len += b
                    if b != 255:
                        break
            out.extend(data[i : i + lit_len])
            i += lit_len
            if len(out) >= uncompressed_size:
                break
            offset = data[i] | (data[i + 1] << 8)
            i += 2
            if offset <= 0 or offset > len(out):
                raise BundleFormatError(
                    f"invalid LZ4 back-reference offset {offset} at output "
                    f"position {len(out)}"
                )
            match_len = token & 0x0F
            if match_len == 15:
                while True:
                    b = data[i]
                    i += 1
                    match_len += b
                    if b != 255:
                        break
            match_len += 4
            start = len(out) - offset
            for k in range(match_len):
                out.append(out[start + k])
    except IndexError as exc:
        raise BundleFormatError("LZ4 stream ended unexpectedly") from exc
    return bytes(out[:uncompressed_size])


def _decompress_chunk(data: bytes, uncompressed_size: int, compression_type: int) -> bytes:
    ctype = compression_type & _COMPRESSION_MASK
    if ctype == 0:
        return data[:uncompressed_size]
    if ctype in (2, 3):
        return lz4_decompress_block(data, uncompressed_size)
    name = _COMPRESSION_NAMES.get(ctype, f"unknown({ctype})")
    raise BundleFormatError(
        f"unsupported compression type: {name} (not implemented; only "
        "'none', 'lz4' and 'lz4hc' are supported)"
    )


def parse_bundle(data: bytes) -> bytes:
    """Parse a UnityFS bundle and return the reassembled serialized-file bytes."""
    if not data.startswith(b"UnityFS\x00"):
        raise BundleFormatError(
            f"expected UnityFS signature, found {data[:16]!r}"
        )
    pos = 8
    version = struct.unpack_from(">I", data, pos)[0]
    pos += 4
    if version != 8:
        raise BundleFormatError(f"expected UnityFS version 8, found {version}")
    _unity_version, pos = _read_cstring(data, pos)
    _unity_revision, pos = _read_cstring(data, pos)
    total_size = struct.unpack_from(">q", data, pos)[0]
    pos += 8
    if total_size != len(data):
        raise BundleFormatError(
            f"header size {total_size} does not match file size {len(data)}"
        )
    compressed_blocks_info_size, uncompressed_blocks_info_size, flags = (
        struct.unpack_from(">III", data, pos)
    )
    pos += 12

    if flags & 0x80:
        raise BundleFormatError(
            "blocks info stored at end of file is not supported by this parser"
        )

    blocks_info_pos = _align16(pos)
    blocks_info_end = blocks_info_pos + compressed_blocks_info_size
    if blocks_info_end > len(data):
        raise BundleFormatError("blocks info extends past end of file")
    compressed_blocks_info = data[blocks_info_pos:blocks_info_end]
    blocks_info = _decompress_chunk(
        compressed_blocks_info, uncompressed_blocks_info_size, flags
    )

    # blocks info layout: 16-byte hash, block count, block table, node count,
    # node table (offset, size, flags, path) -- only the block table matters
    # here since this bundle holds a single serialized asset.
    p = 16
    (block_count,) = struct.unpack_from(">i", blocks_info, p)
    p += 4
    blocks: list[tuple[int, int, int]] = []
    for _ in range(block_count):
        u_size, c_size, b_flags = struct.unpack_from(">IIH", blocks_info, p)
        p += 10
        blocks.append((u_size, c_size, b_flags))

    data_start = _align16(blocks_info_end)
    out = bytearray()
    read_pos = data_start
    for u_size, c_size, b_flags in blocks:
        chunk = data[read_pos : read_pos + c_size]
        if len(chunk) != c_size:
            raise BundleFormatError("data block extends past end of file")
        out.extend(_decompress_chunk(chunk, u_size, b_flags))
        read_pos += c_size

    return bytes(out)


_TAG_RE = re.compile(r"<[^>]*>")
_WHITESPACE_RE = re.compile(r"\s+")


def _clean_text(text: str) -> str:
    text = _TAG_RE.sub("", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text


def _looks_like_text(s: str) -> bool:
    if len(s) < 3:
        return False
    if not any(c.isalpha() for c in s):
        return False
    for c in s:
        cp = ord(c)
        if cp in (9, 10, 13):
            continue
        if cp < 32 or cp == 127:
            # Embedded control/NUL bytes mean this "string" is really a
            # false match straddling a binary field (e.g. an entry id),
            # not real UI/ability text.
            return False
    return True


_MAX_STRING_LEN = 4096


def extract_strings(blob: bytes) -> list[str]:
    """Scan a serialized-file blob for Unity length-prefixed UTF-8 strings.

    Unity serializes strings as a 4-byte little-endian length followed by
    that many UTF-8 bytes, padded to a 4-byte boundary. There is no type
    tree available for this asset, so this scans for that pattern directly
    and keeps only results that look like real printable text.
    """
    texts: list[str] = []
    n = len(blob)
    i = 0
    while i + 4 <= n:
        length = struct.unpack_from("<I", blob, i)[0]
        end = i + 4 + length
        if 3 <= length <= _MAX_STRING_LEN and end <= n:
            raw = blob[i + 4 : end]
            try:
                s = raw.decode("utf-8")
            except UnicodeDecodeError:
                s = None
            if s is not None and _looks_like_text(s):
                cleaned = _clean_text(s)
                if len(cleaned) >= 3:
                    texts.append(cleaned)
                i = end + ((-end) % 4)
                continue
        i += 4
    return texts


def _normalize_for_lookup(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def build_output(bundle_path: Path, entries_text: list[str]) -> dict:
    mtime = datetime.datetime.fromtimestamp(
        bundle_path.stat().st_mtime, tz=datetime.timezone.utc
    ).replace(microsecond=0)
    entries = [{"key": None, "text": t} for t in entries_text]
    entries.sort(key=lambda e: ("", e["text"]))
    return {
        "bundle_modified": mtime.isoformat().replace("+00:00", "Z"),
        "entry_count": len(entries),
        "entries": entries,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE, help="Path to the localization bundle.")
    parser.add_argument("--out", default=None, help="Output JSON path.")
    parser.add_argument("--lookup", default=None, help="Print entries whose key or text contains NAME and exit.")
    args = parser.parse_args(argv)

    bundle_path = Path(args.bundle)
    if not bundle_path.is_file():
        print(f"bundle not found: {bundle_path}", file=sys.stderr)
        return 2

    data = bundle_path.read_bytes()
    try:
        asset_blob = parse_bundle(data)
    except BundleFormatError as exc:
        print(f"unexpected bundle format: {exc}", file=sys.stderr)
        return 3

    texts = extract_strings(asset_blob)
    output = build_output(bundle_path, texts)

    if args.lookup:
        needle = _normalize_for_lookup(args.lookup)
        matches = [
            e
            for e in output["entries"]
            if needle in _normalize_for_lookup(e["text"])
            or (e["key"] and needle in _normalize_for_lookup(e["key"]))
        ]
        for e in matches:
            print(json.dumps(e, ensure_ascii=False))
        print(f"# {len(matches)} match(es) for {args.lookup!r}", file=sys.stderr)
        return 0

    if args.out:
        out_path = Path(args.out)
    else:
        out_path = Path(__file__).resolve().parent.parent / "local" / "card_text.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
