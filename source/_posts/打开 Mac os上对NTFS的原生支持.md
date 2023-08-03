---
title: 打开 Mac os上对NTFS的原生支持
---

NTFS (New Technology File System)，是 WindowsNT 环境的文件系统，微软设计出来用于取代老旧的FAT格式（不支持4g以上的文件读写），并且保持了微软一贯以来的商业风格，并不公开该文件系统的详细定义与实现方式，所以Mac os自然是不能支持的，用bootcamp创建windows虚拟机后，分区只能读不能写入。
有意思的是，早在OS X 10.5的时候，苹果就加入了读写NTFS格式的原生支持，但是可能是由于版权纠纷，把这个功能给屏蔽掉了，所以完全没有必要花¥139去买NTFS for mac这个软件，只需要自己开启就好了。

1. 打开terminal，用`diskutil list`命令查看磁盘信息，记住磁盘名。
  ![](https://ws4.sinaimg.cn/large/006tNc79gy1filbun08afj31ki12gadp.jpg)
2. 打开`/etc/fstab`文件,写下
```
LABEL=磁盘名 none ntfs rw,auto,nobrowse
```
如果你的名字里面有空格键，就需要用\040的意思是代替空格键，如：BOOT/040CAMP
3. 添加磁盘快捷方式到桌面
```
sudo ln -s /Volumes/BOOTCAMP ~/Desktop/BOOTCAMP
```
或者
```
sudo ln -s /Volumes ~/Desktop/Volumes
```
一步到位，之后所有的外挂磁盘都会显示在Volumes文件夹内
> mbp 2016实测读写速度1.5Gb/s，接近满速了