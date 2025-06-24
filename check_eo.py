#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 new_os_url_info.csv 文件中不包含 'eo' 字符的行
"""

def check_lines_without_eo(csv_file):
    """检查CSV文件中不包含'eo'字符的行"""
    lines_without_eo = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # 检查行中是否包含 'eo' 字符
                if 'eo' not in line.lower():  # 不区分大小写检查
                    lines_without_eo.append((line_num, line.strip()))
        
        return lines_without_eo
    
    except FileNotFoundError:
        print(f"错误：找不到文件 {csv_file}")
        return []
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return []

def main():
    csv_file = 'new_os_url_info.csv'
    
    print(f"正在检查文件 {csv_file} 中不包含 'eo' 字符的行...")
    
    # 检查不包含 'eo' 的行
    lines_without_eo = check_lines_without_eo(csv_file)
    
    if lines_without_eo:
        print(f"\n发现 {len(lines_without_eo)} 行不包含 'eo' 字符：")
        print("-" * 80)
        for line_num, line_content in lines_without_eo:
            print(f"第 {line_num} 行：{line_content}")
            print("-" * 80)
    else:
        print("\n✅ 所有行都包含 'eo' 字符")
    
    # 统计信息
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            total_lines = sum(1 for _ in f)
        
        print(f"\n统计信息：")
        print(f"总行数：{total_lines}")
        print(f"不包含 'eo' 的行数：{len(lines_without_eo)}")
        print(f"包含 'eo' 的行数：{total_lines - len(lines_without_eo)}")
        
    except Exception as e:
        print(f"统计文件行数时发生错误：{e}")

if __name__ == "__main__":
    main() 