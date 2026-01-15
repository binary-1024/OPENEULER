# Debian URL 解析器

基于 Debian 组件命名规范的 URL 解析工具，可以从 Debian 组件下载 URL 中提取详细的组件信息。

## 功能特性

### 支持的文件类型

1. **二进制包** (`.deb`)
   - 普通二进制包
   - 带安全更新的二进制包
   - 架构特定的二进制包

2. **源码包**
   - 构建文件 (`.dsc`)
   - 上游源码 (`.orig.tar.*`)
   - 上游源码签名 (`.orig.tar.*.asc`)
   - Debian 补丁 (`.debian.tar.*`)
   - 自研组件源码 (`.tar.*`)

### 解析的信息

- **基础信息**
  - 组件名称
  - 完整版本号
  - 架构（针对二进制包）

- **版本详细信息**
  - 纪元号 (epoch)
  - 上游版本号 (upstream version)
  - Debian 修订号 (debian revision)

- **特殊版本标识**
  - DFSG 重打包标识 (`+dfsg1`)
  - Really 真正版本标识 (`+really1.0`)
  - 二进制重制编号 (`+b2`)
  - Backports 反向移植 (`~bpo11+1`)
  - NMU 非维护者上传 (`+nmu1`)
  - Ubuntu 衍生版本 (`ubuntu1.1`)

- **发行版信息**
  - 发行版版本号 (`deb11`, `deb12` 等)
  - 安全更新编号 (`u1`, `u2` 等)

- **分类信息**
  - 分发类型：源码 / 二进制
  - 文件类型：上游源码 / 上游源码补丁 / 自研源码 / 二进制 / 构建文件
  - 是否为 Debian 自研组件

## 安装

直接复制 `debian_url_parser.py` 到你的项目中即可使用。

## 快速开始

### 基础用法

```python
from debian_url_parser import DebianURLParser

# 创建解析器实例
parser = DebianURLParser()

# 解析一个 URL
url = "https://snapshot.debian.org/archive/debian/20251220T083035Z/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb"
info = parser.parse_url(url)

# 访问解析结果
print(f"组件名: {info.package_name}")
print(f"版本: {info.version}")
print(f"架构: {info.architecture}")
print(f"文件类型: {info.file_type}")
```

### 导出为字典或 JSON

```python
# 转换为字典
data = info.to_dict()

# 转换为 JSON
import json
json_str = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str)
```

## 使用示例

### 示例 1: 识别安全更新包

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()

urls = [
    "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
]

for url in urls:
    info = parser.parse_url(url)
    if info.security_update:
        print(f"🔐 安全更新: {info.package_name}")
        print(f"   发行版: {info.release_version}")
        print(f"   安全更新编号: {info.security_update}")
    else:
        print(f"📦 普通包: {info.package_name}")
```

### 示例 2: 区分自研组件和上游组件

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()

urls = [
    "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",  # 自研
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",  # 上游
]

for url in urls:
    info = parser.parse_url(url)
    if info.is_native:
        print(f"🏠 Debian 自研: {info.package_name}")
    else:
        print(f"🌐 上游组件: {info.package_name}")
```

### 示例 3: 批量处理并过滤

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()

urls = [
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_i386.deb",
    "https://example.com/pool/main/n/nginx/nginx_1.28.0-6.dsc",
]

# 只获取 amd64 架构的二进制包
amd64_packages = []
for url in urls:
    info = parser.parse_url(url)
    if info.file_type == "二进制" and info.architecture == "amd64":
        amd64_packages.append(info)

print(f"找到 {len(amd64_packages)} 个 amd64 二进制包")
```

### 示例 4: 处理复杂版本号

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()

# 包含多种特殊标识的版本
url = "https://example.com/pool/main/p/package/package_1.2.3+dfsg1-2+deb12u1_amd64.deb"
info = parser.parse_url(url)

print(f"完整版本: {info.version}")
print(f"上游版本: {info.upstream_version}")
print(f"Debian 修订: {info.debian_revision}")
print(f"DFSG 标识: {info.dfsg_marker}")
print(f"发行版: {info.release_version}")
print(f"安全更新: {info.security_update}")
```

## API 文档

### `DebianURLParser`

主要的解析器类。

#### 方法

##### `parse_url(url: str) -> DebianPackageInfo`

解析 Debian 组件 URL，返回包含详细信息的 `DebianPackageInfo` 对象。

**参数:**
- `url` (str): Debian 组件的下载 URL

**返回:**
- `DebianPackageInfo`: 解析后的组件信息对象

