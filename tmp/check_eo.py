#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兼容入口：实际实现位于仓库根目录，避免 tmp 中保留过期副本。"""

import importlib.util
from pathlib import Path

ROOT_MODULE = Path(__file__).resolve().parents[1] / "check_eo.py"
SPEC = importlib.util.spec_from_file_location("_openeuler_check_oe_root", ROOT_MODULE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

check_lines_without_eo = MODULE.check_lines_without_eo
check_rows_without_oe_release = MODULE.check_rows_without_oe_release
release_has_oe_marker = MODULE.release_has_oe_marker
main = MODULE.main


if __name__ == "__main__":
    raise SystemExit(main())
