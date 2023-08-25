---
title: 设置VSCode为hexo博客插入图片
cover: /img/assets/设置VSCode为hexo博客插入图片/will-h-mcmahan-S3JdHNXSfnA-unsplash.jpg
thumbnail: /img/assets/设置VSCode为hexo博客插入图片/will-h-mcmahan-S3JdHNXSfnA-unsplash.jpg
categories:
  - null
tags:
  - null
toc: true
date: 2023-08-24 11:46:28
---

在 Hexo 中，默认图片引入路径为 source/ 文件夹下，但是如果使用 VSCode 默认插入路径，则会插入到 _posts/ 文件夹下。

<!-- more -->

在设置中，修改 `markdown.copyFiles.destination`，可以这样设置：

```javascript
"markdown.copyFiles.destination": {
  "/source/_posts/*": "../img/assets/${documentBaseName}/"
}
```

其中 `/source/_posts/*` 代表文件源路径，可以用 ** 代表文件夹通配符，*代表文件，`../img/assets/${documentBaseName}/` 代表图片目的路径，可选值为：

 - ${documentFileName} - Markdown 文档的完整文件名，例如: readme.md。
 - ${documentBaseName} - Markdown 文档的基名，例如: readme。
 - ${documentExtName} - Markdown 文档的扩展，例如: md。
 - ${documentDirName} - Markdown 文档的父目录的名称。
 - ${documentWorkspaceFolder} - Markdown 文档的工作区文件夹，例如: /Users/me/myProject。如果文件不属于工作区，则与 {documentDirName} 相同。
 - ${fileName} - 已删除的文件的文件名，例如: image.png。

<a class="tag is-dark is-medium" href="https://unsplash.com/photos/S3JdHNXSfnA" target="_blank">
<span class="icon"><i class="fas fa-camera"></i></span>&nbsp;&nbsp;
Cover Photo by Will H McMahan on Unsplash</a>