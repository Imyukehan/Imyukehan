---
title: Safari 为什么拒绝 Hugging Face 的 favicon：一次 ICO 分层实验
date: 2026-09-16 09:10:00
updated: 2026-09-19 11:00:00
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

9 月 19 日补记：后来我又查了 X.com 上“旧页面有图标，新页面没有”的问题。这次图片本身正常，最终通过刷新共享图标记录的时间戳并清除对应拒绝状态恢复了。实验和可复现 SQL 放在本文后半部分。

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

## 9 月 19 日：X 的图片没坏，新页面却关联不上

Hugging Face 恢复以后，我又遇到了 X 的图标问题。已有首页能显示 X，新打开的推文却是默认地球图标。我起初以为是推文详情页的特殊行为，但给首页加一个新的查询参数，Safari 同样无法给这个新 URL 关联图标。

这轮观察到的 Safari 版本是 27.2。页面使用的共享图标地址是 [twitter.3.ico](https://abs.twimg.com/favicons/twitter.3.ico)。虽然扩展名是 `.ico`，实际响应却是 549 字节的 32×32 PNG，和 [x.com/favicon.ico](https://x.com/favicon.ico) 的内容完全相同。Safari 自己生成的缓存文件是 16/32px 的 ICO 表示，几份成功与失败记录对应的图片字节也一致。

所以不能把 Hugging Face 的多图 ICO 结论搬过来。X 的原图可以正常使用，旧页面也确实还在显示它，异常发生在新页面取得这条共享图标的过程中。

我用最小 HTML 做了对照，只改变图标 URL：

| 对照 | 图标显示与页面关联 |
|---|---|
| 引用原 CDN 图标 URL | 默认图标，没有新映射 |
| 同一个图标 URL 加查询参数 | 立即显示 X，自动建立映射 |
| 第二个新页面继续引用这个带参数的 URL | 正常显示，复用同一条图标记录 |
| 引用 X 根目录的 favicon URL | 正常显示，自动建立映射 |

失败跟着原图标 URL 来到了最小页面，已经不需要推文内容或 X 的页面路由参与。实验也没有给出归因于 Surge 的证据。带查询参数的办法只在静态 HTML 对照里验证过，我没有把它当成已经可用的 X 用户脚本修复。

## 清掉拒绝记录，还差一步

最初那些失败页面甚至没有各自的拒绝行。后续修复实验中，共享图标 URL 才产生了拒绝记录；只盯着某条推文的 URL 查缓存，很容易漏掉这一层。

我先试过重启，也试过重建共享记录。中间有一次恢复旧记录后仍然失败，但后来发现 Safari 已经回收了那张暂时失去引用的旧图片。那次同时改变了记录和文件是否存在，不能拿来单独证明时间戳有问题。

于是我从备份恢复原图片，核对原 UUID、原时间戳和文件 SHA-256，再做对照：

| 保持完整原图与原 UUID | 结果 |
|---|---|
| 保留旧时间戳，只清除该图标 URL 的拒绝记录 | 新推文仍没有映射，并再次生成拒绝记录 |
| 只将时间戳更新为当前值，再清除该图标 URL 的拒绝记录 | 新推文显示 X，Safari 自动创建映射 |

随后我又打开第二条此前没有关联过的新推文，界面上也出现了 X，数据库里多出了自动映射。最终该共享图标 URL 的拒绝行数为零。修复保留了原 UUID、原图片字节和已有 `page_url` 映射，没有逐条添加推文地址。

这让我更倾向于把问题理解为：共享图标记录过期后，重新验证路径与拒绝状态一起影响了新页面关联。这是根据对照作出的推断；Safari 内部具体在哪一步失败、多久算过期，我还没有查明。

## 在其他 Mac 上复现这次修复

这组 SQL 适用于本机已经有完整 X 图标缓存、表结构也与实验一致的情况。先用 ⌘Q 正常退出 Safari，确认进程已经退出，再打开缓存数据库。不要在 Safari 运行时写它。

```sh
pgrep -x Safari
sqlite3 -bail "$HOME/Library/Safari/Favicon Cache/favicons.db"
```

第一条还有进程输出时，先停在这里。数据库路径必须已经存在；否则不要运行第二条，以免 SQLite 创建一个空库。

进入 SQLite 后，先备份再检查。下面的备份文件名是示例，选一个尚不存在的名字，保存在自己知道的位置；`.backup` 会保存当前逻辑数据库，包括 WAL 中的数据。

```sql
.backup 'favicons-before-x-refresh-20260919.db'
PRAGMA quick_check;
PRAGMA table_info(icon_info);
PRAGMA table_info(rejected_resources);
SELECT * FROM icon_info
WHERE url = 'https://abs.twimg.com/favicons/twitter.3.ico';
```

确认 `quick_check` 为 `ok`，`icon_info` 有 `url`、`timestamp` 字段，`rejected_resources` 有 `icon_url` 字段，并且精确 URL 对应的现存图标记录符合预期。还要检查这条记录引用的缓存图片：本次 Safari 使用 UUID 字符串的大写 MD5 作为 `favicons` 子目录中的文件名，图片应存在且能解码。只看见数据库行不够；如果文件已丢失或损坏，下面的时间戳更新不能补回图片。UUID 和文件都应取自自己的 Mac。

检查通过后，在同一个 SQLite 会话运行：

```sql
BEGIN IMMEDIATE;

UPDATE icon_info
SET timestamp = CAST(strftime('%s','now') AS INTEGER)-978307200
WHERE url = 'https://abs.twimg.com/favicons/twitter.3.ico';

SELECT changes() AS updated_icon_rows;

DELETE FROM rejected_resources
WHERE icon_url = 'https://abs.twimg.com/favicons/twitter.3.ico';

SELECT changes() AS removed_rejection_rows;
```

先核对更新行数与刚才查到的目标记录数一致，再执行 `COMMIT;`；如果不符合预期，执行 `ROLLBACK;`。这里的 `978307200` 是 Unix 1970 年纪元到 Apple 2001 年纪元的秒数差，不能直接把 Unix 时间写进去。

提交后检查并退出：

```sql
PRAGMA quick_check;
SELECT COUNT(*) AS remaining_rejections
FROM rejected_resources
WHERE icon_url = 'https://abs.twimg.com/favicons/twitter.3.ico';
.quit
```

重新启动 Safari，访问此前没关联过图标的 X 页面，看图标是否出现，再检查 Safari 有没有自动写入 `page_url`。这才是本次修复的验收点。已有页面原本就能显示，单看它刷新成功不能说明新页面的问题已解决。

这次操作只触及精确图标 URL 的时间戳和拒绝记录，不需要复制别人的 UUID、图片或整份数据库。我的两个新页面目前都通过了验证；是否长期不再复发，还要继续观察。

## 可下载的定向修复脚本

我把上述操作整理成了 [repair_x_favicon.py](/img/assets/Safari为什么拒绝Hugging-Face的favicon：一次ICO分层实验/repair_x_favicon.py)，方便在其他 Mac 上检查。它只依赖 Python 3 标准库和 macOS 自带工具。将文件保存到下载目录后，先运行默认检查：

```sh
python3 ~/Downloads/repair_x_favicon.py
```

默认不会修改数据库。脚本会核对表结构、精确图标 URL 的唯一记录，以及现存图片能否被系统读取。检查通过后，用 ⌘Q 退出 Safari，再运行：

```sh
python3 ~/Downloads/repair_x_favicon.py --apply
```

它先完整备份 SQLite 数据库，再更新时间并清除匹配拒绝记录，保留图片、UUID 和已有页面映射。备份默认存放在 `~/Downloads/Safari-favicon-backups/`，终端会打印本次备份目录及 `--undo` 撤销命令。撤销也要求退出 Safari，只恢复这次修改前的时间戳和删除的拒绝行，保留后来新增的页面映射；目标记录再次变化时会停止自动撤销。

备份数据库和 `changes.json` 含本机浏览相关网址，应留在本地。不要把这些文件随脚本发给别人。如果终端报 `Operation not permitted`，需要在系统设置的“隐私与安全性 → 完全磁盘访问权限”中允许该终端访问，然后重新启动终端。图片缺失、记录不唯一或表结构不同，则需要重新诊断。

脚本已在合成数据库上测试修复、其他记录保持不变、撤销和缺图停止，在这台 Mac 的真实数据库上只做过默认检查。前面描述的界面修复来自实际实验，可移植脚本还没有在另一台 Mac 上完成显示验证。运行后仍应打开一个此前未关联的新 X 页面，确认图标出现。
