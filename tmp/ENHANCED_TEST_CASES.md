# Debian URL Parser - 增强测试用例文档

## 概述
本文档包含更加丰富和全面的测试用例，覆盖各种极端情况和复杂组合。

## 测试分类

### A. 基础测试用例

#### A1. 简单二进制包
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_amd64.deb
预期结果:
  - package_name: apache2
  - version: 2.4.54-1
  - epoch: null
  - upstream_version: 2.4.54
  - debian_revision: 1
  - architecture: amd64
  - distribution_type: binary
  - file_type: binary
```

#### A2. 简单源码包（DSC）
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.dsc
预期结果:
  - package_name: apache2
  - version: 2.4.54-1
  - upstream_version: 2.4.54
  - debian_revision: 1
  - distribution_type: source
  - file_type: build_file
```

#### A3. 原始上游源码
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.gz
预期结果:
  - package_name: apache2
  - version: 2.4.54
  - upstream_version: 2.4.54
  - debian_revision: null
  - distribution_type: source
  - file_type: upstream_source
```

#### A4. Debian 补丁包
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.debian.tar.xz
预期结果:
  - package_name: apache2
  - version: 2.4.54-1
  - upstream_version: 2.4.54
  - debian_revision: 1
  - distribution_type: source
  - file_type: upstream_source_patch
```

#### A5. Native 包
```
URL: http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.tar.xz
预期结果:
  - package_name: dpkg
  - version: 1.20.9
  - upstream_version: 1.20.9
  - debian_revision: null
  - distribution_type: source
  - file_type: native_source
```

### B. 纪元号（Epoch）测试

#### B1. 带纪元的二进制包
```
URL: http://deb.debian.org/debian/pool/main/o/openjdk-11/openjdk-11-jdk_11.0.16+8-1_amd64.deb
预期结果:
  - package_name: openjdk-11-jdk
  - version: 11.0.16+8-1
  - epoch: null
  - upstream_version: 11.0.16
  - debian_revision: 1
```

#### B2. 高纪元号
```
URL: http://deb.debian.org/debian/pool/main/p/perl/perl_5.32.1-4_amd64.deb
预期结果:
  - package_name: perl
  - version: 5.32.1-4
  - epoch: null
  - upstream_version: 5.32.1
  - debian_revision: 4
```

### C. 预发布版本测试

#### C1. Alpha 版本
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image-5.18~rc1_5.18~rc1-1~exp1_amd64.deb
预期结果:
  - package_name: linux-image-5.18~rc1
  - version: 5.18~rc1-1~exp1
  - upstream_version: 5.18~rc1
  - debian_revision: 1
  - is_prerelease: true
```

#### C2. Beta 版本
```
URL: http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0~b8-1_amd64.deb
预期结果:
  - package_name: firefox
  - version: 91.0~b8-1
  - upstream_version: 91.0~b8
  - debian_revision: 1
  - is_prerelease: true
```

#### C3. RC 版本
```
URL: http://deb.debian.org/debian/pool/main/g/gcc-12/gcc-12_12.0~rc2-1_amd64.deb
预期结果:
  - package_name: gcc-12
  - version: 12.0~rc2-1
  - upstream_version: 12.0~rc2
  - debian_revision: 1
  - is_prerelease: true
```

#### C4. Git 快照版本
```
URL: http://deb.debian.org/debian/pool/main/g/glibc/libc6_2.33~git20210701-1_amd64.deb
预期结果:
  - package_name: libc6
  - version: 2.33~git20210701-1
  - upstream_version: 2.33~git20210701
  - debian_revision: 1
  - is_prerelease: true
```

### D. DFSG 版本测试

#### D1. 单个 DFSG 标记
```
URL: http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1_amd64.deb
预期结果:
  - package_name: firefox
  - version: 91.0+dfsg-1
  - upstream_version: 91.0
  - debian_revision: 1
  - is_dfsg: true
  - dfsg_version: null
```

#### D2. 带版本号的 DFSG
```
URL: http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg2-1_amd64.deb
预期结果:
  - package_name: firefox
  - version: 91.0+dfsg2-1
  - upstream_version: 91.0
  - debian_revision: 1
  - is_dfsg: true
  - dfsg_version: 2
