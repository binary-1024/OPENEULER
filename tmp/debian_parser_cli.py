#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL 解析器命令行工具

用法:
    python3 debian_parser_cli.py <url>                    # 解析单个 URL
    python3 debian_parser_cli.py --file urls.txt          # 批量解析文件中的 URL
    python3 debian_parser_cli.py --json <url>             # 输出 JSON 格式
    python3 debian_parser_cli.py --filter-type 二进制 <url> # 按类型过滤
"""

import sys
import json
import argparse
from debian_url_parser import DebianURLParser


def parse_single_url(parser, url, output_json=False):
    """解析单个 URL"""
    try:
        info = parser.parse_url(url)

        if output_json:
            # JSON 格式输出
            print(json.dumps(info.to_dict(), indent=2, ensure_ascii=False))
        else:
            # 友好格式输出
            print(f"\n{'='*80}")
            print(f"URL: {url}")
            print(f"{'='*80}")
            print(f"📦 文件名: {info.filename}")
            print(f"📌 组件名: {info.package_name}")
            print(f"🔢 版本: {info.version}")

            if info.architecture:
                print(f"🏗️  架构: {info.architecture}")

            print(f"📂 分发类型: {info.distribution_type}")
            print(f"📄 文件类型: {info.file_type}")
            print(f"🏠 是否自研: {'是' if info.is_native else '否'}")

            # 版本详情
            print(f"\n版本详情:")
            if info.epoch:
                print(f"  ⏰ 纪元号: {info.epoch}")
            print(f"  📌 上游版本: {info.upstream_version}")
            if info.debian_revision:
                print(f"  🔧 Debian 修订: {info.debian_revision}")

            # 特殊标识
            special_markers = []
            if info.dfsg_marker:
                special_markers.append(f"DFSG: {info.dfsg_marker}")
            if info.really_version:
                special_markers.append(f"Really: {info.really_version}")
            if info.binary_rebuild:
                special_markers.append(f"二进制重制: {info.binary_rebuild}")
            if info.backport_marker:
                special_markers.append(f"Backports: {info.backport_marker}")
            if info.nmu_marker:
                special_markers.append(f"NMU: {info.nmu_marker}")
            if info.ubuntu_marker:
                special_markers.append(f"Ubuntu: {info.ubuntu_marker}")
            if info.release_version:
                special_markers.append(f"发行版: {info.release_version}")
            if info.security_update:
                special_markers.append(f"安全更新: {info.security_update}")

            if special_markers:
                print(f"\n特殊标识:")
                for marker in special_markers:
                    print(f"  🏷️  {marker}")

            print(f"{'='*80}\n")

        return True

    except ValueError as e:
        print(f"❌ 解析失败: {e}", file=sys.stderr)
        return False


def parse_from_file(parser, filename, output_json=False, filter_type=None, filter_arch=None):
    """从文件批量解析 URL"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filename}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ 读取文件失败: {e}", file=sys.stderr)
        return False

    if not urls:
        print(f"⚠️  文件中没有找到有效的 URL", file=sys.stderr)
        return False

    results = []
    success_count = 0
    fail_count = 0

    print(f"\n📋 开始处理 {len(urls)} 个 URL...\n")

    for i, url in enumerate(urls, 1):
        try:
            info = parser.parse_url(url)

            # 应用过滤条件
            if filter_type and info.file_type != filter_type:
                continue
            if filter_arch and info.architecture != filter_arch:
                continue

            results.append(info)
            success_count += 1

            if not output_json:
                print(f"✅ [{i}/{len(urls)}] {info.package_name} v{info.version}")
                if info.architecture:
                    print(f"    架构: {info.architecture}, 类型: {info.file_type}")
                else:
                    print(f"    类型: {info.file_type}")

        except ValueError as e:
            fail_count += 1
            if not output_json:
                print(f"❌ [{i}/{len(urls)}] {url}")
                print(f"    错误: {e}")

    print(f"\n{'='*80}")
    print(f"处理完成: {success_count} 成功, {fail_count} 失败")

    if filter_type or filter_arch:
        print(f"过滤后结果: {len(results)} 个匹配项")

    print(f"{'='*80}\n")

    if output_json and results:
        print(json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False))

    return True


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='Debian URL 解析器命令行工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 解析单个 URL
  %(prog)s "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb"

  # 批量解析文件中的 URL
  %(prog)s --file urls.txt

  # 输出 JSON 格式
  %(prog)s --json "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb"

  # 按文件类型过滤
  %(prog)s --file urls.txt --filter-type 二进制

  # 按架构过滤
  %(prog)s --file urls.txt --filter-arch amd64

  # 组合使用
  %(prog)s --file urls.txt --filter-type 二进制 --filter-arch amd64 --json
        """
    )

    parser.add_argument('url', nargs='?', help='要解析的 Debian URL')
    parser.add_argument('--file', '-f', help='包含 URL 列表的文件路径（每行一个 URL）')
    parser.add_argument('--json', '-j', action='store_true', help='以 JSON 格式输出')
    parser.add_argument('--filter-type', '-t', help='按文件类型过滤（二进制/源码/上游源码/构建文件等）')
    parser.add_argument('--filter-arch', '-a', help='按架构过滤（amd64/i386/arm64等）')

    args = parser.parse_args()

    # 检查参数
    if not args.url and not args.file:
        parser.print_help()
        print("\n❌ 错误: 必须提供 URL 或使用 --file 参数指定文件", file=sys.stderr)
        return 1

    if args.url and args.file:
        print("❌ 错误: 不能同时指定 URL 和 --file 参数", file=sys.stderr)
        return 1

    # 创建解析器
    url_parser = DebianURLParser()

    # 执行解析
    if args.url:
        # 单个 URL 模式
        if args.filter_type or args.filter_arch:
            print("⚠️  警告: 过滤参数只在批量模式（--file）中有效", file=sys.stderr)

        success = parse_single_url(url_parser, args.url, args.json)
        return 0 if success else 1

    elif args.file:
        # 批量文件模式
        success = parse_from_file(
            url_parser,
            args.file,
            args.json,
            args.filter_type,
            args.filter_arch
        )
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

