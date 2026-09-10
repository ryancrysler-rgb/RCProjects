"""Minimal pure-Python Snappy decompressor.

The Event Centre websocket sends Snappy-compressed UTF-16LE JSON. The usual
python-snappy binding needs a C toolchain, which is a poor thing to require
of someone double-clicking a .bat file, and decompression alone is small
enough to carry ourselves.

Format: a varint of the uncompressed length, then tagged elements -- literals
or back-references into what has been produced so far.
"""
from __future__ import annotations


class SnappyError(ValueError):
    pass


def _varint(data: bytes, pos: int) -> tuple[int, int]:
    result = shift = 0
    while pos < len(data):
        byte = data[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return result, pos
        shift += 7
        if shift > 32:
            break
    raise SnappyError("bad varint")


def decompress(data: bytes, partial: bool = False) -> bytes:
    """Decompress a Snappy block.

    With partial=True a truncated block returns what was decoded so far,
    which is what makes a half-captured frame still readable.
    """
    expected, pos = _varint(data, 0)
    out = bytearray()

    while pos < len(data):
        tag = data[pos]
        kind = tag & 0x03
        pos += 1

        if kind == 0:  # literal
            length = tag >> 2
            if length >= 60:
                extra = length - 59
                if pos + extra > len(data):
                    break
                length = int.from_bytes(data[pos:pos + extra], "little")
                pos += extra
            length += 1
            if pos + length > len(data):
                out += data[pos:]
                if partial:
                    break
                raise SnappyError("truncated literal")
            out += data[pos:pos + length]
            pos += length
            continue

        if kind == 1:  # copy, 1-byte offset
            if pos >= len(data):
                break
            length = 4 + ((tag >> 2) & 0x07)
            offset = ((tag >> 5) << 8) | data[pos]
            pos += 1
        elif kind == 2:  # copy, 2-byte offset
            if pos + 2 > len(data):
                break
            length = (tag >> 2) + 1
            offset = int.from_bytes(data[pos:pos + 2], "little")
            pos += 2
        else:  # copy, 4-byte offset
            if pos + 4 > len(data):
                break
            length = (tag >> 2) + 1
            offset = int.from_bytes(data[pos:pos + 4], "little")
            pos += 4

        if offset == 0 or offset > len(out):
            if partial:
                break
            raise SnappyError(f"bad offset {offset}")
        # Overlapping copies are legal and must be byte-at-a-time.
        for _ in range(length):
            out.append(out[-offset])

    if not partial and len(out) != expected:
        raise SnappyError(f"expected {expected} bytes, produced {len(out)}")
    return bytes(out)


def decode_text(data: bytes, partial: bool = False) -> str | None:
    """Snappy-decompress and decode; the payload is UTF-16LE JSON."""
    try:
        raw = decompress(data, partial=partial)
    except SnappyError:
        return None
    for encoding in ("utf-16-le", "utf-8"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            try:
                return raw.decode(encoding, errors="ignore")
            except Exception:
                continue
    return None
