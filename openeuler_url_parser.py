#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.parse import unquote

def parse_openeuler_component_url(url):
    """
    解析openEuler组件URL，提取组件名和版本号

    参数:
        url (str): openEuler组件的URL
        例如: https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm
    返回:
        - comp_name: 组件名
        - version: 版本号（包含上游版本号-修订号.发行版标识.架构）
    """
    import re

    # 0. url 里面的转义符恢复，比如 %2B 恢复成 +
    url = unquote(url)

    # 1. 获取发行版标识
    release_id = url.split('/')[3]  # openEuler-22.03-LTS-SP4

    # 2. 获取组件名+版本号+架构（去掉.rpm后缀）
    comp_version_arch = url.split('/')[-1].rstrip('.rpm')  # airline-0.7-1.oe2203sp4.src

    # 3. 获取架构
    arch = comp_version_arch.split('.')[-1]  # src

    # 4. 查找发行版标识（oe + 数字开头的字符串）
    # 使用正则表达式查找 .oeXXXX 模式
    oe_pattern = r'\.oe\d+[a-z0-9]*'
    oe_match = re.search(oe_pattern, comp_version_arch)

    if oe_match:
        # 找到了发行版标识
        oe_pos = oe_match.start()  # .oe 的起始位置

        # 组件名+版本号部分（在 .oe 之前的所有内容）
        comp_version_part = comp_version_arch[:oe_pos]

        # 发行版标识+后续部分（从 .oe 开始到最后一个 . 之前）
        # 例如：.oe2203sp4-ACC-1 或 .oe2203sp4
        suffix_with_arch = comp_version_arch[oe_pos:]  # .oe2203sp4-ACC-1.x86_64

        # 去掉最后的架构部分
        if '.' in suffix_with_arch:
            suffix = suffix_with_arch[:suffix_with_arch.rfind('.')]  # .oe2203sp4-ACC-1
        else:
            suffix = suffix_with_arch
    else:
        # 没有发行版标识
        parts = comp_version_arch.split('.')
        comp_version_part = '.'.join(parts[:-1])  # 去掉架构
        suffix = ''

    # 5. 从 comp_version_part 中分离组件名和版本号
    # 格式：组件名-版本号-修订号
    # 例如：airline-0.7-1 或 patch-kernel-5.10.0-216.0.0.115

    # 按 - 分割
    components = comp_version_part.split('-')

    if len(components) >= 3:
        # 需要找到版本号的起始位置
        # 版本号通常以数字开头
        version_start_idx = -1
        for i, comp in enumerate(components):
            # 检查是否以数字开头（可能包含点号，如 5.10.0）
            if comp and comp[0].isdigit():
                version_start_idx = i
                break

        if version_start_idx > 0:
            # 找到了版本号的起始位置
            comp_name = '-'.join(components[:version_start_idx])
            version_part = '-'.join(components[version_start_idx:])
        else:
            # 没找到数字开头的部分，使用原来的逻辑（取最后两个作为版本）
            comp_name = '-'.join(components[:-2])
            version_part = '-'.join(components[-2:])
    elif len(components) == 2:
        # 只有两个部分：组件名-版本号
        comp_name = components[0]
        version_part = components[1]
    else:
        # 只有一个部分，全部作为组件名
        comp_name = comp_version_part
        version_part = ''

    # 6. 组合完整版本号
    if suffix:
        version = version_part + suffix + '.' + arch
    else:
        version = version_part + '.' + arch

    return comp_name, version


def test_parser():
    """测试解析函数"""

    test_urls = [
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-20.03-LTS-SP1/source/Packages/python3-setuptools-40.8.0-2.oe1.noarch.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS/source/Packages/kernel-5.10.0-60.oe2203.x86_64.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/hotpatch_update/x86_64/Packages/patch-kernel-5.10.0-216.0.0.115.oe2203sp4-ACC-1-6.x86_64.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.src.rpm",

    ]

    for url in test_urls:
        comp_name, version = parse_openeuler_component_url(url)
        print(f"URL: {url}")
        print(f"组件名: {comp_name}")
        print(f"版本号: {version}")
        print("-" * 80)


if __name__ == "__main__":
    # 示例使用
    url = "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm"
    comp_name, version = parse_openeuler_component_url(url)

    print("=== openEuler组件URL解析结果 ===")
    print(f"输入URL: {url}")
    print(f"组件名: {comp_name}")
    print(f"版本号: {version}")

    print("\n=== 运行测试用例 ===")
    test_parser()
