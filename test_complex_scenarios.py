#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL 解析器 - 复杂场景测试

测试各种复杂的版本号组合场景
"""

from debian_url_parser import DebianURLParser


def test_complex_scenarios():
    """测试复杂场景"""
    parser = DebianURLParser()

    # 定义各种复杂测试场景
    test_cases = [
        {
            'name': '纪元号 + 普通版本',
            'url': 'https://example.com/pool/main/p/pkg/package_1:2.5.1-3_amd64.deb',
            'expected': {
                'epoch': '1',
                'upstream_version': '2.5.1',
                'debian_revision': '3',
            }
        },
        {
            'name': '纪元号 + 预发布版本',
            'url': 'https://example.com/pool/main/p/pkg/package_2:3.0~rc1-1_amd64.deb',
            'expected': {
                'epoch': '2',
                'upstream_version': '3.0~rc1',
                'debian_revision': '1',
            }
        },
        {
            'name': '纪元号 + DFSG + 安全更新',
            'url': 'https://example.com/pool/main/p/pkg/package_1:2.4.0+dfsg1-5+deb11u2_amd64.deb',
            'expected': {
                'epoch': '1',
                'upstream_version': '2.4.0',
                'debian_revision': '5',
                'dfsg_marker': 'dfsg1',
                'release_version': 'deb11',
                'security_update': 'u2',
            }
        },
        {
            'name': '预发布 + DFSG + 安全更新',
            'url': 'https://example.com/pool/main/p/pkg/package_3.0~beta2+dfsg1-2+deb12u1_amd64.deb',
            'expected': {
                'upstream_version': '3.0~beta2',
                'debian_revision': '2',
                'dfsg_marker': 'dfsg1',
                'release_version': 'deb12',
                'security_update': 'u1',
            }
        },
        {
            'name': '预发布 + Really + 安全更新',
            'url': 'https://example.com/pool/main/p/pkg/package_3.0~rc1+really2.5-1+deb11u3_amd64.deb',
            'expected': {
                'upstream_version': '3.0~rc1',
                'debian_revision': '1',
                'really_version': '2.5',
                'release_version': 'deb11',
                'security_update': 'u3',
            }
        },
        {
            'name': 'DFSG + Really + 二进制重制',
            'url': 'https://example.com/pool/main/p/pkg/package_2.0+dfsg1+really1.5-3+b2_amd64.deb',
            'expected': {
                'upstream_version': '2.0',
                'debian_revision': '3',
                'dfsg_marker': 'dfsg1',
                'really_version': '1.5',
                'binary_rebuild': 'b2',
            }
        },
        {
            'name': '纪元号 + 预发布 + DFSG + Backports',
            'url': 'https://example.com/pool/main/p/pkg/package_2:5.0~rc2+dfsg1-1~bpo11+2_amd64.deb',
            'expected': {
                'epoch': '2',
                'upstream_version': '5.0~rc2',
                'debian_revision': '1',
                'dfsg_marker': 'dfsg1',
                'backport_marker': 'bpo11+2',
            }
        },
        {
            'name': '复杂小版本号 + DFSG + 安全更新',
            'url': 'https://example.com/pool/main/p/pkg/package_1.2.3.4.5+dfsg2-0.1+deb12u5_amd64.deb',
            'expected': {
                'upstream_version': '1.2.3.4.5',
                'debian_revision': '0.1',
                'dfsg_marker': 'dfsg2',
                'release_version': 'deb12',
                'security_update': 'u5',
            }
        },
        {
            'name': 'Ubuntu 衍生版本 + 小版本',
            'url': 'https://example.com/pool/main/p/pkg/package_2.5.1-3ubuntu2.1_amd64.deb',
            'expected': {
                'upstream_version': '2.5.1',
                'debian_revision': '3',
                'ubuntu_marker': 'ubuntu2.1',
            }
        },
        {
            'name': 'NMU + 安全更新',
            'url': 'https://example.com/pool/main/p/pkg/package_1.8.0-2+nmu1+deb11u1_amd64.deb',
            'expected': {
                'upstream_version': '1.8.0',
                'debian_revision': '2',
                'nmu_marker': 'nmu1',
                'release_version': 'deb11',
                'security_update': 'u1',
            }
        },
        {
            'name': '预发布 + Git 快照（应被清理）',
            'url': 'https://example.com/pool/main/p/pkg/package_2.0~alpha1+git20231215-1_amd64.deb',
            'expected': {
                'upstream_version': '2.0~alpha1',  # +git 应被移除
                'debian_revision': '1',
            }
        },
        {
            'name': '复杂日期版本 + DFSG',
            'url': 'https://example.com/pool/main/p/pkg/package_20231215+dfsg1-2_amd64.deb',
            'expected': {
                'upstream_version': '20231215',
                'debian_revision': '2',
                'dfsg_marker': 'dfsg1',
            }
        },
        {
            'name': '纪元号 + 预发布 + DFSG + Really + 安全更新（终极复杂）',
            'url': 'https://example.com/pool/main/p/pkg/package_3:4.0~rc3+dfsg2+really3.5-2+deb12u3_amd64.deb',
            'expected': {
                'epoch': '3',
                'upstream_version': '4.0~rc3',
                'debian_revision': '2',
                'dfsg_marker': 'dfsg2',
                'really_version': '3.5',
                'release_version': 'deb12',
                'security_update': 'u3',
            }
        },
        {
            'name': '多个点号的版本 + 多个连字符的修订',
            'url': 'https://example.com/pool/main/p/pkg/package_5.10.197-1_amd64.deb',
            'expected': {
                'upstream_version': '5.10.197',
                'debian_revision': '1',
            }
        },
        {
            'name': '仅包含预发布标识',
            'url': 'https://example.com/pool/main/p/pkg/package_1.0~beta_amd64.deb',
            'expected': {
                'upstream_version': '1.0~beta',
                'debian_revision': None,
            }
        },
        {
            'name': '源码包 - DSC 文件',
            'url': 'https://snapshot.debian.org/package/nginx/1.28.0+dfsg1-6/nginx_1.28.0+dfsg1-6.dsc',
            'expected': {
                'upstream_version': '1.28.0',
                'debian_revision': '6',
                'dfsg_marker': 'dfsg1',
                'file_type': 'build_file',
                'distribution_type': 'source',
            }
        },
        {
            'name': '源码包 - orig.tar.gz',
            'url': 'https://snapshot.debian.org/package/nginx/1.28.0+dfsg1/nginx_1.28.0+dfsg1.orig.tar.gz',
            'expected': {
                'upstream_version': '1.28.0',
                'debian_revision': None,
                'dfsg_marker': 'dfsg1',
                'file_type': 'upstream_source',
                'distribution_type': 'source',
            }
        },
        {
            'name': '自研组件 - 无修订号',
            'url': 'https://snapshot.debian.org/package/dpkg/1.23.3/dpkg_1.23.3_armhf.deb',
            'expected': {
                'upstream_version': '1.23.3',
                'debian_revision': None,
                'is_native': True,
            }
        },
        {
            'name': '自研组件源码',
            'url': 'https://snapshot.debian.org/package/apt/2.9.8/apt_2.9.8.tar.xz',
            'expected': {
                'upstream_version': '2.9.8',
                'debian_revision': None,
                'file_type': 'native_source',
                'is_native': True,
            }
        },
        {
            'name': '全架构包（all）',
            'url': 'https://example.com/pool/main/p/pkg/package-doc_1.0-1_all.deb',
            'expected': {
                'package_name': 'package-doc',
                'upstream_version': '1.0',
                'debian_revision': '1',
                'architecture': 'all',
            }
        },
    ]

    print("=" * 100)
    print("Debian URL 解析器 - 复杂场景测试")
    print("=" * 100)

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test['name']}")
        print(f"  URL: {test['url']}")

        try:
            info = parser.parse_url(test['url'])

            # 验证期望值
            all_match = True
            mismatches = []

            for key, expected_value in test['expected'].items():
                actual_value = getattr(info, key, None)
                if actual_value != expected_value:
                    all_match = False
                    mismatches.append(f"{key}: 期望 '{expected_value}', 实际 '{actual_value}'")

            if all_match:
                print(f"  ✅ 通过")
                print(f"     完整版本: {info.version}")
                if info.epoch:
                    print(f"     纪元号: {info.epoch}")
                print(f"     上游版本: {info.upstream_version}")
                if info.debian_revision:
                    print(f"     Debian 修订: {info.debian_revision}")

                # 显示特殊标识
                markers = []
                if info.dfsg_marker:
                    markers.append(f"DFSG: {info.dfsg_marker}")
                if info.really_version:
                    markers.append(f"Really: {info.really_version}")
                if info.binary_rebuild:
                    markers.append(f"二进制重制: {info.binary_rebuild}")
                if info.backport_marker:
                    markers.append(f"Backports: {info.backport_marker}")
                if info.nmu_marker:
                    markers.append(f"NMU: {info.nmu_marker}")
                if info.ubuntu_marker:
                    markers.append(f"Ubuntu: {info.ubuntu_marker}")
                if info.release_version:
                    markers.append(f"发行版: {info.release_version}")
                if info.security_update:
                    markers.append(f"安全更新: {info.security_update}")

                if markers:
                    print(f"     特殊标识: {', '.join(markers)}")

                passed += 1
            else:
                print(f"  ❌ 失败")
                for mismatch in mismatches:
                    print(f"     - {mismatch}")
                failed += 1

        except Exception as e:
            print(f"  ❌ 异常: {e}")
            failed += 1

    print("\n" + "=" * 100)
    print(f"测试结果: {passed} 通过, {failed} 失败 (共 {len(test_cases)} 个测试)")
    print("=" * 100)

    return failed == 0


def test_edge_cases():
    """测试边界情况"""
    parser = DebianURLParser()

    print("\n" + "=" * 100)
    print("边界情况测试")
    print("=" * 100)

    edge_cases = [
        {
            'name': '非常长的版本号',
            'url': 'https://example.com/pool/main/p/pkg/package_1.2.3.4.5.6.7.8.9.10-1_amd64.deb',
        },
        {
            'name': '包含加号的包名',
            'url': 'https://example.com/pool/main/l/lib/libstdc++6_12.2.0-14_amd64.deb',
        },
        {
            'name': '包含点号的包名',
            'url': 'https://example.com/pool/main/p/pkg/package.name_1.0-1_amd64.deb',
        },
        {
            'name': '多架构包名',
            'url': 'https://example.com/pool/main/g/gcc/gcc-12-arm-linux-gnueabihf_12.2.0-14_amd64.deb',
        },
        {
            'name': '版本号为0',
            'url': 'https://example.com/pool/main/p/pkg/package_0-1_amd64.deb',
        },
        {
            'name': '修订号为0',
            'url': 'https://example.com/pool/main/p/pkg/package_1.0-0_amd64.deb',
        },
        {
            'name': '小数修订号',
            'url': 'https://example.com/pool/main/p/pkg/package_2.5-0.1_amd64.deb',
        },
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(edge_cases, 1):
        print(f"\n边界测试 {i}: {test['name']}")
        print(f"  URL: {test['url']}")

        try:
            info = parser.parse_url(test['url'])
            print(f"  ✅ 解析成功")
            print(f"     包名: {info.package_name}")
            print(f"     上游版本: {info.upstream_version}")
            print(f"     Debian 修订: {info.debian_revision}")
            passed += 1
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
            failed += 1

    print("\n" + "=" * 100)
    print(f"边界测试结果: {passed} 通过, {failed} 失败 (共 {len(edge_cases)} 个测试)")
    print("=" * 100)

    return failed == 0


def main():
    """主函数"""
    print("\n🧪 开始运行复杂场景测试...\n")

    result1 = test_complex_scenarios()
    result2 = test_edge_cases()

    print("\n" + "=" * 100)
    if result1 and result2:
        print("✅ 所有复杂场景测试通过！")
    else:
        print("❌ 部分测试失败，请检查上述输出")
    print("=" * 100 + "\n")

    return 0 if (result1 and result2) else 1


if __name__ == "__main__":
    exit(main())

