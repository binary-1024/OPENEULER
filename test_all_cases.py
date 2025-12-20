#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from debian_url_parser import DebianURLParser


class TestResult:
    """测试结果统计"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self):
        self.passed += 1

    def add_fail(self, test_name, error_msg):
        self.failed += 1
        self.errors.append((test_name, error_msg))

    def print_summary(self, category):
        total = self.passed + self.failed
        print(f"\n{category} 测试结果: {self.passed}/{total} 通过")
        if self.errors:
            print(f"失败的测试:")
            for name, error in self.errors:
                print(f"  ❌ {name}: {error}")


def run_test(parser, test_name, url, expected, result):
    """运行单个测试"""
    try:
        info = parser.parse_url(url)

        # 验证所有期望值
        all_match = True
        mismatches = []

        for key, expected_value in expected.items():
            actual_value = getattr(info, key, None)
            if actual_value != expected_value:
                all_match = False
                mismatches.append(f"{key}: 期望'{expected_value}', 实际'{actual_value}'")

        if all_match:
            result.add_pass()
            return True
        else:
            result.add_fail(test_name, '; '.join(mismatches))
            return False

    except Exception as e:
        result.add_fail(test_name, f"异常: {str(e)}")
        return False


def test_binary_basic(parser):
    """二进制包 - 基础测试"""
    print("\n" + "="*80)
    print("1.1 二进制制品包 - 基础测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("标准二进制包", "nginx_1.18.0-6_amd64.deb", {
            'package_name': 'nginx',
            'upstream_version': '1.18.0',
            'debian_revision': '6',
            'architecture': 'amd64',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
            'really_version': None,
            'binary_rebuild': None,
            'backport_marker': None,
            'release_version': None,
            'security_update': None,
        }),
        ("自研组件二进制包", "dpkg_1.23.3_armhf.deb", {
            'package_name': 'dpkg',
            'upstream_version': '1.23.3',
            'debian_revision': None,
            'architecture': 'armhf',
            'epoch': None,
            'is_native': True,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
            'really_version': None,
            'binary_rebuild': None,
        }),
        ("全架构包", "package-doc_1.0-1_all.deb", {
            'package_name': 'package-doc',
            'upstream_version': '1.0',
            'debian_revision': '1',
            'architecture': 'all',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.1 基础测试")
    return result


def test_binary_epoch(parser):
    """二进制包 - 纪元号测试"""
    print("\n" + "="*80)
    print("1.2 二进制制品包 - 纪元号测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("纪元号+标准版本", "package_1:2.5.1-3_amd64.deb", {
            'package_name': 'package',
            'epoch': '1',
            'upstream_version': '2.5.1',
            'debian_revision': '3',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
            'release_version': None,
            'security_update': None,
        }),
        ("纪元号+预发布版本", "package_2:3.0~rc1-1_amd64.deb", {
            'package_name': 'package',
            'epoch': '2',
            'upstream_version': '3.0~rc1',
            'debian_revision': '1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
        }),
        ("纪元号+DFSG+安全更新", "package_1:2.4.0+dfsg1-5+deb11u2_amd64.deb", {
            'package_name': 'package',
            'epoch': '1',
            'upstream_version': '2.4.0',
            'debian_revision': '5',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg1',
            'release_version': 'deb11',
            'security_update': 'u2',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.2 纪元号测试")
    return result


def test_binary_prerelease(parser):
    """二进制包 - 预发布版本测试"""
    print("\n" + "="*80)
    print("1.3 二进制制品包 - 预发布版本测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("RC候选版本", "package_1.0~rc1-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.0~rc1',
            'debian_revision': '1',
            'architecture': 'amd64',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
        }),
        ("Alpha测试版本", "package_2.0~alpha1-2_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '2.0~alpha1',
            'debian_revision': '2',
            'architecture': 'amd64',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("Beta测试版本", "package_3.0~beta2-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '3.0~beta2',
            'debian_revision': '1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("预发布+DFSG", "package_1.5~beta1+dfsg1-2_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.5~beta1',
            'debian_revision': '2',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg1',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("预发布+Git快照", "package_2.0~alpha1+git20231215-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '2.0~alpha1',
            'debian_revision': '1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.3 预发布版本测试")
    return result


def test_binary_security(parser):
    """二进制包 - 安全更新测试"""
    print("\n" + "="*80)
    print("1.4 二进制制品包 - 安全更新测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("标准安全更新", "openssl_1.1.1n-0+deb11u5_amd64.deb", {
            'package_name': 'openssl',
            'upstream_version': '1.1.1n',
            'debian_revision': '0',
            'architecture': 'amd64',
            'release_version': 'deb11',
            'security_update': 'u5',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
        }),
        ("DFSG+安全更新", "package_1.2.3+dfsg1-2+deb12u1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.2.3',
            'debian_revision': '2',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg1',
            'release_version': 'deb12',
            'security_update': 'u1',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("预发布+安全更新", "package_3.0~beta2+dfsg1-2+deb12u1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '3.0~beta2',
            'debian_revision': '2',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg1',
            'release_version': 'deb12',
            'security_update': 'u1',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.4 安全更新测试")
    return result


def test_binary_special_markers(parser):
    """二进制包 - 特殊标识测试"""
    print("\n" + "="*80)
    print("1.5 二进制制品包 - 特殊标识测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("Really版本标识", "package_1.0+really1.0-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.0',
            'debian_revision': '1',
            'architecture': 'amd64',
            'really_version': '1.0',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
            'binary_rebuild': None,
        }),
        ("二进制重制", "package_1.0-1+b2_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.0',
            'debian_revision': '1',
            'architecture': 'amd64',
            'binary_rebuild': 'b2',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
            'dfsg_marker': None,
        }),
        ("Backports移植", "package_2.0-1~bpo11+1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '2.0',
            'debian_revision': '1',
            'architecture': 'amd64',
            'backport_marker': 'bpo11+1',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("NMU上传", "package_1.8.0-2+nmu1+deb11u1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.8.0',
            'debian_revision': '2',
            'architecture': 'amd64',
            'nmu_marker': 'nmu1',
            'release_version': 'deb11',
            'security_update': 'u1',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("Ubuntu衍生版本", "package_2.5.1-3ubuntu2.1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '2.5.1',
            'debian_revision': '3',
            'architecture': 'amd64',
            'ubuntu_marker': 'ubuntu2.1',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.5 特殊标识测试")
    return result


def test_binary_complex(parser):
    """二进制包 - 复杂组合测试"""
    print("\n" + "="*80)
    print("1.6 二进制制品包 - 复杂组合测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("DFSG+Really+二进制重制", "package_2.0+dfsg1+really1.5-3+b2_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '2.0',
            'debian_revision': '3',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg1',
            'really_version': '1.5',
            'binary_rebuild': 'b2',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("预发布+Really+安全更新", "package_3.0~rc1+really2.5-1+deb11u3_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '3.0~rc1',
            'debian_revision': '1',
            'architecture': 'amd64',
            'really_version': '2.5',
            'release_version': 'deb11',
            'security_update': 'u3',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("纪元号+预发布+DFSG+Backports", "package_2:5.0~rc2+dfsg1-1~bpo11+2_amd64.deb", {
            'package_name': 'package',
            'epoch': '2',
            'upstream_version': '5.0~rc2',
            'debian_revision': '1',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg1',
            'backport_marker': 'bpo11+2',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("终极复杂组合", "package_3:4.0~rc3+dfsg2+really3.5-2+deb12u3_amd64.deb", {
            'package_name': 'package',
            'epoch': '3',
            'upstream_version': '4.0~rc3',
            'debian_revision': '2',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg2',
            'really_version': '3.5',
            'release_version': 'deb12',
            'security_update': 'u3',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.6 复杂组合测试")
    return result


def test_binary_version_formats(parser):
    """二进制包 - 特殊版本号格式测试"""
    print("\n" + "="*80)
    print("1.7 二进制制品包 - 特殊版本号格式测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("日期版本号", "package_20231215-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '20231215',
            'debian_revision': '1',
            'architecture': 'amd64',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("日期版本号+DFSG", "package_20231215+dfsg1-2_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '20231215',
            'debian_revision': '2',
            'architecture': 'amd64',
            'dfsg_marker': 'dfsg1',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("多级版本号", "package_5.10.197-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '5.10.197',
            'debian_revision': '1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("极长版本号", "package_1.2.3.4.5.6.7.8.9.10-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.2.3.4.5.6.7.8.9.10',
            'debian_revision': '1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("小数修订号", "package_2.5-0.1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '2.5',
            'debian_revision': '0.1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.7 特殊版本号格式测试")
    return result


def test_binary_package_names(parser):
    """二进制包 - 特殊包名格式测试"""
    print("\n" + "="*80)
    print("1.8 二进制制品包 - 特殊包名格式测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("包含加号的包名", "libstdc++6_12.2.0-14_amd64.deb", {
            'package_name': 'libstdc++6',
            'upstream_version': '12.2.0',
            'debian_revision': '14',
            'architecture': 'amd64',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("包含点号的包名", "package.name_1.0-1_amd64.deb", {
            'package_name': 'package.name',
            'upstream_version': '1.0',
            'debian_revision': '1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("交叉编译工具链包名", "gcc-12-arm-linux-gnueabihf_12.2.0-14_amd64.deb", {
            'package_name': 'gcc-12-arm-linux-gnueabihf',
            'upstream_version': '12.2.0',
            'debian_revision': '14',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("1.8 特殊包名格式测试")
    return result


def test_binary_architectures(parser):
    """二进制包 - 不同架构测试"""
    print("\n" + "="*80)
    print("1.9 二进制制品包 - 不同架构测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    architectures = ['amd64', 'i386', 'arm64', 'armhf', 'armel', 'ppc64el', 's390x', 'riscv64']

    for arch in architectures:
        filename = f"package_1.0-1_{arch}.deb"
        expected = {
            'architecture': arch,
            'package_name': 'package',
            'upstream_version': '1.0',
            'debian_revision': '1',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }
        url = base_url + filename
        success = run_test(parser, f"{arch}架构", url, expected, result)
        print(f"  {'✅' if success else '❌'} {arch} 架构")

    result.print_summary("1.9 不同架构测试")
    return result


def test_source_dsc(parser):
    """源码包 - DSC 构建文件测试"""
    print("\n" + "="*80)
    print("2.1 源码包 - DSC 构建文件测试")
    print("="*80)

    result = TestResult()
    base_url = "https://snapshot.debian.org/package/pkg/1.0/"

    tests = [
        ("标准DSC文件", "nginx_1.28.0-6.dsc", {
            'package_name': 'nginx',
            'upstream_version': '1.28.0',
            'debian_revision': '6',
            'architecture': None,
            'file_type': 'build_file',
            'distribution_type': 'source',
            'epoch': None,
            'is_native': False,
            'dfsg_marker': None,
        }),
        ("带DFSG的DSC", "package_1.2.3+dfsg1-2.dsc", {
            'package_name': 'package',
            'upstream_version': '1.2.3',
            'debian_revision': '2',
            'architecture': None,
            'dfsg_marker': 'dfsg1',
            'file_type': 'build_file',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("预发布版本DSC", "package_2.0~rc1-1.dsc", {
            'package_name': 'package',
            'upstream_version': '2.0~rc1',
            'debian_revision': '1',
            'architecture': None,
            'file_type': 'build_file',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("自研组件DSC", "dpkg_1.23.3.dsc", {
            'package_name': 'dpkg',
            'upstream_version': '1.23.3',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'build_file',
            'distribution_type': 'source',
            'is_native': True,
        }),
        ("带纪元号的DSC", "package_1:2.5.1-3.dsc", {
            'package_name': 'package',
            'epoch': '1',
            'upstream_version': '2.5.1',
            'debian_revision': '3',
            'architecture': None,
            'file_type': 'build_file',
            'distribution_type': 'source',
            'is_native': False,
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("2.1 DSC构建文件测试")
    return result


def test_source_orig(parser):
    """源码包 - 上游源码包测试"""
    print("\n" + "="*80)
    print("2.2 源码包 - 上游源码包测试")
    print("="*80)

    result = TestResult()
    base_url = "https://snapshot.debian.org/package/pkg/1.0/"

    tests = [
        ("标准orig.tar.gz", "nginx_1.28.0.orig.tar.gz", {
            'package_name': 'nginx',
            'upstream_version': '1.28.0',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'upstream_source',
            'distribution_type': 'source',
            'is_native': False,
            'epoch': None,
            'dfsg_marker': None,
        }),
        ("orig.tar.xz格式", "package_2.5.0.orig.tar.xz", {
            'package_name': 'package',
            'upstream_version': '2.5.0',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'upstream_source',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("orig.tar.bz2格式", "package_3.0.0.orig.tar.bz2", {
            'package_name': 'package',
            'upstream_version': '3.0.0',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'upstream_source',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("带DFSG的orig", "package_1.2.3+dfsg1.orig.tar.gz", {
            'package_name': 'package',
            'upstream_version': '1.2.3',
            'debian_revision': None,
            'architecture': None,
            'dfsg_marker': 'dfsg1',
            'file_type': 'upstream_source',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("预发布版本orig", "package_2.0~rc1.orig.tar.gz", {
            'package_name': 'package',
            'upstream_version': '2.0~rc1',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'upstream_source',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("orig签名文件", "nginx_1.28.0.orig.tar.gz.asc", {
            'package_name': 'nginx',
            'upstream_version': '1.28.0',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'upstream_source',
            'distribution_type': 'source',
            'is_native': False,
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("2.2 上游源码包测试")
    return result


def test_source_debian(parser):
    """源码包 - Debian 补丁包测试"""
    print("\n" + "="*80)
    print("2.3 源码包 - Debian 补丁包测试")
    print("="*80)

    result = TestResult()
    base_url = "https://snapshot.debian.org/package/pkg/1.0/"

    tests = [
        ("标准debian.tar.xz", "nginx_1.28.0-6.debian.tar.xz", {
            'package_name': 'nginx',
            'upstream_version': '1.28.0',
            'debian_revision': '6',
            'architecture': None,
            'file_type': 'upstream_source_patch',
            'distribution_type': 'source',
            'is_native': False,
            'epoch': None,
            'dfsg_marker': None,
        }),
        ("debian.tar.gz格式", "package_2.5.0-3.debian.tar.gz", {
            'package_name': 'package',
            'upstream_version': '2.5.0',
            'debian_revision': '3',
            'architecture': None,
            'file_type': 'upstream_source_patch',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("带DFSG的补丁包", "package_1.2.3+dfsg1-2.debian.tar.xz", {
            'package_name': 'package',
            'upstream_version': '1.2.3',
            'debian_revision': '2',
            'architecture': None,
            'dfsg_marker': 'dfsg1',
            'file_type': 'upstream_source_patch',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("预发布版本补丁包", "package_2.0~rc1-1.debian.tar.xz", {
            'package_name': 'package',
            'upstream_version': '2.0~rc1',
            'debian_revision': '1',
            'architecture': None,
            'file_type': 'upstream_source_patch',
            'distribution_type': 'source',
            'is_native': False,
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("2.3 Debian补丁包测试")
    return result


def test_source_native(parser):
    """源码包 - 自研组件源码测试"""
    print("\n" + "="*80)
    print("2.4 源码包 - 自研组件源码测试")
    print("="*80)

    result = TestResult()
    base_url = "https://snapshot.debian.org/package/pkg/1.0/"

    tests = [
        ("自研源码tar.xz", "dpkg_1.23.3.tar.xz", {
            'package_name': 'dpkg',
            'upstream_version': '1.23.3',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'native_source',
            'distribution_type': 'source',
            'is_native': True,
            'epoch': None,
            'dfsg_marker': None,
        }),
        ("自研源码tar.gz", "apt_2.9.8.tar.gz", {
            'package_name': 'apt',
            'upstream_version': '2.9.8',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'native_source',
            'distribution_type': 'source',
            'is_native': True,
        }),
        ("自研源码tar.bz2", "debhelper_13.11.4.tar.bz2", {
            'package_name': 'debhelper',
            'upstream_version': '13.11.4',
            'debian_revision': None,
            'architecture': None,
            'file_type': 'native_source',
            'distribution_type': 'source',
            'is_native': True,
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("2.4 自研组件源码测试")
    return result


def test_source_complex(parser):
    """源码包 - 复杂组合测试"""
    print("\n" + "="*80)
    print("2.5 源码包 - 复杂组合测试")
    print("="*80)

    result = TestResult()
    base_url = "https://snapshot.debian.org/package/pkg/1.0/"

    tests = [
        ("纪元号+DFSG源码包", "package_1:2.4.0+dfsg1-5.dsc", {
            'package_name': 'package',
            'epoch': '1',
            'upstream_version': '2.4.0',
            'debian_revision': '5',
            'architecture': None,
            'dfsg_marker': 'dfsg1',
            'file_type': 'build_file',
            'distribution_type': 'source',
            'is_native': False,
        }),
        ("预发布+DFSG+Really", "package_3.0~rc1+dfsg1+really2.5-1.debian.tar.xz", {
            'package_name': 'package',
            'upstream_version': '3.0~rc1',
            'debian_revision': '1',
            'architecture': None,
            'dfsg_marker': 'dfsg1',
            'really_version': '2.5',
            'file_type': 'upstream_source_patch',
            'distribution_type': 'source',
            'is_native': False,
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("2.5 源码包复杂组合测试")
    return result


def test_edge_cases(parser):
    """边界条件测试"""
    print("\n" + "="*80)
    print("3. 边界条件测试")
    print("="*80)

    result = TestResult()
    base_url = "https://example.com/pool/main/p/pkg/"

    tests = [
        ("版本号为0", "package_0-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '0',
            'debian_revision': '1',
            'architecture': 'amd64',
            'epoch': None,
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("修订号为0", "package_1.0-0_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.0',
            'debian_revision': '0',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("仅预发布标识", "package_1.0~beta_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.0~beta',
            'debian_revision': None,
            'architecture': 'amd64',
            'is_native': True,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
        ("多个波浪号", "package_1.0~rc1~git20231215-1_amd64.deb", {
            'package_name': 'package',
            'upstream_version': '1.0~rc1',  # 解析器会移除第二个~及其后的内容
            'debian_revision': '1',
            'architecture': 'amd64',
            'is_native': False,
            'distribution_type': 'binary',
            'file_type': 'binary',
        }),
    ]

    for name, filename, expected in tests:
        url = base_url + filename
        success = run_test(parser, name, url, expected, result)
        print(f"  {'✅' if success else '❌'} {name}")

    result.print_summary("3. 边界条件测试")
    return result


def main():
    """主函数"""
    parser = DebianURLParser()

    print("="*80)
    print("Debian URL 解析器完整测试套件")
    print("基于 TEST_CASES.md 文档的所有测试用例")
    print("="*80)

    # 统计所有结果
    all_results = []

    # 二进制包测试
    print("\n" + "🔷"*40)
    print("第一部分: 二进制制品包测试")
    print("🔷"*40)
    all_results.append(test_binary_basic(parser))
    all_results.append(test_binary_epoch(parser))
    all_results.append(test_binary_prerelease(parser))
    all_results.append(test_binary_security(parser))
    all_results.append(test_binary_special_markers(parser))
    all_results.append(test_binary_complex(parser))
    all_results.append(test_binary_version_formats(parser))
    all_results.append(test_binary_package_names(parser))
    all_results.append(test_binary_architectures(parser))

    # 源码包测试
    print("\n" + "🔶"*40)
    print("第二部分: 源码包测试")
    print("🔶"*40)
    all_results.append(test_source_dsc(parser))
    all_results.append(test_source_orig(parser))
    all_results.append(test_source_debian(parser))
    all_results.append(test_source_native(parser))
    all_results.append(test_source_complex(parser))

    # 边界条件测试
    print("\n" + "🔸"*40)
    print("第三部分: 边界条件测试")
    print("🔸"*40)
    all_results.append(test_edge_cases(parser))

    # 总结
    total_passed = sum(r.passed for r in all_results)
    total_failed = sum(r.failed for r in all_results)
    total_tests = total_passed + total_failed

    print("\n" + "="*80)
    print("最终测试结果")
    print("="*80)
    print(f"总计: {total_tests} 个测试")
    print(f"通过: {total_passed} 个 ✅")
    print(f"失败: {total_failed} 个 ❌")
    print(f"通过率: {total_passed/total_tests*100:.1f}%")

    if total_failed > 0:
        print("\n失败的测试详情:")
        for result in all_results:
            for name, error in result.errors:
                print(f"  ❌ {name}: {error}")

    print("="*80)

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    exit(main())

