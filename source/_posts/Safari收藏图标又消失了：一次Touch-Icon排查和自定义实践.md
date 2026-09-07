---
title: Safari 收藏图标又消失了：一次 Touch Icon 排查和自定义实践
date: 2026-09-07 21:55:00
cover: /img/assets/Safari收藏图标又消失了：一次Touch-Icon排查和自定义实践/cover.png
thumbnail: /img/assets/Safari收藏图标又消失了：一次Touch-Icon排查和自定义实践/cover.png
categories:
- 折腾
tags:
- macOS
- Safari
- Touch Icon
- SQLite
- 图标
toc: true
---

今天又被 Safari 的收藏图标折腾了一遍。

我的环境是 macOS 27.0 build 26A5425a、Safari 27.0。Google 和 B 站原本正常的收藏页大图标突然变成了字母方块。清理缓存后会短暂恢复，过一会儿又回去。后来改了一次收藏网址，两者的大图标恢复了，但 Google 标签页上的小 favicon 仍然不对。

折腾到这里，我才真正把 Safari 里的两套图标分开：标签页小图标是一条缓存链路，起始页收藏大图标是另一条。继续沿着 Touch Icon 的缓存查下去，我把两枚图标恢复了，也在本机实现了自定义。最后一步碰到了 Safari 私有数据库，所以先说清楚：这是一次有备份、只改两个站点的本机实验，不是 Apple 提供的官方自定义功能。

<!-- more -->

## 先别把 favicon 和 Touch Icon 混在一起

Safari 至少有两个容易被混为一谈的缓存目录：

```text
~/Library/Safari/Favicon Cache/
~/Library/Safari/Touch Icons Cache/
```

前者主要关系到标签页、地址栏等位置的小 favicon，后者则是起始页和收藏项目使用的大图标。这次 Google 就给了我一个很直观的对照：改收藏网址以后，大图标回来了，标签页的小图标却没有一起恢复。

