---
title: Pattern Matching 模式匹配
---

在编辑文本的程序过程中，经常需要寻找文本中某个模式的所有位置，有效解决这个问题的算法是字符串匹配算法，也就是模式匹配，除了文本处理，也常被用于DNA序列中特定序列的搜索，网络搜索引擎的查询等等，在诸多领域都有应用。

<!-- more -->

## 形式化定义

先来看看算法导论里怎么说的：

> We assume that the text is an array $ T[1,\dots,n] $ of length $ n $ and that the pattern is an array $ T[1,\dots,m] $ of length $ m > n $ . We further assume that the elements of P and T are characters drawn from a finite alphabet $ \Sigma $. For example, we may have $ \Sigma = \{0, 1\} $or $ \Sigma = \{0, 1,\dots,z\} $. The character arrays $ P $ and $ T $ are often called strings of characters.

## 算法复杂度比较

| 算法                 | 预处理时间            | 匹配时间            |
| ------------------ | ---------------- | --------------- |
| Brute Force暴力      | $ 0 $            | $ O((n-m+1)m) $ |
| Rabini-Karp        | $ \Theta(m) $    | $ O((n-m+1)m) $ |
| 有限自动机算法            | $ O(m|\Sigma|) $ | $ \Theta(n) $   |
| Knuth-Morris-Pratt | $ \Theta(m) $    | $ \Theta(n) $   |
| Boyer-Moore        | $ 0 $            | $ O((n-m+1)m) $ |

## 朴素字符串匹配算法

### 算法介绍

BF算法，即 Brute Force 算法，是普通的模式匹配算法，BF算法的思想就是将目标串S的第一个字符与模式串T的第一个字符进行匹配，若相等，则继续比较S的第二个字符和 T的第二个字符；若不相等，则比较S的第二个字符和T的第一个字符，依次比较下去，直到得出最后的匹配结果。BF算法是一种蛮力算法。

朴素算法通过一个循环找到所有有效的偏移量， 该循环对 $ n-m+1 $ 个可能的值进行检测， 看是否满足条件$ P[1,\dots,m] =T[s+1,\dots,s+m]$ 。

### 复杂度分析

由于不需要预处理，BF运行时间即为其匹配时间。在最坏的情况下，对于每一个偏移量，都需要循环 $ m $ 次来确定偏移的有效性，忽略了检测无效s值是获得的文本的信息，然而这些信息是可以利用的。

### 代码实现（C语言）

```c
/********** Brute Force 算法 **********/
int index_BF(char *content, char *pattern, int pos)
{
    int lc = strlen(content);   //获取主串长度
    int lp = strlen(pattern);   //获取模式串长度
    int j = 0;
    int i = pos;
    while(i < lc && j < lp)
    {
        if(content[i] == pattern[j])
        {
            i++;
            j++;
        }
        else
        {
            i = i - j + 1;
            j = 0;
        }
    }
    if(j == lp)
        return i - lp;
    else
        return -1;
}

void BF(char *content, char *pattern)
{
    int lp = strlen(pattern);
    int pos = index_BF(content, pattern, 0);;
    while(pos != -1)
    {
        printf("在位置 %d 发现匹配！\n", pos + 1);
        pos = index_BF(content, pattern, pos + lp);
    }
}
```

## Knuth-Morris-Pratt 算法

### 算法介绍