```

#### D3. DFSG + 预发布
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc1+dfsg-1_amd64.deb
预期结果:
  - package_name: linux-image
  - version: 5.10~rc1+dfsg-1
  - upstream_version: 5.10~rc1
  - debian_revision: 1
  - is_dfsg: true
  - is_prerelease: true
```

### E. Really 版本测试

#### E1. Really 降级
```
URL: http://deb.debian.org/debian/pool/main/s/systemd/systemd_247+really246-1_amd64.deb
预期结果:
  - package_name: systemd
  - version: 247+really246-1
  - upstream_version: 247
  - debian_revision: 1
  - is_really: true
  - really_version: 246
```

#### E2. Really + DFSG
```
URL: http://deb.debian.org/debian/pool/main/o/openjdk/openjdk-11_11.0.15+really11.0.14+dfsg-1_amd64.deb
预期结果:
  - package_name: openjdk-11
  - version: 11.0.15+really11.0.14+dfsg-1
  - upstream_version: 11.0.15
  - debian_revision: 1
  - is_really: true
  - really_version: 11.0.14
  - is_dfsg: true
```

### F. 二进制重制（Binary Rebuild）测试

#### F1. 基础二进制重制
```
URL: http://deb.debian.org/debian/pool/main/g/glibc/libc6_2.31-13+b2_amd64.deb
预期结果:
  - package_name: libc6
  - version: 2.31-13+b2
  - upstream_version: 2.31
  - debian_revision: 13
  - is_binary_rebuild: true
  - binary_rebuild_version: 2
```

#### F2. 多次二进制重制
```
URL: http://deb.debian.org/debian/pool/main/p/python3.9/python3.9_3.9.2-1+b15_amd64.deb
预期结果:
  - package_name: python3.9
  - version: 3.9.2-1+b15
  - upstream_version: 3.9.2
  - debian_revision: 1
  - is_binary_rebuild: true
  - binary_rebuild_version: 15
```

### G. Backports 测试

#### G1. Bullseye Backports
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.16.0-1~bpo11+1_amd64.deb
预期结果:
  - package_name: linux-image
  - version: 5.16.0-1~bpo11+1
  - upstream_version: 5.16.0
  - debian_revision: 1
  - is_backport: true
  - backport_release: 11
  - backport_version: 1
```

#### G2. Buster Backports
```
URL: http://deb.debian.org/debian/pool/main/d/docker.io/docker.io_20.10.5+dfsg1-1~bpo10+1_amd64.deb
预期结果:
  - package_name: docker.io
  - version: 20.10.5+dfsg1-1~bpo10+1
  - upstream_version: 20.10.5
  - debian_revision: 1
  - is_dfsg: true
  - dfsg_version: 1
  - is_backport: true
  - backport_release: 10
  - backport_version: 1
```

### H. NMU (非维护者上传) 测试

#### H1. 基础 NMU
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.46-4+nmu1_amd64.deb
预期结果:
  - package_name: apache2
  - version: 2.4.46-4+nmu1
  - upstream_version: 2.4.46
  - debian_revision: 4
  - is_nmu: true
  - nmu_version: 1
```

#### H2. 多次 NMU
```
URL: http://deb.debian.org/debian/pool/main/b/bind9/bind9_9.16.15-1+nmu3_amd64.deb
预期结果:
  - package_name: bind9
  - version: 9.16.15-1+nmu3
  - upstream_version: 9.16.15
  - debian_revision: 1
  - is_nmu: true
  - nmu_version: 3
```

### I. Ubuntu 版本测试

#### I1. Ubuntu 基础版本
```
URL: http://archive.ubuntu.com/ubuntu/pool/main/a/apache2/apache2_2.4.41-4ubuntu3_amd64.deb
预期结果:
  - package_name: apache2
  - version: 2.4.41-4ubuntu3
  - upstream_version: 2.4.41
  - debian_revision: 4
  - is_ubuntu: true
  - ubuntu_version: 3
```

#### I2. Ubuntu + 安全更新
```
URL: http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/openssl_1.1.1f-1ubuntu2.16_amd64.deb
预期结果:
  - package_name: openssl
  - version: 1.1.1f-1ubuntu2.16
  - upstream_version: 1.1.1f
  - debian_revision: 1
  - is_ubuntu: true
  - ubuntu_version: 2.16
```

### J. 发行版版本测试

