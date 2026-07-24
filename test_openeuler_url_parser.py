#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from openeuler_url_parser import parse_openeuler_component_url, parse_openeuler_rpm_url

# 从原始根目录/tmp 脚本及使用示例中提取出的全部 34 个唯一 RPM URL。
# 其中包括 run.py 的注释 badcase；这里保留原 URL，而不是只保留等价的
# 合成用例，便于持续审计覆盖率。
HISTORICAL_CASES = [
    (
        "https://archives.openeuler.openatom.cn/openEuler-21.03/everything/x86_64/Packages/389-ds-base-devel-1.4.0.31-2.oe1.x86_64.rpm",
        "389-ds-base-devel",
        "1.4.0.31-2.oe1.x86_64",
    ),
    (
        "https://archives.openeuler.openatom.cn/openEuler-20.09/everything/x86_64/Packages/openEuler-20.09/CUnit-devel-2.1.3-21.oe1.x86_64.rpm",
        "CUnit-devel",
        "2.1.3-21.oe1.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/cpp-10.3.1-20.x86_64.rpm",
        "cpp",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/fpack-3.490-2.x86_64.rpm",
        "fpack",
        "3.490-2.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/gcc-10.3.1-20.x86_64.rpm",
        "gcc",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/iSulad-2.0.17-14.x86_64.rpm",
        "iSulad",
        "2.0.17-14.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/iniparser-4.1-4.x86_64.rpm",
        "iniparser",
        "4.1-4.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libasan-10.3.1-20.x86_64.rpm",
        "libasan",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libatomic-10.3.1-20.x86_64.rpm",
        "libatomic",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libbson-1.13.1-6.x86_64.rpm",
        "libbson",
        "1.13.1-6.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgcc-10.3.1-20.x86_64.rpm",
        "libgcc",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgccjit-10.3.1-20.x86_64.rpm",
        "libgccjit",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgfortran-10.3.1-20.x86_64.rpm",
        "libgfortran",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libgomp-10.3.1-20.x86_64.rpm",
        "libgomp",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libhdfs-3.3.4-2.x86_64.rpm",
        "libhdfs",
        "3.3.4-2.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libitm-10.3.1-20.x86_64.rpm",
        "libitm",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/liblsan-10.3.1-20.x86_64.rpm",
        "liblsan",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libobjc-10.3.1-20.x86_64.rpm",
        "libobjc",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libquadmath-10.3.1-20.x86_64.rpm",
        "libquadmath",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libstdc%2B%2B-10.3.1-20.x86_64.rpm",
        "libstdc++",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libtsan-10.3.1-20.x86_64.rpm",
        "libtsan",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/libubsan-10.3.1-20.x86_64.rpm",
        "libubsan",
        "10.3.1-20.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/mrtg-2.17.7-3.x86_64.rpm",
        "mrtg",
        "2.17.7-3.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/mysql-8.0.29-1.x86_64.rpm",
        "mysql",
        "8.0.29-1.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/sgxsdk-2.15.1-8.x86_64.rpm",
        "sgxsdk",
        "2.15.1-8.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/suitesparse-5.10.1-2.x86_64.rpm",
        "suitesparse",
        "5.10.1-2.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm",
        "airline",
        "0.7-1.oe2203sp4.src",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-20.03-LTS-SP1/source/Packages/python3-setuptools-40.8.0-2.oe1.noarch.rpm",
        "python3-setuptools",
        "40.8.0-2.oe1.noarch",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS/source/Packages/kernel-5.10.0-60.oe2203.x86_64.rpm",
        "kernel",
        "5.10.0-60.oe2203.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/hotpatch_update/x86_64/Packages/patch-kernel-5.10.0-216.0.0.115.oe2203sp4-ACC-1-6.x86_64.rpm",
        "patch-kernel-5.10.0-216.0.0.115.oe2203sp4-ACC",
        "1-6.x86_64",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.src.rpm",
        "airline",
        "0.7-1.src",
    ),
    (
        "https://archive.fedoraproject.org/pub/archive/fedoraa/linux/core/4/ppc/os/fedora/rpms/rp-pppoe-3.5-27.ppc.rpm",
        "rp-pppoe",
        "3.5-27.ppc",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/source/Packages/ros-noetic-ros-nodelet_core-1.10.1-1.src.rpm",
        "ros-noetic-ros-nodelet_core",
        "1.10.1-1.src",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS/source/Packages/gcc-9.3.0-2.oe2203.aarch64.rpm",
        "gcc",
        "9.3.0-2.oe2203.aarch64",
    ),
]


