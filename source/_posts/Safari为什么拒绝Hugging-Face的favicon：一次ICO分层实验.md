---
title: Safari 为什么拒绝 Hugging Face 的 favicon：一次 ICO 分层实验
date: 2026-09-16 09:10:00
cover: /img/assets/Safari为什么拒绝Hugging-Face的favicon：一次ICO分层实验/cover.png
thumbnail: /img/assets/Safari为什么拒绝Hugging-Face的favicon：一次ICO分层实验/cover.png
categories:
- 折腾
tags:
- macOS
- Safari
- favicon
- ICO
- SQLite
toc: true
---

Hugging Face 的 favicon 在 Chrome 里一直正常，到了 Safari 却只剩下默认图标。最开始我以为又是缓存坏了：重建缓存、删除拒绝记录、重新访问，结果完全没变。

这次的问题和我之前处理过的 [Safari Touch Icon](/2026/09/07/Safari收藏图标又消失了：一次Touch-Icon排查和自定义实践/) 不是一回事。Touch Icon 缓存里，Hugging Face 已经有一张下载成功的 128×128 PNG；真正出问题的是 `Favicon Cache`，官方 ICO 只留下了一条拒绝记录。

我原本只想把那个黄色小脸找回来，最后却做成了一次 ICO 分层实验。

<!-- more -->

## 先把网络和旧缓存排除掉

Hugging Face 当前的 [官方 favicon](https://huggingface.co/favicon.ico) 是一个 205,556 字节的 ICO，内部有 9 张图：

```text
16、24、32、48、64、72、96、128、256 px
```

服务器能正常返回文件，Chrome 也能显示。Safari 这边即使删除拒绝记录，下一次访问还是会重新拒绝。把完全相同的网页、响应头和 ICO 搬到本机 HTTP 服务后，结果也一样。

这一步很重要。故障会跟着图片来到 localhost，说明它不是 Hugging Face 域名、CDN 或跨站访问造成的，也不只是某条陈旧缓存没清干净。

## 拆开 ICO，Safari 的边界才露出来

我保留原始像素，只重建 ICO 的目录、数量和偏移，然后让 Safari 分别读取不同组合。结果比预想中有意思：

| ICO 内容 | Safari 结果 |
|---|---|
| 官方 9 层 | 拒绝 |
| 去掉 96px 后的 8 层 | 拒绝 |
| 16～96px 共 7 层 | 拒绝 |
| 16～72px 共 6 层 | 接受 |
| 16、24、32、48、64 共 5 层 | 接受 |
| 16、32、48 共 3 层 | 接受 |
| 单独的 24、32、72、96、128 或 256px | 都接受 |

单张 256px 能过，说明“Safari 不支持大图”说不通。我还把一份只有 32px 的 ICO 补零到 205,556 字节，它照样成功，所以总文件大小也不是原因。

这组样本只能说明：**Safari 的 favicon 处理会拒绝这份多图 ICO；在我的组合里，6 层成功，7、8、9 层失败。** 它没有证明 Safari 对所有 ICO 都存在一个通用的“最多 6 张”规则。编码方式、目录排列或某些层之间的组合仍可能参与判断。

至少排查范围已经很窄了。问题发生在 Safari 的 favicon 解码或采用阶段，不在图片能不能下载。

## 页面脚本也救不了

既然官方 ICO 会被拒绝，我试过从页面侧换一个图标。通过 PageRune 在 `document-start` 注入 `link rel="icon"`，先用 PNG，后来又换成 Hugging Face 官方 SVG。脚本显示已执行，Safari 检查器里也能看到新节点确实进入了 `document.head`，标签页图标还是没变。

这个现象并不新鲜。WebKit 的 [Bug 95979](https://bugs.webkit.org/show_bug.cgi?id=95979) 讨论的就是用 JavaScript 修改 favicon 链接后不重新加载的问题。当年的讨论还明确提到，Apple 平台并不打算默认开放脚本动态修改 favicon。

我因此停掉了脚本。DOM 里有一条正确的链接，不等于 Safari 会采用它；继续堆 MutationObserver 只是在证明同一件事。

## 最后的修复落在 Favicon Cache

我从本机已经通过 Safari 测试的 `16/32/48` 组合做了一份 [兼容 ICO](/img/assets/Safari为什么拒绝Hugging-Face的favicon：一次ICO分层实验/huggingface-compatible.ico)。不过 Hugging Face 页面本身并没有引用它，扩展又无法让 Safari 动态换图，所以最后只能处理 favicon 缓存。

动手前我先完全退出 Safari，并备份：

```text
~/Library/Safari/Favicon Cache/favicons.db
```

缓存里的图标文件不是按网址命名，而是与一条 UUID 记录关联。我的做法是复制 Safari 已经接受的 `16/32/48` ICO，创建新的 UUID，再把 UUID 字符串的 MD5 转成大写，作为 `favicons` 目录里的文件名。随后在数据库里：

- 为 Hugging Face 官方 favicon URL 写入一条 `icon_info`，尺寸和标记沿用已验证样本；
- 在 `page_url` 中把主页映射到新的 UUID；
- 只删除 Hugging Face 对应的拒绝记录；
- 对比修改前后的非 Hugging Face 行，确认其他站点没有变化；
- 最后执行 SQLite `quick_check`，结果为 `ok`。

这不是我愿意公开成“一键修复脚本”的东西。Safari 没有公开这套数据库结构，而且当时的脚本依赖本机测试产生的源 UUID。把它包装成通用工具，风险比价值大。

## 图标回来了，但先观察

重新打开 Safari 后，Hugging Face 首页的 favicon 出现了，刷新后仍然保留。继续访问 `/models`，图标也正常显示，Safari 还自动给这个页面建立了映射。数据库里已经没有 Hugging Face 的拒绝记录。

到这里，当前故障算是修好了。它也让我把几件容易混在一起的事彻底拆开：Touch Icon 正常不代表 favicon 正常；文件下载成功不代表 Safari 会解码采用；DOM 里插入了图标链接，也不代表 Safari 会动态更新标签页。

至于这个修复能维持多久，我还不知道。Safari 可能在未来重新抓取官方 ICO，也可能在系统更新后改变缓存格式。现在我保留了数据库备份和那份三层兼容 ICO；如果图标再次消失，至少不必从“清缓存试试”重新开始。
