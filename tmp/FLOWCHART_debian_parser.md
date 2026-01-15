# Debian URL 解析器流程图

## 1. 主流程图

```mermaid
graph TD
    A[开始: 输入 Debian URL] --> B[从 URL 提取文件名]
    B --> C{文件名是否有效?}
    C -->|否| D[抛出 ValueError]
    C -->|是| E{判断文件类型}

    E -->|.deb| F[解析二进制包]
    E -->|.dsc| G[解析构建文件]
    E -->|.orig.tar.*| H[解析上游源码]
    E -->|.orig.tar.*.asc| I[解析上游源码签名]
    E -->|.debian.tar.*| J[解析 Debian 补丁]
    E -->|.tar.*| K[解析自研组件源码]
    E -->|其他| D

    F --> L[提取包名、版本、架构]
    G --> M[提取包名、版本]
    H --> M
    I --> M
    J --> M
    K --> M

    L --> N[解析版本号]
    M --> N

    N --> O[提取纪元号 epoch]
    O --> P[提取上游版本号]
    P --> Q[提取 Debian 修订号]
    Q --> R[解析特殊标识]

    R --> S[DFSG 标识]
    R --> T[Really 标识]
    R --> U[二进制重制]
    R --> V[Backports]
    R --> W[安全更新]

    S --> X[判断是否自研组件]
    T --> X
    U --> X
    V --> X
    W --> X

    X --> Y[创建 DebianPackageInfo 对象]
    Y --> Z[返回解析结果]
    Z --> END[结束]
```

## 2. 版本号解析详细流程

```mermaid
graph TD
    A[输入版本字符串] --> B{是否包含 ':' ?}
    B -->|是| C[提取纪元号 epoch]
    B -->|否| D[纪元号 = None]

    C --> E{是否包含 '-' ?}
    D --> E

    E -->|是| F[按最后一个 '-' 分割]
    E -->|否| G[上游版本 = 完整版本<br/>修订号 = None]

    F --> H[左边 = 上游版本]
    F --> I[右边 = 修订号]

    H --> J[解析上游版本特殊标识]
    J --> K{包含 +dfsg ?}
    K -->|是| L[提取 DFSG 标识]
    K -->|否| M{包含 +really ?}

    M -->|是| N[提取 Really 版本]
    M -->|否| O[无特殊上游标识]

    L --> P[继续解析修订号]
    N --> P
    O --> P

    I --> P
    P --> Q{修订号包含 +b ?}
    Q -->|是| R[提取二进制重制编号]
    Q -->|否| S{包含 ~bpo ?}

    S -->|是| T[提取 Backports 标识]
    S -->|否| U{包含 deb*u* ?}

    U -->|是| V[提取发行版版本<br/>和安全更新编号]
    U -->|否| W{包含 ubuntu ?}

    W -->|是| X[提取 Ubuntu 标识]
    W -->|否| Y[无特殊修订标识]

    R --> Z[返回版本信息字典]
    T --> Z
    V --> Z
    X --> Z
    Y --> Z
    G --> Z
```

## 3. 文件类型判断流程

```mermaid
graph TD
    A[获取文件名] --> B{文件扩展名?}

    B -->|.deb| C[二进制包]
    C --> D[正则匹配:<br/>package_version_arch.deb]
    D --> E{匹配成功?}
    E -->|是| F[分发类型 = 二进制<br/>文件类型 = 二进制]
    E -->|否| G[抛出错误]

    B -->|.dsc| H[构建文件]
    H --> I[正则匹配:<br/>package_version.dsc]
    I --> J{匹配成功?}
    J -->|是| K[分发类型 = 源码<br/>文件类型 = 构建文件]
    J -->|否| G

    B -->|.orig.tar.*| L{以 .asc 结尾?}
    L -->|是| M[上游源码签名]
    L -->|否| N[上游源码]
    M --> O[分发类型 = 源码<br/>文件类型 = 上游源码]
    N --> O

    B -->|.debian.tar.*| P[Debian 补丁]
    P --> Q[分发类型 = 源码<br/>文件类型 = 上游源码补丁]

    B -->|.tar.*| R{包含 orig 或 debian?}
    R -->|是| S[上游组件源码]
    R -->|否| T[自研组件源码]
    T --> U[分发类型 = 源码<br/>文件类型 = 自研源码]

    B -->|其他| G

    F --> V[继续解析]
    K --> V
    O --> V
    Q --> V
    U --> V
```