在[计算机科学](https://zh.wikipedia.org/wiki/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6)中，**Knuth-Morris-Pratt 字符串查找算法**（常简称为“**KMP算法**”）可在一个**主文本字符串**`S`内查找一个**词**`W`的出现位置。此算法通过运用对这个词在不匹配时本身就包含足够的信息来确定下一个匹配将在哪里开始的发现，从而避免重新检查先前匹配的[字符](https://zh.wikipedia.org/wiki/%E5%AD%97%E7%AC%A6)。

这个算法是由[高德纳](https://zh.wikipedia.org/wiki/%E9%AB%98%E5%BE%B7%E7%BA%B3)（Donald Ervin Knuth）和[沃恩·普拉特](https://zh.wikipedia.org/w/index.php?title=%E6%B2%83%E6%81%A9%C2%B7%E6%99%AE%E6%8B%89%E7%89%B9&action=edit&redlink=1)（英语：[Vaughan Pratt](https://en.wikipedia.org/wiki/Vaughan_Pratt)）在1974年构思，同年[詹姆斯·H·莫里斯](https://zh.wikipedia.org/w/index.php?title=%E8%A9%B9%E5%A7%86%E6%96%AF%C2%B7H%C2%B7%E8%8E%AB%E9%87%8C%E6%96%AF&action=edit&redlink=1)（英语：[James H. Morris](https://en.wikipedia.org/wiki/James_H._Morris)）也独立地设计出该算法，最终由三人于1977年联合发表。

表的作用是让算法无需多次匹配`S`中的任何字符。能够实现线性时间搜索的关键是在主串的一些字段中检查模式串的*初始字段*，我们可以确切地知道在当前位置之前的一个潜在匹配的位置。换句话说，在不错过任何潜在匹配的情况下，我们"预搜索"这个模式串本身并将其译成一个包含所有可能失配的位置对应可以绕过最多无效字符的列表。

对于`W`中的任何位置，我们都希望能够查询那个位置前（不包括那个位置）有可能的`W`的最长初始字段的长度，而不是从`W[0]`开始失配的整个字段，这长度就是我们查找下一个匹配时回退的距离。因此`T[i]`是`W`的可能的*适当*初始字段同时也是结丛于`W[i - 1]`的子串的最大长度。我们使空串长度是0。当一个失配出现在模式串的最开始，这是特殊情况（无法回退），我们设置`T[0] = -1`，在[下面](https://zh.wikipedia.org/wiki/%E5%85%8B%E5%8A%AA%E6%96%AF-%E8%8E%AB%E9%87%8C%E6%96%AF-%E6%99%AE%E6%8B%89%E7%89%B9%E7%AE%97%E6%B3%95#.E5.BB.BA.E7.AB.8B.E8.A1.A8.E7.AE.97.E6.B3.95.E7.9A.84.E4.BC.AA.E4.BB.A3.E7.A0.81.E7.9A.84.E8.A7.A3.E9.87.8A)讨论。

```algorithm
algorithm kmp_table:
    input:
        an array of characters, W (the word to be analyzed)
        an array of integers, T (the table to be filled)
    output:
        nothing (but during operation, it populates the table)

    define variables:
        an integer, pos ← 2 (the current position we are computing in T)
        an integer, cnd ← 0 (the zero-based index in W of the next 
character of the current candidate substring)

    (the first few values are fixed but different from what the algorithm 
might suggest)
    let T[0] ← -1, T[1] ← 0

    while pos < length(W) do
        (first case: the substring continues)
        if W[pos - 1] = W[cnd] then
            let cnd ← cnd + 1, T[pos] ← cnd, pos ← pos + 1

        (second case: it doesn't, but we can fall back)
        else if cnd > 0 then
            let cnd ← T[cnd]

        (third case: we have run out of candidates.  Note cnd = 0)
        else
            let T[pos] ← 0, pos ← pos + 1
```

### 复杂度分析

创建表的算法的复杂度是 $ O(n) $ ，其中 $ n $ 是 $ W $ 的长度。除去一些初始化的工作，所有工作都是在`**while**`循环中完成的，足够说明这个循环执行用了 $ O(n) $ 的时间，同时还会检查`pos`和`pos - cnd`的大小。在第一个分支里，`pos - cnd`被保留，而`pos`与`cnd`同时递增，自然，`pos`增加了。在第二个分支里，`cnd`被`T[cnd]`所替代，即以上总是严格低于`cnd`，从而增加了`pos - cnd`。在第三个分支里，`pos`增加了，而`cnd`没有，所以`pos`和`pos - cnd`都增加了。因为`pos ≥ pos - cnd`，即在每一个阶段要么`pos`增加，要么`pos`的一个下界增加；所以既然此算法只要有`pos = n`就终止了，这个循环必然最多在`2n`次迭代后终止，因为`pos - cnd`从`1`开始。因此创建表的算法的复杂度是 $ O(n) $ 。

### 代码实现（C语言）

```c
/********** Knuth--Morris--Pratt 算法 **********/
int next[MAXN];

void get_next(char *pattern)
{
    int lp = strlen(pattern);   //获取模式串长度
    int k = -1, j = 0;
    next[0] = k;
    while (j < lp)
    {
        if ( (k == -1) || (pattern[j] == pattern[k]) )
        {
            ++k;
            ++j;
            next[j] = k;
        }
        else
            k = next[k];
    }
}

int index_KMP(char *content, char *pattern, int pos)  
{
    int lc = strlen(content);   //获取主串长度
    int lp = strlen(pattern);   //获取模式串长度
    int i = pos, j = 0;
    while ((i < lc) && (j < lp))
    {
        if ((j == -1) || content[i] == pattern[j])
        {  
            i++;
            j++;
        }
        else
            j = next[j];
    }
    if (lp == j)
        return i - lp;
    else
        return -1;
}

void KMP(char *content, char *pattern)
{
    int lp = strlen(pattern);
    get_next(pattern);
    int pos = index_KMP(content, pattern, 0);;
    while(pos != -1)
    {
        printf("在位置 %d 发现匹配！\n", pos + 1);
        pos = index_KMP(content, pattern, pos + lp);
    }
}
```