Debian 组件分类
- 【重要】要区分源码文件和二进制制品文件！
- 【重要】Debian 组件分为自研组件和上游二开组件
- 【重要】Deiban 生态不会直接二开上游组件而是采取构建的时候打补丁的方式
Debian 上游二开组件详细说明示例
https://snapshot.debian.org/package/libabigail/2.9-1/
1.1.1 Source files
[图片]
  这里面包括了如下三类文件；
  1. 上游源码：.orig.tar.xz
  2. 修复&补丁：.debian.tar.xz
  3. 构建文件dsc：.dsc
1.1.2 Binary packages
  二进制则会分为更细粒度的，一般来说会把一份源码变成多个不同细分功能的二进制，例如：
暂时无法在飞书文档外展示此内容
  针对每个二进制都会生成各自不同架构的制品包（除了 doc 文档之外），例如：
[图片]
- amd64
https://snapshot.debian.org/archive/debian-debug/20251114T210651Z/pool/main/liba/libabigail/abigail-tools-dbgsym_2.9-1_amd64.deb
- i386
https://snapshot.debian.org/archive/debian-debug/20251114T210651Z/pool/main/liba/libabigail/abigail-tools-dbgsym_2.9-1_i386.deb
Debian 自研组件详细说明实例
https://snapshot.debian.org/package/dpkg/1.23.3/
自研组件你会发现没有修订号哦！！！
1.1.3 Source files
[图片]
这里面你会发现只包括了如下两类文件；
1. 自研组件源码：.tar.xz
2. 构建文件dsc：.dsc
1.1.4 Binary packages
[图片]
- https://snapshot.debian.org/archive/debian/20251220T083035Z/pool/main/d/dpkg/dpkg_1.23.3_armhf.deb
- https://snapshot.debian.org/archive/debian-ports/20251220T075702Z/pool-hurd-amd64/main/d/dpkg/dpkg_1.23.3_hurd-amd64.deb

---
二进制制品包命名规范
制品包格式也分成两种类型：通用格式与安全更新格式。但是记得考虑到自研组件和上游二开组件的区别。
通用格式
<package-name>_<epoch>:<upstream-version>-<debian-revision>_<architecture>.deb
<软件包名称>_<纪元号>:<上游版本号>-<修订号>_<架构>.deb

    nginx_1.18.0-6.1_amd64.deb
├─────┼────────┼───┼─────┘
   │       │      │      │
   │       │      │      └── 架构标识
   │       │      └───────── Debian 修订版本
   │       └──────────────── 上游版本号
   └─────────────────────── 包名

例如：
abigail-tools-dbgsym_2.9-1_i386.deb

安全更新包格式
<package-name>_<epoch>:<upstream-version>-<debian-revision><发行版本号>u<security-update-number>_<architecture>.deb
<软件包名称>_<纪元号>:<上游版本号>-<debian 修订号><发行版本号>u<安全更新编号>_<架构>.deb

openssl_1.1.1n-0+deb11u5_amd64.deb
├──────┼─────────┼─┼─┼──┼─┼─────┘
   │        │      │ │  │ │    │
   │        │      │ │  │ │    └── 架构
   │        │      │ │  │ └─────── 安全更新编号 (第5次)
   │        │      │ │  └───────── Debian 版本代号 (11 = bullseye)
   │        │      │ └──────────── 安全更新标识符
   │        │      └────────────── Debian 修订版本
   │        └───────────────────── 上游版本号
   └────────────────────────────── 包名
1. 【必选】软件包名称：
  - 允许字符：小写字母 (a-z)、数字 (0-9)、加号 (+)、连字符 (-)、点号 (.)
  - 首字符：必须是字母 (a-z)
  - 禁止字符：大写字母、下划线、空格等特殊字符
    Ps: 那就是说，一般如果是这个包相关的其他二进制或者别的工具包，都会用- 来连接
  - 终止符：下划线 _
    PS: 第一个下划线一定是软件名称后面的下划线
