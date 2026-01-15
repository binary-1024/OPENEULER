#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：批量解析 Debian URL 并导出到 CSV 文件
"""

from debian_url_parser import DebianURLParser, export_to_csv


def main():
    """批量解析 URL 并导出到 CSV"""

    # 创建解析器
    parser = DebianURLParser()

    # 示例 URL 列表
    urls = [
        # 二进制包
        "https://example.com/pool/main/o/openjdk-11/openjdk-11-demo_11.0.29+7-1_s390x.deb",
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
        "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
        "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
        "https://snapshot.debian.org/archive/debian/20251220T083035Z/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",

        # 源码包
        "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.dsc",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0.orig.tar.gz",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0.orig.tar.gz.asc",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.debian.tar.xz",

        # 自研组件
        "https://example.com/pool/main/d/dpkg/dpkg_1.23.3.tar.xz",
        "https://example.com/pool/main/d/dpkg/dpkg_1.23.3.dsc",

        # 带特殊标识的版本
        "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0+really1.0-1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0-1+b2_amd64.deb",
        "https://example.com/pool/main/p/package/package_2.0-1~bpo11+1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0-1ubuntu1.1_amd64.deb",
    ]

    print("="*80)
    print("Debian URL 批量解析并导出到 CSV")
    print("="*80)

    # 解析所有 URL
    package_infos = []
    success_count = 0
    failed_count = 0

    print(f"\n开始解析 {len(urls)} 个 URL...\n")

    for i, url in enumerate(urls, 1):
        try:
            info = parser.parse_url(url)
            package_infos.append(info)
            print(f"✓ [{i:2d}/{len(urls)}] {info.package_name:20s} v{info.version:25s} -> {info.package_purl}")
            success_count += 1
        except ValueError as e:
            print(f"✗ [{i:2d}/{len(urls)}] 解析失败: {e}")
            failed_count += 1

    print(f"\n解析完成: {success_count} 成功, {failed_count} 失败")

    # 导出到 CSV
    if package_infos:
        output_file = "debian_packages_output.csv"
        print(f"\n正在导出到 CSV 文件: {output_file}")
        export_to_csv(package_infos, output_file)

        print(f"\n✓ 导出完成！")
        print(f"  文件路径: {output_file}")
        print(f"  记录数量: {len(package_infos)}")

        # 显示文件预览
        print(f"\n文件预览 (前 5 行):")
        print("-"*80)
        with open(output_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 6:  # 表头 + 前5行数据
                    print(line.rstrip())
                else:
                    break
        print("-"*80)

    print("\n" + "="*80)


if __name__ == "__main__":
    main()

