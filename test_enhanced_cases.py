#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL Parser - 增强测试套件
基于 ENHANCED_TEST_CASES.md 的全面测试
"""

from debian_url_parser import DebianURLParser

def test_section_a_basic():
    """A. 基础测试用例"""
    print("\n=== A. 基础测试用例 ===")
    parser = DebianURLParser()

    # A1. 简单二进制包
    print("\nA1. 简单二进制包")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "apache2"
    assert result.version == "2.4.54-1_amd64"
    assert result.upstream_version == "2.4.54"
    assert result.debian_revision == "1"
    assert result.architecture == "amd64"
    assert result.distribution_type == "binary"
    assert result.file_type == "binary"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # A2. 简单源码包（DSC）
    print("\nA2. 简单源码包（DSC）")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.dsc"
    result = parser.parse_url(url)
    assert result.package_name == "apache2"
    assert result.version == "2.4.54-1"
    assert result.upstream_version == "2.4.54"
    assert result.debian_revision == "1"
    assert result.distribution_type == "source"
    assert result.file_type == "build_file"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # A3. 原始上游源码
    print("\nA3. 原始上游源码")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.gz"
    result = parser.parse_url(url)
    assert result.package_name == "apache2"
    assert result.version == "2.4.54"
    assert result.upstream_version == "2.4.54"
    assert result.debian_revision is None
    assert result.distribution_type == "source"
    assert result.file_type == "upstream_source"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # A4. Debian 补丁包
    print("\nA4. Debian 补丁包")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.debian.tar.xz"
    result = parser.parse_url(url)
    assert result.package_name == "apache2"
    assert result.version == "2.4.54-1"
    assert result.upstream_version == "2.4.54"
    assert result.debian_revision == "1"
    assert result.distribution_type == "source"
    assert result.file_type == "upstream_source_patch"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # A5. Native 包
    print("\nA5. Native 包")
    url = "http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.tar.xz"
    result = parser.parse_url(url)
    assert result.package_name == "dpkg"
    assert result.version == "1.20.9"
    assert result.upstream_version == "1.20.9"
    assert result.debian_revision is None
    assert result.distribution_type == "source"
    assert result.file_type == "native_source"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_b_epoch():
    """B. 纪元号（Epoch）测试"""
    print("\n=== B. 纪元号（Epoch）测试 ===")
    parser = DebianURLParser()

    # B1. 带纪元的二进制包
    print("\nB1. 带纪元的二进制包")
    url = "http://deb.debian.org/debian/pool/main/o/openjdk-11/openjdk-11-jdk_11.0.16+8-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openjdk-11-jdk"
    assert result.upstream_version == "11.0.16+8"  # 保留构建号 +8
    assert result.debian_revision == "1"
    assert result.version == "11.0.16+8-1_amd64"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # B2. Perl 包
    print("\nB2. Perl 包")
    url = "http://deb.debian.org/debian/pool/main/p/perl/perl_5.32.1-4_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "perl"
    assert result.version == "5.32.1-4_amd64"
    assert result.upstream_version == "5.32.1"
    assert result.debian_revision == "4"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_c_prerelease():
    """C. 预发布版本测试"""
    print("\n=== C. 预发布版本测试 ===")
    parser = DebianURLParser()

    # C1. RC 版本
    print("\nC1. RC 版本")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image-5.18~rc1_5.18~rc1-1~exp1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image-5.18~rc1"
    assert result.upstream_version == "5.18~rc1"
    assert result.debian_revision == "1"
    assert result.is_prerelease == True
    assert result.version == "5.18~rc1-1~exp1_amd64"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # C2. Beta 版本
    print("\nC2. Beta 版本")
    url = "http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0~b8-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "firefox"
    assert result.upstream_version == "91.0~b8"
    assert result.debian_revision == "1"
    assert result.is_prerelease == True
    print(f"✓ 通过: {result.package_name} {result.version}")

    # C3. GCC RC 版本
    print("\nC3. GCC RC 版本")
    url = "http://deb.debian.org/debian/pool/main/g/gcc-12/gcc-12_12.0~rc2-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "gcc-12"
    assert result.upstream_version == "12.0~rc2"
    assert result.debian_revision == "1"
    assert result.is_prerelease == True
    print(f"✓ 通过: {result.package_name} {result.version}")

    # C4. Git 快照版本
    print("\nC4. Git 快照版本")
    url = "http://deb.debian.org/debian/pool/main/g/glibc/libc6_2.33~git20210701-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "libc6"
    assert result.upstream_version == "2.33~git20210701"
    assert result.debian_revision == "1"
    assert result.is_prerelease == True
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_d_dfsg():
    """D. DFSG 版本测试"""
    print("\n=== D. DFSG 版本测试 ===")
    parser = DebianURLParser()

    # D1. 单个 DFSG 标记
    print("\nD1. 单个 DFSG 标记")
    url = "http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "firefox"
    assert result.upstream_version == "91.0"
    assert result.debian_revision == "1"
    assert result.is_dfsg == True
    print(f"✓ 通过: {result.package_name} {result.version}")

    # D2. 带版本号的 DFSG
    print("\nD2. 带版本号的 DFSG")
    url = "http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg2-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "firefox"
    assert result.upstream_version == "91.0"
    assert result.debian_revision == "1"
    assert result.is_dfsg == True
    assert result.dfsg_version == "2"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # D3. DFSG + 预发布
    print("\nD3. DFSG + 预发布")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc1+dfsg-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image"
    assert result.upstream_version == "5.10~rc1"
    assert result.debian_revision == "1"
    assert result.is_dfsg == True
    assert result.is_prerelease == True
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_e_really():
    """E. Really 版本测试"""
    print("\n=== E. Really 版本测试 ===")
    parser = DebianURLParser()

    # E1. Really 降级
    print("\nE1. Really 降级")
    url = "http://deb.debian.org/debian/pool/main/s/systemd/systemd_247+really246-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "systemd"
    assert result.upstream_version == "247"
    assert result.debian_revision == "1"
    assert result.is_really == True
    assert result.really_version == "246"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # E2. Really + DFSG
    print("\nE2. Really + DFSG")
    url = "http://deb.debian.org/debian/pool/main/o/openjdk/openjdk-11_11.0.15+really11.0.14+dfsg-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openjdk-11"
    assert result.upstream_version == "11.0.15"
    assert result.debian_revision == "1"
    assert result.is_really == True
    assert result.really_version == "11.0.14"
    assert result.is_dfsg == True
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_f_binary_rebuild():
    """F. 二进制重制（Binary Rebuild）测试"""
    print("\n=== F. 二进制重制（Binary Rebuild）测试 ===")
    parser = DebianURLParser()

    # F1. 基础二进制重制
    print("\nF1. 基础二进制重制")
    url = "http://deb.debian.org/debian/pool/main/g/glibc/libc6_2.31-13+b2_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "libc6"
    assert result.upstream_version == "2.31"
    assert result.debian_revision == "13"
    assert result.is_binary_rebuild == True
    assert result.binary_rebuild_version == "2"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # F2. 多次二进制重制
    print("\nF2. 多次二进制重制")
    url = "http://deb.debian.org/debian/pool/main/p/python3.9/python3.9_3.9.2-1+b15_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "python3.9"
    assert result.upstream_version == "3.9.2"
    assert result.debian_revision == "1"
    assert result.is_binary_rebuild == True
    assert result.binary_rebuild_version == "15"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_g_backports():
    """G. Backports 测试"""
    print("\n=== G. Backports 测试 ===")
    parser = DebianURLParser()

    # G1. Bullseye Backports
    print("\nG1. Bullseye Backports")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.16.0-1~bpo11+1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image"
    assert result.upstream_version == "5.16.0"
    assert result.debian_revision == "1"
    assert result.is_backport == True
    assert result.backport_release == "11"
    assert result.backport_version == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # G2. Buster Backports
    print("\nG2. Buster Backports + DFSG")
    url = "http://deb.debian.org/debian/pool/main/d/docker.io/docker.io_20.10.5+dfsg1-1~bpo10+1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "docker.io"
    assert result.upstream_version == "20.10.5"
    assert result.debian_revision == "1"
    assert result.is_dfsg == True
    assert result.dfsg_version == "1"
    assert result.is_backport == True
    assert result.backport_release == "10"
    assert result.backport_version == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_h_nmu():
    """H. NMU (非维护者上传) 测试"""
    print("\n=== H. NMU (非维护者上传) 测试 ===")
    parser = DebianURLParser()

    # H1. 基础 NMU
    print("\nH1. 基础 NMU")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.46-4+nmu1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "apache2"
    assert result.upstream_version == "2.4.46"
    assert result.debian_revision == "4"
    assert result.is_nmu == True
    assert result.nmu_version == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # H2. 多次 NMU
    print("\nH2. 多次 NMU")
    url = "http://deb.debian.org/debian/pool/main/b/bind9/bind9_9.16.15-1+nmu3_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "bind9"
    assert result.upstream_version == "9.16.15"
    assert result.debian_revision == "1"
    assert result.is_nmu == True
    assert result.nmu_version == "3"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_i_ubuntu():
    """I. Ubuntu 版本测试"""
    print("\n=== I. Ubuntu 版本测试 ===")
    parser = DebianURLParser()

    # I1. Ubuntu 基础版本
    print("\nI1. Ubuntu 基础版本")
    url = "http://archive.ubuntu.com/ubuntu/pool/main/a/apache2/apache2_2.4.41-4ubuntu3_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "apache2"
    assert result.upstream_version == "2.4.41"
    assert result.debian_revision == "4"
    assert result.is_ubuntu == True
    assert result.ubuntu_version == "3"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # I2. Ubuntu + 安全更新
    print("\nI2. Ubuntu + 安全更新")
    url = "http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/openssl_1.1.1f-1ubuntu2.16_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openssl"
    assert result.upstream_version == "1.1.1f"
    assert result.debian_revision == "1"
    assert result.is_ubuntu == True
    assert result.ubuntu_version == "2.16"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_j_release():
    """J. 发行版版本测试"""
    print("\n=== J. 发行版版本测试 ===")
    parser = DebianURLParser()

    # J1. Debian 11 (Bullseye)
    print("\nJ1. Debian 11 (Bullseye)")
    url = "http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u3_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openssl"
    assert result.upstream_version == "1.1.1n"
    assert result.debian_revision == "0"
    assert result.release_version_number == "11"
    assert result.security_update == "u3"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # J2. Debian 10 (Buster)
    print("\nJ2. Debian 10 (Buster)")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_4.19.208-1+deb10u1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image"
    assert result.upstream_version == "4.19.208"
    assert result.debian_revision == "1"
    assert result.release_version_number == "10"
    assert result.security_update == "u1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # J3. Debian 9 (Stretch)
    print("\nJ3. Debian 9 (Stretch)")
    url = "http://deb.debian.org/debian/pool/main/o/openssh/openssh_7.4p1-10+deb9u7_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openssh"
    assert result.upstream_version == "7.4p1"
    assert result.debian_revision == "10"
    assert result.release_version_number == "9"
    assert result.security_update == "u7"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_k_complex():
    """K. 复杂组合测试"""
    print("\n=== K. 复杂组合测试 ===")
    parser = DebianURLParser()

    # K1. 纪元 + DFSG + 修订号
    print("\nK1. 纪元 + DFSG + 修订号")
    url = "http://deb.debian.org/debian/pool/main/o/openjdk-11/openjdk-11-jdk_11.0.16+8+dfsg-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openjdk-11-jdk"
    assert result.upstream_version == "11.0.16+8"  # 保留构建号 +8，移除 +dfsg
    assert result.debian_revision == "1"
    assert result.is_dfsg == True
    print(f"✓ 通过: {result.package_name} {result.version}")

    # K2. 预发布 + DFSG + 二进制重制
    print("\nK2. 预发布 + DFSG + 二进制重制")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc1+dfsg-1+b2_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image"
    assert result.upstream_version == "5.10~rc1"
    assert result.debian_revision == "1"
    assert result.is_prerelease == True
    assert result.is_dfsg == True
    assert result.is_binary_rebuild == True
    assert result.binary_rebuild_version == "2"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # K3. Really + DFSG + Backports
    print("\nK3. Really + DFSG + Backports")
    url = "http://deb.debian.org/debian/pool/main/o/openjdk/openjdk-11_11.0.15+really11.0.14+dfsg-1~bpo11+1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openjdk-11"
    assert result.upstream_version == "11.0.15"
    assert result.debian_revision == "1"
    assert result.is_really == True
    assert result.really_version == "11.0.14"
    assert result.is_dfsg == True
    assert result.is_backport == True
    assert result.backport_release == "11"
    assert result.backport_version == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # K4. 发行版 + 安全更新 + 二进制重制
    print("\nK4. 发行版 + 安全更新 + 二进制重制")
    url = "http://deb.debian.org/debian/pool/main/g/glibc/libc6_2.31-13+deb11u5+b2_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "libc6"
    assert result.upstream_version == "2.31"
    assert result.debian_revision == "13"
    assert result.release_version_number == "11"
    assert result.security_update == "u5"
    assert result.is_binary_rebuild == True
    assert result.binary_rebuild_version == "2"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # K5. DFSG + NMU + 发行版
    print("\nK5. DFSG + NMU + 发行版")
    url = "http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1+nmu1+deb11u2_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "firefox"
    assert result.upstream_version == "91.0"
    assert result.debian_revision == "1"
    assert result.is_dfsg == True
    assert result.is_nmu == True
    assert result.nmu_version == "1"
    assert result.release_version_number == "11"
    assert result.security_update == "u2"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # K6. 预发布 + Really + DFSG + Backports + NMU
    print("\nK6. 预发布 + Really + DFSG + Backports + NMU (终极组合)")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc2+really5.9+dfsg-1+nmu1~bpo10+1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image"
    assert result.upstream_version == "5.10~rc2"
    assert result.debian_revision == "1"
    assert result.is_prerelease == True
    assert result.is_really == True
    assert result.really_version == "5.9"
    assert result.is_dfsg == True
    assert result.is_nmu == True
    assert result.nmu_version == "1"
    assert result.is_backport == True
    assert result.backport_release == "10"
    assert result.backport_version == "1"
    print(f"✓ 通过: {result.package_name} {result.version} (终极组合测试通过!)")

def test_section_l_edge_cases():
    """L. 边缘情况测试"""
    print("\n=== L. 边缘情况测试 ===")
    parser = DebianURLParser()

    # L1. 无修订号的包
    print("\nL1. 无修订号的包")
    url = "http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.tar.xz"
    result = parser.parse_url(url)
    assert result.package_name == "dpkg"
    assert result.upstream_version == "1.20.9"
    assert result.debian_revision is None
    print(f"✓ 通过: {result.package_name} {result.version}")

    # L2. 修订号为 0
    print("\nL2. 修订号为 0")
    url = "http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u3_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openssl"
    assert result.upstream_version == "1.1.1n"
    assert result.debian_revision == "0"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # L3. 长修订号
    print("\nL3. 长修订号 (多段)")
    url = "http://deb.debian.org/debian/pool/main/g/gcc/gcc_10.2.1-6.2.1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "gcc"
    assert result.upstream_version == "10.2.1"
    assert result.debian_revision == "6.2.1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # L4. 包名含多个连字符
    print("\nL4. 包名含多个连字符")
    url = "http://deb.debian.org/debian/pool/main/l/linux-signed-amd64/linux-image-5.10.0-13-amd64_5.10.106-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image-5.10.0-13-amd64"
    assert result.upstream_version == "5.10.106"
    assert result.debian_revision == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # L5. 版本号含字母
    print("\nL5. 版本号含字母")
    url = "http://deb.debian.org/debian/pool/main/o/openssh/openssh_7.4p1-10_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openssh"
    assert result.upstream_version == "7.4p1"
    assert result.debian_revision == "10"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # L6. 多段版本号
    print("\nL6. 多段版本号")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10.120.1-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image"
    assert result.upstream_version == "5.10.120.1"
    assert result.debian_revision == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # L7. 极短版本号
    print("\nL7. 极短版本号")
    url = "http://deb.debian.org/debian/pool/main/a/apt/apt_2.0-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "apt"
    assert result.upstream_version == "2.0"
    assert result.debian_revision == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # L8. 极长上游版本号
    print("\nL8. 极长上游版本号")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10.120.1.2.3.4-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image"
    assert result.upstream_version == "5.10.120.1.2.3.4"
    assert result.debian_revision == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_m_architectures():
    """M. 不同架构测试"""
    print("\n=== M. 不同架构测试 ===")
    parser = DebianURLParser()

    # M1. i386 架构
    print("\nM1. i386 架构")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_i386.deb"
    result = parser.parse_url(url)
    assert result.architecture == "i386"
    print(f"✓ 通过: {result.architecture}")

    # M2. arm64 架构
    print("\nM2. arm64 架构")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_arm64.deb"
    result = parser.parse_url(url)
    assert result.architecture == "arm64"
    print(f"✓ 通过: {result.architecture}")

    # M3. armhf 架构
    print("\nM3. armhf 架构")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_armhf.deb"
    result = parser.parse_url(url)
    assert result.architecture == "armhf"
    print(f"✓ 通过: {result.architecture}")

    # M4. all 架构
    print("\nM4. all 架构 (架构无关)")
    url = "http://deb.debian.org/debian/pool/main/p/python-pip/python3-pip_20.3.4-4_all.deb"
    result = parser.parse_url(url)
    assert result.architecture == "all"
    print(f"✓ 通过: {result.architecture}")

    # M5. ppc64el 架构
    print("\nM5. ppc64el 架构")
    url = "http://deb.debian.org/debian/pool/main/g/gcc/gcc_10.2.1-6_ppc64el.deb"
    result = parser.parse_url(url)
    assert result.architecture == "ppc64el"
    print(f"✓ 通过: {result.architecture}")

def test_section_n_file_formats():
    """N. 不同文件格式测试"""
    print("\n=== N. 不同文件格式测试 ===")
    parser = DebianURLParser()

    # N1. tar.gz 格式
    print("\nN1. tar.gz 格式")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.gz"
    result = parser.parse_url(url)
    assert result.file_type == "upstream_source"
    print(f"✓ 通过: {result.file_type}")

    # N2. tar.xz 格式
    print("\nN2. tar.xz 格式")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.debian.tar.xz"
    result = parser.parse_url(url)
    assert result.file_type == "upstream_source_patch"
    print(f"✓ 通过: {result.file_type}")

    # N3. tar.bz2 格式
    print("\nN3. tar.bz2 格式")
    url = "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.bz2"
    result = parser.parse_url(url)
    assert result.file_type == "upstream_source"
    print(f"✓ 通过: {result.file_type}")

    # N4. 多个 orig 压缩包
    print("\nN4. 多个 orig 压缩包 (orig-jsc)")
    url = "http://deb.debian.org/debian/pool/main/w/webkit2gtk/webkit2gtk_2.36.0.orig-jsc.tar.xz"
    result = parser.parse_url(url)
    assert result.file_type == "upstream_source"
    print(f"✓ 通过: {result.file_type}")

def test_section_o_special_chars():
    """O. 特殊字符测试"""
    print("\n=== O. 特殊字符测试 ===")
    parser = DebianURLParser()

    # O1. 包名含点号
    print("\nO1. 包名含点号")
    url = "http://deb.debian.org/debian/pool/main/p/python3.9/python3.9_3.9.2-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "python3.9"
    print(f"✓ 通过: {result.package_name}")

    # O2. 包名含加号
    print("\nO2. 包名含加号")
    url = "http://deb.debian.org/debian/pool/main/g/g++/g++_10.2.1-6_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "g++"
    print(f"✓ 通过: {result.package_name}")

    # O3. 版本号含波浪号和加号
    print("\nO3. 版本号含波浪号和加号")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc1+git20210101-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.version == "5.10~rc1+git20210101-1_amd64"
    assert result.upstream_version == "5.10~rc1"
    print(f"✓ 通过: {result.version}")

def test_section_p_real_world():
    """P. 真实世界的复杂案例"""
    print("\n=== P. 真实世界的复杂案例 ===")
    parser = DebianURLParser()

    # P1. Linux 内核（完整版本）
    print("\nP1. Linux 内核（完整版本）")
    url = "http://deb.debian.org/debian/pool/main/l/linux/linux-image-5.10.0-13-amd64_5.10.106-1+deb11u2_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "linux-image-5.10.0-13-amd64"
    assert result.upstream_version == "5.10.106"
    assert result.debian_revision == "1"
    assert result.release_version_number == "11"
    assert result.security_update == "u2"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # P2. OpenJDK（多重版本标记）
    print("\nP2. OpenJDK（多重版本标记）")
    url = "http://deb.debian.org/debian/pool/main/o/openjdk-17/openjdk-17-jdk_17.0.3+7-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openjdk-17-jdk"
    assert result.upstream_version == "17.0.3+7"  # 保留构建号 +7
    assert result.debian_revision == "1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # P2.1 OpenJDK（多重版本标记）
    print("\nP2. OpenJDK（多重版本标记）2")
    url = "http://ftp.debian.org/debian/pool/main/o/openjdk-11/openjdk-11-dbg_11.0.24+8-2~deb11u1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "openjdk-11-dbg"
    assert result.upstream_version == "11.0.24+8"
    assert result.debian_revision == "2"
    assert result.release_version_number == "11"
    assert result.security_update == "u1"
    assert result.architecture == "amd64"
    assert result.distribution_type == "binary"
    assert result.file_type == "binary"
    assert result.is_native == False
    assert result.is_dfsg == False
    assert result.is_prerelease == False
    assert result.is_really == False
    assert result.is_binary_rebuild == False
    assert result.is_backport == False
    assert result.is_nmu == False
    assert result.is_ubuntu == False
    print(f"✓ 通过: {result.package_name} {result.version}")

    # P3. Chromium（DFSG + 发行版）
    print("\nP3. Chromium（DFSG + 发行版）")
    url = "http://deb.debian.org/debian/pool/main/c/chromium/chromium_101.0.4951.64-1+deb11u1+dfsg-1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "chromium"
    # 注意：这个版本很复杂，可能有多个 - 分隔符
    assert result.upstream_version == "101.0.4951.64"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # P4. Systemd（复杂修订）
    print("\nP4. Systemd（复杂修订）")
    url = "http://deb.debian.org/debian/pool/main/s/systemd/systemd_247.3-7+deb11u1_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "systemd"
    assert result.upstream_version == "247.3"
    assert result.debian_revision == "7"
    assert result.release_version_number == "11"
    assert result.security_update == "u1"
    print(f"✓ 通过: {result.package_name} {result.version}")

    # P5. GCC（多段修订号）
    print("\nP5. GCC（多段修订号）")
    url = "http://deb.debian.org/debian/pool/main/g/gcc-10/gcc-10_10.2.1-6.2_amd64.deb"
    result = parser.parse_url(url)
    assert result.package_name == "gcc-10"
    assert result.upstream_version == "10.2.1"
    assert result.debian_revision == "6.2"
    print(f"✓ 通过: {result.package_name} {result.version}")

def test_section_q_source_packages():
    """Q. 源码包完整测试"""
    print("\n=== Q. 源码包完整测试 ===")
    parser = DebianURLParser()

    # Q1. 完整源码包集（DSC + orig + debian）
    print("\nQ1. 完整源码包集")
    urls = [
        "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.dsc",
        "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.gz",
        "http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.debian.tar.xz"
    ]
    for url in urls:
        result = parser.parse_url(url)
        assert result.package_name == "apache2"
        print(f"  ✓ {result.file_type}: {result.version}")

    # Q2. DFSG 源码包集
    print("\nQ2. DFSG 源码包集")
    urls = [
        "http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1.dsc",
        "http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg.orig.tar.xz",
        "http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1.debian.tar.xz"
    ]
    for url in urls:
        result = parser.parse_url(url)
        assert result.package_name == "firefox"
        assert result.is_dfsg == True or result.file_type == "upstream_source_patch"
        print(f"  ✓ {result.file_type}: {result.version}")

    # Q3. Native 包（无 debian 补丁）
    print("\nQ3. Native 包")
    urls = [
        "http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.dsc",
        "http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.tar.xz"
    ]
    for url in urls:
        result = parser.parse_url(url)
        assert result.package_name == "dpkg"
        assert result.debian_revision is None
        print(f"  ✓ {result.file_type}: {result.version}")

def test_section_r_security_updates():
    """R. 安全更新专项测试"""
    print("\n=== R. 安全更新专项测试 ===")
    parser = DebianURLParser()

    # R1. 单次安全更新
    print("\nR1. 单次安全更新")
    url = "http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u1_amd64.deb"
    result = parser.parse_url(url)
    assert result.security_update == "u1"
    print(f"✓ 通过: {result.security_update}")

    # R2. 多次安全更新
    print("\nR2. 多次安全更新")
    url = "http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb"
    result = parser.parse_url(url)
    assert result.security_update == "u5"
    print(f"✓ 通过: {result.security_update}")

    # R3. 10+ 次安全更新
    print("\nR3. 10+ 次安全更新")
    url = "http://deb.debian.org/debian/pool/main/o/openssh/openssh_7.4p1-10+deb9u12_amd64.deb"
    result = parser.parse_url(url)
    assert result.security_update == "u12"
    print(f"✓ 通过: {result.security_update} (多次安全更新)")

def main():
    """运行所有增强测试"""
    print("=" * 80)
    print("Debian URL Parser - 增强测试套件")
    print("=" * 80)

    test_functions = [
        test_section_a_basic,
        test_section_b_epoch,
        test_section_c_prerelease,
        test_section_d_dfsg,
        test_section_e_really,
        test_section_f_binary_rebuild,
        test_section_g_backports,
        test_section_h_nmu,
        test_section_i_ubuntu,
        test_section_j_release,
        test_section_k_complex,
        test_section_l_edge_cases,
        test_section_m_architectures,
        test_section_n_file_formats,
        test_section_o_special_chars,
        test_section_p_real_world,
        test_section_q_source_packages,
        test_section_r_security_updates,
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n❌ 测试失败: {test_func.__name__}")
            print(f"   错误: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ 测试异常: {test_func.__name__}")
            print(f"   异常: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"通过: {passed}/{len(test_functions)}")
    print(f"失败: {failed}/{len(test_functions)}")

    if failed == 0:
        print("\n🎉 所有增强测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")
        return 1

if __name__ == "__main__":
    exit(main())

