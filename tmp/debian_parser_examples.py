#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL 解析器使用示例

演示如何使用 DebianURLParser 来解析 Debian 组件 URL
"""

from debian_url_parser import DebianURLParser
import json


def example_1_basic_usage():
    """示例 1：基础用法"""
    print("\n" + "="*80)
    print("示例 1: 基础用法 - 解析单个 URL")
    print("="*80)

    parser = DebianURLParser()

    # 解析一个二进制包 URL
    url = "https://snapshot.debian.org/archive/debian/20251220T083035Z/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb"

    info = parser.parse_url(url)

    print(f"\nURL: {url}")
    print(f"\n解析结果:")
    print(f"  组件名: {info.package_name}")
    print(f"  版本: {info.version}")
    print(f"  架构: {info.architecture}")
    print(f"  分发类型: {info.distribution_type}")
    print(f"  文件类型: {info.file_type}")
    print(f"  是否自研组件: {info.is_native}")


def example_2_batch_processing():
    """示例 2：批量处理多个 URL"""
    print("\n" + "="*80)
    print("示例 2: 批量处理 - 解析多个 URL")
    print("="*80)

    parser = DebianURLParser()

    urls = [
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.dsc",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0.orig.tar.gz",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.debian.tar.xz",
    ]

    print(f"\n处理 {len(urls)} 个 URL:\n")

    results = []
    for url in urls:
        try:
            info = parser.parse_url(url)
            results.append(info)
            print(f"✓ {info.filename}")
            print(f"  组件: {info.package_name}, 版本: {info.version}, 类型: {info.file_type}")
        except ValueError as e:
            print(f"✗ 解析失败: {e}")

    print(f"\n成功解析: {len(results)}/{len(urls)}")


def example_3_filter_by_type():
    """示例 3：按文件类型过滤"""
    print("\n" + "="*80)
    print("示例 3: 按文件类型过滤 - 只获取二进制包")
    print("="*80)

    parser = DebianURLParser()

    urls = [
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.dsc",
        "https://example.com/pool/main/n/nginx/nginx_1.28.0.orig.tar.gz",
        "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
        "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
    ]

    print("\n筛选条件: 文件类型 = 二进制\n")

    binary_packages = []
    for url in urls:
        try:
            info = parser.parse_url(url)
            if info.file_type == "二进制":
                binary_packages.append(info)
                print(f"✓ {info.package_name} v{info.version} ({info.architecture})")
        except ValueError:
            pass

    print(f"\n找到 {len(binary_packages)} 个二进制包")


def example_4_security_updates():
    """示例 4：识别安全更新包"""
    print("\n" + "="*80)
    print("示例 4: 识别安全更新包")
    print("="*80)

    parser = DebianURLParser()

    urls = [
        "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb",
    ]

    print("\n检查安全更新:\n")

    for url in urls:
        try:
            info = parser.parse_url(url)
            if info.security_update:
                print(f"🔐 安全更新: {info.package_name}")
                print(f"   版本: {info.version}")
                print(f"   发行版: {info.release_version}")
                print(f"   安全更新编号: {info.security_update}")
                print()
            else:
                print(f"📦 普通包: {info.package_name} v{info.version}")
                print()
        except ValueError as e:
            print(f"✗ 解析失败: {e}\n")


def example_5_native_vs_upstream():
    """示例 5：区分自研组件和上游组件"""
    print("\n" + "="*80)
    print("示例 5: 区分自研组件和上游组件")
    print("="*80)

    parser = DebianURLParser()

    urls = [
        "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",  # 自研
        "https://example.com/pool/main/d/dpkg/dpkg_1.23.3.tar.xz",  # 自研源码
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",  # 上游
        "https://example.com/pool/main/n/nginx/nginx_1.28.0.orig.tar.gz",  # 上游源码
    ]

    native_packages = []
    upstream_packages = []

    for url in urls:
        try:
            info = parser.parse_url(url)
            if info.is_native:
                native_packages.append(info)
            else:
                upstream_packages.append(info)
        except ValueError:
            pass

    print("\n🏠 Debian 自研组件:")
    for pkg in native_packages:
        print(f"  - {pkg.package_name} v{pkg.version} ({pkg.file_type})")

    print("\n🌐 上游组件:")
    for pkg in upstream_packages:
        print(f"  - {pkg.package_name} v{pkg.version} ({pkg.file_type})")


def example_6_export_to_json():
    """示例 6：导出为 JSON 格式"""
    print("\n" + "="*80)
    print("示例 6: 导出为 JSON 格式")
    print("="*80)

    parser = DebianURLParser()

    url = "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb"

    info = parser.parse_url(url)

    # 转换为字典
    data = info.to_dict()

    # 输出为 JSON
    json_str = json.dumps(data, indent=2, ensure_ascii=False)

    print(f"\nURL: {url}")
    print(f"\nJSON 输出:")
    print(json_str)


def example_7_complex_version():
    """示例 7：解析复杂版本号"""
    print("\n" + "="*80)
    print("示例 7: 解析复杂版本号")
    print("="*80)

    parser = DebianURLParser()

    # 包含多种特殊标识的版本
    urls = [
        "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0+really1.0-1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0-1+b2_amd64.deb",
        "https://example.com/pool/main/p/package/package_2.0-1~bpo11+1_amd64.deb",
    ]

    print("\n解析复杂版本号:\n")

    for url in urls:
        try:
            info = parser.parse_url(url)
            print(f"文件名: {info.filename}")
            print(f"  完整版本: {info.version}")
            print(f"  上游版本: {info.upstream_version}")
            if info.debian_revision:
                print(f"  Debian 修订: {info.debian_revision}")

            # 显示特殊标识
            special = []
            if info.dfsg_marker:
                special.append(f"DFSG重打包: {info.dfsg_marker}")
            if info.really_version:
                special.append(f"真正版本: {info.really_version}")
            if info.binary_rebuild:
                special.append(f"二进制重制: {info.binary_rebuild}")
            if info.backport_marker:
                special.append(f"反向移植: {info.backport_marker}")
            if info.release_version:
                special.append(f"发行版: {info.release_version}")
            if info.security_update:
                special.append(f"安全更新: {info.security_update}")

            if special:
                print(f"  特殊标识: {', '.join(special)}")
            print()

        except ValueError as e:
            print(f"✗ 解析失败: {e}\n")


def example_8_architecture_filter():
    """示例 8：按架构过滤"""
    print("\n" + "="*80)
    print("示例 8: 按架构过滤 - 只获取 amd64 架构的包")
    print("="*80)

    parser = DebianURLParser()

    urls = [
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_i386.deb",
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_arm64.deb",
        "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
        "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
    ]

    print("\n筛选条件: 架构 = amd64\n")

    amd64_packages = []
    for url in urls:
        try:
            info = parser.parse_url(url)
            if info.architecture == "amd64":
                amd64_packages.append(info)
                print(f"✓ {info.package_name} v{info.version}")
        except ValueError:
            pass

    print(f"\n找到 {len(amd64_packages)} 个 amd64 包")


def example_9_error_handling():
    """示例 9：错误处理"""
    print("\n" + "="*80)
    print("示例 9: 错误处理 - 处理无效的 URL")
    print("="*80)

    parser = DebianURLParser()

    invalid_urls = [
        "https://example.com/pool/main/invalid.txt",
        "https://example.com/pool/main/",
        "not_a_url",
    ]

    print("\n尝试解析无效 URL:\n")

    for url in invalid_urls:
        try:
            info = parser.parse_url(url)
            print(f"✓ 成功: {info.filename}")
        except ValueError as e:
            print(f"✗ {url}")
            print(f"  错误: {e}\n")


def main():
    """运行所有示例"""
    print("\n" + "="*80)
    print("Debian URL 解析器使用示例集")
    print("="*80)

    example_1_basic_usage()
    example_2_batch_processing()
    example_3_filter_by_type()
    example_4_security_updates()
    example_5_native_vs_upstream()
    example_6_export_to_json()
    example_7_complex_version()
    example_8_architecture_filter()
    example_9_error_handling()

    print("\n" + "="*80)
    print("所有示例运行完毕")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

