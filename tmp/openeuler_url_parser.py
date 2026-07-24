#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兼容入口：实际实现位于仓库根目录，避免 tmp 中保留过期副本。"""

import importlib.util
from pathlib import Path

ROOT_MODULE = Path(__file__).resolve().parents[1] / "openeuler_url_parser.py"
SPEC = importlib.util.spec_from_file_location("_openeuler_url_parser_root", ROOT_MODULE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

RpmFilenameParts = MODULE.RpmFilenameParts
parse_openeuler_rpm_url = MODULE.parse_openeuler_rpm_url
parse_openeuler_component_url = MODULE.parse_openeuler_component_url
main = MODULE.main


if __name__ == "__main__":
    raise SystemExit(main())
