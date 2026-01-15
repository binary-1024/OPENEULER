# Debian 版本比较算法详解

## 一、版本号结构

```
[epoch:]upstream_version[-debian_revision]
```

比较顺序：
1. 先比较 epoch（纪元号）
2. 再比较 upstream_version（上游版本）
3. 最后比较 debian_revision（Debian修订号）

---

## 二、核心比较规则

### 2.1 Epoch（纪元号）比较
- **纯数值比较**
- 缺省视为 0
- epoch 大的版本一定更新

```
示例：
2:1.0    >  1:9.99.99  >  0:999.0  =  999.0
(epoch优先级最高，无视后面的版本号)
```

---

### 2.2 版本字符串比较算法

对 upstream_version 和 debian_revision 使用**相同的算法**：

#### 步骤 1：字符串分段
将版本号分解为**数字段**和**非数字段**交替的序列

```
示例：
"1.2.3"    → ["", "1", ".", "2", ".", "3"]
"1alpha2"  → ["", "1", "alpha", "2"]
"1.2~rc3"  → ["", "1", ".", "2", "~rc", "3"]
```

#### 步骤 2：逐段比较
从左到右依次比较每一段

---

### 2.3 字符优先级规则

```
优先级（从低到高）：
~  <  (空)  <  字母  <  其他符号  <  数字
```

#### 特殊字符优先级表：

| 字符 | ASCII值 | 优先级 | 说明 |
|------|---------|--------|------|
| ~ (波浪号) | 126 | **最低** | 专门用于预发布版本 |
| (空字符串) | - | 第二低 | 无内容 |
| A-Z, a-z | 65-90, 97-122 | 中等 | 按字典序 |
| + (加号) | 43 | 较高 | 其他符号按ASCII |
| - (减号) | 45 | 较高 | 其他符号按ASCII |
| . (点号) | 46 | 较高 | 其他符号按ASCII |
| : (冒号) | 58 | 较高 | 其他符号按ASCII |
| 0-9 | 48-57 | **最高** | 数字部分特殊处理 |

---

### 2.4 数字段比较规则

**数值比较**，而非字符串比较：

```
规则：
- 前导零被忽略
- 按照数值大小比较
- 空字符串视为 0

示例：
09  =  9
010 =  10
100 >  99
002 >  1
""  =  0
```

---

### 2.5 非数字段比较规则

**字典序比较**（lexicographical），但遵循上述字符优先级：

```
规则：
1. 先按字符优先级比较
2. 同类字符按 ASCII 值比较
3. 长度不同时，短的后面补"空"

示例（字母段）：
a    <  b
abc  <  abd
ab   <  abc  (因为 ab + (空) < ab + c)
A    <  a    (ASCII: 65 < 97)

示例（符号段）：
+    <  -    (ASCII: 43 < 45)
.    <  :    (ASCII: 46 < 58)
```

---

## 三、波浪号 (~) 的特殊作用

### 3.1 预发布版本排序

```
1.0~rc1  <  1.0~rc2  <  1.0  <  1.0.1

分解说明：
1.0~rc1:  ["", "1", ".", "0", "~rc", "1"]
1.0:      ["", "1", ".", "0"]

比较过程：
- 前面相同：1 = 1, . = ., 0 = 0
- 关键比较："~rc" vs (空)
- 因为 ~ < (空)，所以 1.0~rc1 < 1.0
```

### 3.2 实际应用场景

```
版本序列（从旧到新）：
2.0~alpha1   # alpha 测试
2.0~alpha2
2.0~beta1    # beta 测试
2.0~rc1      # 发布候选
2.0~rc2
2.0          # 正式版本 ✓
2.0.1        # 补丁版本
```

---

## 四、完整比较示例

### 4.1 基础数字比较

```
1       <  2
1.0     <  1.1
1.9     <  1.10      # 注意：10 > 9（数值比较）
1.9.9   <  1.10.0
```

### 4.2 预发布版本

```
1.0~alpha  <  1.0~beta   # alpha < beta（字典序）
1.0~rc1    <  1.0~rc2    # 1 < 2（数值）
1.0~rc2    <  1.0        # ~ < (空)
1.0        <  1.0.1
1.0.1      <  1.0.1+git20231215  # (空) < +
```

### 4.3 复杂版本比较

```
# 从旧到新排序：
1.0~rc1
1.0
1.0+git20231201
1.0+git20231215
1.0.1
1.0.1~bpo11+1     # backports 降级
1.0.1
1.0.1-1           # 添加 debian 修订
1.0.1-2
1.0.1-2.1         # NMU
1.0.1-2.1+b1      # 二进制重建
1.0.1-3
```

### 4.4 Epoch 的作用

```
场景：错误发布了 2.0，实际应该是 1.5

不可行：
2.0-1  →  1.5-1    # dpkg 会拒绝"降级"

解决方案 1：使用 +really
2.0-1  →  2.0+really1.5-1  # 2.0+really1.5 > 2.0

解决方案 2：使用 epoch
2.0-1  →  1:1.5-1          # epoch=1 强制大于所有 epoch=0 的版本

版本序列：
2.0-1              # 错误版本
1:1.5-1            # 修正，使用 epoch
1:1.5-2
1:1.6-1
1:2.0-1            # 最终达到真正的 2.0
```

