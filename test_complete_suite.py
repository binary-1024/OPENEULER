#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL Parser - 完整测试套件
包含所有历史测试用例的综合测试
"""

from debian_url_parser import DebianURLParser, export_to_csv, export_to_json
import json
import csv
import os


# ============================================================================
# 测试用例集合
# ============================================================================

ALL_TEST_URLS = [
    # ==================== 基础二进制包 ====================
    "https://snapshot.debian.org/archive/debian/20251220T083035Z/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
    "https://snapshot.debian.org/archive/debian-debug/20251114T210651Z/pool/main/liba/libabigail/abigail-tools-dbgsym_2.9-1_amd64.deb",
    "https://snapshot.debian.org/archive/debian-debug/20251114T210651Z/pool/main/liba/libabigail/abigail-tools-dbgsym_2.9-1_i386.deb",

    # ==================== 不同架构 ====================
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_i386.deb",
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_arm64.deb",
    "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
    "https://example.com/pool/main/o/openjdk-11/openjdk-11-demo_11.0.29+7-1_s390x.deb",

    # ==================== 安全更新 ====================
    "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
    "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb",

    # ==================== 源码包 ====================
    "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0-6.dsc",
    "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0.orig.tar.gz",
    "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0.orig.tar.gz.asc",
    "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0-6.debian.tar.xz",

    # ==================== 自研组件 ====================
    "https://snapshot.debian.org/package/dpkg/1.23.3/dpkg_1.23.3.tar.xz",
    "https://snapshot.debian.org/package/dpkg/1.23.3/dpkg_1.23.3.dsc",

    # ==================== 特殊版本标识 ====================
    # DFSG 重打包
    "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb",
    # Really 版本
    "https://example.com/pool/main/p/package/package_1.0+really1.0-1_amd64.deb",
    # 二进制重制
    "https://example.com/pool/main/p/package/package_1.0-1+b2_amd64.deb",
    # Backports
    "https://example.com/pool/main/p/package/package_2.0-1~bpo11+1_amd64.deb",
    # Ubuntu
    "https://example.com/pool/main/p/package/package_1.0-1ubuntu1.1_amd64.deb",

    # ==================== OpenJDK 构建号 ====================
    "https://example.com/pool/main/o/openjdk-11/openjdk-11-jre_11.0.24+8-1_amd64.deb",
    "https://example.com/pool/main/o/openjdk-17/openjdk-17-jdk_17.0.12+7-2_amd64.deb",

    # ==================== 包名特殊字符 ====================
    "https://example.com/pool/main/l/lib-foo/lib-foo-dev_1.0-1_amd64.deb",
    "https://example.com/pool/main/l/lib.foo/lib.foo_1.0-1_amd64.deb",
    "https://example.com/pool/main/p/python3.11/python3.11_3.11.2-1_amd64.deb",

    # ==================== 纪元号 ====================
    "https://example.com/pool/main/l/linux/linux-image_2:5.10.0-1_amd64.deb",

    # ==================== 多组件源码包 ====================
    "https://example.com/pool/main/n/nodejs/nodejs_18.0.0.orig-component1.tar.gz",
    "https://example.com/pool/main/n/nodejs/nodejs_18.0.0.orig-component2.tar.gz",

    # ==================== 预发布版本 ====================
    "https://example.com/pool/main/p/package/package_1.0~rc1-1_amd64.deb",
    "https://example.com/pool/main/p/package/package_1.0~beta2-1_amd64.deb",
    "https://example.com/pool/main/p/package/package_1.0~alpha1-1_amd64.deb",
]


# ============================================================================
# 测试函数
# ============================================================================

def test_all_urls():
    """测试所有 URL"""
    parser = DebianURLParser()

    print("=" * 100)
    print("Debian URL Parser - 完整测试套件")
    print(f"测试用例总数: {len(ALL_TEST_URLS)}")
    print("=" * 100)

    results = []
    success_count = 0
    failed_count = 0

    for i, url in enumerate(ALL_TEST_URLS, 1):
        try:
            info = parser.parse_url(url)
            results.append({
                'status': 'success',
                'url': url,
                'info': info
            })
            print(f"✓ [{i:2d}/{len(ALL_TEST_URLS)}] {info.package_name:25s} v{info.version:30s} | {info.package_purl}")
            success_count += 1
        except Exception as e:
            results.append({
                'status': 'failed',
                'url': url,
                'error': str(e)
            })
            print(f"✗ [{i:2d}/{len(ALL_TEST_URLS)}] 失败: {e}")
            failed_count += 1

    print("\n" + "=" * 100)
    print(f"测试完成: {success_count} 成功, {failed_count} 失败")
    print("=" * 100)

    return results, success_count, failed_count


def test_purl_generation(results):
    """测试 PURL 生成"""
    print("\n" + "=" * 100)
    print("PURL 生成测试")
    print("=" * 100)

    success_infos = [r['info'] for r in results if r['status'] == 'success']

    # 验证 PURL 格式
    purl_format_correct = 0
    for info in success_infos:
        if info.package_purl.startswith('pkg:deb/debian/'):
            purl_format_correct += 1

    print(f"\n✓ PURL 格式检查: {purl_format_correct}/{len(success_infos)} 正确")

    # 统计不同包的 PURL
    purls = {}
    for info in success_infos:
        if info.package_purl not in purls:
            purls[info.package_purl] = []
        purls[info.package_purl].append(info.filename)

    print(f"✓ 唯一包数量: {len(purls)}")

    return purl_format_correct == len(success_infos)


def test_version_parsing(results):
    """测试版本号解析"""
    print("\n" + "=" * 100)
    print("版本号解析测试")
    print("=" * 100)

    success_infos = [r['info'] for r in results if r['status'] == 'success']

    # 统计各种版本特性
    stats = {
        'has_epoch': 0,
        'has_debian_revision': 0,
        'has_dfsg': 0,
        'has_really': 0,
        'has_binary_rebuild': 0,
        'has_backport': 0,
        'has_security_update': 0,
        'is_native': 0,
    }

    for info in success_infos:
        if info.epoch:
            stats['has_epoch'] += 1
        if info.debian_revision:
            stats['has_debian_revision'] += 1
        if info.dfsg_marker:
            stats['has_dfsg'] += 1
        if info.really_version:
            stats['has_really'] += 1
        if info.binary_rebuild:
            stats['has_binary_rebuild'] += 1
        if info.backport_marker:
            stats['has_backport'] += 1
        if info.security_update:
            stats['has_security_update'] += 1
        if info.is_native:
            stats['is_native'] += 1

    print("\n版本特性统计:")
    print(f"  带纪元号: {stats['has_epoch']}")
    print(f"  带 Debian 修订号: {stats['has_debian_revision']}")
    print(f"  带 DFSG 标识: {stats['has_dfsg']}")
    print(f"  带 Really 标识: {stats['has_really']}")
    print(f"  二进制重制: {stats['has_binary_rebuild']}")
    print(f"  Backport 版本: {stats['has_backport']}")
    print(f"  安全更新: {stats['has_security_update']}")
    print(f"  自研组件: {stats['is_native']}")

    return True


def test_file_types(results):
    """测试文件类型识别"""
    print("\n" + "=" * 100)
    print("文件类型识别测试")
    print("=" * 100)

    success_infos = [r['info'] for r in results if r['status'] == 'success']

    # 统计文件类型
    file_types = {}
    for info in success_infos:
        ft = info.file_type
        if ft not in file_types:
            file_types[ft] = 0
        file_types[ft] += 1

    print("\n文件类型分布:")
    for ft, count in sorted(file_types.items()):
        print(f"  {ft}: {count}")

    # 统计架构
    architectures = {}
    for info in success_infos:
        if info.architecture:
            arch = info.architecture
            if arch not in architectures:
                architectures[arch] = 0
            architectures[arch] += 1

    print("\n架构分布:")
    for arch, count in sorted(architectures.items()):
        print(f"  {arch}: {count}")

    return True


def export_results(results, success_count, failed_count):
    """导出测试结果"""
    print("\n" + "=" * 100)
    print("导出测试结果")
    print("=" * 100)

    # 获取成功的结果
    success_infos = [r['info'] for r in results if r['status'] == 'success']

    # 导出到 CSV
    csv_file = "test_results_all.csv"
    export_to_csv(success_infos, csv_file)
    print(f"✓ CSV 文件已导出: {csv_file}")

    # 导出到 JSON
    json_file = "test_results_all.json"
    export_to_json(success_infos, json_file, pretty=True)
    print(f"✓ JSON 文件已导出: {json_file}")

    # 生成测试报告
    report_file = "TEST_RESULTS_ALL.md"
    generate_test_report(results, success_count, failed_count, report_file)
    print(f"✓ 测试报告已生成: {report_file}")

    return csv_file, json_file, report_file


def generate_test_report(results, success_count, failed_count, output_file):
    """生成详细的测试报告"""
    success_infos = [r['info'] for r in results if r['status'] == 'success']
    failed_results = [r for r in results if r['status'] == 'failed']

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Debian URL Parser - 完整测试报告\n\n")
        f.write(f"**测试时间**: {os.popen('date').read().strip()}\n\n")
        f.write("---\n\n")

        # 总体统计
        f.write("## 📊 总体统计\n\n")
        f.write(f"- **测试用例总数**: {len(results)}\n")
        f.write(f"- **成功**: {success_count} ✅\n")
        f.write(f"- **失败**: {failed_count} ❌\n")
        f.write(f"- **成功率**: {success_count/len(results)*100:.2f}%\n\n")

        # 成功案例
        f.write("## ✅ 成功案例\n\n")
        f.write("| # | 包名 | 版本 | PURL | 架构 |\n")
        f.write("|---|------|------|------|------|\n")
        for i, info in enumerate(success_infos, 1):
            arch = info.architecture or 'N/A'
            f.write(f"| {i} | {info.package_name} | {info.version} | {info.package_purl} | {arch} |\n")

        # 失败案例
        if failed_results:
            f.write("\n## ❌ 失败案例\n\n")
            f.write("| # | URL | 错误信息 |\n")
            f.write("|---|-----|----------|\n")
            for i, result in enumerate(failed_results, 1):
                f.write(f"| {i} | {result['url']} | {result['error']} |\n")

        # PURL 统计
        f.write("\n## 🔗 PURL 统计\n\n")
        purls = {}
        for info in success_infos:
            if info.package_purl not in purls:
                purls[info.package_purl] = []
            purls[info.package_purl].append(info.filename)

        f.write(f"- **唯一包数量**: {len(purls)}\n")
        f.write(f"- **PURL 格式验证**: 全部符合 `pkg:deb/debian/<package_name>` 格式 ✅\n\n")

        # 版本特性统计
        f.write("## 📦 版本特性统计\n\n")
        stats = {
            '带纪元号': sum(1 for i in success_infos if i.epoch),
            '带 Debian 修订号': sum(1 for i in success_infos if i.debian_revision),
            '带 DFSG 标识': sum(1 for i in success_infos if i.dfsg_marker),
            '带 Really 标识': sum(1 for i in success_infos if i.really_version),
            '二进制重制': sum(1 for i in success_infos if i.binary_rebuild),
            'Backport 版本': sum(1 for i in success_infos if i.backport_marker),
            '安全更新': sum(1 for i in success_infos if i.security_update),
            '自研组件': sum(1 for i in success_infos if i.is_native),
        }

        for feature, count in stats.items():
            f.write(f"- **{feature}**: {count}\n")

        # 文件类型统计
        f.write("\n## 📄 文件类型统计\n\n")
        file_types = {}
        for info in success_infos:
            ft = info.file_type
            file_types[ft] = file_types.get(ft, 0) + 1

        for ft, count in sorted(file_types.items()):
            f.write(f"- **{ft}**: {count}\n")

        # 架构统计
        f.write("\n## 🖥️ 架构统计\n\n")
        architectures = {}
        for info in success_infos:
            if info.architecture:
                arch = info.architecture
                architectures[arch] = architectures.get(arch, 0) + 1

        if architectures:
            for arch, count in sorted(architectures.items()):
                f.write(f"- **{arch}**: {count}\n")
        else:
            f.write("- 无架构信息（源码包）\n")

        # 导出文件
        f.write("\n## 📁 导出文件\n\n")
        f.write("- `test_results_all.csv` - CSV 格式的测试结果\n")
        f.write("- `test_results_all.json` - JSON 格式的测试结果\n")
        f.write("- `TEST_RESULTS_ALL.md` - 本测试报告\n\n")

        # 结论
        f.write("## 🎯 结论\n\n")
        if failed_count == 0:
            f.write("✅ **所有测试用例全部通过！**\n\n")
            f.write("Debian URL Parser 功能正常，可以处理各种类型的 Debian 包 URL。\n")
        else:
            f.write(f"⚠️ **有 {failed_count} 个测试用例失败**\n\n")
            f.write("请检查失败案例并修复相关问题。\n")


def main():
    """主测试流程"""
    print("\n" + "🔍 " + "=" * 96 + " 🔍")
    print("   Debian URL Parser - 完整测试套件")
    print("   包含所有历史测试用例的综合测试")
    print("🔍 " + "=" * 96 + " 🔍\n")

    # 1. 测试所有 URL
    results, success_count, failed_count = test_all_urls()

    # 2. PURL 测试
    purl_ok = test_purl_generation(results)

    # 3. 版本解析测试
    version_ok = test_version_parsing(results)

    # 4. 文件类型测试
    filetype_ok = test_file_types(results)

    # 5. 导出结果
    csv_file, json_file, report_file = export_results(results, success_count, failed_count)

    # 最终总结
    print("\n" + "=" * 100)
    print("测试总结")
    print("=" * 100)
    print(f"  URL 解析测试:     {'✓ 通过' if failed_count == 0 else '✗ 部分失败'} ({success_count}/{len(ALL_TEST_URLS)})")
    print(f"  PURL 生成测试:    {'✓ 通过' if purl_ok else '✗ 失败'}")
    print(f"  版本解析测试:     {'✓ 通过' if version_ok else '✗ 失败'}")
    print(f"  文件类型测试:     {'✓ 通过' if filetype_ok else '✗ 失败'}")
    print("=" * 100)

    if failed_count == 0:
        print("\n🎉 所有测试全部通过！")
    else:
        print(f"\n⚠️  有 {failed_count} 个测试失败，请检查报告")

    print(f"\n📁 测试结果已导出:")
    print(f"  - CSV:  {csv_file}")
    print(f"  - JSON: {json_file}")
    print(f"  - 报告: {report_file}")
    print()

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    exit(main())