#### J1. Debian 11 (Bullseye)
```
URL: http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u3_amd64.deb
预期结果:
  - package_name: openssl
  - version: 1.1.1n-0+deb11u3
  - upstream_version: 1.1.1n
  - debian_revision: 0
  - release_version: 11
  - security_update: 3
```

#### J2. Debian 10 (Buster)
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_4.19.208-1+deb10u1_amd64.deb
预期结果:
  - package_name: linux-image
  - version: 4.19.208-1+deb10u1
  - upstream_version: 4.19.208
  - debian_revision: 1
  - release_version: 10
  - security_update: 1
```

#### J3. Debian 9 (Stretch)
```
URL: http://deb.debian.org/debian/pool/main/o/openssh/openssh_7.4p1-10+deb9u7_amd64.deb
预期结果:
  - package_name: openssh
  - version: 7.4p1-10+deb9u7
  - upstream_version: 7.4p1
  - debian_revision: 10
  - release_version: 9
  - security_update: 7
```

### K. 复杂组合测试

#### K1. 纪元 + DFSG + 修订号
```
URL: http://deb.debian.org/debian/pool/main/o/openjdk-11/openjdk-11-jdk_11.0.16+8+dfsg-1_amd64.deb
预期结果:
  - package_name: openjdk-11-jdk
  - version: 11.0.16+8+dfsg-1
  - upstream_version: 11.0.16
  - debian_revision: 1
  - is_dfsg: true
```

#### K2. 预发布 + DFSG + 二进制重制
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc1+dfsg-1+b2_amd64.deb
预期结果:
  - package_name: linux-image
  - version: 5.10~rc1+dfsg-1+b2
  - upstream_version: 5.10~rc1
  - debian_revision: 1
  - is_prerelease: true
  - is_dfsg: true
  - is_binary_rebuild: true
  - binary_rebuild_version: 2
```

#### K3. Really + DFSG + Backports
```
URL: http://deb.debian.org/debian/pool/main/o/openjdk/openjdk-11_11.0.15+really11.0.14+dfsg-1~bpo11+1_amd64.deb
预期结果:
  - package_name: openjdk-11
  - version: 11.0.15+really11.0.14+dfsg-1~bpo11+1
  - upstream_version: 11.0.15
  - debian_revision: 1
  - is_really: true
  - really_version: 11.0.14
  - is_dfsg: true
  - is_backport: true
  - backport_release: 11
  - backport_version: 1
```

#### K4. 发行版 + 安全更新 + 二进制重制
```
URL: http://deb.debian.org/debian/pool/main/g/glibc/libc6_2.31-13+deb11u5+b2_amd64.deb
预期结果:
  - package_name: libc6
  - version: 2.31-13+deb11u5+b2
  - upstream_version: 2.31
  - debian_revision: 13
  - release_version: 11
  - security_update: 5
  - is_binary_rebuild: true
  - binary_rebuild_version: 2
```

#### K5. DFSG + NMU + 发行版
```
URL: http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1+nmu1+deb11u2_amd64.deb
预期结果:
  - package_name: firefox
  - version: 91.0+dfsg-1+nmu1+deb11u2
  - upstream_version: 91.0
  - debian_revision: 1
  - is_dfsg: true
  - is_nmu: true
  - nmu_version: 1
  - release_version: 11
  - security_update: 2
```

#### K6. 预发布 + Really + DFSG + Backports + NMU
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc2+really5.9+dfsg-1+nmu1~bpo10+1_amd64.deb
预期结果:
  - package_name: linux-image
  - version: 5.10~rc2+really5.9+dfsg-1+nmu1~bpo10+1
  - upstream_version: 5.10~rc2
  - debian_revision: 1
  - is_prerelease: true
  - is_really: true
  - really_version: 5.9
  - is_dfsg: true
  - is_nmu: true
  - nmu_version: 1
  - is_backport: true
  - backport_release: 10
  - backport_version: 1
```

### L. 边缘情况测试

#### L1. 无修订号的包
```
URL: http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.tar.xz
预期结果:
  - package_name: dpkg
  - version: 1.20.9
  - upstream_version: 1.20.9
  - debian_revision: null
```

#### L2. 修订号为 0
```
URL: http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u3_amd64.deb
预期结果:
  - package_name: openssl
  - version: 1.1.1n-0+deb11u3
  - upstream_version: 1.1.1n
  - debian_revision: 0
