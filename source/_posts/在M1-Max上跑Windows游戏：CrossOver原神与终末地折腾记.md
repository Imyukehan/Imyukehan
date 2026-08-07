---
title: 在 M1 Max 上跑 Windows 游戏：CrossOver、原神与终末地折腾记
date: 2026-08-06 09:30:00
cover: /img/assets/在M1-Max上跑Windows游戏：CrossOver原神与终末地折腾记/cover.png
thumbnail: /img/assets/在M1-Max上跑Windows游戏：CrossOver原神与终末地折腾记/cover.png
categories:
- 折腾
tags:
- macOS
- CrossOver
- 游戏
- Wine
toc: true
---

Mac 能不能玩 PC 游戏？

以前我的答案大概是：能，但没有必要。真想玩就开 Windows，或者干脆用主机。直到最近看到《明日方舟：终末地》的 CrossOver 兼容补丁有了新进展，我还是没忍住，拿自己的 M1 Max 做了一轮实验。既然终末地都要折腾了，索性把《原神》也一起塞进 Mac，看看这条路究竟能走到哪里。

这不是一篇“复制几个文件就一定能玩”的教程。两款游戏都涉及非官方兼容方案，尤其碰到保护壳、反作弊和第三方解锁工具后，游戏更新一次，昨天成立的结论今天就可能失效。本文更像一次阶段性复盘：它们为什么能运行、最难的地方在哪里，以及我最后怎样把一堆命令收进两个看起来普通的 macOS App。

<!-- more -->

## 先说结果

测试环境是 M1 Max、64GB 内存、macOS 27 测试版和 CrossOver 26.2。

两款游戏都曾经成功进入并正常游玩：

|  | 《原神》 | 《明日方舟：终末地》 |
|---|---|---|
| 图形路径 | DirectX 11 + DXMT | DirectX 11 + D3DMetal |
| HiDPI | 开启 | 开启 |
| 键位 | Option → Alt，Command → Ctrl | Option → Alt，Command → Ctrl |
| 日常入口 | `原神.app` | `明日方舟：终末地.app` |
| 更新方式 | 需要时打开米哈游启动器 | 需要时打开鹰角启动器 |

原神实测时 GPU 占用大约 87%～97%，游戏主进程占用约 2.7～3.5 个 CPU 核心，整套运行环境大约使用 8GB 内存。机器没有出现内存压力，体感也比我原先预期流畅得多。

但“跑通过”和“从此稳定可用”是两回事。后续原神又在一次启动时停在反作弊初始化阶段，日志出现 DLL 初始化失败；旧版兼容文件、游戏 6.7 更新和帧率解锁器都有嫌疑。这恰好说明了这类方案的真实状态：它可以很好玩，也随时可能因为上游更新重新变成研究项目。

## CrossOver 到底做了什么

