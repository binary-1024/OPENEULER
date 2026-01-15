# 🚀 快速开始 - PURL 和 CSV 导出

## 安装

无需额外安装，直接使用：

```bash
cd /Users/mbpr-m4/WorkSpace/sectrend/openEuler
```

## 基础用法

### 1. 解析单个 URL 并获取 PURL

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()

# 解析 URL
url = "https://example.com/pool/main/o/openjdk-11/openjdk-11-demo_11.0.29+7-1_s390x.deb"
info = parser.parse_url(url)

# 获取信息
print(f"包名: {info.package_name}")           # openjdk-11-demo
print(f"版本: {info.version}")                # 11.0.29+7-1
print(f"PURL: {info.package_purl}")           # pkg:deb/debian/openjdk-11-demo
print(f"架构: {info.architecture}")           # s390x
```

### 2. 批量解析并导出到 CSV

```python
from debian_url_parser import DebianURLParser, export_to_csv

parser = DebianURLParser()

# URL 列表
urls = [
    "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb",
    "https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb",
    "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb",
]

# 解析
package_infos = []
for url in urls:
    info = parser.parse_url(url)
    package_infos.append(info)
    print(f"✓ {info.package_name} -> {info.package_purl}")

# 导出到 CSV
export_to_csv(package_infos, "my_packages.csv")
print("✓ 导出完成！")
```

### 3. 运行示例脚本

```bash
# 运行完整测试
python test_purl_complete.py

# 运行 CSV 导出示例
python example_export_csv.py
```

## PURL 格式说明

**格式**: `pkg:deb/debian/<package_name>`

**示例**:
- `openjdk-11-demo_11.0.29+7-1_s390x.deb` → `pkg:deb/debian/openjdk-11-demo`
- `nginx_1.18.0-6.1_amd64.deb` → `pkg:deb/debian/nginx`
- `dpkg_1.23.3_armhf.deb` → `pkg:deb/debian/dpkg`

## CSV 文件说明

### 包含的字段 (20个)

| 字段 | 说明 | 示例 |
|------|------|------|
| `url` | 原始 URL | https://... |
| `filename` | 文件名 | nginx_1.18.0-6.1_amd64.deb |
| `package_name` | 包名 | nginx |
| **`package_purl`** | **Package URL** | **pkg:deb/debian/nginx** |
| `version` | 完整版本 | 1.18.0-6.1 |
| `architecture` | 架构 | amd64 |
| `upstream_version` | 上游版本 | 1.18.0 |
| `debian_revision` | Debian 修订 | 6.1 |
| ... | 其他字段 | ... |

### 查看 CSV 文件

```bash
# 查看前几行
head debian_packages_output.csv

# 使用 Python
python -c "import csv; [print(row) for row in csv.DictReader(open('debian_packages_output.csv'))]"

# 使用 Excel/LibreOffice 直接打开
```

## 常见用例

### 用例 1: 从文件读取 URL 列表

```python
from debian_url_parser import DebianURLParser, export_to_csv

parser = DebianURLParser()

# 从文件读取 URL
with open('urls.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# 解析所有 URL
package_infos = []
for url in urls:
    try:
        info = parser.parse_url(url)
        package_infos.append(info)
    except ValueError as e:
        print(f"✗ 跳过: {url} - {e}")

# 导出
export_to_csv(package_infos, "packages.csv")
```

### 用例 2: 过滤特定架构

```python
parser = DebianURLParser()

# 只保留 amd64 架构的包
amd64_packages = []
for url in urls:
    info = parser.parse_url(url)
    if info.architecture == "amd64":
        amd64_packages.append(info)

export_to_csv(amd64_packages, "amd64_packages.csv")
```

### 用例 3: 生成软件清单 (SBOM)

```python
parser = DebianURLParser()

# 解析并生成 SBOM
sbom = []
for url in urls:
    info = parser.parse_url(url)
    sbom.append({
        "purl": info.package_purl,
        "name": info.package_name,
        "version": info.version,
        "type": "deb"
    })

# 导出为 JSON
import json
with open('sbom.json', 'w') as f:
    json.dump(sbom, f, indent=2)
```

## 支持的文件类型

✅ 二进制包 (`.deb`)
✅ 构建文件 (`.dsc`)
✅ 上游源码 (`.orig.tar.*`)
✅ 源码签名 (`.orig.tar.*.asc`)
✅ Debian 补丁 (`.debian.tar.*`)
✅ 自研源码 (`.tar.*`)

## 测试

### 运行所有测试

```bash
# PURL 完整测试
python test_purl_complete.py

# CSV 导出测试
python example_export_csv.py
```

### 预期输出

```
🎉 所有测试通过！PURL 功能正常工作。
✓ 已导出 16 条记录到 debian_packages_output.csv
```

## 文档

- 📘 [完整使用指南](PURL_CSV_GUIDE.md)
- 📊 [测试报告](TEST_REPORT_PURL_CSV.md)
- 💡 [示例脚本](example_export_csv.py)

## 问题排查

### Q: 无法解析某个 URL
**A**: 检查 URL 格式是否正确，文件名是否符合 Debian 包命名规范

### Q: CSV 文件乱码
**A**: 使用 UTF-8 编码打开文件

### Q: PURL 格式是否正确
**A**: PURL 格式为 `pkg:deb/debian/<package_name>`，不包含版本号和架构

## 更多帮助

查看完整文档：
```bash
python -c "from debian_url_parser import DebianURLParser; help(DebianURLParser)"
```

---

✅ 功能已完全测试并可用！

