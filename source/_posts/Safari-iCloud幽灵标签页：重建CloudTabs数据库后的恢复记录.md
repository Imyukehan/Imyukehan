---
title: Safari iCloud 幽灵标签页：重建 CloudTabs 数据库后的恢复记录
date: 2026-09-16 09:12:00
cover: /img/assets/Safari-iCloud幽灵标签页：重建CloudTabs数据库后的恢复记录/cover.png
thumbnail: /img/assets/Safari-iCloud幽灵标签页：重建CloudTabs数据库后的恢复记录/cover.png
categories:
- 折腾
tags:
- macOS
- Safari
- iCloud
- SQLite
- 同步
toc: true
---

我的两台 Mac 最近互相看见了一批早已关闭的 Safari 标签页。最烦的不是列表旧，而是我从另一台设备点掉它们以后，过一阵又会回来，像从 iCloud 里复活了一样。

关闭再开启 Safari 的 iCloud 同步没有用。完整退出 Apple ID 曾经短暂解决过一次，后来问题还是复发。我不想再为几个标签页重新同步整套账号数据，于是这次只查 Safari 的 Cloud Tabs 本地状态。

现在，删除并重建 CloudTabs 数据库的方案暂时成功了。先记下过程，也给以后可能的复发留一个边界清楚的处理方法。

<!-- more -->

## 这不是只有我遇到

这种“已经关闭、远程删除后又回来”的标签页，社区通常叫 ghost tabs 或 zombie tabs。Reddit 上有一条持续多年的 [iCloud Safari zombie tabs 讨论](https://www.reddit.com/r/applehelp/comments/p8zhvd/icloud_safari_tabs_zombie_tabs_from_macbook_pro/)，现象几乎一样：旧标签页会在其他设备上出现，远程关闭后又被某台 Mac 重新同步上去。[Apple 社区](https://discussions.apple.com/thread/253960314) 也有类似的多设备 Safari 同步故障报告。

Jesse Squires 在 2023 年记录过一种相对温和的 [iCloud Safari 重置流程](https://www.jessesquires.com/blog/2023/03/02/icloud-tabs-bug/)：在参与同步的设备上关闭 Safari iCloud 同步，完全退出 Safari，再重新启用同步。这个方向比退出整个 Apple ID 合理得多。

不过我已经试过单纯切换同步，幽灵标签页仍会回来。接下来要看的，是 Mac 本地到底还保存着什么。

## CloudTabs.db 里没有一个漂亮的答案

Safari 的 Cloud Tabs 数据在这里：

```text
~/Library/Containers/com.apple.Safari/Data/Library/Safari/CloudTabs.db
```

我先复制数据库，只对副本做只读检查。SQLite `quick_check` 返回 `ok`，设备标记没有明显重复，所以这不是一个“数据库已损坏”或“同一台 Mac 被登记了两次”就能解释的问题。

更值得注意的是，数据库里还留着 3 条关闭请求，而它们对应的标签页依然存在于 `cloud_tabs`。这与实际表现对得上：关闭动作发出过，但本地同步状态没有稳定地收敛，标签页随后又出现。

这只能支持“本地同步状态卡住了”，不能证明问题的云端根因。iCloud 服务端怎么合并记录、哪台设备又把旧状态上传回来，我从本机数据库里看不到。

还有一个容易误读的字段：`last_viewed_time` 描述的是标签页最后查看时间，不是关闭请求的创建时间。把它当成“我什么时候点了关闭”，会把时间线讲错。

## 最后只重建 Cloud Tabs 状态

社区里比较一致的做法，是先暂停参与设备上的 Safari iCloud 同步，退出 Mac 上的 Safari，然后只处理这三个文件：

```text
CloudTabs.db
CloudTabs.db-shm
CloudTabs.db-wal
```

它们都位于：

```text
~/Library/Containers/com.apple.Safari/Data/Library/Safari/
```

我没有直接永久删除，而是把存在的文件移到一个备份目录。这样 Safari 下次启动时会创建新的 CloudTabs 数据库，旧文件仍然可以拿回来检查。随后重新打开 Safari、恢复 iCloud 同步，留一点时间让各设备重新汇合当前状态。

这里有两个范围不能扩大：

- 不要把整个 Safari 目录一起清掉，那里还有历史记录、标签页和其他浏览数据；
- 不要把 `SafariTabs.db` 当成同一个文件，它管理的是另一类本地标签页状态，这次没有动它。

相比退出整个 Apple ID，这次处理只针对 Cloud Tabs 的本地同步缓存，也保留了退路。

## 目前成功，先不宣布永久解决

重建后，两台 Mac 上那批反复出现的旧标签页目前没有再回来。新状态能重新同步，原来的幽灵记录也消失了。

我仍然不会把它写成“永久修复”。这次结果说明，清掉卡住的本地 CloudTabs 状态有效；它没有证明 iCloud 服务端以后不会再次进入同样的状态。社区里也有人在重置后长期正常，有人隔一段时间又遇到同步延迟。

至少现在我不需要为了几条幽灵标签页退出整个 Apple ID。下次如果复发，我会先停用 Safari 同步、退出浏览器，备份并重建这三个 `CloudTabs.db` 文件，再观察设备间是否重新收敛。范围小，过程可回退，也和这次真正生效的改动一致。
