# 📦 JSON 导出功能说明

## 功能概述

`export_to_json()` 函数可以将 Debian 包解析结果导出为 JSON 格式，包含所有字段和 PURL。

## 使用方法

### 基础用法

```python
from debian_url_parser import DebianURLParser, export_to_json

parser = DebianURLParser()

# 解析 URL
urls = [
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
    "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
]

infos = [parser.parse_url(url) for url in urls]

# 导出到 JSON
export_to_json(infos, "packages.json")
```

### 参数说明

```python
export_to_json(
    package_infos: list,      # DebianPackageInfo 对象列表
    output_file: str = "debian_packages.json",  # 输出文件路径
    pretty: bool = True       # 是否美化输出（默认 True）
)
```

## JSON 格式

### 字段列表 (20个)

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `url` | string | 原始 URL | https://... |
| `filename` | string | 文件名 | nginx_1.18.0-6.1_amd64.deb |
| `package_name` | string | 包名 | nginx |
| **`package_purl`** | **string** | **Package URL** | **pkg:deb/debian/nginx** |
| `version` | string | 完整版本号 | 1.18.0-6.1 |
| `architecture` | string/null | 架构 | amd64 |
| `epoch` | string/null | 纪元号 | 2 |
| `upstream_version` | string | 上游版本 | 1.18.0 |
| `debian_revision` | string/null | Debian 修订号 | 6.1 |
| `dfsg_marker` | string/null | DFSG 标识 | dfsg1 |
| `really_version` | string/null | Really 版本 | 1.0 |
| `binary_rebuild` | string/null | 二进制重制 | b2 |
| `backport_marker` | string/null | Backport 标识 | bpo11+1 |
| `nmu_marker` | string/null | NMU 标识 | nmu1 |
| `ubuntu_marker` | string/null | Ubuntu 标识 | ubuntu1.1 |
| `release_version` | string/null | 发行版版本 | deb11 |
| `security_update` | string/null | 安全更新 | u5 |
| `distribution_type` | string | 分发类型 | binary / source |
| `file_type` | string | 文件类型 | binary / upstream_source / ... |
| `is_native` | boolean | 是否自研 | true / false |

### JSON 示例

```json
{
  "url": "https://example.com/pool/main/o/openjdk-11/openjdk-11-demo_11.0.29+7-1_s390x.deb",
  "filename": "openjdk-11-demo_11.0.29+7-1_s390x.deb",
  "package_name": "openjdk-11-demo",
  "version": "11.0.29+7-1",
  "architecture": "s390x",
  "epoch": null,
  "upstream_version": "11.0.29+7",
  "debian_revision": "1",
  "dfsg_marker": null,
  "really_version": null,
  "binary_rebuild": null,
  "backport_marker": null,
  "nmu_marker": null,
  "ubuntu_marker": null,
  "release_version": null,
  "security_update": null,
  "distribution_type": "binary",
  "file_type": "binary",
  "is_native": false,
  "package_purl": "pkg:deb/debian/openjdk-11-demo"
}
```

## 使用场景

### 1. 生成软件清单 (SBOM)

```python
from debian_url_parser import DebianURLParser, export_to_json

parser = DebianURLParser()
urls = [...]  # URL 列表

infos = [parser.parse_url(url) for url in urls]
export_to_json(infos, "sbom.json", pretty=True)
```

### 2. API 数据交换

```python
# 紧凑格式，适合 API 传输
export_to_json(infos, "api_data.json", pretty=False)
```

### 3. 与其他工具集成

```python
import json

# 导出后可以被其他工具读取
export_to_json(infos, "packages.json")

# 在其他程序中读取
with open("packages.json") as f:
    data = json.load(f)
    for pkg in data:
        print(f"{pkg['package_purl']}: {pkg['version']}")
```

### 4. 数据分析

```python
import json
import pandas as pd

# 导出为 JSON
export_to_json(infos, "packages.json")

# 使用 pandas 分析
df = pd.read_json("packages.json")
print(df.describe())
print(df['architecture'].value_counts())
```

## 对比 CSV 和 JSON

| 特性 | CSV | JSON |
|------|-----|------|
| 可读性 | 表格形式，易读 | 结构化，易于解析 |
| 数据类型 | 纯文本 | 保留类型（boolean, null） |
| 嵌套结构 | 不支持 | 支持 |
| 文件大小 | 较小 | 较大（美化后） |
| API 友好 | ❌ | ✅ |
| Excel 打开 | ✅ | ❌ |
| 程序解析 | 需要处理 | 直接解析 |

## 完整示例

```python
#!/usr/bin/env python3
from debian_url_parser import DebianURLParser, export_to_json, export_to_csv

parser = DebianURLParser()

urls = [
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
    "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
    "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
]

# 解析所有 URL
infos = []
for url in urls:
    try:
        info = parser.parse_url(url)
        infos.append(info)
        print(f"✓ {info.package_name} -> {info.package_purl}")
    except Exception as e:
        print(f"✗ 失败: {e}")

# 导出为 JSON（美化）
export_to_json(infos, "packages_pretty.json", pretty=True)

# 导出为 JSON（紧凑）
export_to_json(infos, "packages_compact.json", pretty=False)

# 同时导出为 CSV
export_to_csv(infos, "packages.csv")

print("\n✓ 导出完成！")
```

## 读取 JSON 文件

### Python

```python
import json

with open("packages.json") as f:
    data = json.load(f)
    for pkg in data:
        print(f"{pkg['package_name']}: {pkg['package_purl']}")
```

### JavaScript/Node.js

```javascript
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('packages.json', 'utf8'));
data.forEach(pkg => {
    console.log(`${pkg.package_name}: ${pkg.package_purl}`);
});
```

### jq (命令行)

```bash
# 提取所有 PURL
jq '.[].package_purl' packages.json

# 过滤 amd64 架构的包
jq '.[] | select(.architecture == "amd64")' packages.json

# 统计架构分布
jq 'group_by(.architecture) | map({arch: .[0].architecture, count: length})' packages.json
```

## 注意事项

1. **编码**: JSON 文件使用 UTF-8 编码
2. **Null 值**: Python 的 `None` 会转换为 JSON 的 `null`
3. **布尔值**: Python 的 `True/False` 会转换为 JSON 的 `true/false`
4. **文件大小**: 美化输出会增加文件大小，紧凑格式更节省空间
5. **package_purl**: 这个字段是通过 `@property` 计算得出的，已自动包含在导出结果中

## 测试

运行完整测试套件查看 JSON 导出效果：

```bash
python test_complete_suite.py
```

这将生成：
- `test_results_all.json` - 包含 32 个测试用例的完整 JSON 数据
- `test_results_all.csv` - CSV 格式
- `TEST_RESULTS_ALL.md` - 详细测试报告

## API 参考

### `export_to_json(package_infos, output_file, pretty)`

**参数**:
- `package_infos` (list): DebianPackageInfo 对象列表
- `output_file` (str): 输出文件路径，默认 `"debian_packages.json"`
- `pretty` (bool): 是否美化输出，默认 `True`

**返回**: 无

**异常**:
- `IOError`: 文件写入失败
- `TypeError`: 无效的对象类型

**示例**:
```python
export_to_json(infos, "output.json", pretty=True)
```

---

✅ JSON 导出功能已完全测试并可用！

