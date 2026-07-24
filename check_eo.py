#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 RPM Release 中没有 openEuler ``oe<数字>`` 标识的 CSV 行。"""

import argparse
import csv
import re
from pathlib import Path

from openeuler_url_parser import parse_openeuler_rpm_url

OE_RELEASE_PATTERN = re.compile(r"(?:^|[._+~])oe\d", re.IGNORECASE)


def release_has_oe_marker(release):
    """只检查 Release 字段，避免被 ``noetic`` 等包名误导。"""
    return bool(OE_RELEASE_PATTERN.search(release))


def check_rows_without_oe_release(csv_file):
    """返回 ``(CSV 行号, 行数据, Release)`` 列表。"""
    results = []
    with Path(csv_file).open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        required = {"comp_name", "version", "url"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"invalid CSV header: {reader.fieldnames!r}")

        for line_number, row in enumerate(reader, 2):
            parts = parse_openeuler_rpm_url(row["url"])
            if not release_has_oe_marker(parts.release):
                results.append((line_number, row, parts.release))
    return results


def check_lines_without_eo(csv_file):
    """兼容旧函数名；语义已修正为检查 Release 的 ``oe`` 标识。"""
    return [
        (line_number, row["url"])
        for line_number, row, _ in check_rows_without_oe_release(csv_file)
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", nargs="?", default="new_os_url_info.csv")
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="输出全部命中行；默认只输出前 20 条",
    )
    args = parser.parse_args(argv)

    rows = check_rows_without_oe_release(args.csv_file)
    limit = len(rows) if args.show_all else min(20, len(rows))
    for line_number, row, release in rows[:limit]:
        print(
            f"line={line_number} release={release} "
            f"name={row['comp_name']} url={row['url']}"
        )
    if len(rows) > limit:
        print(f"... omitted {len(rows) - limit} rows; use --show-all to display them")
    print(f"rows_without_oe_release={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
