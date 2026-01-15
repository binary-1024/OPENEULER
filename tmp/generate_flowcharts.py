#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL 解析器流程图生成器

使用 Graphviz 生成流程图的 Python 脚本
需要安装: pip install graphviz

生成的图片:
1. main_flow.png - 主流程图
2. version_parse_flow.png - 版本号解析流程图
3. file_type_flow.png - 文件类型判断流程图
4. usage_flow.png - 使用场景流程图
"""

try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("⚠️  警告: 未安装 graphviz 库")
    print("请运行: pip install graphviz")
    print("同时确保系统已安装 Graphviz: https://graphviz.org/download/")


def create_main_flow():
    """创建主流程图"""
    dot = Digraph(comment='Debian URL 解析器主流程', format='png')
    dot.attr(rankdir='TB', size='12,16')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Arial')

    # 开始节点
    dot.node('start', '开始\n输入 Debian URL', shape='ellipse', fillcolor='lightgreen')

    # 主流程节点
    dot.node('extract', '从 URL 提取文件名')
    dot.node('check_valid', '文件名是否有效?', shape='diamond', fillcolor='lightyellow')
    dot.node('error1', '抛出 ValueError\n无法提取文件名', fillcolor='lightcoral')
    dot.node('check_type', '判断文件类型', fillcolor='lightcyan')

    # 文件类型分支
    dot.node('type_deb', '.deb 文件\n解析二进制包', fillcolor='wheat')
    dot.node('type_dsc', '.dsc 文件\n解析构建文件', fillcolor='wheat')
    dot.node('type_orig', '.orig.tar.*\n解析上游源码', fillcolor='wheat')
    dot.node('type_debian', '.debian.tar.*\n解析 Debian 补丁', fillcolor='wheat')
    dot.node('type_native', '.tar.*\n解析自研源码', fillcolor='wheat')
    dot.node('error2', '不支持的文件类型', fillcolor='lightcoral')

    # 提取信息
    dot.node('extract_info', '提取包名、版本、架构')
    dot.node('parse_version', '解析版本号', fillcolor='lightcyan')

    # 版本解析步骤
    dot.node('parse_epoch', '提取纪元号 epoch')
    dot.node('parse_upstream', '提取上游版本号')
    dot.node('parse_revision', '提取 Debian 修订号')
    dot.node('parse_markers', '解析特殊标识\n(DFSG/Really/Backports等)')

    # 最终步骤
    dot.node('check_native', '判断是否自研组件')
    dot.node('create_obj', '创建 DebianPackageInfo 对象', fillcolor='lightgreen')
    dot.node('end', '返回解析结果', shape='ellipse', fillcolor='lightgreen')

    # 连接节点
    dot.edge('start', 'extract')
    dot.edge('extract', 'check_valid')
    dot.edge('check_valid', 'error1', label='否')
    dot.edge('check_valid', 'check_type', label='是')

    dot.edge('check_type', 'type_deb', label='.deb')
    dot.edge('check_type', 'type_dsc', label='.dsc')
    dot.edge('check_type', 'type_orig', label='.orig.tar.*')
    dot.edge('check_type', 'type_debian', label='.debian.tar.*')
    dot.edge('check_type', 'type_native', label='.tar.*')
    dot.edge('check_type', 'error2', label='其他')

    dot.edge('type_deb', 'extract_info')
    dot.edge('type_dsc', 'extract_info')
    dot.edge('type_orig', 'extract_info')
    dot.edge('type_debian', 'extract_info')
    dot.edge('type_native', 'extract_info')

    dot.edge('extract_info', 'parse_version')
    dot.edge('parse_version', 'parse_epoch')
    dot.edge('parse_epoch', 'parse_upstream')
    dot.edge('parse_upstream', 'parse_revision')
    dot.edge('parse_revision', 'parse_markers')
    dot.edge('parse_markers', 'check_native')
    dot.edge('check_native', 'create_obj')
    dot.edge('create_obj', 'end')

    return dot


def create_version_parse_flow():
    """创建版本号解析流程图"""
    dot = Digraph(comment='版本号解析流程', format='png')
    dot.attr(rankdir='TB', size='10,14')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Arial')

    # 节点
    dot.node('start', '输入版本字符串\n例: 1:1.18.0-6.1+deb11u5', shape='ellipse', fillcolor='lightgreen')
    dot.node('check_epoch', '是否包含 ":" ?', shape='diamond', fillcolor='lightyellow')
    dot.node('extract_epoch', '提取纪元号\nepoch = 1', fillcolor='wheat')
    dot.node('no_epoch', 'epoch = None', fillcolor='wheat')

    dot.node('check_revision', '是否包含 "-" ?', shape='diamond', fillcolor='lightyellow')
    dot.node('split_version', '按最后一个 "-" 分割\n左: 上游版本\n右: 修订号')
    dot.node('no_revision', '上游版本 = 完整版本\n修订号 = None', fillcolor='wheat')

    dot.node('parse_upstream', '解析上游版本\n检查特殊标识', fillcolor='lightcyan')
    dot.node('check_dfsg', '包含 +dfsg ?', shape='diamond', fillcolor='lightyellow')
    dot.node('extract_dfsg', '提取 DFSG 标识\ndfsg1, dfsg2...', fillcolor='wheat')

    dot.node('check_really', '包含 +really ?', shape='diamond', fillcolor='lightyellow')
    dot.node('extract_really', '提取 Really 版本\n真正的版本号', fillcolor='wheat')

    dot.node('parse_revision_detail', '解析修订号\n检查特殊标识', fillcolor='lightcyan')
    dot.node('check_build', '包含 +b ?', shape='diamond', fillcolor='lightyellow')
    dot.node('extract_build', '提取二进制重制编号\nb1, b2...', fillcolor='wheat')

    dot.node('check_bpo', '包含 ~bpo ?', shape='diamond', fillcolor='lightyellow')
    dot.node('extract_bpo', '提取 Backports 标识\nbpo11+1', fillcolor='wheat')

    dot.node('check_security', '包含 deb*u* ?', shape='diamond', fillcolor='lightyellow')
    dot.node('extract_security', '提取发行版版本\n和安全更新编号\ndeb11, u5', fillcolor='wheat')

    dot.node('end', '返回版本信息字典', shape='ellipse', fillcolor='lightgreen')

    # 连接
    dot.edge('start', 'check_epoch')
    dot.edge('check_epoch', 'extract_epoch', label='是')
    dot.edge('check_epoch', 'no_epoch', label='否')

    dot.edge('extract_epoch', 'check_revision')
    dot.edge('no_epoch', 'check_revision')

    dot.edge('check_revision', 'split_version', label='是')
    dot.edge('check_revision', 'no_revision', label='否')

    dot.edge('split_version', 'parse_upstream')
    dot.edge('no_revision', 'end')

    dot.edge('parse_upstream', 'check_dfsg')
    dot.edge('check_dfsg', 'extract_dfsg', label='是')
    dot.edge('check_dfsg', 'check_really', label='否')
    dot.edge('extract_dfsg', 'check_really')

    dot.edge('check_really', 'extract_really', label='是')
    dot.edge('check_really', 'parse_revision_detail', label='否')
    dot.edge('extract_really', 'parse_revision_detail')

    dot.edge('parse_revision_detail', 'check_build')
    dot.edge('check_build', 'extract_build', label='是')
    dot.edge('check_build', 'check_bpo', label='否')
    dot.edge('extract_build', 'check_bpo')

    dot.edge('check_bpo', 'extract_bpo', label='是')
    dot.edge('check_bpo', 'check_security', label='否')
    dot.edge('extract_bpo', 'check_security')

    dot.edge('check_security', 'extract_security', label='是')
    dot.edge('check_security', 'end', label='否')
    dot.edge('extract_security', 'end')

    return dot


def create_file_type_flow():
    """创建文件类型判断流程图"""
    dot = Digraph(comment='文件类型判断流程', format='png')
    dot.attr(rankdir='TB', size='10,12')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Arial')

    # 节点
    dot.node('start', '获取文件名', shape='ellipse', fillcolor='lightgreen')
    dot.node('check_ext', '检查文件扩展名', shape='diamond', fillcolor='lightyellow')

    # .deb 分支
    dot.node('deb_branch', '.deb 文件', fillcolor='wheat')
    dot.node('deb_regex', '正则匹配:\npackage_version_arch.deb')
    dot.node('deb_result', '分发类型: 二进制\n文件类型: 二进制', fillcolor='lightgreen')

    # .dsc 分支
    dot.node('dsc_branch', '.dsc 文件', fillcolor='wheat')
    dot.node('dsc_regex', '正则匹配:\npackage_version.dsc')
    dot.node('dsc_result', '分发类型: 源码\n文件类型: 构建文件', fillcolor='lightgreen')

    # .orig.tar.* 分支
    dot.node('orig_branch', '.orig.tar.* 文件', fillcolor='wheat')
    dot.node('orig_check', '以 .asc 结尾?', shape='diamond', fillcolor='lightyellow')
    dot.node('orig_sig', '上游源码签名', fillcolor='wheat')
    dot.node('orig_source', '上游源码', fillcolor='wheat')
    dot.node('orig_result', '分发类型: 源码\n文件类型: 上游源码', fillcolor='lightgreen')

    # .debian.tar.* 分支
    dot.node('debian_branch', '.debian.tar.* 文件', fillcolor='wheat')
    dot.node('debian_result', '分发类型: 源码\n文件类型: 上游源码补丁', fillcolor='lightgreen')

    # .tar.* 分支
    dot.node('tar_branch', '.tar.* 文件', fillcolor='wheat')
    dot.node('tar_check', '包含 orig 或 debian?', shape='diamond', fillcolor='lightyellow')
    dot.node('tar_upstream', '上游组件源码', fillcolor='wheat')
    dot.node('tar_native', '自研组件源码', fillcolor='wheat')
    dot.node('tar_result', '分发类型: 源码\n文件类型: 自研源码', fillcolor='lightgreen')

    # 错误分支
    dot.node('error', '不支持的文件类型\n抛出 ValueError', fillcolor='lightcoral')

    dot.node('end', '继续解析', shape='ellipse', fillcolor='lightgreen')

    # 连接
    dot.edge('start', 'check_ext')
    dot.edge('check_ext', 'deb_branch', label='.deb')
    dot.edge('check_ext', 'dsc_branch', label='.dsc')
    dot.edge('check_ext', 'orig_branch', label='.orig.tar.*')
    dot.edge('check_ext', 'debian_branch', label='.debian.tar.*')
    dot.edge('check_ext', 'tar_branch', label='.tar.*')
    dot.edge('check_ext', 'error', label='其他')

    dot.edge('deb_branch', 'deb_regex')
    dot.edge('deb_regex', 'deb_result')
    dot.edge('deb_result', 'end')

    dot.edge('dsc_branch', 'dsc_regex')
    dot.edge('dsc_regex', 'dsc_result')
    dot.edge('dsc_result', 'end')

    dot.edge('orig_branch', 'orig_check')
    dot.edge('orig_check', 'orig_sig', label='是')
    dot.edge('orig_check', 'orig_source', label='否')
    dot.edge('orig_sig', 'orig_result')
    dot.edge('orig_source', 'orig_result')
    dot.edge('orig_result', 'end')

    dot.edge('debian_branch', 'debian_result')
    dot.edge('debian_result', 'end')

    dot.edge('tar_branch', 'tar_check')
    dot.edge('tar_check', 'tar_upstream', label='是')
    dot.edge('tar_check', 'tar_native', label='否')
    dot.edge('tar_native', 'tar_result')
    dot.edge('tar_result', 'end')

    return dot


def create_usage_flow():
    """创建使用场景流程图"""
    dot = Digraph(comment='使用场景流程', format='png')
    dot.attr(rankdir='TB', size='12,14')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Arial')

    # 节点
    dot.node('start', '用户需求', shape='ellipse', fillcolor='lightgreen')
    dot.node('choose_way', '选择使用方式', shape='diamond', fillcolor='lightyellow')

    # Python 库分支
    dot.node('import', '导入\nDebianURLParser', fillcolor='wheat')
    dot.node('create_parser', '创建 parser 实例')
    dot.node('call_parse', '调用 parse_url(url)')
    dot.node('get_info', '获取\nDebianPackageInfo 对象')
    dot.node('choose_format', '选择输出格式', shape='diamond', fillcolor='lightyellow')
    dot.node('use_object', '直接使用对象属性', fillcolor='lightgreen')
    dot.node('use_dict', '调用 to_dict()', fillcolor='lightgreen')
    dot.node('use_json', 'json.dumps()', fillcolor='lightgreen')

    # CLI 分支
    dot.node('run_cli', '运行\ndebian_parser_cli.py', fillcolor='wheat')
    dot.node('choose_input', '选择输入方式', shape='diamond', fillcolor='lightyellow')
    dot.node('single_url', '单个 URL\n命令行参数', fillcolor='wheat')
    dot.node('batch_file', '批量处理\n--file 参数', fillcolor='wheat')
    dot.node('choose_output', '选择输出格式', shape='diamond', fillcolor='lightyellow')
    dot.node('readable', '人类可读格式\n(默认)', fillcolor='lightgreen')
    dot.node('json_output', 'JSON 格式\n--json 参数', fillcolor='lightgreen')
    dot.node('choose_filter', '是否需要过滤?', shape='diamond', fillcolor='lightyellow')
    dot.node('filter_arch', '按架构过滤\n--filter-arch', fillcolor='wheat')
    dot.node('filter_type', '按类型过滤\n--filter-type', fillcolor='wheat')
    dot.node('no_filter', '不过滤', fillcolor='wheat')

    dot.node('end', '处理业务逻辑', shape='ellipse', fillcolor='lightgreen')

    # 连接
    dot.edge('start', 'choose_way')
    dot.edge('choose_way', 'import', label='Python 库')
    dot.edge('choose_way', 'run_cli', label='命令行工具')

    # Python 库流程
    dot.edge('import', 'create_parser')
    dot.edge('create_parser', 'call_parse')
    dot.edge('call_parse', 'get_info')
    dot.edge('get_info', 'choose_format')
    dot.edge('choose_format', 'use_object', label='对象')
    dot.edge('choose_format', 'use_dict', label='字典')
    dot.edge('choose_format', 'use_json', label='JSON')
    dot.edge('use_object', 'end')
    dot.edge('use_dict', 'end')
    dot.edge('use_json', 'end')

    # CLI 流程
    dot.edge('run_cli', 'choose_input')
    dot.edge('choose_input', 'single_url', label='单个')
    dot.edge('choose_input', 'batch_file', label='批量')
    dot.edge('single_url', 'choose_output')
    dot.edge('batch_file', 'choose_output')
    dot.edge('choose_output', 'readable', label='文本')
    dot.edge('choose_output', 'json_output', label='JSON')
    dot.edge('readable', 'choose_filter')
    dot.edge('json_output', 'choose_filter')
    dot.edge('choose_filter', 'filter_arch', label='架构')
    dot.edge('choose_filter', 'filter_type', label='类型')
    dot.edge('choose_filter', 'no_filter', label='否')
    dot.edge('filter_arch', 'end')
    dot.edge('filter_type', 'end')
    dot.edge('no_filter', 'end')

    return dot


def create_class_diagram():
    """创建类关系图"""
    dot = Digraph(comment='类关系图', format='png')
    dot.attr(rankdir='TB', size='10,8')
    dot.attr('node', shape='record', style='filled', fillcolor='lightblue', fontname='Arial')

    # DebianURLParser 类
    parser_class = '''DebianURLParser|
    + BINARY_PATTERN: re.Pattern
    + DSC_PATTERN: re.Pattern
    + ORIG_PATTERN: re.Pattern
    + DEBIAN_PATCH_PATTERN: re.Pattern
    + NATIVE_SOURCE_PATTERN: re.Pattern
    |
    + parse_url(url: str): DebianPackageInfo
    - _parse_binary_package()
    - _parse_dsc_file()
    - _parse_orig_source()
    - _parse_debian_patch()
    - _parse_native_source()
    - _parse_version(version: str): Dict
    - _parse_upstream_markers()
    - _parse_revision_markers()
    '''

    # DebianPackageInfo 类
    info_class = '''DebianPackageInfo|
    + url: str
    + filename: str
    + package_name: str
    + version: str
    + architecture: Optional[str]
    + epoch: Optional[str]
    + upstream_version: str
    + debian_revision: Optional[str]
    + dfsg_marker: Optional[str]
    + really_version: Optional[str]
    + binary_rebuild: Optional[str]
    + backport_marker: Optional[str]
    + nmu_marker: Optional[str]
    + ubuntu_marker: Optional[str]
    + release_version: Optional[str]
    + security_update: Optional[str]
    + distribution_type: str
    + file_type: str
    + is_native: bool
    |
    + to_dict(): Dict
    '''

    dot.node('Parser', parser_class, fillcolor='lightcyan')
    dot.node('Info', info_class, fillcolor='wheat')

    dot.edge('Parser', 'Info', label='  creates  ', style='dashed', arrowhead='open')

    return dot


def main():
    """主函数"""
    if not GRAPHVIZ_AVAILABLE:
        print("\n无法生成流程图，请先安装依赖:")
        print("  pip install graphviz")
        print("\n同时确保系统已安装 Graphviz:")
        print("  - macOS: brew install graphviz")
        print("  - Ubuntu/Debian: sudo apt-get install graphviz")
        print("  - Windows: 从 https://graphviz.org/download/ 下载安装")
        return 1

    print("=" * 80)
    print("Debian URL 解析器流程图生成器")
    print("=" * 80)

    graphs = [
        ('main_flow', create_main_flow, '主流程图'),
        ('version_parse_flow', create_version_parse_flow, '版本号解析流程图'),
        ('file_type_flow', create_file_type_flow, '文件类型判断流程图'),
        ('usage_flow', create_usage_flow, '使用场景流程图'),
        ('class_diagram', create_class_diagram, '类关系图'),
    ]

    print("\n开始生成流程图...\n")

    success_count = 0
    for filename, create_func, description in graphs:
        try:
            print(f"正在生成: {description}...")
            dot = create_func()
            output_path = dot.render(filename, cleanup=True)
            print(f"  ✅ 成功生成: {output_path}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ 生成失败: {e}")

    print("\n" + "=" * 80)
    print(f"完成! 成功生成 {success_count}/{len(graphs)} 个流程图")
    print("=" * 80)

    if success_count > 0:
        print("\n生成的文件:")
        for filename, _, description in graphs:
            print(f"  - {filename}.png - {description}")

        print("\n💡 提示:")
        print("  - 所有图片已保存在当前目录")
        print("  - 可以使用图片查看器打开查看")
        print("  - 也可以插入到文档中使用")

    return 0 if success_count == len(graphs) else 1


if __name__ == "__main__":
    exit(main())

