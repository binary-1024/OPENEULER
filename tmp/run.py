#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兼容入口：实际实现位于仓库根目录，避免 tmp 中保留过期副本。"""

import importlib.util
from pathlib import Path

ROOT_MODULE = Path(__file__).resolve().parents[1] / "run.py"
SPEC = importlib.util.spec_from_file_location("_openeuler_run_root", ROOT_MODULE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

parsed_url_record = MODULE.parsed_url_record
generate_csv_from_urls = MODULE.generate_csv_from_urls
generate_csv_from_url_lists = MODULE.generate_csv_from_url_lists
normalize_csv = MODULE.normalize_csv
validate_csv = MODULE.validate_csv
main = MODULE.main


if __name__ == "__main__":
    raise SystemExit(main())