```

#### L3. 长修订号
```
URL: http://deb.debian.org/debian/pool/main/g/gcc/gcc_10.2.1-6.2.1_amd64.deb
预期结果:
  - package_name: gcc
  - version: 10.2.1-6.2.1
  - upstream_version: 10.2.1
  - debian_revision: 6.2.1
```

#### L4. 包名含多个连字符
```
URL: http://deb.debian.org/debian/pool/main/l/linux-signed-amd64/linux-image-5.10.0-13-amd64_5.10.106-1_amd64.deb
预期结果:
  - package_name: linux-image-5.10.0-13-amd64
  - version: 5.10.106-1
  - upstream_version: 5.10.106
  - debian_revision: 1
```

#### L5. 版本号含字母
```
URL: http://deb.debian.org/debian/pool/main/o/openssh/openssh_7.4p1-10_amd64.deb
预期结果:
  - package_name: openssh
  - version: 7.4p1-10
  - upstream_version: 7.4p1
  - debian_revision: 10
```

#### L6. 多段版本号
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10.120.1-1_amd64.deb
预期结果:
  - package_name: linux-image
  - version: 5.10.120.1-1
  - upstream_version: 5.10.120.1
  - debian_revision: 1
```

#### L7. 极短版本号
```
URL: http://deb.debian.org/debian/pool/main/a/apt/apt_2.0-1_amd64.deb
预期结果:
  - package_name: apt
  - version: 2.0-1
  - upstream_version: 2.0
  - debian_revision: 1
```

#### L8. 极长上游版本号
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10.120.1.2.3.4-1_amd64.deb
预期结果:
  - package_name: linux-image
  - version: 5.10.120.1.2.3.4-1
  - upstream_version: 5.10.120.1.2.3.4
  - debian_revision: 1
```

### M. 不同架构测试

#### M1. i386 架构
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_i386.deb
预期结果:
  - architecture: i386
```

#### M2. arm64 架构
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_arm64.deb
预期结果:
  - architecture: arm64
```

#### M3. armhf 架构
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1_armhf.deb
预期结果:
  - architecture: armhf
```

#### M4. all 架构
```
URL: http://deb.debian.org/debian/pool/main/p/python-pip/python3-pip_20.3.4-4_all.deb
预期结果:
  - architecture: all
```

#### M5. ppc64el 架构
```
URL: http://deb.debian.org/debian/pool/main/g/gcc/gcc_10.2.1-6_ppc64el.deb
预期结果:
  - architecture: ppc64el
```

### N. 不同文件格式测试

#### N1. tar.gz 格式
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.gz
预期结果:
  - file_type: upstream_source
```

#### N2. tar.xz 格式
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.debian.tar.xz
预期结果:
  - file_type: upstream_source_patch
```

#### N3. tar.bz2 格式
```
URL: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.bz2
预期结果:
  - file_type: upstream_source
```

#### N4. 多个 orig 压缩包
```
URL: http://deb.debian.org/debian/pool/main/w/webkit2gtk/webkit2gtk_2.36.0.orig-jsc.tar.xz
预期结果:
  - file_type: upstream_source
```

### O. 特殊字符测试

#### O1. 包名含点号
```
URL: http://deb.debian.org/debian/pool/main/p/python3.9/python3.9_3.9.2-1_amd64.deb
预期结果:
  - package_name: python3.9
```

#### O2. 包名含加号
```
URL: http://deb.debian.org/debian/pool/main/g/g++/g++_10.2.1-6_amd64.deb
预期结果:
  - package_name: g++
```

#### O3. 版本号含波浪号和加号
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image_5.10~rc1+git20210101-1_amd64.deb
预期结果:
  - version: 5.10~rc1+git20210101-1
  - upstream_version: 5.10~rc1
```

### P. 真实世界的复杂案例

#### P1. Linux 内核（完整版本）
```
URL: http://deb.debian.org/debian/pool/main/l/linux/linux-image-5.10.0-13-amd64_5.10.106-1+deb11u2_amd64.deb
预期结果:
  - package_name: linux-image-5.10.0-13-amd64
  - version: 5.10.106-1+deb11u2
  - upstream_version: 5.10.106
  - debian_revision: 1
  - release_version: 11
  - security_update: 2
