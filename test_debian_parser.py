#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL 解析器单元测试

验证解析器对各种 Debian 包 URL 的解析正确性
"""

from debian_url_parser import DebianURLParser


def test_binary_package():
    """测试二进制包解析"""
    print("测试: 二进制包解析")
    parser = DebianURLParser()

    url = "https://snapshot.debian.org/archive/debian/20251220T083035Z/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb"
    info = parser.parse_url(url)

    assert info.package_name == "dpkg", f"包名错误: {info.package_name}"
    assert info.version == "1.23.3_armhf", f"版本错误: {info.version}"  # 包含架构
    assert info.architecture == "armhf", f"架构错误: {info.architecture}"
    assert info.distribution_type == "binary", f"分发类型错误: {info.distribution_type}"
    assert info.file_type == "binary", f"文件类型错误: {info.file_type}"
    assert info.is_native == True, "应该识别为自研组件"
    assert info.upstream_version == "1.23.3", f"上游版本错误: {info.upstream_version}"
    assert info.debian_revision is None, "自研组件不应该有修订号"

    print("  ✓ 通过\n")


def test_upstream_binary_package():
    """测试上游二进制包解析"""
    print("测试: 上游二进制包解析")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb"
    info = parser.parse_url(url)

    assert info.package_name == "nginx", f"包名错误: {info.package_name}"
    assert info.version == "1.18.0-6.1_amd64", f"版本错误: {info.version}"  # 包含架构
    assert info.architecture == "amd64", f"架构错误: {info.architecture}"
    assert info.is_native == False, "应该识别为上游组件"
    assert info.upstream_version == "1.18.0", f"上游版本错误: {info.upstream_version}"
    assert info.debian_revision == "6.1", f"修订号错误: {info.debian_revision}"

    print("  ✓ 通过\n")


def test_security_update():
    """测试安全更新包解析"""
    print("测试: 安全更新包解析")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb"
    info = parser.parse_url(url)

    assert info.package_name == "openssl", f"包名错误: {info.package_name}"
    assert info.version == "1.1.1n-0+deb11u5_amd64", f"版本错误: {info.version}"  # 包含架构
    assert info.upstream_version == "1.1.1n", f"上游版本错误: {info.upstream_version}"
    assert info.debian_revision == "0", f"修订号错误: {info.debian_revision}"  # 纯净的修订号，不含特殊标识
    assert info.release_version == "deb11", f"发行版错误: {info.release_version}"
    assert info.security_update == "u5", f"安全更新编号错误: {info.security_update}"

    print("  ✓ 通过\n")


def test_dsc_file():
    """测试构建文件解析"""
    print("测试: 构建文件解析")
    parser = DebianURLParser()

    url = "https://snapshot.debian.org/package/nginx/1.28.0-6/nginx_1.28.0-6.dsc"
    info = parser.parse_url(url)

    assert info.package_name == "nginx", f"包名错误: {info.package_name}"
    assert info.version == "1.28.0-6", f"版本错误: {info.version}"
    assert info.architecture is None, "构建文件不应该有架构"
    assert info.distribution_type == "source", f"分发类型错误: {info.distribution_type}"
    assert info.file_type == "build_file", f"文件类型错误: {info.file_type}"

    print("  ✓ 通过\n")


def test_orig_source():
    """测试上游源码解析"""
    print("测试: 上游源码解析")
    parser = DebianURLParser()

    url = "https://snapshot.debian.org/package/nginx/1.28.0-6/nginx_1.28.0.orig.tar.gz"
    info = parser.parse_url(url)

    assert info.package_name == "nginx", f"包名错误: {info.package_name}"
    assert info.version == "1.28.0", f"版本错误: {info.version}"
    assert info.distribution_type == "source", f"分发类型错误: {info.distribution_type}"
    assert info.file_type == "upstream_source", f"文件类型错误: {info.file_type}"
    assert info.is_native == False, "上游源码不是自研组件"

    print("  ✓ 通过\n")


def test_debian_patch():
    """测试 Debian 补丁解析"""
    print("测试: Debian 补丁解析")
    parser = DebianURLParser()

    url = "https://snapshot.debian.org/package/nginx/1.28.0-6/nginx_1.28.0-6.debian.tar.xz"
    info = parser.parse_url(url)

    assert info.package_name == "nginx", f"包名错误: {info.package_name}"
    assert info.version == "1.28.0-6", f"版本错误: {info.version}"
    assert info.file_type == "upstream_source_patch", f"文件类型错误: {info.file_type}"
    assert info.is_native == False, "有补丁的不是自研组件"

    print("  ✓ 通过\n")


def test_native_source():
    """测试自研组件源码解析"""
    print("测试: 自研组件源码解析")
    parser = DebianURLParser()

    url = "https://snapshot.debian.org/package/dpkg/1.23.3/dpkg_1.23.3.tar.xz"
    info = parser.parse_url(url)

    assert info.package_name == "dpkg", f"包名错误: {info.package_name}"
    assert info.version == "1.23.3", f"版本错误: {info.version}"
    assert info.file_type == "native_source", f"文件类型错误: {info.file_type}"
    assert info.is_native == True, "应该识别为自研组件"

    print("  ✓ 通过\n")


def test_dfsg_package():
    """测试 DFSG 重打包包解析"""
    print("测试: DFSG 重打包包解析")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb"
    info = parser.parse_url(url)

    assert info.package_name == "package", f"包名错误: {info.package_name}"
    assert info.upstream_version == "1.2.3", f"上游版本错误: {info.upstream_version}"  # 纯净的上游版本
    assert info.dfsg_marker == "dfsg1", f"DFSG 标识错误: {info.dfsg_marker}"
    assert info.debian_revision == "2", f"修订号错误: {info.debian_revision}"  # 纯净的修订号
    assert info.release_version == "deb12", f"发行版错误: {info.release_version}"
    assert info.security_update == "u1", f"安全更新编号错误: {info.security_update}"

    print("  ✓ 通过\n")


def test_really_package():
    """测试 really 版本包解析"""
    print("测试: really 版本包解析")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/p/package/package_1.0+really1.0-1_amd64.deb"
    info = parser.parse_url(url)

    assert info.package_name == "package", f"包名错误: {info.package_name}"
    assert info.upstream_version == "1.0", f"上游版本错误: {info.upstream_version}"  # 纯净的上游版本
    assert info.really_version == "1.0", f"really 版本错误: {info.really_version}"

    print("  ✓ 通过\n")


def test_binary_rebuild():
    """测试二进制重制包解析"""
    print("测试: 二进制重制包解析")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/p/package/package_1.0-1+b2_amd64.deb"
    info = parser.parse_url(url)

    assert info.package_name == "package", f"包名错误: {info.package_name}"
    assert info.binary_rebuild == "b2", f"二进制重制编号错误: {info.binary_rebuild}"

    print("  ✓ 通过\n")


def test_backport_package():
    """测试 backports 包解析"""
    print("测试: backports 包解析")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/p/package/package_2.0-1~bpo11+1_amd64.deb"
    info = parser.parse_url(url)

    assert info.package_name == "package", f"包名错误: {info.package_name}"
    assert info.backport_marker == "bpo11+1", f"backports 标识错误: {info.backport_marker}"

    print("  ✓ 通过\n")


def test_ubuntu_package():
    """测试 Ubuntu 衍生版本包解析"""
    print("测试: Ubuntu 衍生版本包解析")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/p/package/package_1.0-1ubuntu1.1_amd64.deb"
    info = parser.parse_url(url)

    assert info.package_name == "package", f"包名错误: {info.package_name}"
    assert info.ubuntu_marker == "ubuntu1.1", f"Ubuntu 标识错误: {info.ubuntu_marker}"

    print("  ✓ 通过\n")


def test_to_dict():
    """测试转换为字典"""
    print("测试: 转换为字典")
    parser = DebianURLParser()

    url = "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb"
    info = parser.parse_url(url)

    data = info.to_dict()

    assert isinstance(data, dict), "应该返回字典类型"
    assert "package_name" in data, "字典应该包含 package_name"
    assert "version" in data, "字典应该包含 version"
    assert "package_purl" in data, "字典应该包含 package_purl"
    assert data["package_name"] == "nginx", f"包名错误: {data['package_name']}"
    assert data["package_purl"] == "pkg:deb/debian/nginx", f"PURL 错误: {data['package_purl']}"

    print("  ✓ 通过\n")


def test_package_purl():
    """测试 package_purl 属性"""
    print("测试: package_purl 属性")
    parser = DebianURLParser()

    test_cases = [
        ("https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb", "pkg:deb/debian/nginx"),
        ("https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb", "pkg:deb/debian/dpkg"),
        ("https://example.com/pool/main/o/openjdk-11/openjdk-11-demo_11.0.29+7-1_s390x.deb", "pkg:deb/debian/openjdk-11-demo"),
        ("https://example.com/pool/main/n/nginx/nginx_1.28.0-6.dsc", "pkg:deb/debian/nginx"),
    ]

    for url, expected_purl in test_cases:
        info = parser.parse_url(url)
        assert info.package_purl == expected_purl, f"PURL 错误: 期望 {expected_purl}, 实际 {info.package_purl}"

    print("  ✓ 通过\n")


def test_invalid_url():
    """测试无效 URL"""
    print("测试: 无效 URL")
    parser = DebianURLParser()

    invalid_url = "https://example.com/pool/main/invalid.txt"

    try:
        info = parser.parse_url(invalid_url)
        assert False, "应该抛出 ValueError"
    except ValueError as e:
        assert "不支持的文件类型" in str(e), f"错误消息不正确: {e}"
        print("  ✓ 通过 - 正确抛出异常\n")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*80)
    print("开始运行单元测试")
    print("="*80 + "\n")

    tests = [
        test_binary_package,
        test_upstream_binary_package,
        test_security_update,
        test_dsc_file,
        test_orig_source,
        test_debian_patch,
        test_native_source,
        test_dfsg_package,
        test_really_package,
        test_binary_rebuild,
        test_backport_package,
        test_ubuntu_package,
        test_to_dict,
        test_package_purl,
        test_invalid_url,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"  ✗ 失败: {e}\n")
        except Exception as e:
            failed += 1
            print(f"  ✗ 异常: {e}\n")

    print("="*80)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("="*80 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