ADDITIONAL_CASES = [
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-24.09/everything/riscv64/Packages/texlive-nolbreaks-doc-svn26786.1.2-2.oe2409.noarch.rpm",
        "texlive-nolbreaks-doc",
        "svn26786.1.2-2.oe2409.noarch",
    ),
    (
        "https://example.invalid/Packages/kata-integration-v1.0.0-10.oe2409.x86_64.rpm",
        "kata-integration",
        "v1.0.0-10.oe2409.x86_64",
    ),
    (
        "https://example.invalid/Packages/lshw-B.02.19.2-2.oe2409.x86_64.rpm",
        "lshw",
        "B.02.19.2-2.oe2409.x86_64",
    ),
    (
        "https://example.invalid/Packages/pseudo-df1d1321fb093283485c387e3c933d2d264e509c-1.oe2409.x86_64.rpm",
        "pseudo",
        "df1d1321fb093283485c387e3c933d2d264e509c-1.oe2409.x86_64",
    ),
    (
        "https://example.invalid/Packages/cockpit-389-ds-3.1.1-2.oe2409.noarch.rpm",
        "cockpit-389-ds",
        "3.1.1-2.oe2409.noarch",
    ),
    (
        "https://example.invalid/Packages/hadoop-3.1-client-3.1.4-6.oe2309.noarch.rpm",
        "hadoop-3.1-client",
        "3.1.4-6.oe2309.noarch",
    ),
    (
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP1/everything/x86_64/Packages/ros-noetic-ros-nodelet_core-1.10.1-1.x86_64.rpm",
        "ros-noetic-ros-nodelet_core",
        "1.10.1-1.x86_64",
    ),
    (
        "https://example.invalid/Packages/libstdc%2B%2B-10.3.1-20.oe1.x86_64.rpm?download=1",
        "libstdc++",
        "10.3.1-20.oe1.x86_64",
    ),
    ("example-1.0-1.oe1.arm.rpm", "example", "1.0-1.oe1.arm"),
]


class ParseOpenEulerComponentUrlTests(unittest.TestCase):
    def test_all_historical_script_cases(self):
        self.assertEqual(len(HISTORICAL_CASES), 34)
        self.assertEqual(len({case[0] for case in HISTORICAL_CASES}), 34)
        for url, name, version in HISTORICAL_CASES:
            with self.subTest(url=url):
                self.assertEqual(parse_openeuler_component_url(url), (name, version))

    def test_additional_edge_cases(self):
        for url, name, version in ADDITIONAL_CASES:
            with self.subTest(url=url):
                self.assertEqual(parse_openeuler_component_url(url), (name, version))

    def test_structured_fields_source_marker_and_unknown_epoch(self):
        parts = parse_openeuler_rpm_url(
            "https://example.invalid/Packages/airline-0.7-1.oe2203sp4.src.rpm"
        )
        self.assertEqual(parts.name, "airline")
        self.assertEqual(parts.version, "0.7")
        self.assertEqual(parts.release, "1.oe2203sp4")
        self.assertEqual(parts.filename_arch, "src")
        self.assertTrue(parts.is_source_package)
        self.assertIsNone(parts.epoch)
        self.assertFalse(parts.epoch_known)

        nosrc = parse_openeuler_rpm_url("example-1.0-1.nosrc.rpm")
        self.assertTrue(nosrc.is_source_package)

    def test_rejects_non_rpm_filename(self):
        with self.assertRaisesRegex(ValueError, "not an RPM filename"):
            parse_openeuler_component_url("https://example.invalid/package.tar.gz")

    def test_rejects_incomplete_nevra(self):
        with self.assertRaisesRegex(ValueError, "invalid NAME-VERSION-RELEASE"):
            parse_openeuler_component_url(
                "https://example.invalid/package-1.x86_64.rpm"
            )

    def test_rejects_missing_architecture(self):
        with self.assertRaisesRegex(ValueError, "missing RPM architecture"):
            parse_openeuler_component_url("https://example.invalid/package-1-1.rpm")

    def test_rejects_non_string_input(self):
        with self.assertRaisesRegex(TypeError, "url must be a string"):
            parse_openeuler_component_url(None)


if __name__ == "__main__":
    unittest.main()
