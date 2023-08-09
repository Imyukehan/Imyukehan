---
title: 让Typecho支持emoji表情
date: 2019-08-03 14:20:01
cover: /img/assets/让Typecho支持emoji表情/count-chris-hQNFPZK8F80-unsplash.jpg
toc: true
---

所谓Emoji就是一种在Unicode位于`\u1F601-\u1F64F`区段的字符。

在服务器根目录下查看config.ini.php可以发现typecho默认使用的是utf-8编码，而在 MySQL 中，`UTF-8`只支持最多 3 个字节，而 emoji 是 4 个字节，这个显然超过了目前常用的`UTF-8`字符集的编码范围`\u0000-\uFFFF`。

<!-- more -->

所以只要将默认的数据库编码更改为`utf8mb4`即可
> 注：utf8mb4在PHP5.5后才支持

## 操作步骤

### 1. 修改数据库编码

进入`PhpMyadmin`,选择typecho数据库，操作-->排序规则-->选择utf8mb4_unicode_ci然后执行。

### 2. 修改所有表的编码

执行以下sql语句

```sql
alter table typecho_comments convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table typecho_contents convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table typecho_fields convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table typecho_metas convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table typecho_options convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table typecho_relationships convert to character set utf8mb4 collate utf8mb4_unicode_ci;
alter table typecho_users convert to character set utf8mb4 collate utf8mb4_unicode_ci;
```

### 3. 修改数据库配置文件

把服务器根目录下`config.inc.php`文件这一行

```
'charset'   =>  'utf8', 
```

修改为

```
'charset'   =>  'utf8mb4', 

```

然后typecho就可以使用emoji表情了。

😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😙😚☺️🙂🤗😇

> 推荐一个Emoji表情网站 [http://getemoji.com/](http://getemoji.com/) 方便寻找需要的emoji