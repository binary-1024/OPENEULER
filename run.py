#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仅依据 RPM URL 解析、生成、修正和验证 openEuler CSV。"""

import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

from openeuler_url_parser import parse_openeuler_component_url, parse_openeuler_rpm_url

BASE_CSV_FIELDS = {"comp_name", "version", "url"}
PARSED_URL_FIELDS = [
    "comp_name",
    "rpm_version",
    "release",
    "arch",
    "epoch",
    "epoch_known",
    "version",
    "url",
]


def parsed_url_record(url):
    """把一个 RPM URL 转换为结构化记录；Epoch 明确标记为未知。"""
    parts = parse_openeuler_rpm_url(url)
    return {
        "comp_name": parts.name,
        "rpm_version": parts.version,
        "release": parts.release,
        "arch": parts.filename_arch,
        "epoch": None,
        "epoch_known": False,
        "version": parts.composite_version,
        "url": url,
    }


def _atomic_text_writer(path, newline=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline=newline,
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    )
    try:
        # NamedTemporaryFile 默认是 0600。保留已有文件权限，新文件使用 0644。
        mode = path.stat().st_mode & 0o7777 if path.exists() else 0o644
        os.chmod(temporary.name, mode)
    except Exception:
        temporary.close()
        Path(temporary.name).unlink(missing_ok=True)
        raise
    return path, temporary


def _write_compatibility_csv(rows_by_url, output_csv):
    path, temporary = _atomic_text_writer(output_csv, newline="")
    try:
        writer = csv.writer(temporary, lineterminator="\n")
        writer.writerow(["comp_name", "version", "url"])
        for url in sorted(rows_by_url):
            comp_name, version = rows_by_url[url]
            writer.writerow([comp_name, version, url])
        temporary.close()
        os.replace(temporary.name, path)
    except Exception:
        temporary.close()
        Path(temporary.name).unlink(missing_ok=True)
        raise


def generate_csv_from_urls(urls, output_csv):
    """从 URL iterable 生成稳定排序、去重的兼容三列 CSV。"""
    rows_by_url = {}
    for index, raw_url in enumerate(urls, 1):
        url = raw_url.strip()
        if not url:
            continue
        try:
            rows_by_url[url] = parse_openeuler_component_url(url)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"URL item {index}: {exc}") from exc
    _write_compatibility_csv(rows_by_url, output_csv)


def generate_csv_from_url_lists(input_dir, output_csv):
    """读取目录内全部 ``*.txt`` URL 列表并生成兼容三列 CSV。"""
    rows_by_url = {}
    for path in sorted(Path(input_dir).glob("*.txt")):
        with path.open("r", encoding="utf-8") as source:
            for line_number, raw_line in enumerate(source, 1):
                url = raw_line.strip()
                if not url:
                    continue
                try:
                    rows_by_url[url] = parse_openeuler_component_url(url)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"{path}:{line_number}: {exc}") from exc
    _write_compatibility_csv(rows_by_url, output_csv)


def normalize_csv(csv_path, output_path=None):
    """按 URL 修正 comp_name/version，保留字段和行序并原子写入。

    返回实际修正行数。原地处理且 0 行变化时不替换原文件。
    """
    csv_path = Path(csv_path)
    output_path = Path(output_path) if output_path else csv_path
    changed = 0
    path, temporary = _atomic_text_writer(output_path, newline="")
    try:
        with csv_path.open("r", encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source)
            if reader.fieldnames is None or not BASE_CSV_FIELDS.issubset(
                reader.fieldnames
            ):
                raise ValueError(f"invalid CSV header: {reader.fieldnames!r}")
            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                raise ValueError(f"duplicate CSV header: {reader.fieldnames!r}")

            writer = csv.DictWriter(
                temporary, fieldnames=list(reader.fieldnames), lineterminator="\n"
            )
            writer.writeheader()
            for line_number, row in enumerate(reader, 2):
                if None in row:
                    raise ValueError(f"line {line_number}: unexpected extra CSV fields")
                comp_name, version = parse_openeuler_component_url(row["url"])
                if (row["comp_name"], row["version"]) != (comp_name, version):
                    row["comp_name"] = comp_name
                    row["version"] = version
                    changed += 1
                writer.writerow(row)

        temporary.close()
        if changed == 0 and output_path == csv_path:
            Path(temporary.name).unlink()
        else:
            os.replace(temporary.name, path)
    except Exception:
        temporary.close()
        Path(temporary.name).unlink(missing_ok=True)
        raise
    return changed


def validate_csv(csv_path):
    """严格验证 URL、组件名和兼容 version，返回错误字符串列表。"""
    errors = []
    seen_urls = set()
    with Path(csv_path).open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not BASE_CSV_FIELDS.issubset(reader.fieldnames):
            return [f"invalid CSV header: {reader.fieldnames!r}"]
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            return [f"duplicate CSV header: {reader.fieldnames!r}"]

        for line_number, row in enumerate(reader, 2):
            if None in row:
                errors.append(f"line {line_number}: unexpected extra CSV fields")
            if not all(row.get(field) for field in BASE_CSV_FIELDS):
                errors.append(f"line {line_number}: empty required field")
                continue

            url = row["url"]
            if url in seen_urls:
                errors.append(f"line {line_number}: duplicate URL: {url}")
            seen_urls.add(url)

            try:
                actual = parse_openeuler_component_url(url)
            except (TypeError, ValueError) as exc:
                errors.append(f"line {line_number}: parse error: {exc}")
                continue

            expected = (row["comp_name"], row["version"])
            if actual != expected:
                errors.append(
                    f"line {line_number}: expected {expected!r}, parsed {actual!r}"
                )
    return errors


def _parse_urls_to_stdout(urls):
    writer = csv.DictWriter(
        sys.stdout, fieldnames=PARSED_URL_FIELDS, lineterminator="\n"
    )
    writer.writeheader()
    error_count = 0
    for url in urls:
        try:
            writer.writerow(parsed_url_record(url))
        except (TypeError, ValueError) as exc:
            error_count += 1
            print(f"{url}: {exc}", file=sys.stderr)
    return 1 if error_count else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_parser = subparsers.add_parser(
        "parse", help="解析一个或多个 RPM URL，结果以 CSV 输出到 stdout"
    )
    parse_parser.add_argument("url", nargs="+")

    validate_parser = subparsers.add_parser("validate", help="严格验证三列 CSV")
    validate_parser.add_argument("csv", nargs="+", type=Path)

    normalize_parser = subparsers.add_parser(
        "normalize", help="按 URL 修正 CSV 中的组件名和版本"
    )
    normalize_parser.add_argument("csv", nargs="+", type=Path)

    rebuild_parser = subparsers.add_parser(
        "rebuild-local", help="从本地 TXT URL 列表重新生成三列 CSV"
    )
    rebuild_parser.add_argument("input_dir", type=Path)
    rebuild_parser.add_argument("output_csv", type=Path)

    args = parser.parse_args(argv)

    if args.command == "parse":
        return _parse_urls_to_stdout(args.url)

    if args.command == "validate":
        error_count = 0
        for path in args.csv:
            errors = validate_csv(path)
            if errors:
                error_count += len(errors)
                for error in errors:
                    print(f"{path}: {error}")
            else:
                print(f"{path}: OK")
        return 1 if error_count else 0

    if args.command == "normalize":
        for path in args.csv:
            changed = normalize_csv(path)
            print(f"{path}: normalized_rows={changed}")
        return 0

    generate_csv_from_url_lists(args.input_dir, args.output_csv)
    print(f"wrote {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