CrossOver 不是虚拟机，也没有在后台运行一套完整 Windows。它基于 Wine，把 Windows API 调用动态转换成 macOS 可以处理的调用。Wine 官方把自己定义为 compatibility layer，而不是 emulator，这个区别也解释了为什么它通常比虚拟机更轻，但兼容性需要逐个应用打磨。[Wine 的官方介绍](https://www.winehq.org/about/)

在 Apple Silicon 上，整个链路可以粗略画成这样：

```text
Windows x86-64 游戏代码
        ↓ Rosetta 2
Apple Silicon 可执行指令

Windows / Win32 / NT API
        ↓ Wine / CrossOver
macOS 系统能力

DirectX 11 / 12
        ↓ DXMT / D3DMetal / DXVK
Metal → Apple GPU
```

CrossOver 里的 Bottle（容器）则像一个彼此隔离的迷你 Windows 环境，保存虚拟 C 盘、注册表、运行库和单独设置。我给两款游戏各建了一个容器，避免终末地的底层补丁污染原神环境。

图形后端最容易把人绕晕：DX11 是游戏选择的图形 API，DXMT、D3DMetal 和 DXVK 是 CrossOver 用来翻译它的后端。根据 CodeWeavers 的说明，DXMT 主要实现 Direct3D 11 到 Metal，D3DMetal 支持 DirectX 11/12，DXVK 则把 Direct3D 10/11 翻译到 Vulkan。[CrossOver 26 图形设置说明](https://support.codeweavers.com/en_US/advanced-settings-in-crossover-mac-26)

所以“游戏使用 DX11”和“CrossOver 使用 D3DMetal”并不矛盾。前者是输入，后者是翻译器。

## 终末地：难点在 Wine 更底层

终末地最开始的情况很典型：鹰角启动器可以安装、登录和下载游戏，点开始以后游戏本体却过不了保护壳和 ACE 反作弊初始化。

这次能够突破，关键是社区项目 [Endfield_FineWine](https://github.com/stoicswe/Endfield_FineWine)。它没有修改游戏画面或玩法，而是针对 CrossOver 26.2 的 Wine 重新构建了三个核心模块：

| 模块 | 大致职责 |
|---|---|
| `ntdll.so` | 异常、线程、计时和底层系统调用 |
| `kernel32.dll` | 常用 Windows 用户态 API |
| `ntoskrnl.exe` | Wine 提供的 Windows 内核接口 |

保护壳和反作弊会检查一些非常接近 Windows 内核的行为。Rosetta、Wine 与真正的 Windows 在少数指令异常、计时和接口实现上并不完全一样；检查结果不符合预期，游戏就会退出、报驱动错误，或者干脆陷入高 CPU 死循环。

补丁修正了 Rosetta 传递部分异常的方式，也补齐了 ACE 初始化会用到的一些内核接口。它并不是在 macOS 里加载真正的 Windows 内核驱动，而是让 Wine 提供一套足够接近预期的行为。

游戏本体跑起来以后，问题反而变得比较“普通”：

- DX12 可以进入，但部分图标和贴图显示异常；
- DX11 + D3DMetal 的画面更稳定；
- HiDPI 打开以后清晰很多，但 GPU 压力随之上升；
- 默认全屏会捕获鼠标，最后改成窗口化或无边框更适合 Mac；
- Wine 默认的修饰键映射不符合肌肉记忆，需要把 Option 和 Command 重新映射；
- 绕过启动器直达游戏时，还要补回启动器原本传入的中文、渠道和 DX11 参数。

最终的启动命令保留了三个关键参数：简体中文、强制 DX11 和国服渠道。平时直接打开游戏本体，需要更新时才回到鹰角启动器。

## 原神：难点在启动时序

原神走的是另一条路线。普通 CrossOver 可以运行米哈游启动器，但游戏本体会在反作弊驱动初始化时退出。社区方案需要使用与当前游戏版本匹配的兼容文件，并在启动瞬间临时阻断几个调度域名；检测到 `YuanShen.exe` 后，再恢复网络规则。

听起来像“加规则、启动、删规则”三步，实际最折磨人的是时序。

一开始我设置检测到进程后等待 8 秒恢复网络。它有时成功，有时卡在账号令牌登录；把等待拉到 20 秒，又正好撞上全局调度请求。其间还排查过 Surge、DNS、缓存、MSync 和 CrossOver 的线程同步。最后才意识到：固定等待时间本身就是脆弱的，只是之前机器和游戏启动速度刚好落在可用窗口里。

这段排查里最有意思的误导是 Surge。连接确实经过了增强模式的虚拟网卡，账号 SDK 也停在 `LoginByToken`，看上去很像网络问题。但域名实际走的是直连，连接已经收到数据，游戏线程却没有继续处理。关闭 MSync 后，高 CPU 忙循环变成低 CPU 等待，卡点仍然不变——症状改变了，根因没有消失。

后来我又加入 HoYoFPS，让它直接拉起 `YuanShen.exe` 并把目标设为 120 FPS。文件与开发者官方发布版本核对过哈希，但它仍然属于第三方内存修改工具，账号和稳定性风险需要单独看待。[HoYoFPS 项目](https://github.com/winTEuser/Genshin_StarRail_fps_unlocker)

这条路线最终做到了一次双击完成：

```text
原神.app
  → 临时准备启动环境
  → HoYoFPS 拉起游戏本体
  → 检测游戏进程
  → 恢复网络规则
```

真正需要更新游戏时，再打开 CrossOver 里的米哈游启动器。

## 最后为什么要再做两个 macOS App

游戏已经能跑以后，我最不满意的反而变成了启动体验。

从 CrossOver 点容器、找启动器、再点开始游戏，当然能用，但它仍然像在维护一个实验环境。我希望平时看到的就是两个游戏图标：双击，游戏启动；更新时才需要知道 CrossOver 的存在。

于是我写了一个很薄的原生启动助手。两款游戏共用同一份代码，通过各自的配置提供 Bottle 名称、可执行文件、工作目录和参数。它负责调用 CrossOver 的 Wine，完成必要的准备和清理，然后退出；外层 App 自己不常驻 Dock，也不包含游戏本体。

这个小东西顺手解决了不少细节：

- 不再误开卸载程序或 Windows 启动器；
- 保证终末地始终带着 DX11、中文和渠道参数；
- 原神的临时网络规则即使超时也会清理；
- 使用游戏本体图标，而不是启动器图标；
- 外层助手不额外占一个 Dock 位置；
- 两款游戏的更新入口和日常入口彻底分开。

从体验上看，这一步甚至比多榨出几帧更重要。折腾的最终目的不是让启动步骤变得更复杂，而是把复杂度藏起来。

## GPTK 4 会让一切自动变好吗

Apple 最新的 Game Porting Toolkit 4 已经支持在评估环境中测试 Metal 4，也提供了更完整的移植、调试和性能分析工具。[Apple Game Porting Toolkit 4](https://developer.apple.com/cn/games/game-porting-toolkit/)

但安装新 macOS，不等于 CrossOver 里的所有游戏自动切换成 GPTK 4，也不等于 DX12 必然比 DX11 快。我的终末地测试就是一个很现实的反例：DX12 能进，贴图却不完整；DX11 理论上没那么“新”，实际画面反而正确。

兼容层的世界里，最新的路径未必是当前最好的路径。能稳定渲染、能正常退出、游戏更新后还容易修，往往比跑分更重要。

## 这次探索留下了什么

最初我只是想验证“Mac 现在是不是也能玩这两款游戏”，最后却一路碰到了 Wine、Rosetta 异常语义、图形 API 翻译、反作弊接口、线程同步、网络时序、macOS 权限和原生 App 打包。

它们最后确实跑起来了，而且在 M1 Max 上的实际表现足以让我意外。但我也不会把这套东西包装成长期稳定的一键方案：

1. 两款游戏都没有官方支持这种 macOS 运行方式；
2. 游戏、CrossOver 或 macOS 更新都可能让方案失效；
3. 反作弊兼容文件和帧率解锁工具存在账号风险；
4. 为旧版 CrossOver 构建的 Wine 模块不能直接塞进未知新版本；
5. 来源不明的 DLL、脚本和整合包不值得拿主账号尝试。

不过，对一次“想看看能不能做到”的尝鲜来说，这趟旅程已经值回票价。Mac 并没有突然变成最省心的游戏平台，但兼容层、图形翻译和社区补丁拼到一起以后，它能做到的事情确实比几年前多了很多。

至于下一次游戏更新后它们还会不会继续工作——大概又是下一篇折腾记录了。