Apple 社区里也有人遇到 Google 收藏图标错乱，做法是在 `www.google.com` 和 `google.com` 之间改一次收藏地址，借此触发重新关联。[Apple 社区的案例](https://discussions.apple.com/thread/255602326)和我这次的结果相似，但这只能说明改 URL 在本次有效，不能说明所有图标问题都来自同一个缓存键。

所以后面所有排查，我只盯着 `Touch Icons Cache`。Google 标签页 favicon 的问题留在另一条线上，不拿它干扰这篇记录。

## 蜜柑的图标路径很可疑，但它不是最终答案

Google 和 B 站恢复后，蜜柑计划仍然没有显示收藏大图标。奇怪的是，iOS 上重新加载却正常。这排除了一个很顺手、也很容易说错的解释：不能直接把 iOS 的正常显示归结为旧缓存。

网站端确实存在可疑之处。蜜柑主页面声明的 Touch Icon 路径带有反斜杠和大写 `Images`；我实际请求时，大写路径返回 404，小写的 `/images/apple-touch-icon-180x180.png` 正常返回。备用域名 `mikanime.tv` 最后又跳回了 `mikanani.me`，所以换域名没有解决 Mac 上的显示问题。

Apple 的旧版 Web Clip 文档说明，网站可以用 `rel="apple-touch-icon"` 指定 PNG，也可以针对不同分辨率声明多个尺寸，其中就有 180×180；如果没有声明，系统还会尝试在站点根目录寻找以 `apple-touch-icon` 开头的文件。[Apple《Configuring Web Applications》](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)

不过这份文档写的是旧版 iOS Web Clip，不能直接当成 Safari 27 私有缓存的说明书。反斜杠、大小写和重定向都可能影响图标选择，但 iOS 新加载正常又说明事情没那么简单。我把这些现象保留下来，没有把网站路径异常写成唯一根因。

## 数据库说“下载成功”，收藏页却不一定采用

直接读取 Safari 缓存时，我先撞上了 macOS 隐私权限。最后把整份 `Touch Icons Cache` 复制到下载目录，再对副本做只读查询。这样也避免了 Safari 正在运行时碰原数据库。

`TouchIconCacheSettings.db` 里的 `cache_settings` 表给出了两个很有意思的记录：

| host | 已在缓存 | 下载状态 | HTTP 状态 | transparency 分析值 | 缓存图片 |
|---|---:|---:|---:|---:|---|
| `mikanani.me` | 1 | 1 | 200 | 2 | 64×64 PNG |
| `lisahost.com` | 1 | 1 | 200 | 2 | 48×48 PNG |

两个站点都下载成功，PNG 也真实存在。蜜柑缓存的是黄色橘子剖面，丽萨主机缓存的是蓝色 L 标志。问题已经不再是“Safari 有没有拿到图片”，而是“收藏页最后怎样采用和展示它”。

缓存文件名也不是随机字符串。我分别对纯主机名计算 MD5，再转成大写：

```text
mikanani.me → CDE9CFFBFC7870408F7E125F29E84101.png
lisahost.com → D2D3AC0DF1206C3B796380F253D01EA7.png
```

这里不包含协议，也不包含后面的路径。两组结果与本机缓存文件名完全一致。它是我在 Safari 27 里实测的两个样本，不代表 Apple 承诺以后永远用同一套命名方式。

这个发现也解释了为什么反复清缓存不一定有用：Safari 可以成功重新下载同一张小图，数据库继续显示 200，起始页却仍然给出字母占位或不理想的尺寸。

## 换成 180×180 后，还要让 Safari 真正刷新

蜜柑站点现有的 180×180 Touch Icon 是人物抱着橘子的插图，并不是我想要的橘子剖面；它的 favicon 最大只有 64×64。丽萨主机的缓存图则只有 48×48。于是我给两者各准备了一张 180×180 PNG，统一改成白底、主体缩小居中。

![蜜柑的 180×180 自定义 Touch Icon](/img/assets/Safari收藏图标又消失了：一次Touch-Icon排查和自定义实践/mikanani-custom-touch-icon.png)

![丽萨主机的 180×180 自定义 Touch Icon](/img/assets/Safari收藏图标又消失了：一次Touch-Icon排查和自定义实践/lisahost-custom-touch-icon.png)

蜜柑的橘子是参考缓存图重新绘制，不是官方高清原图；丽萨的 L 图标后来也重新做了白底排版。两张图都经过了图像生成处理，不能说成对原像素的无损放大。

社区最近有人在 Safari 26 做过一个很干净的对照：32×32、48×48 和 64×64 的缓存图显示成字母占位，而保留数据库记录与文件名、只把其中一张换成 256×256 后，收藏页立刻采用了图标。[Reddit 上的 Safari 26 实测](https://www.reddit.com/r/Safari/comments/1vnwx2c/safari_26_start_page_favorites_show_generic/)

这个案例给了我尺寸方向，但我的结果不能简化成“180×180 就一定成功”。第一次替换后，我以为没有效果；把收藏链接改回原地址，Safari 重新关联图标，显示才恢复。也就是说，换图片和触发刷新在这次实验里缺一不可。Safari 以后也可能重新下载网站的小图，再把自定义文件覆盖掉。

## 最后一层灰色边框，藏在展示状态里

两枚白底图标已经出现后，画面还差一点：白色方块被缩在 Safari 的灰色圆角底内，看起来像图标外面又套了一层壳。继续查社区讨论时，我在一份老的 Safari 图标脚本评论区找到一条 2023 年的线索：`transparency_analysis_result` 可能影响图标的留白和边框，把它改成 1，有人观察到外圈间距消失。[GitHub Gist 评论](https://gist.github.com/dardo82/f7cc7c5c864fb5afa04bb12ecbcf3a9f#file-safari-favicons-sh)

字段名字听起来像“透明度分析结果”，但 Apple 没有公开它的语义。我没有给它编一个官方定义，只把社区经验当成一次可回退实验。

我最后做的脚本遵守几个很窄的边界：

1. 先确认 Safari 已完全退出；
2. 只查询 `mikanani.me` 和 `lisahost.com`，缺少任何一条记录就停止；
3. 用 SQLite 的 backup 接口备份当前逻辑数据库，让 WAL 中尚未合并的数据也进入备份；
4. 记录两个站点原来的字段值，只把它们从 2 改成 1；
5. 撤销时只恢复这两个字段，不用旧数据库覆盖后来产生的全部缓存。

实际更新的范围可以概括成下面这句 SQL，但我没有把它包装成随手复制就能跑的通用命令：

```sql
UPDATE cache_settings
SET transparency_analysis_result = 1
WHERE host IN ('mikanani.me', 'lisahost.com');
```

社区旧脚本还会批量改整张表、给缓存目录加 append-only 标志。我这次都没有采用。锁死缓存可能妨碍 Safari 正常更新，而我只想验证两个图标的展示状态。

我运行定点脚本、重新打开 Safari 后，效果很好，Touch Icon 问题基本解决。这里的最终结论来自实际视觉确认；由于原缓存仍受隐私权限保护，我没有声称自己又直接读回了原数据库。

## 这次到底解决了什么

这轮排查让我拿到了一个很实用的结果：在这台 Mac、这个 Safari 版本上，我可以按主机名找到收藏图标缓存，用自定义 PNG 替换它，再针对目标记录调整展示状态。

但它仍然有明确边界：

- 这不是 Safari 提供的官方“自定义收藏图标”入口；
- `transparency_analysis_result=1` 的效果只在本机两个站点上得到验证；
- Safari 刷新缓存或系统升级后，图片和数据库字段都可能被覆盖；
- 我没有验证这些改动会通过 iCloud 同步，也没有锁定缓存阻止 Safari 更新；
- Google 标签页的小 favicon 属于另一套缓存，这篇没有把它一起解决。

所以我不会把它叫作永久修复。至少现在，Google 和 B 站的收藏大图标恢复了，蜜柑与丽萨也换成了我想要的样子；如果以后 Safari 再覆盖，备份、目标主机和撤销路径都还在。

从“清缓存又复发”一路查下来，我最后把问题拆成了下载、关联、图片尺寸和展示状态四层。这比继续反复清缓存可靠得多。Safari 没给我一个自定义按钮，我还是把这件事做成了。
