from __future__ import annotations


def lookup(
    index: dict[str, dict[str, str]],
    key: str,
) -> dict[str, str]:
    if key not in index:
        raise KeyError(f"Missing lookup key: {key}")

    return index[key]


def inner_join(
    left_rows: list[dict[str, str]],
    right_index: dict[str, dict[str, str]],
    left_key: str,
) -> list[tuple[dict[str, str], dict[str, str]]]:
    joined = []

    for left in left_rows:
        key = left[left_key]

        if key in right_index:
            joined.append((left, right_index[key]))

    return joined


def require_keys(
    rows: list[dict[str, str]],
    required_keys: set[str],
) -> None:
    for row in rows:
        missing = required_keys - set(row.keys())

        if missing:
            raise KeyError(f"Missing required keys: {sorted(missing)}")
