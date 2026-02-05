# Debian URL Parser - 完整测试报告

**测试时间**: 2026년  2월  5일 목요일 14시 20분 33초 CST

---

## 📊 总体统计

- **测试用例总数**: 32
- **成功**: 32 ✅
- **失败**: 0 ❌
- **成功率**: 100.00%

## ✅ 成功案例

| # | 包名 | 版本 | PURL | 架构 |
|---|------|------|------|------|
| 1 | dpkg | 1.23.3_armhf | pkg:deb/debian/dpkg | armhf |
| 2 | abigail-tools-dbgsym | 2.9-1_amd64 | pkg:deb/debian/abigail-tools-dbgsym | amd64 |
| 3 | abigail-tools-dbgsym | 2.9-1_i386 | pkg:deb/debian/abigail-tools-dbgsym | i386 |
| 4 | nginx | 1.18.0-6.1_amd64 | pkg:deb/debian/nginx | amd64 |
| 5 | nginx | 1.18.0-6.1_i386 | pkg:deb/debian/nginx | i386 |
| 6 | nginx | 1.18.0-6.1_arm64 | pkg:deb/debian/nginx | arm64 |
| 7 | dpkg | 1.23.3_armhf | pkg:deb/debian/dpkg | armhf |
| 8 | openjdk-11-demo | 11.0.29+7-1_s390x | pkg:deb/debian/openjdk-11-demo | s390x |
| 9 | openssl | 1.1.1n-0+deb11u5_amd64 | pkg:deb/debian/openssl | amd64 |
| 10 | package | 1.2.3+dfsg1-2+deb12u1_amd64 | pkg:deb/debian/package | amd64 |
| 11 | nginx | 1.28.0-6 | pkg:deb/debian/nginx | N/A |
| 12 | nginx | 1.28.0 | pkg:deb/debian/nginx | N/A |
| 13 | nginx | 1.28.0 | pkg:deb/debian/nginx | N/A |
| 14 | nginx | 1.28.0-6 | pkg:deb/debian/nginx | N/A |
| 15 | dpkg | 1.23.3 | pkg:deb/debian/dpkg | N/A |
| 16 | dpkg | 1.23.3 | pkg:deb/debian/dpkg | N/A |
| 17 | package | 1.2.3+dfsg1-2+deb12u1_amd64 | pkg:deb/debian/package | amd64 |
| 18 | package | 1.0+really1.0-1_amd64 | pkg:deb/debian/package | amd64 |
| 19 | package | 1.0-1+b2_amd64 | pkg:deb/debian/package | amd64 |
| 20 | package | 2.0-1~bpo11+1_amd64 | pkg:deb/debian/package | amd64 |
| 21 | package | 1.0-1ubuntu1.1_amd64 | pkg:deb/debian/package | amd64 |
| 22 | openjdk-11-jre | 11.0.24+8-1_amd64 | pkg:deb/debian/openjdk-11-jre | amd64 |
| 23 | openjdk-17-jdk | 17.0.12+7-2_amd64 | pkg:deb/debian/openjdk-17-jdk | amd64 |
| 24 | lib-foo-dev | 1.0-1_amd64 | pkg:deb/debian/lib-foo-dev | amd64 |
| 25 | lib.foo | 1.0-1_amd64 | pkg:deb/debian/lib.foo | amd64 |
| 26 | python3.11 | 3.11.2-1_amd64 | pkg:deb/debian/python3.11 | amd64 |
| 27 | linux-image | 2:5.10.0-1_amd64 | pkg:deb/debian/linux-image | amd64 |
| 28 | nodejs | 18.0.0 | pkg:deb/debian/nodejs | N/A |
| 29 | nodejs | 18.0.0 | pkg:deb/debian/nodejs | N/A |
| 30 | package | 1.0~rc1-1_amd64 | pkg:deb/debian/package | amd64 |
| 31 | package | 1.0~beta2-1_amd64 | pkg:deb/debian/package | amd64 |
| 32 | package | 1.0~alpha1-1_amd64 | pkg:deb/debian/package | amd64 |

## 🔗 PURL 统计

- **唯一包数量**: 13
- **PURL 格式验证**: 全部符合 `pkg:deb/debian/<package_name>` 格式 ✅

## 📦 版本特性统计

- **带纪元号**: 1
- **带 Debian 修订号**: 24
- **带 DFSG 标识**: 2
- **带 Really 标识**: 1
- **二进制重制**: 1
- **Backport 版本**: 1
- **安全更新**: 3
- **自研组件**: 4

## 📄 文件类型统计

- **binary**: 24
- **build_file**: 2
- **native_source**: 1
- **upstream_source**: 3
- **upstream_source_patch**: 1
- **upstream_source_sig**: 1

## 🖥️ 架构统计

- **amd64**: 18
- **arm64**: 1
- **armhf**: 2
- **i386**: 2
- **s390x**: 1

## 📁 导出文件

- `test_results_all.csv` - CSV 格式的测试结果
- `test_results_all.json` - JSON 格式的测试结果
- `TEST_RESULTS_ALL.md` - 本测试报告

## 🎯 结论

✅ **所有测试用例全部通过！**

Debian URL Parser 功能正常，可以处理各种类型的 Debian 包 URL。
