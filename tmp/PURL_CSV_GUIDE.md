# Debian URL Parser - PURL 和 CSV 导出功能

## 功能说明

### 1. `package_purl` 属性

从 Debian 包 URL 中自动生成 Package URL (PURL)。

**格式**: `pkg:deb/debian/<package_name>`

**示例**:
```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()
url = "https://example.com/pool/main/o/openjdk-11/openjdk-11-demo_11.0.29+7-1_s390x.deb"
info = parser.parse_url(url)

print(info.package_name)  # openjdk-11-demo
print(info.version)       # 11.0.29+7-1
print(info.package_purl)  # pkg:deb/debian/openjdk-11-demo
```

### 2. CSV 导出功能

使用 `export_to_csv()` 函数将解析结果批量导出到 CSV 文件。

## 快速开始

### 单个 URL 解析

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()
url = "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb"
info = parser.parse_url(url)

print(f"包名: {info.package_name}")
print(f"版本: {info.version}")
print(f"PURL: {info.package_purl}")
print(f"架构: {info.architecture}")
```

**输出**:
```
包名: nginx
版本: 1.18.0-6.1
PURL: pkg:deb/debian/nginx
架构: amd64
```

### 批量解析并导出到 CSV

```python
from debian_url_parser import DebianURLParser, export_to_csv

parser = DebianURLParser()

# URL 列表
urls = [
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
    "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
    "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
]

# 解析所有 URL
package_infos = []
for url in urls:
    try:
        info = parser.parse_url(url)
        package_infos.append(info)
        print(f"✓ {info.package_name} -> {info.package_purl}")
    except ValueError as e:
        print(f"✗ 解析失败: {e}")

# 导出到 CSV
export_to_csv(package_infos, "output.csv")
```

**输出**:
```
✓ nginx -> pkg:deb/debian/nginx
✓ dpkg -> pkg:deb/debian/dpkg
✓ openssl -> pkg:deb/debian/openssl
✓ 已导出 3 条记录到 output.csv
```

### CSV 文件格式

生成的 CSV 文件包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| `url` | 原始 URL | https://example.com/.../nginx_1.18.0-6.1_amd64.deb |
| `filename` | 文件名 | nginx_1.18.0-6.1_amd64.deb |
| `package_name` | 包名 | nginx |
| `package_purl` | Package URL | pkg:deb/debian/nginx |
| `version` | 完整版本号 | 1.18.0-6.1 |
| `architecture` | 架构 | amd64 |
| `epoch` | 纪元号 | (空或数字) |
| `upstream_version` | 上游版本 | 1.18.0 |
| `debian_revision` | Debian 修订号 | 6.1 |
| `distribution_type` | 分发类型 | binary / source |
| `file_type` | 文件类型 | binary / upstream_source / ... |
| `is_native` | 是否自研 | True / False |
| `dfsg_marker` | DFSG 标识 | dfsg1 |
| `really_version` | Really 版本 | 1.0 |
| `binary_rebuild` | 二进制重制 | b2 |
| `backport_marker` | Backport 标识 | bpo11+1 |
| `nmu_marker` | NMU 标识 | nmu1 |
| `ubuntu_marker` | Ubuntu 标识 | ubuntu1.1 |
| `release_version` | 发行版版本 | deb11 |
| `security_update` | 安全更新 | u5 |

### CSV 示例内容

```csv
url,filename,package_name,package_purl,version,architecture,...
https://example.com/.../nginx_1.18.0-6.1_amd64.deb,nginx_1.18.0-6.1_amd64.deb,nginx,pkg:deb/debian/nginx,1.18.0-6.1,amd64,...
https://example.com/.../dpkg_1.23.3_armhf.deb,dpkg_1.23.3_armhf.deb,dpkg,pkg:deb/debian/dpkg,1.23.3,armhf,...
```

## 完整示例

参考 `example_export_csv.py` 文件，运行:

```bash
python example_export_csv.py
```

这将：
1. 解析 16 个示例 URL
2. 显示解析进度和结果
3. 将所有结果导出到 `debian_packages_output.csv`
4. 显示文件预览

## 支持的文件类型

- **二进制包**: `.deb`
- **构建文件**: `.dsc`
- **上游源码**: `.orig.tar.gz`, `.orig.tar.xz`, `.orig.tar.bz2`
- **源码签名**: `.orig.tar.*.asc`
- **Debian 补丁**: `.debian.tar.gz`, `.debian.tar.xz`
- **自研源码**: `.tar.gz`, `.tar.xz`, `.tar.bz2`

## PURL 示例

| 文件名 | Package Name | PURL |
|--------|--------------|------|
| `openjdk-11-demo_11.0.29+7-1_s390x.deb` | openjdk-11-demo | pkg:deb/debian/openjdk-11-demo |
| `nginx_1.18.0-6.1_amd64.deb` | nginx | pkg:deb/debian/nginx |
| `dpkg_1.23.3_armhf.deb` | dpkg | pkg:deb/debian/dpkg |
| `openssl_1.1.1n-0+deb11u5_amd64.deb` | openssl | pkg:deb/debian/openssl |

## 注意事项

1. PURL 只包含包名，不包含版本号和架构信息
2. CSV 文件使用 UTF-8 编码
3. 空值在 CSV 中显示为空字符串
4. 布尔值（`is_native`）在 CSV 中显示为 `True` 或 `False`

## API 参考

### `export_to_csv(package_infos, output_file="debian_packages.csv")`

**参数**:
- `package_infos` (list): `DebianPackageInfo` 对象列表
- `output_file` (str): 输出文件路径，默认为 `debian_packages.csv`

**返回**: 无

**示例**:
```python
export_to_csv(package_infos, "my_packages.csv")
```