```

#### P2. OpenJDK（多重版本标记）
```
URL: http://deb.debian.org/debian/pool/main/o/openjdk-17/openjdk-17-jdk_17.0.3+7-1_amd64.deb
预期结果:
  - package_name: openjdk-17-jdk
  - version: 17.0.3+7-1
  - upstream_version: 17.0.3
  - debian_revision: 1
```

#### P3. Chromium（DFSG + 发行版）
```
URL: http://deb.debian.org/debian/pool/main/c/chromium/chromium_101.0.4951.64-1+deb11u1+dfsg-1_amd64.deb
预期结果:
  - package_name: chromium
  - version: 101.0.4951.64-1+deb11u1+dfsg-1
  - upstream_version: 101.0.4951.64
  - debian_revision: 1
  - is_dfsg: true
  - release_version: 11
  - security_update: 1
```

#### P4. Systemd（复杂修订）
```
URL: http://deb.debian.org/debian/pool/main/s/systemd/systemd_247.3-7+deb11u1_amd64.deb
预期结果:
  - package_name: systemd
  - version: 247.3-7+deb11u1
  - upstream_version: 247.3
  - debian_revision: 7
  - release_version: 11
  - security_update: 1
```

#### P5. GCC（多段修订号）
```
URL: http://deb.debian.org/debian/pool/main/g/gcc-10/gcc-10_10.2.1-6.2_amd64.deb
预期结果:
  - package_name: gcc-10
  - version: 10.2.1-6.2
  - upstream_version: 10.2.1
  - debian_revision: 6.2
```

### Q. 源码包完整测试

#### Q1. 完整源码包集（DSC + orig + debian）
```
DSC: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.dsc
ORIG: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54.orig.tar.gz
DEBIAN: http://deb.debian.org/debian/pool/main/a/apache2/apache2_2.4.54-1.debian.tar.xz
```

#### Q2. DFSG 源码包集
```
DSC: http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1.dsc
ORIG: http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg.orig.tar.xz
DEBIAN: http://deb.debian.org/debian/pool/main/f/firefox/firefox_91.0+dfsg-1.debian.tar.xz
```

#### Q3. Native 包（无 debian 补丁）
```
DSC: http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.dsc
TAR: http://deb.debian.org/debian/pool/main/d/dpkg/dpkg_1.20.9.tar.xz
```

### R. 安全更新专项测试

#### R1. 单次安全更新
```
URL: http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u1_amd64.deb
预期结果:
  - security_update: 1
```

#### R2. 多次安全更新
```
URL: http://deb.debian.org/debian/pool/main/o/openssl/openssl_1.1.1n-0+deb11u5_amd64.deb
预期结果:
  - security_update: 5
```

#### R3. 10+ 次安全更新
```
URL: http://deb.debian.org/debian/pool/main/o/openssh/openssh_7.4p1-10+deb9u12_amd64.deb
预期结果:
  - security_update: 12
```

### S. 版本比较测试用例

#### S1. 简单版本比较
```
2.4.54 > 2.4.53
2.4.54 > 2.4
2.4.54 < 2.5
```

#### S2. 预发布版本比较
```
2.0~rc1 < 2.0
2.0~beta1 < 2.0~rc1
2.0~alpha1 < 2.0~beta1
```

#### S3. 纪元版本比较
```
2:2.0 > 1:2.1
1:2.0 > 2.0
```

#### S4. 修订号比较
```
2.0-2 > 2.0-1
2.0-1.2 > 2.0-1.1
2.0-1ubuntu2 > 2.0-1ubuntu1
```

## 测试统计

- **基础测试**: 5 个
- **纪元号测试**: 2 个
- **预发布版本测试**: 4 个
- **DFSG 测试**: 3 个
- **Really 测试**: 2 个
- **二进制重制测试**: 2 个
- **Backports 测试**: 2 个
- **NMU 测试**: 2 个
- **Ubuntu 版本测试**: 2 个
- **发行版版本测试**: 3 个
- **复杂组合测试**: 6 个
- **边缘情况测试**: 8 个
- **不同架构测试**: 5 个
- **不同文件格式测试**: 4 个
- **特殊字符测试**: 3 个
- **真实世界案例**: 5 个
- **源码包完整测试**: 3 个
- **安全更新专项测试**: 3 个
- **版本比较测试**: 4 个

**总计**: 68+ 个测试用例

