#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试特殊场景的URL解析

这个测试文件专门测试一些特殊的Debian包格式:
1. 老式 .diff.gz 补丁格式 (Debian 3.0 之前)
2. .udeb 安装器微型包
3. 包名中包含大写字母的老包
4. 文件名中不包含架构信息的老式二进制包
"""

import sys
from debian_url_parser import DebianURLParser


def test_special_cases():
    """测试特殊场景"""
    parser = DebianURLParser()

    test_cases = [
        {
            'name': '老式二进制包(文件名无架构,路径中有架构)',
            'url': 'https://snapshot.debian.org/archive/debian-archive/20090802T004153Z/debian/dists/slink/contrib/binary-i386/misc/dbf2mysqL_1.10b-2.deb',
            'expected': {
                'package_name': 'dbf2mysqL',
                'architecture': 'i386',
                'upstream_version': '1.10b',
                'debian_revision': '2',
                'file_type': 'binary',
            }
        },
        {
            'name': '老式.diff.gz补丁格式',
            'url': 'https://snapshot.debian.org/archive/debian-archive/20110127T084257Z/debian/pool/main/a/dbf2mysqL/dbf2mysql_1.14a-3.1.diff.gz',
            'expected': {
                'package_name': 'dbf2mysql',
                'upstream_version': '1.14a',
                'debian_revision': '3.1',
                'file_type': 'upstream_source_patch',
            }
        },
        {
            'name': '老式.diff.gz补丁(Hamm时代)',
            'url': 'https://snapshot.debian.org/archive/debian-archive/20090802T004153Z/debian/dists/hamm/hamm/source/admin/dialdcost_0.2-1.diff.gz',
            'expected': {
                'package_name': 'dialdcost',
                'upstream_version': '0.2',
                'debian_revision': '1',
                'file_type': 'upstream_source_patch',
            }
        },
        {
            'name': '标准.diff.gz补丁',
            'url': 'https://snapshot.debian.org/archive/debian/20080815T000000Z/pool/main/d/djbdns/djbdns_1.05-4.diff.gz',
            'expected': {
                'package_name': 'djbdns',
                'upstream_version': '1.05',
                'debian_revision': '4',
                'file_type': 'upstream_source_patch',
            }
        },
        {
            'name': 'backport版本的.diff.gz',
            'url': 'https://snapshot.debian.org/archive/debian-archive/20110127T084257Z/debian-backports/pool/main/d/djbdns/djbdns_1.05-2~bpo40+1.diff.gz',
            'expected': {
                'package_name': 'djbdns',
                'upstream_version': '1.05',
                'debian_revision': '2',
                'backport_marker': 'bpo40+1',
                'file_type': 'upstream_source_patch',
            }
        },
        {
            'name': '实验性版本的.diff.gz (exp0)',
            'url': 'https://snapshot.debian.org/archive/debian/20100412T162845Z/pool/main/d/djbdns/djbdns_1.05-9~exp0.diff.gz',
            'expected': {
                'package_name': 'djbdns',
                'upstream_version': '1.05',
                'debian_revision': '9',
                'file_type': 'upstream_source_patch',
            }
        },
        {
            'name': '实验性版本的.diff.gz (exp1)',
            'url': 'https://snapshot.debian.org/archive/debian/20111026T214244Z/pool/main/d/djbdns/djbdns_1.05-9~exp1.diff.gz',
            'expected': {
                'package_name': 'djbdns',
                'upstream_version': '1.05',
                'debian_revision': '9',
                'file_type': 'upstream_source_patch',
            }
        },
        {
            'name': '实验性版本的.diff.gz (exp2)',
            'url': 'https://snapshot.debian.org/archive/debian/20130528T214604Z/pool/main/d/djbdns/djbdns_1.05-9~exp2.diff.gz',
            'expected': {
                'package_name': 'djbdns',
                'upstream_version': '1.05',
                'debian_revision': '9',
                'file_type': 'upstream_source_patch',
            }
        },
        {
            'name': 'Lenny安全更新的.dsc',
            'url': 'https://snapshot.debian.org/archive/debian-archive/20120328T092752Z/debian-security/pool/updates/main/d/djbdns/djbdns_1.05-4+Lenny1.dsc',
            'expected': {
                'package_name': 'djbdns',
                'upstream_version': '1.05',
                'debian_revision': '4',
                'file_type': 'build_file',
            }
        },
        {
            'name': '.udeb安装器包 (sh4架构)',
            'url': 'https://snapshot.debian.org/archive/debian-ports/20181024T093254Z/pool-sh4/main/e/espeak-ng/espeak-ng-data-udeb_1.49.2+dfsg-6_sh4.udeb',
            'expected': {
                'package_name': 'espeak-ng-data-udeb',
                'architecture': 'sh4',
                'upstream_version': '1.49.2',
                'debian_revision': '6',
                'dfsg_marker': 'dfsg',
                'file_type': 'binary',
            }
        },
        {
            'name': '.udeb安装器包 (kfreebsd-i386架构)',
            'url': 'https://snapshot.debian.org/archive/debian/20181027T032749Z/pool/main/e/espeak-ng/espeak-ng-data-udeb_1.49.2+dfsg-6_kfreebsd-i386.udeb',
            'expected': {
                'package_name': 'espeak-ng-data-udeb',
                'architecture': 'kfreebsd-i386',
                'upstream_version': '1.49.2',
                'debian_revision': '6',
                'dfsg_marker': 'dfsg',
                'file_type': 'binary',
            }
        },
        {
            'name': '.udeb安装器包 (amd64架构)',
            'url': 'https://snapshot.debian.org/archive/debian/20181024T025940Z/pool/main/e/espeak-ng/espeak-ng-data-udeb_1.49.2+dfsg-6_amd64.udeb',
            'expected': {
                'package_name': 'espeak-ng-data-udeb',
                'architecture': 'amd64',
                'upstream_version': '1.49.2',
                'debian_revision': '6',
                'dfsg_marker': 'dfsg',
                'file_type': 'binary',
            }
        },
        {
            'name': '.udeb安装器包 (armhf架构)',
            'url': 'https://snapshot.debian.org/archive/debian/20181024T025940Z/pool/main/e/espeak-ng/espeak-ng-data-udeb_1.49.2+dfsg-6_armhf.udeb',
            'expected': {
                'package_name': 'espeak-ng-data-udeb',
                'architecture': 'armhf',
                'upstream_version': '1.49.2',
                'debian_revision': '6',
                'dfsg_marker': 'dfsg',
                'file_type': 'binary',
            }
        },
    ]

    print('=' * 100)
    print('Debian URL 解析器 - 特殊场景测试')
    print('=' * 100)

    passed = 0
    failed = 0

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] {test_case['name']}")
        print(f"URL: {test_case['url']}")

        try:
            info = parser.parse_url(test_case['url'])

            # 验证期望的字段
            all_match = True
            for key, expected_value in test_case['expected'].items():
                actual_value = getattr(info, key)
                if actual_value != expected_value:
                    print(f"  ✗ 字段不匹配: {key}")
                    print(f"    期望: {expected_value}")
                    print(f"    实际: {actual_value}")
                    all_match = False

            if all_match:
                print(f"  ✓ 测试通过")
                print(f"    包名: {info.package_name}")
                print(f"    版本: {info.version}")
                if info.architecture:
                    print(f"    架构: {info.architecture}")
                print(f"    文件类型: {info.file_type}")
                passed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  ✗ 解析失败: {e}")
            failed += 1

    print(f'\n\n' + '=' * 100)
    print('测试总结')
    print('=' * 100)
    print(f'✓ 通过: {passed}/{len(test_cases)} ({passed*100//len(test_cases)}%)')
    print(f'✗ 失败: {failed}/{len(test_cases)}')

    if passed == len(test_cases):
        print('\n🎉 所有特殊场景测试全部通过!')
        return 0
    else:
        print(f'\n⚠️  有 {failed} 个测试失败')
        return 1


if __name__ == '__main__':
    sys.exit(test_special_cases())
