#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian 组件 URL 解析器

功能：从 Debian 组件下载 URL 中解析出组件信息
输入：Debian 组件的下载 URL
输出：组件名、版本名、架构、发行版版本、分发类型、文件类型等信息
"""

import re
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse
from dataclasses import dataclass, asdict


@dataclass
class DebianPackageInfo:
    """Debian 组件信息"""
    # 原始信息
    url: str
    filename: str

    # 基础信息
    package_name: str  # 组件名
    version: str  # 完整版本字符串
    architecture: Optional[str]  # 架构（二进制包才有）

    # 版本详细信息
    epoch: Optional[str]  # 纪元号
    upstream_version: str  # 上游版本号
    debian_revision: Optional[str]  # Debian 修订号

    # 版本特殊标识
    dfsg_marker: Optional[str]  # DFSG 重打包标识（如 dfsg1）
    really_version: Optional[str]  # really 真正版本标识
    binary_rebuild: Optional[str]  # 二进制重制编号（如 b2）
    backport_marker: Optional[str]  # backports 标识（如 bpo11+1）
    nmu_marker: Optional[str]  # 非维护者上传标识（如 nmu1）
    ubuntu_marker: Optional[str]  # Ubuntu 衍生版本标识
    exp_marker: Optional[str]  # Experimental 实验性版本标识（如 exp1）

    # 发行版和安全更新信息
    release_version: Optional[str]  # 发行版版本号（如 deb12）
    security_update: Optional[str]  # 安全更新编号（如 u1）

    # 分类信息
    distribution_type: str  # 分发类型：源码 | 二进制
    file_type: str  # 文件类型：上游源码 | 上游源码补丁 | 自研源码 | 二进制 | 构建文件
    is_native: bool  # 是否为 Debian 自研组件

    def to_dict(self) -> Dict:
        """转换为字典，包含所有字段和计算属性"""
        data = asdict(self)
        # 添加 package_purl 属性
        data['package_purl'] = self.package_purl
        return data

    @property
    def is_dfsg(self) -> bool:
        """是否为 DFSG 重打包版本"""
        return self.dfsg_marker is not None

    @property
    def dfsg_version(self) -> Optional[str]:
        """DFSG 版本号"""
        if self.dfsg_marker and self.dfsg_marker.startswith('dfsg'):
            version = self.dfsg_marker[4:]  # 移除 'dfsg' 前缀
            return version if version else None
        return None

    @property
    def is_really(self) -> bool:
        """是否为 really 降级版本"""
        return self.really_version is not None

    @property
    def is_prerelease(self) -> bool:
        """是否为预发布版本（包含波浪号）"""
        return '~' in self.upstream_version

    @property
    def is_binary_rebuild(self) -> bool:
        """是否为二进制重制"""
        return self.binary_rebuild is not None

    @property
    def binary_rebuild_version(self) -> Optional[str]:
        """二进制重制版本号"""
        if self.binary_rebuild and self.binary_rebuild.startswith('b'):
            return self.binary_rebuild[1:]  # 移除 'b' 前缀
        return None

    @property
    def is_backport(self) -> bool:
        """是否为 backports 版本"""
        return self.backport_marker is not None

    @property
    def backport_release(self) -> Optional[str]:
        """Backport 的目标发行版版本"""
        if self.backport_marker:
            match = re.match(r'bpo(\d+)\+', self.backport_marker)
            if match:
                return match.group(1)
        return None

    @property
    def backport_version(self) -> Optional[str]:
        """Backport 版本号"""
        if self.backport_marker:
            match = re.search(r'\+(\d+)$', self.backport_marker)
            if match:
                return match.group(1)
        return None

    @property
    def is_nmu(self) -> bool:
        """是否为非维护者上传"""
        return self.nmu_marker is not None

    @property
    def nmu_version(self) -> Optional[str]:
        """NMU 版本号"""
        if self.nmu_marker and self.nmu_marker.startswith('nmu'):
            return self.nmu_marker[3:]  # 移除 'nmu' 前缀
        return None

    @property
    def is_ubuntu(self) -> bool:
        """是否为 Ubuntu 版本"""
        return self.ubuntu_marker is not None

    @property
    def ubuntu_version(self) -> Optional[str]:
        """Ubuntu 版本号"""
        if self.ubuntu_marker and self.ubuntu_marker.startswith('ubuntu'):
            return self.ubuntu_marker[6:]  # 移除 'ubuntu' 前缀
        return None

    @property
    def release_version_number(self) -> Optional[str]:
        """发行版版本号（纯数字）"""
        if self.release_version and self.release_version.startswith('deb'):
            return self.release_version[3:]  # 移除 'deb' 前缀
        return None



    @property
    def package_purl(self) -> str:
        """
        生成 Package URL (PURL)
        格式: pkg:deb/debian/<package_name>
        只包含包名，不包含版本号和架构信息
        例如：
        - openjdk-11-demo_11.0.29+7-1_s390x.deb -> pkg:deb/debian/openjdk-11-demo
        - nginx_1.18.0-6.1_amd64.deb -> pkg:deb/debian/nginx
        """
        # 基础 PURL
        purl = f"pkg:deb/debian/{self.package_name}"

        # 如果有架构信息（二进制包），添加架构参数
        if self.distribution_type == "binary" and self.architecture:
            purl += f"?arch={self.architecture}"
        else:
            purl += f"?arch=src"
        return purl


class DebianURLParser:
    """Debian URL 解析器"""

    # 二进制包文件名正则（.deb 文件）
    # 格式: <package>_<version>_<arch>.deb
    BINARY_PATTERN = re.compile(
        # 包名是第一个_之前的内容
        # +？ 非贪婪匹配保证了遇到第一个下划线停止
        # 包名可以包含：字母、数字、加号、点号、连字符、波浪号
        r'^(?P<package>[a-z0-9][a-z0-9+.~-]+?)_'
        # 版本是第一个_到第二个_之间的内容
        r'(?P<version>.+?)_'
        # 架构要用最后一个下划线到.deb等文件后缀名之间的内容
        r'(?P<arch>[a-z0-9-]+)\.deb$'
    )


    # 源码包构建正则文件名
    # 构建文件: <package>_<version>.dsc
    DSC_PATTERN = re.compile(
        r'^(?P<package>[a-z0-9][a-z0-9+.~-]+?)_'
        r'(?P<version>.+?)\.dsc$'
    )

    # 上游源码: <package>_<version>.orig.tar.(gz|xz|bz2)
    # 或 <package>_<version>.orig-<component>.tar.(gz|xz|bz2) (多源码包)
    ORIG_PATTERN = re.compile(
        r'^(?P<package>[a-z0-9][a-z0-9+.~-]+?)_'
        r'(?P<version>.+?)\.orig(?:-[a-z0-9]+)?\.tar\.(gz|xz|bz2)$'
    )

    # 上游源码签名: <package>_<version>.orig.tar.(gz|xz|bz2).asc
    # 或 <package>_<version>.orig-<component>.tar.(gz|xz|bz2).asc
    ORIG_SIG_PATTERN = re.compile(
        r'^(?P<package>[a-z0-9][a-z0-9+.~-]+?)_'
        r'(?P<version>.+?)\.orig(?:-[a-z0-9]+)?\.tar\.(gz|xz|bz2)\.asc$'
    )

    # Debian 补丁源码: <package>_<version>.debian.tar.(gz|xz)
    DEBIAN_PATCH_PATTERN = re.compile(
        r'^(?P<package>[a-z0-9][a-z0-9+.~-]+?)_'
        r'(?P<version>.+?)\.debian\.tar\.(gz|xz)$'
    )

    # 自研组件源码: <package>_<version>.tar.(gz|xz)（不含 orig 或 debian）
    NATIVE_SOURCE_PATTERN = re.compile(
        r'^(?P<package>[a-z0-9][a-z0-9+.~-]+?)_'
        r'(?P<version>.+?)\.tar\.(gz|xz|bz2)$'
    )

    def parse_url(self, url: str) -> DebianPackageInfo:
        """
        解析 Debian 组件 URL
        Args:
            url: Debian 组件下载 URL
        Returns:
            DebianPackageInfo: 解析后的组件信息
        Raises:
            ValueError: 无法解析 URL
        """
        # 从 URL 中提取文件名
        parsed = urlparse(url)
        filename = parsed.path.split('/')[-1]

        if not filename:
            raise ValueError(f"无法从 URL 中提取文件名: {url}")
        info = None
        # 尝试匹配不同类型的文件
        if filename.endswith('.deb'):
            info = self._parse_binary_package(url, filename)

        elif filename.endswith('.dsc'):
            info =  self._parse_dsc_file(url, filename)
        elif '.orig' in filename and filename.endswith(('.tar.gz', '.tar.xz', '.tar.bz2')):
            # 处理 .orig.tar.* 和 .orig-component.tar.* 格式
            info = self._parse_orig_source(url, filename)
        elif '.orig' in filename and filename.endswith('.asc'):
            # 处理签名文件
            info = self._parse_orig_signature(url, filename)
        elif '.debian.tar.' in filename:
            info = self._parse_debian_patch(url, filename)
        elif filename.endswith(('.tar.gz', '.tar.xz', '.tar.bz2')):
            info = self._parse_native_source(url, filename)
        else:
            raise ValueError(f"不支持的文件类型: {filename}")

        return info

    def _parse_binary_package(self, url: str, filename: str) -> DebianPackageInfo:
        """解析二进制包（.deb 文件）"""
        match = self.BINARY_PATTERN.match(filename)
        if not match:
            raise ValueError(f"无法解析二进制包文件名: {filename}")

        package_name = match.group('package')
        version_str = match.group('version')
        architecture = match.group('arch')

        # 解析版本号
        version_info = self._parse_version(version_str)

        # 判断是否为自研组件（没有 debian_revision）
        is_native = version_info['debian_revision'] is None

        # 对于二进制包，version 应该包含架构信息
        # full_version = f"{version_str}_{architecture}"
        full_version = f"{version_str}"

        return DebianPackageInfo(
            url=url,
            filename=filename,
            package_name=package_name,
            version=full_version,  # 包含架构的完整版本
            architecture=architecture,
            distribution_type="binary",
            file_type="binary",
            is_native=is_native,
            **version_info
        )

    def _parse_dsc_file(self, url: str, filename: str) -> DebianPackageInfo:
        """解析构建文件（.dsc 文件）"""
        match = self.DSC_PATTERN.match(filename)
        if not match:
            raise ValueError(f"无法解析 DSC 文件名: {filename}")

        package_name = match.group('package')
        version_str = match.group('version')

        version_info = self._parse_version(version_str)
        is_native = version_info['debian_revision'] is None
        
        # full_version = f"{version_str}"

        return DebianPackageInfo(
            url=url,
            filename=filename,
            package_name=package_name,
            version=version_str,
            architecture=None,
            distribution_type="source",
            file_type="build_file",
            is_native=is_native,
            **version_info
        )

    def _parse_orig_source(self, url: str, filename: str) -> DebianPackageInfo:
        """解析上游源码（.orig.tar.* 文件）"""
        match = self.ORIG_PATTERN.match(filename)
        if not match:
            raise ValueError(f"无法解析上游源码文件名: {filename}")

        package_name = match.group('package')
        version_str = match.group('version')

        version_info = self._parse_version(version_str)

        return DebianPackageInfo(
            url=url,
            filename=filename,
            package_name=package_name,
            version=version_str,
            architecture=None,
            distribution_type="source",
            file_type="upstream_source",
            is_native=False,  # 有 orig 标识说明是上游组件
            **version_info
        )

    def _parse_orig_signature(self, url: str, filename: str) -> DebianPackageInfo:
        """解析上游源码签名文件（.orig.tar.*.asc 文件）"""
        match = self.ORIG_SIG_PATTERN.match(filename)
        if not match:
            raise ValueError(f"无法解析上游源码签名文件名: {filename}")

        package_name = match.group('package')
        version_str = match.group('version')

        version_info = self._parse_version(version_str)

        return DebianPackageInfo(
            url=url,
            filename=filename,
            package_name=package_name,
            version=version_str,
            architecture=None,
            distribution_type="source",
            file_type="upstream_source_sig",  # 签名文件归类为上游源码的一部分
            is_native=False,
            **version_info
        )

    def _parse_debian_patch(self, url: str, filename: str) -> DebianPackageInfo:
        """解析 Debian 补丁文件（.debian.tar.* 文件）"""
        match = self.DEBIAN_PATCH_PATTERN.match(filename)
        if not match:
            raise ValueError(f"无法解析 Debian 补丁文件名: {filename}")

        package_name = match.group('package')
        version_str = match.group('version')

        version_info = self._parse_version(version_str)

        return DebianPackageInfo(
            url=url,
            filename=filename,
            package_name=package_name,
            version=version_str,
            architecture=None,
            distribution_type="source",
            file_type="upstream_source_patch",
            is_native=False,  # 有补丁说明是上游组件
            **version_info
        )

    def _parse_native_source(self, url: str, filename: str) -> DebianPackageInfo:
        """解析自研组件源码（.tar.* 文件，不含 orig 或 debian）"""
        match = self.NATIVE_SOURCE_PATTERN.match(filename)
        if not match:
            raise ValueError(f"无法解析自研源码文件名: {filename}")

        package_name = match.group('package')
        version_str = match.group('version')

        version_info = self._parse_version(version_str)

        return DebianPackageInfo(
            url=url,
            filename=filename,
            package_name=package_name,
            version=version_str,
            architecture=None,
            distribution_type="source",
            file_type="native_source",
            is_native=True,  # 自研组件
            **version_info
        )

    def _parse_version(self, version_str: str) -> Dict:
        """
        解析版本号字符串

        版本格式: [epoch:]upstream_version[-debian_revision][other_markers]

        Args:
            version_str: 版本字符串

        Returns:
            包含版本各部分信息的字典
        """
        result = {
            'epoch': None,
            'upstream_version': version_str,
            'debian_revision': None,
            'dfsg_marker': None,
            'really_version': None,
            'binary_rebuild': None,
            'backport_marker': None,
            'nmu_marker': None,
            'ubuntu_marker': None,
            'exp_marker': None,
            'release_version': None,
            'security_update': None,
        }

        remaining = version_str

        # 1. 提取 epoch（纪元号）
        if ':' in remaining:
            epoch_part, remaining = remaining.split(':', 1)
            if epoch_part.isdigit():
                result['epoch'] = epoch_part

        # 2. 分离 upstream_version 和 debian_revision
        # debian_revision 从第一个 '-' 开始
        if '-' in remaining:
            # 找到第一个 '-' 的位置
            first_dash = remaining.find('-')
            upstream_part = remaining[:first_dash]
            revision_part = remaining[first_dash+1:]

            # 解析上游版本中的特殊标识（在设置 upstream_version 之前）
            self._parse_upstream_markers(upstream_part, result)

            # 设置纯净的上游版本号（移除所有特殊标识）
            result['upstream_version'] = self._clean_upstream_version(upstream_part)

            # 解析 revision 部分（包含各种标识符）
            self._parse_revision_markers(revision_part, result)

            # 设置纯净的 Debian 修订号（移除所有特殊标识）
            result['debian_revision'] = self._clean_revision_version(revision_part)
        else:
            # 没有 debian_revision（可能是自研组件）
            self._parse_upstream_markers(remaining, result)
            result['upstream_version'] = self._clean_upstream_version(remaining)

        return result

    def _parse_upstream_markers(self, upstream: str, result: Dict):
        """解析上游版本号中的特殊标识"""
        # 提取 DFSG 标识（如 +dfsg1）
        dfsg_match = re.search(r'\+dfsg(\d*)', upstream)
        if dfsg_match:
            result['dfsg_marker'] = f"dfsg{dfsg_match.group(1)}"

        # 提取 Experimental 标识（如 +exp1 或 ~exp1）
        exp_match = re.search(r'[+~]exp(\d*)', upstream)
        if exp_match:
            result['exp_marker'] = f"exp{exp_match.group(1)}"

        # 提取 really 标识（如 +really1.0.0）
        # 只捕获版本号部分，不包括后续的 +dfsg 等标记
        really_match = re.search(r'\+really([\d.]+)', upstream)
        if really_match:
            result['really_version'] = really_match.group(1)

    def _clean_upstream_version(self, upstream: str) -> str:
        """
        清理上游版本号，智能处理不同类型的后缀

        保留规则：
        1. 保留第一个 ~ 及其后的内容（预发布标识）
        2. 保留 +数字 格式（如 +8，OpenJDK 构建号）

        移除规则：
        1. 移除第二个 ~ 及其后的内容
        2. 移除 +dfsg, +really, +git 等特殊标识
        3. 移除所有 - 号后面的内容
        """
        clean_version = upstream

        # 步骤 1: 移除第二个 ~ 及其后的内容
        # 匹配第一个~...第二个~之后的所有内容
        clean_version = re.sub(r'(~[^~+-]*?)~.*$', r'\1', clean_version)

        # 步骤 2: 智能处理 + 号后缀
        # 策略：保留 +数字 格式（如 +8），移除 +dfsg, +really, +git 等特殊标识

        # 先移除已知的特殊标识（按顺序处理，避免相互干扰）
        # 移除 +really...
        clean_version = re.sub(r'\+really[\d.]+', '', clean_version)
        # 移除 +dfsg...
        clean_version = re.sub(r'\+dfsg\d*', '', clean_version)
        # 移除 +exp... 或 ~exp... (experimental)
        clean_version = re.sub(r'[+~]exp\d*', '', clean_version)
        # 移除 +git...
        clean_version = re.sub(r'\+git\d+', '', clean_version)
        # 移除 +svn...
        clean_version = re.sub(r'\+svn\d+', '', clean_version)
        # 移除 +cvs...
        clean_version = re.sub(r'\+cvs\d+', '', clean_version)
        # 移除 +hg...
        clean_version = re.sub(r'\+hg\d+', '', clean_version)
        # 移除 +bzr...
        clean_version = re.sub(r'\+bzr\d+', '', clean_version)

        # 对于剩余的 + 后缀，如果是纯数字（如 +8），则保留
        # 如果是其他格式，则移除
        # 使用更精确的模式：保留版本号+数字的格式
        # 例如：11.0.24+8 保留，但 2.4.54+ds-1 中的 +ds 要移除

        # 移除 +ds (Debian source 标记)
        clean_version = re.sub(r'\+ds\d*', '', clean_version)
        # 移除 +repack
        clean_version = re.sub(r'\+repack\d*', '', clean_version)
        # 移除 +nmu (但这通常在 revision 中)
        clean_version = re.sub(r'\+nmu\d+', '', clean_version)

        # 现在处理剩余的 + 号：
        # 如果 +后面是纯数字（且前面是版本号），保留它（如 11.0.24+8）
        # 否则移除所有剩余的 + 及其后内容
        # 检查是否有 +数字 的模式（构建号）
        if re.search(r'\+\d+$', clean_version):
            # 保留 +数字 格式（如 +8）
            pass
        else:
            # 移除其他所有 + 后缀
            clean_version = re.sub(r'\+.*$', '', clean_version)

        # 步骤 3: 移除所有 - 号后面的内容
        clean_version = re.sub(r'-.*$', '', clean_version)

        return clean_version

    def _parse_revision_markers(self, revision: str, result: Dict):
        """解析 debian revision 中的特殊标识"""
        # 注意：这里不再设置 result['debian_revision']，而是让 _clean_revision_version 处理

        # 提取二进制重制编号（如 +b2）
        build_match = re.search(r'\+b(\d+)', revision)
        if build_match:
            result['binary_rebuild'] = f"b{build_match.group(1)}"

        # 提取 backports 标识（如 ~bpo11+1）
        backport_match = re.search(r'~bpo(\d+)\+(\d+)', revision)
        if backport_match:
            result['backport_marker'] = f"bpo{backport_match.group(1)}+{backport_match.group(2)}"

        # 提取 NMU 标识（如 +nmu1）
        nmu_match = re.search(r'\+nmu(\d+)', revision)
        if nmu_match:
            result['nmu_marker'] = f"nmu{nmu_match.group(1)}"

        # 提取 Ubuntu 标识（如 ubuntu1.1）
        ubuntu_match = re.search(r'ubuntu([\d.]+)', revision)
        if ubuntu_match:
            result['ubuntu_marker'] = f"ubuntu{ubuntu_match.group(1)}"

        # 提取发行版版本和安全更新（如 +deb12u1 或 -deb11u5 或 ~deb12u2）
        release_match = re.search(r'[+\-~]deb(\d+)u(\d+)', revision)
        if release_match:
            result['release_version'] = f"deb{release_match.group(1)}"
            result['security_update'] = f"u{release_match.group(2)}"
        else:
            # 只有发行版版本，没有安全更新
            release_only = re.search(r'[+\-~]deb(\d+)', revision)
            if release_only:
                result['release_version'] = f"deb{release_only.group(1)}"

    def _clean_revision_version(self, revision: str) -> str:
        """
        清理 Debian 修订号，移除所有特殊标识

        Args:
            revision: 原始修订号字符串

        Returns:
            纯净的修订号
        """
        clean_revision = revision
        # 移除发行版版本和安全更新标识（如 +deb12u1）
        clean_revision = re.sub(r'[+\-~]deb\d+u?\d*', '', clean_revision)
        # 只保留第一个 semver
        # 保留版本号，删除其他内容（假设版本号在开头）
        match = re.match(r'(\d+(?:\.\d+)*)', clean_revision)
        if match:
            clean_revision = match.group(1)


        # # 移除 +b 标识（二进制重制）
        # clean_revision = re.sub(r'\+b\d+', '', clean_revision)

        # # 移除 ~bpo 标识（backports）
        # clean_revision = re.sub(r'~bpo\d+\+\d+', '', clean_revision)

        # # 移除 +nmu 标识（非维护者上传）
        # clean_revision = re.sub(r'\+nmu\d+', '', clean_revision)

        # # 移除 ubuntu 标识
        # clean_revision = re.sub(r'ubuntu[\d.]+', '', clean_revision)

        # # 移除发行版版本和安全更新标识（如 +deb12u1）
        # clean_revision = re.sub(r'[+\-~]deb\d+u?\d*', '', clean_revision)

        # 移除可能残留的尾随符号
        clean_revision = clean_revision.strip('+~-')

        return clean_revision


def main():
    """示例用法"""
    parser = DebianURLParser()

    # 测试用例
    test_urls = [
        # 二进制包
        "https://snapshot.debian.org/archive/debian/20251220T083035Z/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
        "https://snapshot.debian.org/archive/debian-debug/20251114T210651Z/pool/main/liba/libabigail/abigail-tools-dbgsym_2.9-1_amd64.deb",
        "https://snapshot.debian.org/archive/debian-debug/20251114T210651Z/pool/main/liba/libabigail/abigail-tools-dbgsym_2.9-1_i386.deb",
        "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
        "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",

        # 源码包
        "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0-6.dsc",
        "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0.orig.tar.gz",
        "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0.orig.tar.gz.asc",
        "https://snapshot.debian.org/package/libabigail/2.9-1/nginx_1.28.0-6.debian.tar.xz",

        # 自研组件
        "https://snapshot.debian.org/package/dpkg/1.23.3/dpkg_1.23.3.tar.xz",
        "https://snapshot.debian.org/package/dpkg/1.23.3/dpkg_1.23.3.dsc",

        # 带特殊标识的版本
        "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0+really1.0-1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0-1+b2_amd64.deb",
        "https://example.com/pool/main/p/package/package_2.0-1~bpo11+1_amd64.deb",
        "https://example.com/pool/main/p/package/package_1.0-1ubuntu1.1_amd64.deb",
    ]

    print("=" * 100)
    print("Debian URL 解析器测试")
    print("=" * 100)

    for url in test_urls:
        print(f"\n原始 URL: {url}")
        try:
            info = parser.parse_url(url)
            print(f"  文件名: {info.filename}")
            print(f"  组件名: {info.package_name}")
            print(f"  完整版本: {info.version}")
            print(f"  架构: {info.architecture or 'N/A'}")
            print(f"  分发类型: {info.distribution_type}")
            print(f"  文件类型: {info.file_type}")
            print(f"  是否自研: {'是' if info.is_native else '否'}")

            # 版本详情
            print(f"  版本详情:")
            if info.epoch:
                print(f"    - 纪元号: {info.epoch}")
            print(f"    - 上游版本: {info.upstream_version}")
            if info.debian_revision:
                print(f"    - Debian 修订号: {info.debian_revision}")

            # 特殊标识
            special_markers = []
            if info.dfsg_marker:
                special_markers.append(f"DFSG: {info.dfsg_marker}")
            if info.really_version:
                special_markers.append(f"Really: {info.really_version}")
            if info.binary_rebuild:
                special_markers.append(f"二进制重制: {info.binary_rebuild}")
            if info.backport_marker:
                special_markers.append(f"Backports: {info.backport_marker}")
            if info.nmu_marker:
                special_markers.append(f"NMU: {info.nmu_marker}")
            if info.ubuntu_marker:
                special_markers.append(f"Ubuntu: {info.ubuntu_marker}")
            if info.release_version:
                special_markers.append(f"发行版: {info.release_version}")
            if info.security_update:
                special_markers.append(f"安全更新: {info.security_update}")

            if special_markers:
                print(f"  特殊标识: {', '.join(special_markers)}")

        except ValueError as e:
            print(f"  ❌ 解析失败: {e}")

        print("-" * 100)


def export_to_csv(package_infos: list, output_file: str = "debian_packages.csv"):
    """
    将解析结果导出到 CSV 文件

    Args:
        package_infos: DebianPackageInfo 对象列表
        output_file: 输出的 CSV 文件路径
    """
    import csv

    # 定义 CSV 的列
    fieldnames = [
        'url',
        'filename',
        'package_name',
        'package_purl',
        'version',
        'architecture',
        'epoch',
        'upstream_version',
        'debian_revision',
        'distribution_type',
        'file_type',
        'is_native',
        'dfsg_marker',
        'exp_marker',
        'really_version',
        'binary_rebuild',
        'backport_marker',
        'nmu_marker',
        'ubuntu_marker',
        'release_version',
        'security_update',
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入表头
        writer.writeheader()

        # 写入数据
        for info in package_infos:
            row = {
                'url': info.url,
                'filename': info.filename,
                'package_name': info.package_name,
                'package_purl': info.package_purl,
                'version': info.version,
                'architecture': info.architecture or '',
                'epoch': info.epoch or '',
                'upstream_version': info.upstream_version,
                'debian_revision': info.debian_revision or '',
                'distribution_type': info.distribution_type,
                'file_type': info.file_type,
                'is_native': info.is_native,
                'dfsg_marker': info.dfsg_marker or '',
                'exp_marker': info.exp_marker or '',
                'really_version': info.really_version or '',
                'binary_rebuild': info.binary_rebuild or '',
                'backport_marker': info.backport_marker or '',
                'nmu_marker': info.nmu_marker or '',
                'ubuntu_marker': info.ubuntu_marker or '',
                'release_version': info.release_version or '',
                'security_update': info.security_update or '',
            }
            writer.writerow(row)

    print(f"✓ 已导出 {len(package_infos)} 条记录到 {output_file}")


def export_to_json(package_infos: list, output_file: str = "debian_packages.json", pretty: bool = True):
    """
    将解析结果导出到 JSON 文件

    Args:
        package_infos: DebianPackageInfo 对象列表
        output_file: 输出的 JSON 文件路径
        pretty: 是否美化输出（默认 True）
    """
    import json

    # 转换为字典列表
    data = [info.to_dict() for info in package_infos]

    # 写入 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)

    print(f"✓ 已导出 {len(package_infos)} 条记录到 {output_file}")


if __name__ == "__main__":
    main()

