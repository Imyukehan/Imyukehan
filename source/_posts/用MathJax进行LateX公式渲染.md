---
title: 用MathJax进行LateX公式渲染
date: 2018-07-23 10:10:10
cover: /img/assets/用MathJax进行LateX公式渲染/thomas-t-OPpCbAAKWv8-unsplash.jpg
thumbnail: /img/assets/用MathJax进行LateX公式渲染/thomas-t-OPpCbAAKWv8-unsplash.jpg
categories: 
- 编程
tags:
- 编程
- 教程
- LateX
toc: true
---

理论上来说只要载入MathJax.js就行了，于是直接修改了模版header文件，结果发现了一个坑，就是我选的CDN加速服务不是https的，所以以https访问的话就没法加载，查了好多资料才发现原来是这个问题。

于是改用[BootCDN](http://www.bootcdn.cn)的加速服务，测试效果如下

$$ \LaTeX{} $$
$$ J\alpha(x) = \sum{m=0}^\infty \frac{(-1)^m}{m! \Gamma (m + \alpha + 1)} {\left({ \frac{x}{2} }\right)}^{2m + \alpha} $$

可以看到公式正确显示了。