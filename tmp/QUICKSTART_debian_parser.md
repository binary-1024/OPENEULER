# Debian URL 解析器 - 快速使用指南

## 📦 项目文件清单

### 核心文件
- `debian_url_parser.py` - 核心解析器库
- `debian_parser_cli.py` - 命令行工具
- `debian_parser_examples.py` - 使用示例代码
- `test_debian_parser.py` - 单元测试

### 文档文件
- `README_debian_parser.md` - 完整使用文档和 API 参考
- `SUMMARY_debian_parser.md` - 项目总结
- `sample_urls.txt` - URL 示例文件

### 相关文档
- `deb_version_parse.md` - Debian 命名规范（基础文档）

## 🚀 快速开始

### 方式一：作为 Python 库使用

```python
from debian_url_parser import DebianURLParser

# 创建解析器
parser = DebianURLParser()

# 解析 URL
url = "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb"
info = parser.parse_url(url)

# 访问解析结果
print(f"组件名: {info.package_name}")
print(f"版本: {info.version}")
print(f"架构: {info.architecture}")
print(f"文件类型: {info.file_type}")
```

### 方式二：使用命令行工具

```bash
# 解析单个 URL
python3 debian_parser_cli.py "https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb"

# 批量解析文件中的 URL
python3 debian_parser_cli.py --file sample_urls.txt

# 输出 JSON 格式
python3 debian_parser_cli.py --json "URL"

# 过滤 amd64 架构的包
python3 debian_parser_cli.py --file urls.txt --filter-arch amd64

# 只显示二进制包
python3 debian_parser_cli.py --file urls.txt --filter-type 二进制
```

## 📋 常用功能示例

### 1. 识别安全更新包

```python
from debian_url_parser import DebianURLParser

parser = DebianURLParser()
url = "https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb"
info = parser.parse_url(url)

if info.security_update:
    print(f"🔐 这是一个安全更新包")
    print(f"   发行版: {info.release_version}")
    print(f"   更新编号: {info.security_update}")
```

### 2. 区分自研和上游组件

```python
info = parser.parse_url(url)

if info.is_native:
    print(f"🏠 Debian 自研组件: {info.package_name}")
else:
    print(f"🌐 上游组件: {info.package_name}")
    print(f"   上游版本: {info.upstream_version}")
    print(f"   Debian 修订: {info.debian_revision}")
```

### 3. 批量处理和过滤

```python
urls = [...]  # URL 列表

# 只获取 amd64 架构的二进制包
amd64_packages = []
for url in urls:
    info = parser.parse_url(url)
    if info.file_type == "二进制" and info.architecture == "amd64":
        amd64_packages.append(info)

print(f"找到 {len(amd64_packages)} 个 amd64 包")
```

### 4. 导出为 JSON

```python
import json

info = parser.parse_url(url)
data = info.to_dict()

# 保存到文件
with open('package_info.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## 🧪 运行测试

```bash
# 运行单元测试（推荐先运行这个确保一切正常）
python3 test_debian_parser.py

# 运行示例代码（查看各种使用场景）
python3 debian_parser_examples.py

# 查看基本测试用例
python3 debian_url_parser.py
```

## 📊 支持的文件类型

| 类型 | 文件扩展名 | 示例 |
|------|-----------|------|
| 二进制包 | `.deb` | `nginx_1.18.0-6.1_amd64.deb` |
| 构建文件 | `.dsc` | `nginx_1.28.0-6.dsc` |
| 上游源码 | `.orig.tar.*` | `nginx_1.28.0.orig.tar.gz` |
| 源码签名 | `.orig.tar.*.asc` | `nginx_1.28.0.orig.tar.gz.asc` |
| Debian 补丁 | `.debian.tar.*` | `nginx_1.28.0-6.debian.tar.xz` |
| 自研源码 | `.tar.*` | `dpkg_1.23.3.tar.xz` |

## 🏗️ 支持的架构

`amd64`, `i386`, `arm64`, `armhf`, `armel`, `ppc64el`, `s390x`, `riscv64`, `mips64el`, `mipsel`, `all`

## 🏷️ 支持的版本标识

- ✅ 纪元号 (epoch): `1:`
- ✅ DFSG 重打包: `+dfsg1`
- ✅ Really 版本: `+really1.0`
- ✅ 二进制重制: `+b2`
- ✅ Backports: `~bpo11+1`
- ✅ NMU 标识: `+nmu1`
- ✅ Ubuntu 标识: `ubuntu1.1`
- ✅ 发行版版本: `deb11`, `deb12`
- ✅ 安全更新: `u1`, `u2`

## 📝 URL 文件格式

创建一个文本文件（如 `urls.txt`），每行一个 URL：

```
# 这是注释行
https://example.com/pool/main/n/nginx/nginx_1.18.0-6.1_amd64.deb
https://example.com/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb

