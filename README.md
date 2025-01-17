# fast-poster通用海报生成器

#### 介绍

在线体验：[https://poster.prodapi.cn/](https://poster.prodapi.cn/#from=tour)

`fast-poster`通用海报生成器，一分钟完成海报开发。


#### 特性

- 快速：三步完成海报开发工作：`启动服务` > `编辑海报` > `生成代码`
- 简单：组件丰富、支持拖拽、复制、所见即所得、下载等功能。
- 动态：无需更改代码，直接在编辑器修改海报即可获得最新的海报。

#### 效果图

![输入图片说明](https://images.gitee.com/uploads/images/2021/0615/082012_7d54dbf7_301987.jpeg "WX20210615-081039.jpg")


#### 安装

1. 运行命令: 
```bash
docker run --name fast-poster -p 9001:9001 tangweixin/fast-poster
```

2.  打开浏览器: [http://127.0.0.1:9001/](http://127.0.0.1:9001/)

#### 使用说明

1.  编辑海报：
点击 [新建] 按钮，在 [海报设置] > 背景图⽚ ，点击 [上传] ⼀个海报背景图。
点击所需的控件【⽂本、⼆维码、头像、图⽚】，拖动调整位置，设置相关参数。
点击 效果预览 ，可以实时查看最终⽣成的效果。

2.  获取代码：
点击 [代码] ，可以查看相关的接⼝调⽤代码。

![输入图片说明](https://images.gitee.com/uploads/images/2021/0615/082035_96001430_301987.jpeg "WX20210615-081414.jpg")

3.  效果预览

![输入图片说明](https://images.gitee.com/uploads/images/2021/0615/082128_c7afb0fd_301987.jpeg "WX20210615-082049.jpg")

#### 参与贡献

* Thomas
* Alex

#### 赞赏

你的一点赞赏，是作者坚持的动力。(多少都是心意😁)


![输入图片说明](https://images.gitee.com/uploads/images/2021/0609/152314_a6c2dbc5_301987.jpeg "微信.jpg")

#### 项目背景

`fast-poster`海报生成器，是经过众多电商项⽬后，由于经常遇到需要⽣成海报的需求，所以特别开发的⼀款⼯具。

期间也参考了很多类似项⽬，最开始⽤ `Java` 实现。后⾯发现海报效果不是特别理想，达不到像素级要求。最后使⽤ `Python` 全⾯重构，效果⽐较满意。

现在已经服务了好⼏个电商项⽬，多个项⽬有`33W+`⽤户，通过过⽣产的考验，稳定可靠。

如果⼤家在使⽤过程中，发现有任何问题，欢迎添加 微信 进⾏反馈。


#### 软件架构


技术栈
* `Python`
* `Vue`

客户端调用支持`Java` `Python` `cURL` `JS` 等可以发送`HTTP`请求的语言.