## 4. 自研组件识别流程

```mermaid
graph TD
    A[已解析的包信息] --> B{Debian 修订号存在?}
    B -->|否| C[is_native = True<br/>这是 Debian 自研组件]
    B -->|是| D[is_native = False<br/>这是上游组件]

    C --> E{文件类型?}
    D --> F{文件类型?}

    E -->|.tar.*| G[自研源码包]
    E -->|.deb| H[自研二进制包]
    E -->|.dsc| I[自研构建文件]

    F -->|.orig.tar.*| J[上游源码]
    F -->|.debian.tar.*| K[Debian 补丁]
    F -->|.deb| L[上游二进制包]
    F -->|.dsc| M[上游构建文件]

    G --> N[示例: dpkg_1.23.3.tar.xz]
    H --> O[示例: dpkg_1.23.3_amd64.deb]
    J --> P[示例: nginx_1.28.0.orig.tar.gz]
    K --> Q[示例: nginx_1.28.0-6.debian.tar.xz]
    L --> R[示例: nginx_1.18.0-6.1_amd64.deb]
```

## 5. 使用场景流程

```mermaid
graph TD
    A[用户需求] --> B{使用方式?}

    B -->|Python 库| C[导入 DebianURLParser]
    B -->|命令行工具| D[运行 debian_parser_cli.py]

    C --> E[创建 parser 实例]
    E --> F[调用 parse_url 方法]
    F --> G[获取 DebianPackageInfo 对象]
    G --> H{需要的格式?}

    H -->|Python 对象| I[直接使用对象属性]
    H -->|字典| J[调用 to_dict 方法]
    H -->|JSON| K[json.dumps]

    D --> L{输入方式?}
    L -->|单个 URL| M[命令行参数传入 URL]
    L -->|批量处理| N[--file 参数指定文件]

    M --> O{输出格式?}
    N --> O

    O -->|人类可读| P[默认格式化输出]
    O -->|JSON| Q[--json 参数]

    P --> R{需要过滤?}
    Q --> R

    R -->|按架构| S[--filter-arch amd64]
    R -->|按类型| T[--filter-type 二进制]
    R -->|不过滤| U[输出所有结果]

    I --> V[处理业务逻辑]
    J --> V
    K --> V
    S --> V
    T --> V
    U --> V
```

## 6. 数据结构关系图

```mermaid
classDiagram
    class DebianURLParser {
        +BINARY_PATTERN: re.Pattern
        +DSC_PATTERN: re.Pattern
        +ORIG_PATTERN: re.Pattern
        +parse_url(url: str) DebianPackageInfo
        -_parse_binary_package() DebianPackageInfo
        -_parse_dsc_file() DebianPackageInfo
        -_parse_orig_source() DebianPackageInfo
        -_parse_debian_patch() DebianPackageInfo
        -_parse_native_source() DebianPackageInfo
        -_parse_version(version: str) Dict
    }

    class DebianPackageInfo {
        +url: str
        +filename: str
        +package_name: str
        +version: str
        +architecture: Optional~str~
        +epoch: Optional~str~
        +upstream_version: str
        +debian_revision: Optional~str~
        +dfsg_marker: Optional~str~
        +really_version: Optional~str~
        +binary_rebuild: Optional~str~
        +backport_marker: Optional~str~
        +nmu_marker: Optional~str~
        +ubuntu_marker: Optional~str~
        +release_version: Optional~str~
        +security_update: Optional~str~
        +distribution_type: str
        +file_type: str
        +is_native: bool
        +to_dict() Dict
    }

    DebianURLParser --> DebianPackageInfo : creates

    note for DebianURLParser "核心解析器类\n负责解析各种类型的 Debian 包"
    note for DebianPackageInfo "数据类\n存储解析后的所有信息"
```