---

## 五、实战比较题

### 练习 1：基础排序
```
待排序：
a) 1.0
b) 1.0~rc1
c) 1.0.1
d) 0.9.9

答案（从旧到新）：
d) 0.9.9
b) 1.0~rc1
a) 1.0
c) 1.0.1
```

### 练习 2：复杂版本
```
待排序：
a) 1.0-1+b1
b) 1.0-1
c) 1.0-1.1
d) 1.0-2
e) 1.0-0

答案：
e) 1.0-0
b) 1.0-1
a) 1.0-1+b1     # +b1 在修订号之后，所以 > 1.0-1
c) 1.0-1.1      # NMU 版本
d) 1.0-2
```

### 练习 3：混合场景
```
待排序：
a) 2:1.0-1
b) 1:9.9-9
c) 10.0-1
d) 1:10.0-1

答案：
c) 10.0-1       # epoch=0（默认）
b) 1:9.9-9      # epoch=1
d) 1:10.0-1     # epoch=1, 但 10.0 > 9.9
a) 2:1.0-1      # epoch=2 最大
```

### 练习 4：特殊符号
```
待排序：
a) 1.0+dfsg-1
b) 1.0-1
c) 1.0~rc1-1
d) 1.0+git20231215-1

答案：
c) 1.0~rc1-1              # ~ 最低
b) 1.0-1                  # (空) 居中
d) 1.0+git20231215-1      # + 较高，20231215 > dfsg（数字>字母）
a) 1.0+dfsg-1
```

---

## 六、命令行验证

### 使用 dpkg 比较版本：

```bash
# 比较两个版本
dpkg --compare-versions "1.0~rc1" lt "1.0"
echo $?  # 返回 0 表示真（1.0~rc1 < 1.0）

dpkg --compare-versions "1.0~rc1" gt "1.0"
echo $?  # 返回 1 表示假

# 操作符：
# lt  (<)   - 小于
# le  (<=)  - 小于等于
# eq  (=)   - 等于
# ne  (!=)  - 不等于
# ge  (>=)  - 大于等于
# gt  (>)   - 大于
```

### 实际测试：

```bash
# 验证波浪号
dpkg --compare-versions "1.0~rc1" lt "1.0" && echo "正确：rc1 < 正式版"

# 验证数字比较
dpkg --compare-versions "1.9" lt "1.10" && echo "正确：1.9 < 1.10"

# 验证 epoch
dpkg --compare-versions "1:1.0" gt "9.9" && echo "正确：epoch 优先"

# 验证 +b 后缀
dpkg --compare-versions "1.0-1+b1" gt "1.0-1" && echo "正确：+b1 更新"
```

---

## 七、Python 实现参考

```python
import re

def compare_versions(ver1, ver2):
    """
    简化的 Debian 版本比较（实际 dpkg 更复杂）
    返回: -1 (ver1<ver2), 0 (相等), 1 (ver1>ver2)
    """
    def parse_version(ver):
        # 解析 epoch
        if ':' in ver:
            epoch, rest = ver.split(':', 1)
            epoch = int(epoch)
        else:
            epoch = 0
            rest = ver

        # 分离 upstream 和 revision
        if '-' in rest:
            parts = rest.rsplit('-', 1)
            upstream = parts[0]
            revision = parts[1] if len(parts) > 1 else ''
        else:
            upstream = rest
            revision = ''

        return (epoch, upstream, revision)

    def compare_part(a, b):
        """比较单个版本部分"""
        # 分割数字和非数字
        def tokenize(s):
            return re.findall(r'\d+|[^\d]+', s)

        a_tokens = tokenize(a)
        b_tokens = tokenize(b)

        for i in range(max(len(a_tokens), len(b_tokens))):
            a_tok = a_tokens[i] if i < len(a_tokens) else ''
            b_tok = b_tokens[i] if i < len(b_tokens) else ''

            # 都是数字
            if a_tok.isdigit() and b_tok.isdigit():
                result = int(a_tok) - int(b_tok)
                if result != 0:
                    return -1 if result < 0 else 1
            # 数字 vs 非数字：数字更大
            elif a_tok.isdigit():
                return 1
            elif b_tok.isdigit():
                return -1
            # 都是非数字
            else:
                # 波浪号特殊处理
                a_priority = -1 if a_tok.startswith('~') else 0
                b_priority = -1 if b_tok.startswith('~') else 0

                if a_priority != b_priority:
                    return a_priority - b_priority

                if a_tok < b_tok:
                    return -1
                elif a_tok > b_tok:
                    return 1

        return 0

    # 解析两个版本
    epoch1, upstream1, rev1 = parse_version(ver1)
    epoch2, upstream2, rev2 = parse_version(ver2)

    # 比较 epoch
    if epoch1 != epoch2:
        return -1 if epoch1 < epoch2 else 1

    # 比较 upstream
    result = compare_part(upstream1, upstream2)
    if result != 0:
        return result

    # 比较 revision
    return compare_part(rev1, rev2)

# 测试
test_cases = [
    ("1.0~rc1", "1.0", -1),
    ("1.0", "1.0.1", -1),
    ("1:1.0", "9.9", 1),
    ("1.9", "1.10", -1),
    ("1.0-1+b1", "1.0-1", 1),
]

for v1, v2, expected in test_cases:
    result = compare_versions(v1, v2)
    status = "✓" if result == expected else "✗"
    print(f"{status} {v1} vs {v2}: {result} (expected {expected})")
```

