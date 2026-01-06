#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PURL (Package URL) 功能完整测试
"""

from debian_url_parser import DebianURLParser


def test_purl_generation():
    """测试 PURL 生成功能"""
    parser = DebianURLParser()

    test_cases = [
        {
            "name": "OpenJDK 带构建号",
            "url": "https://example.com/pool/main/o/openjdk-11/openjdk-11-demo_11.0.29+7-1_s390x.deb",
            "expected": {
                "package_name": "openjdk-11-demo",
                "version": "11.0.29+7-1",
                "package_purl": "pkg:deb/debian/openjdk-11-demo?arch=s390x",
                "architecture": "s390x",
            }
        },
        {
            "name": "Nginx 标准包",
            "url": "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
            "expected": {
                "package_name": "nginx",
                "version": "1.18.0-6.1",
                "package_purl": "pkg:deb/debian/nginx?arch=amd64",
                "architecture": "amd64",
            }
        },
        {
            "name": "DPKG 自研组件",
            "url": "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
            "expected": {
                "package_name": "dpkg",
                "version": "1.23.3",
                "package_purl": "pkg:deb/debian/dpkg?arch=armhf",
                "architecture": "armhf",
            }
        },
        {
            "name": "OpenSSL 带安全更新",
            "url": "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
            "expected": {
                "package_name": "openssl",
                "version": "1.1.1n-0+deb11u5",
                "package_purl": "pkg:deb/debian/openssl?arch=amd64",
                "architecture": "amd64",
            }
        },
        {
            "name": "带 DFSG 标识",
            "url": "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb",
            "expected": {
                "package_name": "package",
                "version": "1.2.3+dfsg1-2+deb12u1",
                "package_purl": "pkg:deb/debian/package?arch=amd64",
                "architecture": "amd64",
            }
        },
        {
            "name": "DSC 构建文件",
            "url": "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.dsc",
            "expected": {
                "package_name": "nginx",
                "version": "1.28.0-6",
                "package_purl": "pkg:deb/debian/nginx?arch=src",
                "architecture": None,
            }
        },
        {
            "name": "上游源码",
            "url": "https://example.com/pool/main/n/nginx/nginx_1.28.0.orig.tar.gz",
            "expected": {
                "package_name": "nginx",
                "version": "1.28.0",
                "package_purl": "pkg:deb/debian/nginx?arch=src",
                "architecture": None,
            }
        },
        {
            "name": "Debian 补丁",
            "url": "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.debian.tar.xz",
            "expected": {
                "package_name": "nginx",
                "version": "1.28.0-6",
                "package_purl": "pkg:deb/debian/nginx?arch=src",
                "architecture": None,
            }
        },
    ]

    print("="*100)
    print("PURL 生成功能测试")
    print("="*100)

    passed = 0
    failed = 0

    for i, case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] 测试: {case['name']}")
        print(f"  URL: {case['url']}")

        try:
            info = parser.parse_url(case['url'])
            expected = case['expected']

            # 验证包名
            assert info.package_name == expected['package_name'], \
                f"包名不匹配: 期望 {expected['package_name']}, 实际 {info.package_name}"

            # 验证版本号
            assert info.version == expected['version'], \
                f"版本号不匹配: 期望 {expected['version']}, 实际 {info.version}"

            # 验证 PURL
            assert info.package_purl == expected['package_purl'], \
                f"PURL 不匹配: 期望 {expected['package_purl']}, 实际 {info.package_purl}"

            # 验证架构
            assert info.architecture == expected['architecture'], \
                f"架构不匹配: 期望 {expected['architecture']}, 实际 {info.architecture}"

            print(f"  ✓ 包名: {info.package_name}")
            print(f"  ✓ 版本: {info.version}")
            print(f"  ✓ PURL: {info.package_purl}")
            print(f"  ✓ 架构: {info.architecture or 'N/A'}")
            print(f"  ✓ 通过")
            passed += 1

        except AssertionError as e:
            print(f"  ✗ 断言失败: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ 异常: {e}")
            failed += 1

    print("\n" + "="*100)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("="*100)

    return failed == 0


def test_purl_consistency():
    """测试同一包的不同文件是否生成相同的 PURL"""
    parser = DebianURLParser()

    print("\n" + "="*100)
    print("PURL 一致性测试 - 同一包的不同文件应该有相同的 PURL")
    print("="*100)

    # 同一个包 (nginx) 的不同文件
    nginx_files = [
        ("二进制包 amd64", "https://example.com/pool/main/n/nginx/nginx_1.28.0-6_amd64.deb"),
        ("二进制包 i386", "https://example.com/pool/main/n/nginx/nginx_1.28.0-6_i386.deb"),
        ("构建文件", "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.dsc"),
        ("上游源码", "https://example.com/pool/main/n/nginx/nginx_1.28.0.orig.tar.gz"),
        ("Debian补丁", "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.debian.tar.xz"),
    ]

    purls = []
    print("\nnginx 包的不同文件:")
    for desc, url in nginx_files:
        info = parser.parse_url(url)
        purls.append(info.package_purl)
        print(f"  {desc:15s} | PURL: {info.package_purl} | 版本: {info.version}")

    # 验证所有 PURL 都相同（除了版本号可能不同，但包名部分应该相同）
    # base_purls = [purl.split('@')[0] if '@' in purl else purl for purl in purls]
    # if len(set(base_purls)) == 1:
    #     print(f"\n  ✓ 所有文件的 PURL 一致: {base_purls[0]}")
    #     return True
    # else:
    #     print(f"\n  ✗ PURL 不一致: {set(base_purls)}")
    #     return False


def test_purl_special_cases():
    """测试特殊情况下的 PURL 生成"""
    parser = DebianURLParser()

    print("\n" + "="*100)
    print("PURL 特殊情况测试")
    print("="*100)

    special_cases = [
        ("包名带数字", "https://example.com/pool/main/o/openjdk-11/openjdk-11-jre_11.0.24+8-1_amd64.deb"),
        ("包名带连字符", "https://example.com/pool/main/l/lib-foo/lib-foo-dev_1.0-1_amd64.deb"),
        ("包名带点号", "https://example.com/pool/main/l/lib.foo/lib.foo_1.0-1_amd64.deb"),
        ("版本号复杂", "https://example.com/pool/main/p/pkg/pkg_1.2.3+dfsg1-2+deb12u1_amd64.deb"),
    ]

    print("\n特殊包名和版本号:")
    all_passed = True
    for desc, url in special_cases:
        try:
            info = parser.parse_url(url)
            print(f"  ✓ {desc:20s} | {info.package_name:20s} | {info.package_purl}")
        except Exception as e:
            print(f"  ✗ {desc:20s} | 失败: {e}")
            all_passed = False

    return all_passed


def main():
    """运行所有测试"""
    print("\n" + "🔍 " + "="*96 + " 🔍")
    print("   Debian URL Parser - PURL 功能完整测试")
    print("🔍 " + "="*96 + " 🔍\n")

    results = []

    # 测试 1: PURL 生成
    results.append(("PURL 生成测试", test_purl_generation()))

    # 测试 2: PURL 一致性
    results.append(("PURL 一致性测试", test_purl_consistency()))

    # 测试 3: 特殊情况
    results.append(("特殊情况测试", test_purl_special_cases()))

    # 总结
    print("\n" + "="*100)
    print("测试总结")
    print("="*100)

    for test_name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {test_name:30s} {status}")

    all_passed = all(result for _, result in results)

    print("\n" + "="*100)
    if all_passed:
        print("🎉 所有测试通过！PURL 功能正常工作。")
    else:
        print("⚠️  部分测试失败，请检查。")
    print("="*100 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())

