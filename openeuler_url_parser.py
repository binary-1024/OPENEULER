#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def parse_openeuler_component_url(url):
    """
    解析openEuler组件URL，提取组件名和版本号
    
    参数:
        url (str): openEuler组件的URL
        例如: https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm
    
    返回:
        tuple: (comp_name, version)
        - comp_name: 组件名
        - version: 版本号（包含上游版本号-修订号.发行版标识.架构）
    """
    
    # 1. 获取发行版标识
    release_id = url.split('/')[3]  # openEuler-22.03-LTS-SP4
    
    # 2. 获取组件名+版本号+架构（去掉.rpm后缀）
    comp_version_arch = url.split('/')[-1].rstrip('.rpm')  # airline-0.7-1.oe2203sp4.src
    
    # 3. 获取架构
    arch = comp_version_arch.split('.')[-1]  # src
    
    # 4. 切分版本号（按照文档的稳妥方法）
    # 版本号格式：上游版本号-修订号.发行版标识.架构
    # 例如：0.7-1.oe2203sp4.src
    
    # 稳妥方法实现
    parts = comp_version_arch.split('.')
    
    # comp_version_arch.split('.')[-3] 是包含修订号的部分
    # 例如: ['airline-0', '7-1', 'oe2203sp4', 'src']，取 '7-1'
    revision_part = parts[-3]  # '7-1'
    
    # 从修订号部分取最后两个'-'分隔的元素（版本号和修订号）
    revision_components = revision_part.split('-')
    if len(revision_components) >= 2:
        version_revision = '-'.join(revision_components[-2:])  # '7-1'
    else:
        version_revision = revision_part
        
    # 组合完整版本号
    suffix = '.'.join(parts[-2:])  # 'oe2203sp4.src'
    version = version_revision + '.' + suffix  # '7-1.oe2203sp4.src'
    
    # 但是这样缺少了主版本号，需要从前一个部分获取
    if len(parts) >= 4:
        # 例如: 'airline-0' 中的 '0'
        main_version_part = parts[-4].split('-')[-1]  # '0'
        version = main_version_part + '-' + version  # '0-7-1.oe2203sp4.src'
        

    # # 备用方法：直接从'-'分割
    # version_components = comp_version_arch.split('-')
    # if len(version_components) >= 3:
    #     # 取最后几个组件作为版本
    #     version = '-'.join(version_components[1:])  # 去掉组件名部分
    # else:
    #     version = version_components[-1] if len(version_components) > 1 else ""
    
    # 5. 获取组件名
    # 组件名 = comp_version_arch 去掉版本号的部分
    # 需要找到第一个版本数字出现的位置
    
    # 重新用简单方法实现：找到第一个数字开始的位置
    import re
    match = re.search(r'-(\d+)', comp_version_arch)
    if match:
        version_start_pos = match.start()
        comp_name = comp_version_arch[:version_start_pos]
        version = comp_version_arch[version_start_pos+1:]  # 去掉开头的'-'
    else:
        # 如果没找到数字，使用原来的方法
        comp_name = comp_version_arch.split('-')[0]
        version = '-'.join(comp_version_arch.split('-')[1:])
    
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