---

## 八、关键要点总结

1. **Epoch 绝对优先**：有 epoch 的版本一定大于没 epoch 的
2. **波浪号最低**：`~` 用于预发布版本，保证小于正式版
3. **数字是数值**：`10 > 9`，不是字符串比较
4. **符号提升级**：`+` 等符号提升版本（高于空）
5. **空串有意义**：空字符串有特定优先级，介于 `~` 和字母之间
6. **逐段比较**：左到右，遇到差异立即返回
7. **实际验证**：使用 `dpkg --compare-versions` 验证

---

## 九、常见陷阱

### 陷阱 1：字符串比较 vs 数值比较
```
错误：认为 "10" < "9"（字符串比较）
正确：10 > 9（数值比较）
```

### 陷阱 2：波浪号的位置
```
错误：1.0-1~bpo11+1  # ~ 在修订号中，不影响 upstream
正确理解：这个版本的 revision 是 "1~bpo11+1"，依然小于 "2"
```

### 陷阱 3：加号不总是提升
```
1.0+really0.9  实际想表达这是 0.9 但版本号要大于 1.0
比较：1.0+really0.9 > 1.0（因为 +really0.9 > 空）
```

---

## 十、特殊后缀位置说明

### 完整版本号结构

```
<name>_[<epoch>:]<upstream>[上游后缀]-<revision>[修订后缀][+b<n>]_<arch>.deb
       └────┬────┘└────┬─────┘└───┬───┘└────┬────┘└──┬──┘└──┬──┘
         可选纪元    上游版本     修订号   修订后缀   二进制  架构
                   (包含各种+标识)        (NMU/bpo)   重建
```

### 上游版本后缀（在修订号之前）

```
<base>[~<pre>][+git<date>][+dfsg<n>][+really<ver>][+exp<n>]
└──┬──┘└──┬──┘└─────┬─────┘└────┬────┘└─────┬──────┘└───┬──┘
基础  预发布    快照      DFSG    真实版本   实验性
     (降级)   (升级)    (升级)   (升级)    (升级)

示例：
nginx_1.25.0+exp1-1_amd64.deb
nginx_1.22.0+git20231215+dfsg1-1_amd64.deb
```

### 修订号后缀（在修订号之后，架构之前）

```
-<revision>[.<nmu>][~bpo<ver>+<n>][+deb<ver>u<n>][+b<n>]
└────┬────┘└───┬──┘└──────┬───────┘└──────┬───────┘└─┬─┘
  基础修订   NMU子版本  backports标识  发行版安全更新 二进制重建

示例：
nginx_1.18.0-6.1_amd64.deb              # NMU
nginx_1.22.0-1~bpo11+1_amd64.deb        # backports
openssl_1.1.1n-0+deb11u5_amd64.deb      # 安全更新
nginx_1.18.0-6+b2_amd64.deb             # 二进制重建
```

### 位置优先级规则

```
从低到高（版本号递增）：
~bpo  <  -<rev>  <  -<rev>.<nmu>  <  -<rev>+deb<ver>  <  -<rev>+b<n>
(降级)    (标准)      (NMU修复)         (发行版特定)      (重编译)
```

### 实际复杂案例

```
完整示例：
package_1.0+git20231215+dfsg1-1.1~bpo11+1+b2_amd64.deb

分解：
- package name: package
- upstream: 1.0+git20231215+dfsg1
  - base: 1.0
  - git snapshot: +git20231215
  - DFSG: +dfsg1
- revision: 1.1~bpo11+1+b2
  - base revision: 1
  - NMU: .1
  - backports: ~bpo11+1
  - binary rebuild: +b2
- architecture: amd64

版本演进序列：
package_1.0-1_amd64.deb                          # 基础版本
package_1.0-1.1_amd64.deb                        # NMU修复
package_1.0-2_amd64.deb                          # 维护者正式修复
package_1.0+git20231215-1_amd64.deb              # Git快照版本
package_1.0+git20231215+dfsg1-1_amd64.deb        # 移除非自由内容
package_1.0+git20231215+dfsg1-1~bpo11+1_amd64.deb # backport到debian 11
package_1.0+git20231215+dfsg1-1~bpo11+1+b1_amd64.deb # amd64重新编译
```

---

## 十一、参考资源

- [Debian Policy Manual - Version](https://www.debian.org/doc/debian-policy/ch-controlfields.html#version)
- [dpkg man page](https://manpages.debian.org/testing/dpkg/dpkg.1.en.html)
- [Debian Package Management](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html)
- [Version Comparison Algorithm Source Code](https://git.dpkg.org/cgit/dpkg/dpkg.git/tree/lib/dpkg/version.c)