**异常:**
- `ValueError`: 当 URL 无法解析或文件类型不支持时抛出

**示例:**
```python
parser = DebianURLParser()
info = parser.parse_url("https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb")
```

### `DebianPackageInfo`

包含 Debian 组件详细信息的数据类。

#### 属性

**原始信息:**
- `url` (str): 原始 URL
- `filename` (str): 文件名

**基础信息:**
- `package_name` (str): 组件名
- `version` (str): 完整版本字符串
- `architecture` (Optional[str]): 架构（二进制包才有）

**版本详细信息:**
- `epoch` (Optional[str]): 纪元号
- `upstream_version` (str): 上游版本号
- `debian_revision` (Optional[str]): Debian 修订号

**版本特殊标识:**
- `dfsg_marker` (Optional[str]): DFSG 重打包标识
- `really_version` (Optional[str]): really 真正版本标识
- `binary_rebuild` (Optional[str]): 二进制重制编号
- `backport_marker` (Optional[str]): backports 标识
- `nmu_marker` (Optional[str]): 非维护者上传标识
- `ubuntu_marker` (Optional[str]): Ubuntu 衍生版本标识

**发行版和安全更新信息:**
- `release_version` (Optional[str]): 发行版版本号
- `security_update` (Optional[str]): 安全更新编号

**分类信息:**
- `distribution_type` (str): 分发类型（"源码" 或 "二进制"）
- `file_type` (str): 文件类型
- `is_native` (bool): 是否为 Debian 自研组件

#### 方法

##### `to_dict() -> Dict`

将对象转换为字典格式，便于序列化或导出。

**返回:**
- `Dict`: 包含所有属性的字典

**示例:**
```python
info = parser.parse_url(url)
data = info.to_dict()
```

## 版本号格式说明

### 通用格式

```
<package-name>_<epoch>:<upstream-version>-<debian-revision>_<architecture>.deb
```

**示例:**
- `nginx_1.18.0-6.1_amd64.deb`
- `dpkg_1.23.3_armhf.deb` (自研组件，无修订号)

### 安全更新格式

```
<package-name>_<upstream-version>-<debian-revision><release>u<security-number>_<architecture>.deb
```

**示例:**
- `openssl_1.1.1n-0+deb11u5_amd64.deb`

### 源码包格式

```
<package-name>_<version>.dsc                    # 构建文件
<package-name>_<version>.orig.tar.gz            # 上游源码
<package-name>_<version>.debian.tar.xz          # Debian 补丁
<package-name>_<version>.tar.xz                 # 自研组件源码
```

## 运行示例代码

项目包含完整的示例代码：

```bash
# 运行基本的测试用例
python3 debian_url_parser.py

# 运行详细的使用示例
python3 debian_parser_examples.py
```

## 测试用例

解析器已通过以下类型的 URL 测试：

- ✅ 普通二进制包
- ✅ 自研组件二进制包
- ✅ 安全更新包
- ✅ 带 DFSG 标识的包
- ✅ 带 really 标识的包
- ✅ 二进制重制包
- ✅ Backports 包
- ✅ Ubuntu 衍生版本包
- ✅ 构建文件 (.dsc)
- ✅ 上游源码 (.orig.tar.*)
- ✅ 上游源码签名 (.orig.tar.*.asc)
- ✅ Debian 补丁 (.debian.tar.*)
- ✅ 自研组件源码 (.tar.*)

## 注意事项

1. **包名规则**: 包名必须以小写字母开头，只能包含小写字母、数字、加号、连字符和点号
2. **架构信息**: 只有二进制包（.deb）才有架构信息，源码包返回 `None`
3. **自研组件识别**: 通过是否包含 Debian 修订号来判断是否为自研组件
4. **版本号复杂度**: 支持解析包含多种特殊标识的复杂版本号

## 错误处理

解析器会对无效的 URL 或不支持的文件类型抛出 `ValueError` 异常：

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()

try:
    info = parser.parse_url("https://example.com/invalid.txt")
except ValueError as e:
    print(f"解析失败: {e}")
```

## 依赖

- Python 3.6+
- 标准库: `re`, `urllib.parse`, `dataclasses`, `typing`

无需安装第三方依赖。

## 许可证

根据项目根目录的 LICENSE 文件。

## 相关文档

- `deb_version_parse.md` - Debian 版本命名规范详细说明
- `deb_version_compare.md` - Debian 版本比较规则

## 作者

基于 Debian 官方命名规范开发。