python3-requests    # 语言前缀 + 包名
libxml2-dev         # 库包开发文件
nginx-extras        # 主包的扩展功能
gcc-10-arm-linux-gnueabihf  # 交叉编译工具链
2. 【必选】上游版本号：
  Dpkg对上游版本号的硬性语法规则本身是 [A-Za-z0-9.+~:]
  - Debian 不会强行要求上游版本号的规范，但是大多数都会遵从 semver
  - 如果上游版本号存在预发布版本，使用了中划线下划线等，则 debian 会将其连接符转成波浪号
  综合下来是只使用数字，字母，点号，波浪号, 加号
1.0~rc1
  - 终止符：中划线-作为连接符，连接了上游版本号与修订号
  - 【可选】纪元号（Epoch）:
    - 作用与场景：当原有的版本号体系出现一些无法比较的情况，需要通过增加 epoch 来开启一个新的维度，否则无法基于原有的版本来进行比较。所以用 epoch 这个词，代表开启一个新纪元，“重新开始”，比较场景场景有：
      - 上游版本号格式发生变更 从 20251122 -> 1.0.0 这种就加一个 epoch 让 1:1.0.0 大于 20251122
      - 修复一个错误发布的版本号，比如 1.0.1 -> 2.0.1  这个 2.0.1 是错误的版本号，那我要发布一个更新一些的，就让他等于 1:1.1.0 这样 1:1.1.0 就大于 2.0.1 了
      - 反正新纪元的目的就是开启一个全新的比较维度
    - 终止符：冒号:，如果存在纪元号那就用冒号连接纪元号和上游版本号
  - 【可选】DFSG（Debian Free Software Guidelines）开源？免费？自由？软件指南
    - 冒号:我们知道了，这个是用于连接纪元号的，那加号+是什么？为什么还有加号？
      加号是用于连接重打包标识 dfsg 的。 例如：1.2.3+dfsg1-2+deb12u1
      这里上游版本号是 1.2.3-2 但是，由于存在一些不能开源的内容，debian 会移除这部分内容后重新打包。
    - 作用：如果上游软件包含不能免费开源的内容，比如包含专利的编码格式的媒体文件，文档，字体，算法，debian 会移除这些内容之后重新打包，dfsg1 代表第一次重新打包，dfsg2代表第二次重新打包
    - 连接符是加号➕，如果存在 dsfg 那么就在 上游版本号后面加+dsfg
  - 【可选】真正版本标识：加号+really+真正上游版本号
    如果当前已经有了一个错误的版本 2.0.0-1_amd64.deb 但是实际上，上游版本号是 1.0.0。 并且客户已经安装了这个错误版本，那我想纠正一下发布一个1.0.0-1_amd64.deb 不行，因为 dpkg 不给你降级。只有我发布一个package_1.0.0+really1.0.0-1_amd64.deb 这样才可以安装
    这个时候 dpkg 会认为 这个版本大于 2.0.0，后续版本也要一直+really 下去，直到版本号大于2.0.0
    位置：+really会放在上游版本号的后面，紧跟上游版本号，然后其他后缀前面比如 dfsg 这种.
package_1.0.0+really1.0.0+dfsg1
package_1.0+really1.0-1_amd64.deb
package_2.0+really1.5-1_amd64.deb
package_1.5+really1.5+is+not+2.0-1_amd64.deb
# 非常明确地说明:这不是 2.0,而是 1.5
package_2.0+really2.0+dfsg-1_amd64.deb
package_2.0+really2.0+git20231215-1_amd64.deb
  - 【可选】还有~预发布版本，+git 快照版本，+svn 快照版本，+hg 快照版本，+ds（debian source），+repack（重打包），+upstream（上游变体？），+vendor<name>（供应商）, +exp<n>（实验性版本）,
    优先级顺序 (从低到高):
    1. ~ 预发布后缀 (最低)
    2. 基础版本
    3. +really, +git, +dfsg, +ds, +repack 等 (都比基础版本高)
3. 【可选】debian 修订号：修订号用于标识 debian 做的修改和更新
  - 修订号是semver，从 0 开始递增，0 代表直接使用上游版本
  - 场景 1：原生 debian 包 （debian 自研）自研的包，不会包含修订号
dpkg_1.21.22_amd64.deb          # dpkg 本身就是 Debian 的工具
apt_2.6.1_amd64.deb             # apt 也是 Debian 原创
debhelper_13.11.4_all.deb       # Debian 打包工具
base-files_12.4_amd64.deb       # Debian 基础文件
  - 场景 2：非原生包（上游软件）
    上游软件因为要做区分所以必须包含修订号
