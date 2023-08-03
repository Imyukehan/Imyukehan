---
title: Hello World
---
# 给SublimeText3添加zsh终端命令支持

1. 命令行添加如下内容(如果提示~/bin文件夹不存在就新建一个)
```shell
sudo ln -s /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/bin/subl
```
2. 利用alias命令将subl设置为打开文本文件命令的别名
```shell
alias subl="'/Applications/SublimeText.app/Contents/SharedSupport/bin/subl'"
alias nano="subl"
export EDITOR="subl"
```
![oh-my-zsh][1]


[1]: https://ws2.sinaimg.cn/large/006tNc79gy1fhji0rhkioj31d00mutc5.jpg