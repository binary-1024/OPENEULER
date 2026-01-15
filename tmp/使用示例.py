#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openeuler_url_parser import parse_openeuler_component_url

def main():
    """openEuler组件URL解析使用示例"""
    
    # 示例URL列表
    example_urls = [
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS-SP4/source/Packages/airline-0.7-1.oe2203sp4.src.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-20.03-LTS-SP1/source/Packages/python3-setuptools-40.8.0-2.oe1.noarch.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS/source/Packages/kernel-5.10.0-60.oe2203.x86_64.rpm",
        "https://dl-cdn.openeuler.openatom.cn/openEuler-22.03-LTS/source/Packages/gcc-9.3.0-2.oe2203.aarch64.rpm"
    ]
    
    print("=" * 60)
    print("openEuler组件URL解析结果")
    print("=" * 60)
    
    for i, url in enumerate(example_urls, 1):
        print(f"\n[示例 {i}]")
        print(f"URL: {url}")
        
        try:
            comp_name, version = parse_openeuler_component_url(url)
            print(f"✅ 组件名: {comp_name}")
            print(f"✅ 版本号: {version}")
        except Exception as e:
            print(f"❌ 解析失败: {e}")
        
        print("-" * 60)

if __name__ == "__main__":
    main() 