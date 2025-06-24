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
    # 0. url 里面的转义符恢复，比如 %2B 恢复成 +
    # url = url.replace('%2B', '+')
    url = unquote(url)

    # 1. 获取发行版标识
    release_id = url.split('/')[3]  # openEuler-22.03-LTS-SP4
    
    # 2. 获取组件名+版本号+架构（去掉.rpm后缀）
    comp_version_arch = url.split('/')[-1].rstrip('.rpm')  # airline-0.7-1.oe2203sp4.src
    
    # 3. 获取架构
    arch = comp_version_arch.split('.')[-1]  # src
    
    # 4. 切分版本号（按照文档的稳妥方法）
    # 版本号格式：上游版本号-修订号.发行版标识.架构
    # 例如：airline-0.7-1.oe2203sp4.src -> 0.7-1.oe2203sp4
    
    # 稳妥方法实现
    parts = comp_version_arch.split('.')  
    if 'oe' in comp_version_arch:
        # 组件名+版本号+修订号
        revision_part = '.'.join(parts[:-2])  # 'airline-x.x'
        # 发行版+架构
        suffix = '.'.join(parts[-2:])  # '7-1.oe2203sp4.src'
    else:
        # 组件名+版本号+修订号
        revision_part = '.'.join(parts[:-1])  # 'airline-x.x'
        # 没有发行版， 只有架构
        suffix = '.'.join(parts[-1:])  # 'src'    
    
    # 提取出修订号
    revision_components = revision_part.split('-') 

    if len(revision_components) >= 3:
        # airline-0.7-1 -> 0.7-1
        version_revision = '-'.join(revision_components[-2:])
        # airline
        prefix = '-'.join(revision_components[:-2])
    else:
        print(f"url: {url}")
        print(f"revision_components: {revision_components}")
        
        # 如果只有两个元素，则没有修订号
        version_revision = '-'.join(revision_components[-1:])  # '7-1'
        prefix = '-'.join(revision_components[:-1])  # 'airline-x.x'
        
    # 组合完整版本号
    version = version_revision + '.' + suffix  # 'airline-x.x-7-1.oe2203sp4.src'
    comp_name = prefix

    
    return comp_name, version


def test_parser():
    """测试解析函数"""
    
    test_urls = [
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-20.03-LTS-SP1/source/Packages/python3-setuptools-40.8.0-2.oe1.noarch.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS/source/Packages/kernel-5.10.0-60.oe2203.x86_64.rpm"
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