nginx_1.18.0-6.1_amd64.deb
python3.11_3.11.2-6_amd64.deb
gcc-12_12.2.0-14_amd64.deb
4. 【可选】其他编号：
  其他编号的位置一定是修订号之后, 一定是在架构号的前面
  - +b<number>( 二进制重制编号)
package_1.0-1+b2_amd64.deb
  - ~bpo<ver>+<n> (backports) - 反向移植
package_2.0-1~bpo11+1_amd64.deb

bpo11里的 11 指的是要移植到 debian11
  - +nmu<n> (Non-Maintainer Upload ) - 非维护着上传
package_1.0-1+nmu1_amd64.deb
  - Ubuntu 衍生版本： ubuntu + semver
 package_1.0-1ubuntu1.1_amd64.deb (Ubuntu 的安全更新)
5. 【可选】发行版本号：连接符 + deb + deb 发行版本号
  - 连接符： + | - | ~
  - 发行版本号：例如 11 代表 debian 11 (Bullseye）, 12代表 debian 12 (Bookworm)
    例如 +deb12u1 或者 -deb12u1 或者 ~deb12u1
  - 为什么带着
6. 【可选】安全更新编号：连接符 + 安全更新序号
  - 连接符：u
  - 安全更新序号：如果是第一次安全修复更新 那么就是 1， 如果是第二次更新那就是 2
  - 示例：u1, u2
7. 【必选】架构：连接符+架构号
  - 连接符：下划线_
  - 架构号：
架构
说明
示例
all
架构无关包
nginx-doc_1.18.0-6.1_all.deb
amd64
64位x86
nginx_1.18.0-6.1_amd64.deb
i386
32位x86
nginx_1.18.0-6.1_i386.deb
arm64
64位ARM
nginx_1.18.0-6.1_arm64.deb
armhf
ARM硬浮点
nginx_1.18.0-6.1_armhf.deb
ppc64el
PowerPC 64位小端
nginx_1.18.0-6.1_ppc64el.deb
s390x
IBM System z
nginx_1.18.0-6.1_s390x.deb
armel
老 ARM 32 位架构，无硬件浮点
vlc_3.0.22-0+deb13u1_armel.deb
riscv64
64 位 RISC-V
vlc_3.0.22-0+deb13u1_riscv64.deb
mips64el
 基于 MIPS 指令集的 64 位、小端字节序架构（Little-Endian）
vlc_3.0.22-0+deb12u1_mips64el.deb
mipsel
基于 MIPS 指令集的 32 位、小端字节序架构
vlc_3.0.22-0+deb12u1_mipsel.deb
- 解惑：为什么有一个通用命名规范以及包含发行版本号安全更新号的两套规范呢
  - 同一个组件版本会被多个发行版复用，如果你不做多余的修改他们是同一个东西
  - 只有那些在不同的发行版做过特殊修订，补丁的那些才会增加发行版标识以及安全补丁标识来区分不同
源码包命名规范
<package-name>_<upstream-version>-<debian-revision>.<type>.<extention>

主要包括三种文件：
<package-name>_<upstream-version>-<debian-revision>.dsc 构建文件
<package-name>_<upstream-version>.orig.tar.gz 上游源码
<package-name>_<upstream-version>-<debian-revision>.debian.tar.xz 补丁patch文件

示例：
nginx_1.28.0-6.dsc
nginx_1.28.0.orig.tar.gz
nginx_1.28.0.orig.tar.gz.asc
nginx_1.28.0-6.debian.tar.xz
- 软件包名同二进制一样
- 上游版本号同二进制一样
- Deb 修订号同二进制一样
- 【可选】Type 文件类型：orig | debian
  - orig: 上游软件源码
  - debian：debian 自己做的修订补丁（可能包含多个，在构建的时候按照顺序 patch 进去）
  - 如果是 debian 自研组件则没有这个 type
- 后缀文件名：dsc | tar.gz | tar.xz
  - dsc: 构建文件，里面声明了如何打补丁的顺序与命令等
  - tar.gz: 上游源码包压缩文件
  - tar.xz: 补丁包的压缩文件