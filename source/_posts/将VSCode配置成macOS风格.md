---
title: 将VSCode配置成macOS风格
cover: /img/assets/将VSCode配置成macOS风格/kevin-ku-w7ZyuGYNpRQ-unsplash.jpg
thumbnail: /img/assets/将VSCode配置成macOS风格/kevin-ku-w7ZyuGYNpRQ-unsplash.jpg
categories:
  - 教程
tags:
  - 教程
toc: true
date: 2023-08-21 08:35:25
---

## 效果展示

目标是将 VSCode 配置成 Xcode 风格的主题，主要步骤与用到的插件为：
1. 调整一些工具栏的位置（Customize UI）
2. 将侧栏设置为毛玻璃风格（Vibrancy Continued）
3. Icon 与代码字体调整（VSCode Icon Mac/SFMono Nerd Font）

<!-- more -->

![VSCode主题][1]

## 注意事项

想要达成以上效果，最重要的是获得内嵌的状态栏布局，可惜的是 Customize UI 无法在 VSCode 1.73 以上版本使用，GitHub 上的声明如下：

> Note: As of VSCode 1.74, this extension does not work, and will cause VSCode to crash. You can remain on 1.73.1 or prior to continue to use this extension. If you wish to move to a newer version of VSCode, you'll want to uninstall this extension before updating.

其原因为：

> VSCode added a build step that mangles all typescript private fields so they can't be reasonably accessed by Customize UI. This greatly reduces hooks that customize-ui can intercept and methods it can call.

> It might still be possible to change font size, but other layout changes are probably gone. Or at least made much more difficult.

所以需要安装1.73版本的 VSCode。[链接在此](https://code.visualstudio.com/updates/v1_73)

同时需要对应版本的 Vibrancy Continued 插件，这里选择了 1.1.11 版本，1.1.12及以后版本测试无法使用。另外安装时需要完全按照 Readme 要求来进行，否则会失败。

## 自定义过程

在安装 Vibrancy Continued 时，安装一旦完成，不要使用右下角系统弹框的重启，要使用 command palette 中的 Reload Vibrancy。

这里是我的设置配置，供参考：

```json
{
    "update.mode": "none",
    "window.titleBarStyle": "native",
    "terminal.integrated.gpuAcceleration": "off",
    "vscode_vibrancy.opacity": -1,
    "customizeUI.activityBar": "bottom",
    "customizeUI.statusBarPosition": "under-panel",
    "customizeUI.titleBar": "inline",
    "editor.fontFamily": "SFMono Nerd Font, Monaco, 'Courier New', monospace",
    "editor.fontSize": 16,
    "editor.minimap.enabled": false,
    "terminal.integrated.fontSize": 16,
    "terminal.integrated.fontFamily": "SFMono Nerd Font",
    "vscode_vibrancy.theme": "Dark (Only Subbar)",
    "workbench.productIconTheme": "macos-modern",
    "vscode_vibrancy.refreshInterval": 1000,
    "workbench.colorTheme": "MacOS Modern Dark - Ventura Xcode Default",
    "vscode_vibrancy.type": "dark",
    "workbench.iconTheme": "vscode-icons-mac"
}
```

字体我的设置为 SFMono Nerd Font，在 macOS 上比较协调。

## 总结
{% raw %}<article class="message is-info"><div class="message-body">{% endraw %}
⚠️注意：以下内容由ChatGPT自动生成
{% raw %}</div></article>{% endraw %}

这篇博客介绍了如何将 Visual Studio Code (VSCode) 配置成 macOS 风格的界面：

1. **工具栏位置调整（Customize UI）：** 使用 Customize UI 插件，可以调整工具栏的位置，以符合 macOS 风格的界面布局。

2. **侧栏毛玻璃效果（Vibrancy Continued）：** 使用 Vibrancy Continued 插件，将侧栏设置成毛玻璃效果，提升界面美观度。

3. **图标与字体调整：** 使用 VSCode Icon Mac 图标主题和 SFMono Nerd Font 代码字体，使界面更符合 macOS 风格。

作者分享了设置示例，包括界面布局、字体、图标主题等。要注意使用 VSCode 1.73 版本，并配合相应版本的 Vibrancy Continued 插件，按照博客中的指示进行设置。

[1]: /img/assets/将VSCode配置成macOS风格/截屏2023-08-21.png
