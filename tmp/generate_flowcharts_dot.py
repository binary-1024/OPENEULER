#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debian URL 解析器流程图生成器（DOT 文件版本）

直接生成 .dot 文件，无需 Graphviz 可执行文件
生成后可以使用以下方式查看：
1. 在线查看: https://dreampuf.github.io/GraphvizOnline/
2. VS Code: 安装 Graphviz Preview 插件
3. 命令行渲染: dot -Tpng main_flow.dot -o main_flow.png

生成的文件:
1. main_flow.dot - 主流程图
2. version_parse_flow.dot - 版本号解析流程图
3. file_type_flow.dot - 文件类型判断流程图
4. usage_flow.dot - 使用场景流程图
5. class_diagram.dot - 类关系图
"""


def create_main_flow_dot():
    """创建主流程图的 DOT 源代码"""
    return '''digraph main_flow {
    rankdir=TB;
    size="12,16";

    node [shape=box, style="rounded,filled", fillcolor=lightblue, fontname="Arial"];

    // 节点定义
    start [label="开始\\n输入 Debian URL", shape=ellipse, fillcolor=lightgreen];
    extract [label="从 URL 提取文件名"];
    check_valid [label="文件名是否有效?", shape=diamond, fillcolor=lightyellow];
    error1 [label="抛出 ValueError\\n无法提取文件名", fillcolor=lightcoral];
    check_type [label="判断文件类型", fillcolor=lightcyan];

    type_deb [label=".deb 文件\\n解析二进制包", fillcolor=wheat];
    type_dsc [label=".dsc 文件\\n解析构建文件", fillcolor=wheat];
    type_orig [label=".orig.tar.*\\n解析上游源码", fillcolor=wheat];
    type_debian [label=".debian.tar.*\\n解析 Debian 补丁", fillcolor=wheat];
    type_native [label=".tar.*\\n解析自研源码", fillcolor=wheat];
    error2 [label="不支持的文件类型", fillcolor=lightcoral];

    extract_info [label="提取包名、版本、架构"];
    parse_version [label="解析版本号", fillcolor=lightcyan];

    parse_epoch [label="提取纪元号 epoch"];
    parse_upstream [label="提取上游版本号"];
    parse_revision [label="提取 Debian 修订号"];
    parse_markers [label="解析特殊标识\\n(DFSG/Really/Backports等)"];

    check_native [label="判断是否自研组件"];
    create_obj [label="创建 DebianPackageInfo 对象", fillcolor=lightgreen];
    end [label="返回解析结果", shape=ellipse, fillcolor=lightgreen];

    // 连接
    start -> extract;
    extract -> check_valid;
    check_valid -> error1 [label="否"];
    check_valid -> check_type [label="是"];

    check_type -> type_deb [label=".deb"];
    check_type -> type_dsc [label=".dsc"];
    check_type -> type_orig [label=".orig.tar.*"];
    check_type -> type_debian [label=".debian.tar.*"];
    check_type -> type_native [label=".tar.*"];
    check_type -> error2 [label="其他"];

    type_deb -> extract_info;
    type_dsc -> extract_info;
    type_orig -> extract_info;
    type_debian -> extract_info;
    type_native -> extract_info;

    extract_info -> parse_version;
    parse_version -> parse_epoch;
    parse_epoch -> parse_upstream;
    parse_upstream -> parse_revision;
    parse_revision -> parse_markers;
    parse_markers -> check_native;
    check_native -> create_obj;
    create_obj -> end;
}'''


def create_version_parse_flow_dot():
    """创建版本号解析流程图的 DOT 源代码"""
    return '''digraph version_parse_flow {
    rankdir=TB;
    size="10,14";

    node [shape=box, style="rounded,filled", fillcolor=lightblue, fontname="Arial"];

    start [label="输入版本字符串\\n例: 1:1.18.0-6.1+deb11u5", shape=ellipse, fillcolor=lightgreen];
    check_epoch [label="是否包含 ':' ?", shape=diamond, fillcolor=lightyellow];
    extract_epoch [label="提取纪元号\\nepoch = 1", fillcolor=wheat];
    no_epoch [label="epoch = None", fillcolor=wheat];

    check_revision [label="是否包含 '-' ?", shape=diamond, fillcolor=lightyellow];
    split_version [label="按最后一个 '-' 分割\\n左: 上游版本\\n右: 修订号"];
    no_revision [label="上游版本 = 完整版本\\n修订号 = None", fillcolor=wheat];

    parse_upstream [label="解析上游版本\\n检查特殊标识", fillcolor=lightcyan];
    check_dfsg [label="包含 +dfsg ?", shape=diamond, fillcolor=lightyellow];
    extract_dfsg [label="提取 DFSG 标识\\ndfsg1, dfsg2...", fillcolor=wheat];

    check_really [label="包含 +really ?", shape=diamond, fillcolor=lightyellow];
    extract_really [label="提取 Really 版本\\n真正的版本号", fillcolor=wheat];

    parse_revision_detail [label="解析修订号\\n检查特殊标识", fillcolor=lightcyan];
    check_build [label="包含 +b ?", shape=diamond, fillcolor=lightyellow];
    extract_build [label="提取二进制重制编号\\nb1, b2...", fillcolor=wheat];

    check_bpo [label="包含 ~bpo ?", shape=diamond, fillcolor=lightyellow];
    extract_bpo [label="提取 Backports 标识\\nbpo11+1", fillcolor=wheat];

    check_security [label="包含 deb*u* ?", shape=diamond, fillcolor=lightyellow];
    extract_security [label="提取发行版版本\\n和安全更新编号\\ndeb11, u5", fillcolor=wheat];

    end [label="返回版本信息字典", shape=ellipse, fillcolor=lightgreen];

    // 连接
    start -> check_epoch;
    check_epoch -> extract_epoch [label="是"];
    check_epoch -> no_epoch [label="否"];

    extract_epoch -> check_revision;
    no_epoch -> check_revision;

    check_revision -> split_version [label="是"];
    check_revision -> no_revision [label="否"];

    split_version -> parse_upstream;
    no_revision -> end;

    parse_upstream -> check_dfsg;
    check_dfsg -> extract_dfsg [label="是"];
    check_dfsg -> check_really [label="否"];
    extract_dfsg -> check_really;

    check_really -> extract_really [label="是"];
    check_really -> parse_revision_detail [label="否"];
    extract_really -> parse_revision_detail;

    parse_revision_detail -> check_build;
    check_build -> extract_build [label="是"];
    check_build -> check_bpo [label="否"];
    extract_build -> check_bpo;

    check_bpo -> extract_bpo [label="是"];
    check_bpo -> check_security [label="否"];
    extract_bpo -> check_security;

    check_security -> extract_security [label="是"];
    check_security -> end [label="否"];
    extract_security -> end;
}'''


def create_file_type_flow_dot():
    """创建文件类型判断流程图的 DOT 源代码"""
    return '''digraph file_type_flow {
    rankdir=TB;
    size="10,12";

    node [shape=box, style="rounded,filled", fillcolor=lightblue, fontname="Arial"];

    start [label="获取文件名", shape=ellipse, fillcolor=lightgreen];
    check_ext [label="检查文件扩展名", shape=diamond, fillcolor=lightyellow];

    deb_branch [label=".deb 文件", fillcolor=wheat];
    deb_regex [label="正则匹配:\\npackage_version_arch.deb"];
    deb_result [label="分发类型: 二进制\\n文件类型: 二进制", fillcolor=lightgreen];

    dsc_branch [label=".dsc 文件", fillcolor=wheat];
    dsc_regex [label="正则匹配:\\npackage_version.dsc"];
    dsc_result [label="分发类型: 源码\\n文件类型: 构建文件", fillcolor=lightgreen];

    orig_branch [label=".orig.tar.* 文件", fillcolor=wheat];
    orig_check [label="以 .asc 结尾?", shape=diamond, fillcolor=lightyellow];
    orig_sig [label="上游源码签名", fillcolor=wheat];
    orig_source [label="上游源码", fillcolor=wheat];
    orig_result [label="分发类型: 源码\\n文件类型: 上游源码", fillcolor=lightgreen];

    debian_branch [label=".debian.tar.* 文件", fillcolor=wheat];
    debian_result [label="分发类型: 源码\\n文件类型: 上游源码补丁", fillcolor=lightgreen];

    tar_branch [label=".tar.* 文件", fillcolor=wheat];
    tar_check [label="包含 orig 或 debian?", shape=diamond, fillcolor=lightyellow];
    tar_native [label="自研组件源码", fillcolor=wheat];
    tar_result [label="分发类型: 源码\\n文件类型: 自研源码", fillcolor=lightgreen];

    error [label="不支持的文件类型\\n抛出 ValueError", fillcolor=lightcoral];
    end [label="继续解析", shape=ellipse, fillcolor=lightgreen];

    // 连接
    start -> check_ext;
    check_ext -> deb_branch [label=".deb"];
    check_ext -> dsc_branch [label=".dsc"];
    check_ext -> orig_branch [label=".orig.tar.*"];
    check_ext -> debian_branch [label=".debian.tar.*"];
    check_ext -> tar_branch [label=".tar.*"];
    check_ext -> error [label="其他"];

    deb_branch -> deb_regex;
    deb_regex -> deb_result;
    deb_result -> end;

    dsc_branch -> dsc_regex;
    dsc_regex -> dsc_result;
    dsc_result -> end;

    orig_branch -> orig_check;
    orig_check -> orig_sig [label="是"];
    orig_check -> orig_source [label="否"];
    orig_sig -> orig_result;
    orig_source -> orig_result;
    orig_result -> end;

    debian_branch -> debian_result;
    debian_result -> end;

    tar_branch -> tar_check;
    tar_check -> tar_native [label="否"];
    tar_native -> tar_result;
    tar_result -> end;
}'''


def create_usage_flow_dot():
    """创建使用场景流程图的 DOT 源代码"""
    return '''digraph usage_flow {
    rankdir=TB;
    size="12,14";

    node [shape=box, style="rounded,filled", fillcolor=lightblue, fontname="Arial"];

    start [label="用户需求", shape=ellipse, fillcolor=lightgreen];
    choose_way [label="选择使用方式", shape=diamond, fillcolor=lightyellow];

    import [label="导入\\nDebianURLParser", fillcolor=wheat];
    create_parser [label="创建 parser 实例"];
    call_parse [label="调用 parse_url(url)"];
    get_info [label="获取\\nDebianPackageInfo 对象"];
    choose_format [label="选择输出格式", shape=diamond, fillcolor=lightyellow];
    use_object [label="直接使用对象属性", fillcolor=lightgreen];
    use_dict [label="调用 to_dict()", fillcolor=lightgreen];
    use_json [label="json.dumps()", fillcolor=lightgreen];

    run_cli [label="运行\\ndebian_parser_cli.py", fillcolor=wheat];
    choose_input [label="选择输入方式", shape=diamond, fillcolor=lightyellow];
    single_url [label="单个 URL\\n命令行参数", fillcolor=wheat];
    batch_file [label="批量处理\\n--file 参数", fillcolor=wheat];
    choose_output [label="选择输出格式", shape=diamond, fillcolor=lightyellow];
    readable [label="人类可读格式\\n(默认)", fillcolor=lightgreen];
    json_output [label="JSON 格式\\n--json 参数", fillcolor=lightgreen];
    choose_filter [label="是否需要过滤?", shape=diamond, fillcolor=lightyellow];
    filter_arch [label="按架构过滤\\n--filter-arch", fillcolor=wheat];
    filter_type [label="按类型过滤\\n--filter-type", fillcolor=wheat];
    no_filter [label="不过滤", fillcolor=wheat];

    end [label="处理业务逻辑", shape=ellipse, fillcolor=lightgreen];

    // 连接
    start -> choose_way;
    choose_way -> import [label="Python 库"];
    choose_way -> run_cli [label="命令行工具"];

    import -> create_parser;
    create_parser -> call_parse;
    call_parse -> get_info;
    get_info -> choose_format;
    choose_format -> use_object [label="对象"];
    choose_format -> use_dict [label="字典"];
    choose_format -> use_json [label="JSON"];
    use_object -> end;
    use_dict -> end;
    use_json -> end;

    run_cli -> choose_input;
    choose_input -> single_url [label="单个"];
    choose_input -> batch_file [label="批量"];
    single_url -> choose_output;
    batch_file -> choose_output;
    choose_output -> readable [label="文本"];
    choose_output -> json_output [label="JSON"];
    readable -> choose_filter;
    json_output -> choose_filter;
    choose_filter -> filter_arch [label="架构"];
    choose_filter -> filter_type [label="类型"];
    choose_filter -> no_filter [label="否"];
    filter_arch -> end;
    filter_type -> end;
    no_filter -> end;
}'''


def create_class_diagram_dot():
    """创建类关系图的 DOT 源代码"""
    return '''digraph class_diagram {
    rankdir=TB;
    size="10,8";

    node [shape=record, style=filled, fillcolor=lightblue, fontname="Arial"];

    Parser [label="{DebianURLParser|+ BINARY_PATTERN\\l+ DSC_PATTERN\\l+ ORIG_PATTERN\\l+ DEBIAN_PATCH_PATTERN\\l+ NATIVE_SOURCE_PATTERN\\l|+ parse_url(url: str)\\l- _parse_binary_package()\\l- _parse_dsc_file()\\l- _parse_orig_source()\\l- _parse_debian_patch()\\l- _parse_native_source()\\l- _parse_version(version)\\l- _parse_upstream_markers()\\l- _parse_revision_markers()\\l}", fillcolor=lightcyan];

    Info [label="{DebianPackageInfo|+ url: str\\l+ filename: str\\l+ package_name: str\\l+ version: str\\l+ architecture: Optional[str]\\l+ epoch: Optional[str]\\l+ upstream_version: str\\l+ debian_revision: Optional[str]\\l+ dfsg_marker: Optional[str]\\l+ really_version: Optional[str]\\l+ binary_rebuild: Optional[str]\\l+ backport_marker: Optional[str]\\l+ nmu_marker: Optional[str]\\l+ ubuntu_marker: Optional[str]\\l+ release_version: Optional[str]\\l+ security_update: Optional[str]\\l+ distribution_type: str\\l+ file_type: str\\l+ is_native: bool\\l|+ to_dict(): Dict\\l}", fillcolor=wheat];

    Parser -> Info [label="  creates  ", style=dashed, arrowhead=open];
}'''


def main():
    """主函数"""
    print("=" * 80)
    print("Debian URL 解析器流程图生成器（DOT 文件版本）")
    print("=" * 80)

    graphs = [
        ('main_flow.dot', create_main_flow_dot, '主流程图'),
        ('version_parse_flow.dot', create_version_parse_flow_dot, '版本号解析流程图'),
        ('file_type_flow.dot', create_file_type_flow_dot, '文件类型判断流程图'),
        ('usage_flow.dot', create_usage_flow_dot, '使用场景流程图'),
        ('class_diagram.dot', create_class_diagram_dot, '类关系图'),
    ]

    print("\n开始生成 DOT 文件...\n")

    success_count = 0
    for filename, create_func, description in graphs:
        try:
            print(f"正在生成: {description}...")
            dot_content = create_func()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(dot_content)
            print(f"  ✅ 成功生成: {filename}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ 生成失败: {e}")

    print("\n" + "=" * 80)
    print(f"完成! 成功生成 {success_count}/{len(graphs)} 个 DOT 文件")
    print("=" * 80)

    if success_count > 0:
        print("\n生成的文件:")
        for filename, _, description in graphs:
            print(f"  - {filename} - {description}")

        print("\n💡 如何查看流程图:")
        print("\n方法 1: 在线查看（推荐）")
        print("  访问: https://dreampuf.github.io/GraphvizOnline/")
        print("  或者: http://www.webgraphviz.com/")
        print("  然后复制 .dot 文件内容粘贴进去")

        print("\n方法 2: VS Code")
        print("  安装插件: Graphviz Preview")
        print("  然后打开 .dot 文件，右键选择 'Open Preview'")

        print("\n方法 3: 命令行渲染为图片")
        print("  dot -Tpng main_flow.dot -o main_flow.png")
        print("  dot -Tsvg version_parse_flow.dot -o version_parse_flow.svg")

        print("\n方法 4: 批量渲染所有图片")
        print("  for f in *.dot; do dot -Tpng $f -o ${f%.dot}.png; done")

    return 0 if success_count == len(graphs) else 1


if __name__ == "__main__":
    exit(main())

