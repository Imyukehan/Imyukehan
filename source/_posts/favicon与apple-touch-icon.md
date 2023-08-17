---
title: favicon与apple-touch-icon
date: 2019-12-01 09:55:53
cover: /img/assets/favicon与apple-touch-icon/alexander-shatov-mr4JG4SYOF8-unsplash.jpg
thumbnail: /img/assets/favicon与apple-touch-icon/alexander-shatov-mr4JG4SYOF8-unsplash.jpg
categories: 
- 编程
tags:
- 编程
- web
toc: true
---

在根目录下添加 apple-touch-icon.png 可以让safari读取作为标签图标

```html
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png"/>
```
<!-- more -->

![apple-touch-icon][1]
在header下添加

```html
<link rel="icon" type="image/x-icon" href="favicon.ico">
```
可以指定网页的小图标


[1]: /img/assets/favicon与apple-touch-icon/截屏2023-08-09.jpg