# 空行会被忽略

https://example.com/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb
```

然后使用命令行工具处理：

```bash
python3 debian_parser_cli.py --file urls.txt
```

## 🔍 CLI 工具完整选项

```bash
用法: debian_parser_cli.py [-h] [--file FILE] [--json]
                           [--filter-type TYPE] [--filter-arch ARCH]
                           [url]

选项:
  url                      要解析的 Debian URL
  --file, -f FILE          包含 URL 列表的文件路径
  --json, -j               以 JSON 格式输出
  --filter-type, -t TYPE   按文件类型过滤
  --filter-arch, -a ARCH   按架构过滤
  --help, -h               显示帮助信息
```

## 💡 实用技巧

### 技巧 1: 快速查看包信息

```bash
# 解析并高亮显示关键信息
python3 debian_parser_cli.py "URL"
```

### 技巧 2: 导出为 JSON 供其他工具使用

```bash
# 导出到文件
python3 debian_parser_cli.py --json "URL" > package.json

# 批量导出
python3 debian_parser_cli.py --file urls.txt --json > packages.json
```

### 技巧 3: 过滤特定架构的包

```bash
# 只看 amd64 的包
python3 debian_parser_cli.py --file urls.txt --filter-arch amd64

# 组合过滤：amd64 的二进制包
python3 debian_parser_cli.py --file urls.txt \
  --filter-type 二进制 --filter-arch amd64
```

### 技巧 4: 在脚本中使用

```bash
#!/bin/bash

# 解析多个 URL 并保存
for url in $(cat urls.txt); do
    python3 debian_parser_cli.py --json "$url" >> results.json
done
```

### 技巧 5: Python 脚本集成

```python
#!/usr/bin/env python3
from debian_url_parser import DebianURLParser
import sys

parser = DebianURLParser()

# 从标准输入读取 URL
for line in sys.stdin:
    url = line.strip()
    if url and not url.startswith('#'):
        try:
            info = parser.parse_url(url)
            print(f"{info.package_name},{info.version},{info.architecture}")
        except ValueError:
            continue
```

使用方式：
```bash
cat urls.txt | python3 your_script.py > output.csv
```

## ⚠️ 注意事项

1. **包名规则**: 包名必须以小写字母开头
2. **架构信息**: 只有二进制包（.deb）才有架构信息
3. **自研组件**: 通过是否包含 Debian 修订号来判断
4. **错误处理**: 无效 URL 会抛出 `ValueError`

## 🐛 常见问题

### Q: 如何判断一个包是否是安全更新？

```python
info = parser.parse_url(url)
is_security = info.security_update is not None
```

### Q: 如何获取包的所有源码文件？

对于同一个包，会有多个源码文件：
- `.dsc` - 构建文件
- `.orig.tar.*` - 上游源码
- `.debian.tar.*` - Debian 补丁（如果是上游组件）

```python
# 按包名和版本分组
from collections import defaultdict

sources = defaultdict(list)
for url in urls:
    info = parser.parse_url(url)
    if info.distribution_type == "源码":
        key = (info.package_name, info.version)
        sources[key].append(info)
```

### Q: 如何区分不同架构的同一个包？

```python
packages_by_arch = defaultdict(list)
for url in urls:
    info = parser.parse_url(url)
    if info.architecture:
        packages_by_arch[info.architecture].append(info)

# 获取所有 amd64 的包
amd64_packages = packages_by_arch['amd64']
```

## 📚 更多信息

- 查看 `README_debian_parser.md` 了解完整 API 文档
- 查看 `debian_parser_examples.py` 查看 9 个详细示例
- 查看 `deb_version_parse.md` 了解 Debian 命名规范
- 运行 `test_debian_parser.py` 查看测试用例

## 🎉 开始使用

```bash
# 1. 测试解析器是否正常工作
python3 test_debian_parser.py

# 2. 查看示例代码
python3 debian_parser_examples.py

# 3. 尝试解析一个 URL
python3 debian_parser_cli.py "YOUR_URL_HERE"

# 4. 批量处理
python3 debian_parser_cli.py --file sample_urls.txt
```

祝使用愉快！🚀

