#!/usr/bin/env python3
"""Show TOML key paths and value types without printing values."""

import argparse
from collections import Counter
import datetime
import json
from pathlib import Path
import sys
import tomllib


# ponytail: cap parsing at 16 MiB; add streaming support only if larger configs matter.
MAX_INPUT_BYTES = 16 * 1024 * 1024


def type_name(value):
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, datetime.datetime):
        return "datetime"
    if isinstance(value, datetime.date):
        return "date"
    if isinstance(value, datetime.time):
        return "time"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "float"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "table"
    return "unknown"


def describe_array(values):
    if not values:
        return "array[empty]"
    counts = Counter(type_name(value) for value in values)
    members = ", ".join(f"{kind}×{counts[kind]}" for kind in sorted(counts))
    return f"array[{members}]"


def walk(table, parent=()):
    for key, value in table.items():
        path = parent + (key,)
        if isinstance(value, dict):
            yield path, "table"
            yield from walk(value, path)
        elif isinstance(value, list):
            yield path, describe_array(value)
        else:
            yield path, type_name(value)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="List TOML key paths and types without showing configured values."
    )
    parser.add_argument("file", type=Path, help="UTF-8 TOML file")
    args = parser.parse_args(argv)

    try:
        with args.file.expanduser().open("rb") as source:
            raw = source.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("input exceeds the 16 MiB limit")
        document = tomllib.loads(raw.decode("utf-8"))
    except OSError as error:
        print(f"toml-shape: cannot read input ({type(error).__name__})", file=sys.stderr)
        return 2
    except UnicodeError:
        print("toml-shape: input is not valid UTF-8", file=sys.stderr)
        return 2
    except tomllib.TOMLDecodeError:
        print("toml-shape: invalid TOML", file=sys.stderr)
        return 2
    except ValueError as error:
        print(f"toml-shape: {error}", file=sys.stderr)
        return 2

    found = False
    for path, description in walk(document):
        found = True
        print(f"{json.dumps(path, ensure_ascii=True)}\t{description}")
    if not found:
        print("(empty TOML document)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