## 7. 完整示例流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant CLI as CLI工具
    participant Parser as DebianURLParser
    participant Info as DebianPackageInfo

    User->>CLI: python3 debian_parser_cli.py "URL"
    CLI->>Parser: 创建解析器实例
    CLI->>Parser: parse_url(url)

    Parser->>Parser: 提取文件名
    Parser->>Parser: 判断文件类型

    alt 二进制包 (.deb)
        Parser->>Parser: _parse_binary_package()
        Parser->>Parser: 正则匹配提取包名、版本、架构
    else 源码包 (.dsc/.orig/.debian/.tar)
        Parser->>Parser: _parse_*_file()
        Parser->>Parser: 正则匹配提取包名、版本
    end

    Parser->>Parser: _parse_version(version)
    Parser->>Parser: 提取纪元号
    Parser->>Parser: 提取上游版本
    Parser->>Parser: 提取修订号
    Parser->>Parser: 解析特殊标识

    Parser->>Info: 创建 DebianPackageInfo 对象
    Parser-->>CLI: 返回 Info 对象

    alt JSON 输出
        CLI->>Info: to_dict()
        CLI->>CLI: json.dumps()
        CLI-->>User: JSON 格式结果
    else 人类可读输出
        CLI->>Info: 访问各个属性
        CLI->>CLI: 格式化输出
        CLI-->>User: 格式化的文本结果
    end
```

## 8. 错误处理流程

```mermaid
graph TD
    A[parse_url 开始] --> B{URL 有效?}
    B -->|否| C[ValueError: 无法提取文件名]
    B -->|是| D{文件类型支持?}

    D -->|否| E[ValueError: 不支持的文件类型]
    D -->|是| F{正则匹配成功?}

    F -->|否| G[ValueError: 无法解析文件名]
    F -->|是| H[继续解析版本号]

    H --> I{版本格式正确?}
    I -->|否| J[使用默认值/跳过可选字段]
    I -->|是| K[解析所有版本组件]

    J --> L[创建 PackageInfo 对象]
    K --> L

    L --> M[返回结果]

    C --> N[CLI: 捕获异常并显示错误]
    E --> N
    G --> N

    N --> O[打印友好的错误消息]
    O --> P[继续处理下一个 URL<br/>或退出]
```

## 流程图说明

### 图 1: 主流程图
展示从输入 URL 到输出解析结果的完整流程，包括文件类型判断、版本解析、特殊标识提取等关键步骤。

### 图 2: 版本号解析详细流程
专门展示版本号解析的详细过程，包括纪元号、上游版本、修订号以及各种特殊标识的提取逻辑。

### 图 3: 文件类型判断流程
展示如何根据文件扩展名和正则表达式判断文件类型（二进制/源码）和具体分类。

### 图 4: 自研组件识别流程
展示如何区分 Debian 自研组件和上游组件的逻辑。

### 图 5: 使用场景流程
展示用户如何使用解析器（Python 库或 CLI 工具）以及各种输出格式和过滤选项。

### 图 6: 数据结构关系图
展示核心类之间的关系和各类的属性方法。

### 图 7: 完整示例流程
使用时序图展示一次完整的解析过程中各组件之间的交互。

### 图 8: 错误处理流程
展示各种错误情况的处理流程。

## 如何查看流程图

这些流程图使用 Mermaid 语法编写。您可以通过以下方式查看：

1. **GitHub**: 直接在 GitHub 上查看此 Markdown 文件，会自动渲染
2. **VS Code**: 安装 "Markdown Preview Mermaid Support" 插件
3. **在线工具**: 复制代码到 https://mermaid.live/ 查看
4. **Typora**: 支持 Mermaid 的 Markdown 编辑器

## 快速理解建议

1. **新手**: 先看"图 1: 主流程图"和"图 7: 完整示例流程"
2. **开发者**: 重点看"图 2: 版本号解析"和"图 6: 数据结构关系图"
3. **用户**: 看"图 5: 使用场景流程"了解如何使用
4. **调试**: 看"图 8: 错误处理流程"了解异常处理

