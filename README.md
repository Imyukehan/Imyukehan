# Imyukehan Blog

Khan 的个人博客，使用 Hexo、定制版 Icarus 主题和 Vercel。

- 线上地址：<https://blog.khan.moe>
- 文章源文件：`source/_posts/`
- 图片目录：`source/img/assets/<文章标题>/`
- 主题目录：`themes/icarus/`

## 本地写作

项目使用 Node.js 24。安装依赖后，可以通过以下命令完成日常写作：

```bash
npm install
npm run draft -- "文章标题"
npm run dev
```

预览确认后，将草稿移到正式文章目录：

```bash
npm run publish -- "文章文件名"
npm run check
```

也可以直接创建正式文章：

```bash
npm run new -- "文章标题"
```

推送到生产分支后，由 Vercel 自动构建和发布。

## 内容策略

博客中的 Markdown 是唯一原稿。后续分发到微博、小红书、X 等平台时，从原稿生成各平台需要的摘要、短帖、图片或长文版本，博客始终保留完整原文和固定链接。

当前计划：

1. 保留 Hexo 和自定义主题，恢复稳定更新。
2. 建立 Markdown 到博客及社交平台的半自动分发流程。
3. 形成更新频率后，再评估迁移到 Astro 的收益。

## 维护说明

- Hexo：7.3
- Icarus：基于 6.1.1 的定制版本
- Node.js：24
- 评论：旧 Gitalk 已停用，等待迁移到 GitHub Discussions 方案

升级 Icarus 时不要直接覆盖 `themes/icarus`。当前主题保留了自定义字体、深色模式、背景动画、双版本 Logo、B 站关注入口和版面宽度调整，需要单独做视觉回归。
