#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仅依据 RPM URL/文件名解析其中实际存在的字段。"""

import argparse
import sys
from typing import NamedTuple
from urllib.parse import unquote, urlsplit


class RpmFilenameParts(NamedTuple):
    """从 RPM 文件名可恢复的字段；Epoch 明确为未知。"""

    name: str
    version: str
    release: str
    filename_arch: str
    filename: str

    @property
    def epoch(self):
        """URL 文件名不携带 Epoch，因此始终返回 ``None``。"""
        return None

    @property
    def epoch_known(self):
        """URL-only 模式下 Epoch 永远不是已知字段。"""
        return False

    @property
    def composite_version(self):
        """返回项目历史格式 ``VERSION-RELEASE.文件名架构``。"""
        return f"{self.version}-{self.release}.{self.filename_arch}"

    @property
    def is_source_package(self):
        """文件名是否为 ``.src.rpm`` 或 ``.nosrc.rpm``。"""
        return self.filename_arch in {"src", "nosrc"}


def parse_openeuler_rpm_url(url):
    """解析 URL 或文件名中的 NAME、VERSION、RELEASE 和文件名架构。

    RPM 文件名结构为 ``NAME-VERSION-RELEASE.ARCH.rpm``。Epoch 不在
    文件名中，本函数不会把缺失的 Epoch 猜成 ``0``。
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    # 只解码 URL path，查询参数和 fragment 不参与文件名解析。
    path = unquote(urlsplit(url).path)
    filename = path.rsplit("/", 1)[-1]

    if not filename.endswith(".rpm"):
        raise ValueError(f"not an RPM filename: {filename!r}")

    # 精确删除后缀；rstrip('.rpm') 会把参数当作字符集合。
    nevra_without_epoch = filename[:-4]
    nvr, arch_separator, filename_arch = nevra_without_epoch.rpartition(".")
    if not arch_separator or not nvr or not filename_arch:
        raise ValueError(f"missing RPM architecture: {filename!r}")

    # RPM 的 Version/Release 标签不使用 '-'，所以从右侧最后两个 '-'
    # 可以稳定识别固定字段；NAME 可以包含任意数量的连字符和数字段。
    nvr_parts = nvr.rsplit("-", 2)
    if len(nvr_parts) != 3 or not all(nvr_parts):
        raise ValueError(f"invalid NAME-VERSION-RELEASE fields: {filename!r}")

    name, version, release = nvr_parts
    return RpmFilenameParts(name, version, release, filename_arch, filename)


def parse_openeuler_component_url(url):
    """兼容原接口，返回 ``(NAME, VERSION-RELEASE.ARCH)``。"""
    parts = parse_openeuler_rpm_url(url)
    return parts.name, parts.composite_version


def main(argv=None):
    """命令行解析一个或多个 RPM URL，不访问网络或仓库元数据。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="+", help="RPM URL 或 RPM 文件名")
    args = parser.parse_args(argv)

    error_count = 0
    for index, url in enumerate(args.url):
        if index:
            print()
        try:
            parts = parse_openeuler_rpm_url(url)
        except (TypeError, ValueError) as exc:
            error_count += 1
            print(f"url={url}", file=sys.stderr)
            print(f"error={exc}", file=sys.stderr)
            continue

        print(f"url={url}")
        print(f"comp_name={parts.name}")
        print(f"rpm_version={parts.version}")
        print(f"release={parts.release}")
        print(f"arch={parts.filename_arch}")
        print("epoch=unknown")
        print(f"version={parts.composite_version}")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
