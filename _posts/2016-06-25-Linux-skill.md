---
layout: post
title:  "Linux技能大全"
date:   2016-06-25 23:35:00
categories: 编程语言
tags: Linux linux Shell yaml github 文件服务 vscode crontab curl post ssh 加密 mac 苹果 隧道 pssh pdsh
excerpt: Linux使用技能总结，持续更新
mathjax: true
permalink: /linux
---
* content
{:toc}

- 汇总linux下开发知识

# Linux系统

- 良好的 Linux 素养会让你在日常的工作中如鱼得水，在命令行里体会流水般的畅快感。

![](https://raw.githubusercontent.com/woaielf/woaielf.github.io/master/_posts/Pic/1709/170915-1.png)
![](https://raw.githubusercontent.com/woaielf/woaielf.github.io/master/_posts/Pic/1709/170915-2.png)
![](https://raw.githubusercontent.com/woaielf/woaielf.github.io/master/_posts/Pic/1709/170915-3.png)

## 内核

- [漫画图解linux内核-原版](http://www.techug.com/post/carton-inside-the-linux-kernel.html)，[国内源](https://blog.csdn.net/passerbysrs/article/details/81604498)
- 解读一幅来自 TurnOff.us 的漫画 “[InSide The Linux Kernel](http://turnoff.us/geek/inside-the-linux-kernel/)[1]” 

![](https://static.oschina.net/uploads/space/2017/0206/122129_TqPO_12.jpeg)

## 环境

### 操作系统信息

```shell
cat /etc/issue
# Debian GNU/Linux 10 \n \l
cat /etc/redhat-release # redhat 专用
cat /proc/version
# Linux version 5.4.56.bsk.10-amd64 (root@n14-042-020) (gcc version 8.3.0 (Debian 8.3.0-6)) #5.4.56.bsk.10 SMP Debian 5.4.56.bsk.10 Fri Sep 24 12:17:03 UTC 
uname -a 
# Linux n37-139-225 5.4.56.bsk.10-amd64 #5.4.56.bsk.10 SMP Debian 5.4.56.bsk.10 Fri Sep 24 12:17:03 UTC  x86_64 GNU/Linux
```

为什么ssh登录linux服务器后，bashrc里的变量没生效？非要单独source一遍？

### bash文件

bash的startup文件

Linux shell是用户与Linux系统进行交互的媒介，而bash作为目前Linux系统中最常用的shell，它支持的startup文件也并不单一，甚至容易让人感到费解。本文以CentOS7系统为例
- `/etc/profile`：登入时执行，The systemwide initialization file, executed for login shells
- `/etc/bash.bash_logout`：登出时执行，The systemwide login shell cleanup file, executed when a login shell exits
- `~/.bash_profile`：用户自定义，The personal initialization file, executed for login shells
- `~/.bashrc`：The individual per-interactive-shell startup file
- `~/.bash_logout`：The individual login shell cleanup file, executed when a login shell exits

此外，bash还支持~/.bash_login和~/.profile文件，作为对其他shell的兼容，它们与~/.bash_profile文件的作用是相同的。

备注：Debian系统会使用~/.profile文件取代~/.bash_profile文件，因此在相关细节上，会与CentOS略有不同。

#### .bashrc和.bash_profile之间的差异

[.bashrc与.bash_profile区别](https://www.myfreax.com/bashrc-vs-bash-profile/)
- 当Bash作为交互式登录shell调用时，将读取并执行.bash_profile
- 对于交互式非登录shell，则执行.bashrc。
- 仅应运行一次的命令应该使用.bash_profile ，例如自定义 \$PATH 环境变量。
- 将每次启动新Shell时应该运行的命令放在.bashrc文件中。 这包括您的别名和function，自定义提示，历史记录自定义等。

通常，~/.bash_profile包含以下类似于.bashrc文件来源的行。 这意味着每次您登录到终端时，都会读取并执行两个文件。

```shell
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi
```

大多数Linux发行版都使用`~/.profile`而不是`~/.bash_profile`。 所有Shell程序都读取~/.profile文件，而Bash仅读取~/.bash_profile文件。

如果系统上没有任何启动文件，则可以创建该文件。

### 登录顺序

bash的运行模式
- “登陆shell”启动时会加载“profile”系列的startup文件
  - “profile”系列的代表文件为~/.bash_profile，它用于“登录shell”的环境加载，这个“登录shell”既可以是“交互式”的，也可以是“非交互式”的。
- 而“交互式非登陆shell”启动时会加载“rc”系列的startup文件

总结：
- `交互式shell`是读取和写入用户终端的shell程序
  - 交互式shell程序可以是登录shell程序，也可以是非登录shell程序。
- 而`非交互式shell`程序是与终端无关的shell程序，例如**执行脚本**时。

CentOS规定了startup文件的加载顺序如下：

#### 交互式登陆shell

**登陆**过程：
1. 读取并执行`/etc/profile`文件；
2. 读取并执行`~/.bash_profile`文件；
  - 若文件不存在，则读取并执行`~/.bash_login`文件；
  - 若文件不存在，则读取并执行`~/.profile`文件；

当Bash作为交互式非登录shell程序调用时，它会从`~/.bashrc`中读取并执行命令（如果该文件存在并且可读)

**登出**过程：
1. 读取并执行`~/.bash_logout`文件；
2. 读取并执行`/etc/bash.bash_logout`文件；

#### 非交互式登陆shell

对于非交互式的登陆shell而言，CentOS规定了startup文件的加载顺序如下：

登陆过程：
1. 读取并执行`/etc/profile`文件；
2. 读取并执行`~/.bash_profile`文件；
  - 若文件不存在，则读取并执行`~/.bash_login`文件；
  - 若文件不存在，则读取并执行`~/.profile`文件；

与“交互式登陆shell”相比，“非交互式登陆shell”并没有登出的过程


[原文链接](https://blog.csdn.net/sch0120/article/details/70256318)


#### 登录历史

【2024-3-6】查看服务器登录历史

```sh
last
# 输出信息
root@singapore:~/wqw# last
root     pts/1        120.244.236.142  Wed Mar  6 11:32   still logged in
root     pts/1        120.244.236.142  Wed Mar  6 11:19 - 11:32  (00:13)
root     pts/4        114.251.196.89   Tue Mar  5 13:13 - 14:50  (01:36)
root     pts/4        2.59.151.97      Sun Mar  3 16:52 - 16:56  (00:03)
```


## Mac OS 技巧


### macbook 配置总结


| **功能** | **方法** | **备注** |
|----|:------|:---- |
| 终端用户名自定义 | 系统偏好设置->共享->编辑电脑名称  | - |
| 画图工具 OmniGraffle+Pro 6| [下载地址](http://www.onlinedown.net/soft/87746.htm),[注册码](http://blog.csdn.net/x_focus/article/details/41349623);[7下载地址（含许可证）](https://d11.baidupcs.com/file/890a1f15ffddb6f3c3dab4fdadb47912?bkt=p3-000080d1e545b74de7d8e2a7d8017edaf20c&xcode=ff73db6f0d13a10269722ca0706f4f2d57cb92d68ca6af42837047dfb5e85c39&fid=1610614513-250528-218454854633625&time=1494382563&sign=FDTAXGERLBHS-DCb740ccc5511e5e8fedcff06b081203-HpWzZufk4Ih1Y%2FFYHmSq25HYFyM%3D&to=d11&size=93883767&sta_dx=93883767&sta_cs=11417&sta_ft=dmg&sta_ct=5&sta_mt=0&fm2=MH,Yangquan,Netizen-anywhere,,hunan,ct&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=000080d1e545b74de7d8e2a7d8017edaf20c&sl=83034191&expires=8h&rt=pr&r=580566339&mlogid=3001796489994348567&vuk=1610614513&vbdid=502618811&fin=OmniGraffle+7.2+for+Mac.dmg&fn=OmniGraffle+7.2+for+Mac.dmg&rtype=1&iv=0&dp-logid=3001796489994348567&dp-callid=0.1.1&hps=1&csl=300&csign=SlvW2m2iS5Dhs4IYR0kvCbxY%2BwQ%3D&by=themis)  | 兼容viso，功能强大 |
|Mac Office 2016破解|操作简单，安装完mac office正式版后，下载破解文件，双击锁，就可以|[参考地址](http://www.jianshu.com/p/2172835cfb17)|
|Mac下安装Windows|[Mac电脑上用VMware Fusion安装Windows7](http://jingyan.baidu.com/article/54b6b9c0f8830f2d583b47ce.html)|提前下载vmware+Windows安装包，添加Windows虚拟机后默认无法启动，需要单独指定iso镜像位置，再重启即可|
| 画图工具OmniGraffle+Pro | [OmniGraffle Pro 7.19.2 中文破解版](https://macwk.lanzouo.com/i70Mawdk9mb)，[下载地址](http://www.onlinedown.net/soft/87746.htm),[注册码](http://blog.csdn.net/x_focus/article/details/41349623);[7下载地址（含许可证）](http://bbs.feng.com/forum.php?mod=viewthread&tid=10739827)  | 兼容viso，功能强大（【2017-12-6】注：7.4版才能用许可证，7.5以上不行） |
| 安装pip | sudo easy_install pip  | pip直接安装其他工具 |
|软件包管理器|homebrew安装（[参考地址](http://www.itbulu.com/macbook-wget-install.html)）；安装wget：brew install wget|brew安装命令：ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"|
| 翻墙 | 1.有代理ip的直接设置：网络->高级->代理->勾选网页代理+安全网页代理，输入服务器域名及端口，无需填入账号。<br>2.用[lantern下载](https://github.com/getlantern/forum/issues/833)，[蓝灯无限制版](https://github.com/JuncoJet/unlimited-landeng-for-win) | 备选方案很多，[汇总地址](https://github.com/bannedbook/fanqiang/wiki), [chromego](https://github.com/killgcd/chromego), [ss](https://ppt.qjzd.net/ppt-google-aireplane/#/9/2), [拥有一家小飞机是怎样的体验](https://github.com/kaiye/kaiye.github.com/issues/9)，[shadowsocks地址](https://order.shadowsocks.se)，【2019-07-31】撸油管、刷INS、访推特，完美支持高清1080P视频，无任何流量限制,真正免费的[旋风加速器](https://www.highspeeds.live/redirect?code=2881YPR) |
|vim颜色显示|1.vim ~/.vimrc <br>2.添加colorscheme desert;syntax on |vim [sublime颜色主题](http://www.cnblogs.com/fsjohnhuang/p/3911611.html)|
|vim开发环境|[vim IDE部署](https://github.com/wklken/k-vim)|其他主题包，[vim-go开发环境](http://blog.csdn.net/chosen0ne/article/details/40782991)|
|shell目录颜色显示|开启方法：编辑~/.bash_profile<br>增加：export CLICOLOR=1;export LSCOLORS=exfxaxdxcxegedabagacad|注：[如何在shell字符串中显示彩色字符？](http://7938217.blog.51cto.com/7928217/1651807/),显示白色：echo -e "\033[37m white \033[0m"|
|mac免密码远程登录|使用ssh创建rsa公钥密码。基本步骤：<br>1.ssh-keygen生成密钥(ssh-keygen -t rsa)  <br>2.复制密钥文件到远程机器(scp ~/.ssh/id_rsa.pub wangqiwen@ip.com:/home/wangqiwen/.ssh) <br>3.登录远程机器，修改文件权限(cd ~/.ssh && cat id_rsa.pub >> authorized_keys; chmod 644 authorized_keys;chmod 700 ~/.ssh/)|参考地址：[mac无密码登录](http://blog.csdn.net/cdut100/article/details/70277091),[Linux 下 SSH 命令实例指南](https://linux.cn/article-3858-1.html),[菜鸟学Linux命令:ssh命令 远程登录](https://blog.csdn.net/sky786905664/article/details/60580594)|
|ssh会话管理|[ssh配置文件实现别名快捷登录](http://blog.csdn.net/newjueqi/article/details/47293897)，【2018-9-29】[图解ssh及登录原理](https://www.toutiao.com/a6605433008616899076/?tt_from=mobile_qq&utm_campaign=client_share&timestamp=1538181445&app=news_article&utm_source=mobile_qq&iid=44328463468&utm_medium=toutiao_android&group_id=6605433008616899076)||
|chrome浏览器中右键失灵|双指触碰链接时，并未弹出右键菜单，而是“图片另存为”|解决办法：这是由于chrome浏览器上开启了鼠标手势，造成干扰，关闭或删除插件即可|
|chrome域名自动跳转|【2022-8-5】更改个人网站域名，恢复GitHub page地址，结果chrome浏览器自动跳转到老地址，其它浏览器正常|解决：[清除域名缓存](https://cloud.tencent.com/developer/article/1773432)；打开开发者工具（F12），选择 Network——Disable cache 即可|
|image not recognized|dmg文件无法安装，原因：文件损坏，dmg权限不允许任意来源的包；换浏览器|如何开启任意来源包？sudo spctl --master-disable|
|redis安装|brew install redis|使用方法：启动服务，redis-server，连接服务：redis-cli|
|mac mail客户端设置|连接163时，需要先去163邮箱开启pop3/imap选项，通过手机验证码设置连接密码；mail终端配置时填入的密码是连接密码（非登录密码！）|wqw3721|
|安装虚拟机|vmware安装，下载地址|vmware fusion 8 激活码：FY75A-06W1M-H85PZ-0XP7T-MZ8E8，ZY7TK-A3D4N-08EUZ-TQN5E-XG2TF，FG1MA-25Y1J-H857P-6MZZE-YZAZ6|
|Mac下运行Windows软件|（1）boot camp安装Windows虚拟机（win 10文件过大）；<br>（2）安装wine|步骤：（1）brew cask install xquartz<br>（2）brew install wine|
|Mac下无法安装第三方软件|软件源受限，需要打开|步骤：sudo spctl --master-disable，[参考方法](https://www.mobibrw.com/2019/20766)|
|java|官方[下载地址](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)|优先使用绿色版（tar.gz，非二进制的rpm）。环境变量配置方法：修改/etc/profile文件，在文件的最下边加入下边的文本：<br>export JAVA_HOME=/opt/jdk1.7; <br>export CLASSPATH=.:$JAVA_HOME/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar;<br>export PATH=$JAVA_HOME/bin:$PATH|
|Web服务|[Mac OS 启用web服务](http://www.jianshu.com/p/d006a34a343f),[简网教程](http://www.jianshu.com/p/d006a34a343f)||
|linux 服务器mail|mail command not found|解决方法：sudo yum install mailx;echo "test" (竖线) mail -s "content" wangqiwen@p1.com|
|linux下安装http服务|安装httpd|1.yum install httpd -y <br>2.随系统启动:chkconfig httpd on <br>3.开启Apache:service httpd start|
|terminal下如何开启应用？|用open命令开启（open .用finder打开当前位置目录；<font size=4 color='res'>open file自动调用默认程序打开文件;</font>say hello语音说话），可以传参，备注：放到别命中，alias view='open /Applications/Preview.app'或alias edit='open /Applications/Sublime\ Text.app'|open /Applications/Sublime\ Text.app README.md|
|shell美化|[Oh My ZSH!](http://ohmyz.sh/)|安装：sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"|
|刻盘|[Etcher](https://etcher.io/)全平台工具|操作过程极其简单|
|移动硬盘无法写入|原因：mac不支持ntfs格式，需要安装特殊软件：[ntfs for mac](http://www.ntfsformac.cn/xiazai.html)||
|mac显示当前路径|命令：defaults write com.apple.finder _FXShowPosixPathInTitle -bool YES|顶栏出现路径，还可以点击定位到子目录|
|mac当前位置打开终端|[命令](https://jingyan.baidu.com/article/ce436649281a293773afd3d8.html)|[mac右键新建文件](https://zhuanlan.zhihu.com/p/39600106)|
|mac下excel打开csv中文乱码|原因是mac底下中文一律utf8编码，而excel文档默认中文是gbk编码，需要单独设置下才行。[地址](https://www.zhihu.com/question/20562901)|亲测有效|
|mac下锁屏|系统自带锁屏快捷键：Ctrl + Command + Q<br>Ctrl+Shift+Power: 关闭屏幕<br>Cmd+Opt+Power: 睡眠 (sleep)<br>Cmd+Ctrl+Power: 重启 (restart)|windows下：Windows + L|
|【2022-7-19】|pdf文档拆分/合并|mac分拆pdf方法：mac自带的预览软件，用侧边栏设置看缩略图，然后点选pdf，然后复制、黏贴，或者直接拖到桌面，放开鼠标，就会在桌面生成一份后缀带加了带“（拖移项目）”的文件。；<br>合并方法：打开一个pdf，“插入”→导入另一个文档→保存即可|
|【2018-1-11】|[网易mumu模拟器](http://mumu.163.com/)||
|【2018-1-11】|[mac下安装adb，调试Android](https://www.jianshu.com/p/1b3fb1f27b67)|brew cask install android-platform-tools|
|【2018-6-25】|[crossover mac版](http://www.pc6.com/mac/111646.html)|mac上运行ie浏览器,[使用步骤](https://jingyan.baidu.com/article/dca1fa6f78ea48f1a5405210.html)|
|【2018-12-25】|复制高亮代码到ppt|方法：notepad++或sublime text插件SublimeHighlight，[详见](https://www.v2ex.com/t/258518), Plugin commands - Copy Text with Syntax Highlighting|
|【2019-05-07】|[pycharm专业版激活](https://blog.csdn.net/u014044812/article/details/86679150)||
|【2020-6-29】|[十款Windows命令行工具](https://www.cnblogs.com/onelikeone/p/10716424.html)|powercmd,xshell,consolez,git bash,全能王mobaxterm等|
|【2021-12-21】|markdown转ppt，[pandoc](https://www.cnblogs.com/wardensky/p/5194332.html)||
|【2021-12-31】|文档复制受限|右键开发者模式：<br>①从html源码中抠<br>②debugger里disable js代码即可获取纯文本|
|【2022-8-6】|vscode无法打开终端|解决：更改默认终端配置，“文件”→“首选项”→“设置”，弹出配置文件，按照[链接](https://blog.csdn.net/m0_57189842/article/details/120073595)修改接口|
|【2024-5-9】|vscode里编辑输入时，卡顿，延迟1-3s，尝试更改setting里各种参数，无效|解决：重启电脑|

【2022-11-22】windows 的图标打架效果，steam平台程序[the lcon battles](https://steamspy.com/app/2135980)，还可以设置成屏保，[效果](https://store.steampowered.com/app/2135980/The_Icon_Battles/), 仅 windows可用
- ![](https://media.st.dl.eccdnx.com/steam/apps/2135980/ss_8d535886b9b54808e86d617354906802e140c5da.600x338.jpg?t=1667389893)


原因：Github没有fork项目代码，或没加所在机器的sshkey（settings->deplot keys）

### 软件包 brew

[Homebrew](https://brew.sh/) 安装

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# 默认保存目录 /opt/homebrew/bin
# 添加到 ~/.bash_profile 中
export PATH="$PATH:/opt/homebrew/bin"
source ~/.bash_profile
# 安装工具包
brew install wget
```

### 鼠标、触摸板方向设置

【2023-7-31】mac用鼠标滚轮滚动方向相反
- 点击屏幕左上角的苹果标志，在下拉列表中选择“系统偏好设置”。
- 在打开的“系统偏好设置”窗口中，选择“鼠标”。
- 在打开的“鼠标”窗口中，将“滚动方向：自然”前面的勾去掉。 之后，再使用鼠标，就跟在windows中使用的一样。

### 终端启动 sublime text

自带命令行工具 subl, 便于在终端启动，不用点icon

```sh
# 安装sublime text
brew install sublimetext # 使用brew工具安装，Application下有显示，而单独下载安装不会
# 应用程序地址， 自带命令行工具 subl, 便于在终端启动
ls /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl
subl your_file # 快速办法
# 通用办法
open -a "sublime text" your_file # 单行命令
echo 'export PATH="/Applications/Sublime Text.app/Contents/SharedSupport/bin:$PATH"' >> ~/.bash_profile # 或导入路径
ln -s /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl # 或建立软连接

```


## 文件

[图解 Linux 最常用命令](https://www.toutiao.com/a6756106065248518664/)

### linux的目录结构

[linux的目录结构](https://p3-tt.byteimg.com/origin/pgc-image/ab3bdd7224a14682a35e60fe1ee802cf?from=pc)

![](https://p3-tt.byteimg.com/origin/pgc-image/ab3bdd7224a14682a35e60fe1ee802cf?from=pc)

下级目录结构
- bin (binaries)存放二进制可执行文件
- sbin (super user binaries)存放二进制可执行文件，只有root才能访问
- etc (etcetera)存放系统配置文件
- usr (unix shared resources)用于存放共享的系统资源
- home 存放用户文件的根目录
- root 超级用户目录
- dev (devices)用于存放设备文件
- lib (library)存放跟文件系统中的程序运行所需要的共享库及内核模块
- mnt (mount)系统管理员安装临时文件系统的安装点
- boot 存放用于系统引导时使用的各种文件
- tmp (temporary)用于存放各种临时文件
- var (variable)用于存放运行时需要改变数据的文件

### 文件权限

![图解 Linux 最常用命令](https://p3-tt.byteimg.com/origin/pgc-image/61a15ef57bd4472e949236049ce0bdda?from=pc)

linux文件权限的描述格式解读
- r 可读权限，w可写权限，x可执行权限（也可以用二进制表示 111 110 100 --> 764）
- 第1位：文件类型（d 目录，- 普通文件，l 链接文件）
- 第2-4位：所属用户权限，用u（user）表示
- 第5-7位：所属组权限，用g（group）表示
- 第8-10位：其他用户权限，用o（other）表示
- 第2-10位：表示所有的权限，用a（all）表示

![](https://p6-tt.byteimg.com/origin/pgc-image/3000314a51c249cab168bc400dd7c5f3?from=pc)

### 文件大小

du 是 Disk Usage 的缩写， Linux 上最受欢迎的命令之一，用来估算文件或目录占用的磁盘空间
- -a: 显示目录中所有文件以及文件夹大小
- -h: 以 Kb、Mb 、Gb 等易读的单位显示大小
- --si: 类似 -h 选项，但是计算是用 1000 为基数而不是1024
- -s: 显示目录总大小
- -d: 是 --max-depth=N 选项的简写，表示深入到第几层目录,超过指定层数目录则忽略
- -c: 除了显示目录大小外，额外一行显示总占用量
- --time: 显示每一个目录下最近修改文件的时间
- -t: 是 --threshold=SIZE 的简写，过滤掉小于 SIZE 大小的文件以及目录
- --exclude=PATTERN：过滤与 PATTERN 匹配的文件名或者目录名

[du命令详解](https://www.cnblogs.com/wanng/p/linux-du-command.html)

```shell
tree -d temp/ # 显示目录深度
du -d 1 temp/ # 指定目录深度（1级）
du --max-depth=2 temp/ # 最多两级
du temp # 默认情况下只显示目录大小，不显示文件大小。即执行du temp/ 只会显示目录大小
du -a temp/ # 子目录大小
du -b temp/ # 默认显示的大小只有一个孤零零的数字，没有单位
du -h temp/ # 易读方式显示
du -sh temp/ # 易读方式显示目录总大小，基数是 1024
du --si temp/ # --si 选项默认计算基数是 1000，更精确
```

### 文件颜色

颜色区分不同类型文件，[详见](https://blog.51cto.com/u_12039705/5077330)
- 白色：普通文件
- 蓝色：目录
- 绿色：可执行文件
- 浅蓝色：链接文件
- 黄色：设备文件
- 红色：压缩文件
- 红色闪烁：链接的文件有问题
- 灰色：其它文件

如果遇到linux系统上，文件夹与文件颜色无区分，非蓝色，可以这么做：

```shell
vim ~/.bashrc
# 添加以下代码
alias ls="ls --color" # 默认蓝色
export LS_COLORS='di=01;34;40' # 粗体-蓝色字体-黑色背景
# export LS_COLORS=${LS_COLORS}:'di=01;37;44' # 【可忽略】自定义：灰色字体，蓝色背景
source ~/.bashrc
```

更多颜色区分
- [如何在 Bash 中更改 LS 的颜色](https://cn.linux-console.net/?p=17495)

【2023-8-5】debian 系统下目录颜色恢复
- old方法不管用！
- [参考](https://wiki.debian.org/BashColors)

```sh
# ---- old -----
export CLICOLOR=1;
export LSCOLORS=exfxaxdxcxegedabagacad
# ------new-------
export LS_OPTIONS='--color=auto'
eval "`dircolors`"
alias ls='ls $LS_OPTIONS'

source /etc/bash.bashrc; source ~/.bashrc
```


### 时间戳

[Linux下文件的三种时间标记](https://www.cnblogs.com/cherishry/p/5885098.html)

三种时间戳
- **访问**时间：读一次文件的内容，这个时间就会更新。比如more、cat等命令。ls、stat命令不会修改atime
- **修改**时间：修改时间是文件内容最后一次被修改的时间。比如：vim操作后保存文件。ls -l列出的就是这个时间
- 状态**改动**时间是该文件的inode节点最后一次被修改的时间，通过chmod、chown命令修改一次文件属性，这个时间就会更新。

stat字段说明及ls命令查询时间戳

| column | column | column|column|
|--------|--------|
| 字段 | 说明 |例子|ls(-l)|
|st_atime| 文件内容最后访问时间 |read|-u|
|st_mtime|文件内容的最后修改时间|write|缺省|
|st_ctime|文件状态的最后更改时间|chown、chmod|-c|

touch命令修改文件时间
- -a 修改文件的存取时间
- -c 不创建文件file
- -m 修改文件file的修改时间
- -r ref_file 将参照文件ref_file相应的时间戳的数值作为指定文件file时间戳记的新值
- -t time 使用指定时间值time作为指定文件file相应时间戳的新值，此处的time规定如下形式的十进制数

```shell
#!/bin/bash
stat filename # 显示三种时间戳
stat -c %Y log_cron.txt  # 获取最后修改的时间戳
date +%s -d "2022-01-04 09:00:17" # 字符串转时间戳

# 时间戳比较
date1="2008-4-09 12:00:00"
date2="2008-4-10 15:00:00"
t1=`date -d "$date1" +%s`
t2=`date -d "$date2" +%s`
if [ $t1 -gt $t2 ]; then
    echo "$date1 > $date2"
elif [ $t1 -eq $t2 ]; then
    echo "$date1 == $date2"
else
    echo "$date1 < $date2"
fi

# 过期删除功能（超过两分钟）
dir=`ls /root/20160705/`
DIR_PATH="/root/20160705/"
for fi in $dir
do
    FILE_NAME=${DIR_PATH}${fi}
    echo $FILE_NAME
    a=`stat -c %Y $FILE_NAME`
    b=`date +%s`
    if [ $[ $b - $a ] -gt 120 ];then
       echo "delete file:$FILE_NAME"
       rm -rf $FILE_NAME
    fi
done
 
echo "done"
```

### 软连接

如何建立软链接？
- 大文件，复制多份不环保

```sh
# (1) 创建
ln –s  /var/www/test(源)   /var/test(目标)
# 将/source/file1目录链接到./file
ln -s /source/file1 ./file
# [2024-4-25] 将远程大文件链接到本地小文件
ln -s /mnt/bn/flow-algo-intl/zhouzefan/aidp_result/20240331/20240331_witheval.json 20240331_witheval.json
du -sh 20240331_witheval.json # 4k
less 20240331_witheval.json # 内容正常
# (2) 修改
# 将./file的链接目录改成/source/file2
ln -snf /source/file2 ./file
# (3) 删除
rm -rf file
rm -rf file/ # 目录
```


### 文件操作命令

[文件操作命令](https://p3-tt.byteimg.com/origin/pgc-image/6fe9b14521964698aad985d270cf6d9b?from=pc)
- ![](https://p3-tt.byteimg.com/origin/pgc-image/6fe9b14521964698aad985d270cf6d9b?from=pc)
- ![](https://p1-tt.byteimg.com/origin/pgc-image/dba5dffe4dcd446987f9b252f0b21c50?from=pc)
- ![](https://p1-tt.byteimg.com/origin/pgc-image/80d9bc3abcf34b3eb7efc9655698e6f6?from=pc)



```sh
# 复制文件, vi ~/.bashrc 中 alias cp='cp -i'
cp -rf zongguofeng linuxzgf # 遇到重复文件时，需要挨个提示
# 免提示
\cp -rf zongguofeng linuxzgf
```


### 解压命令

如下：
- (1) `*.tar` 用 `tar –xvf` 解压
- (2) `*.gz` 用 `gzip -d` 或者 `gunzip` 解压
- (3) `*.tar.gz` 和 `*.tgz` 用 `tar –xzf` 解压
- (4) `*.bz2` 用 `bzip2 -d` 或者用 `bunzip2` 解压
- (5) `*.tar.bz2` 用 `tar –xjf` 解压
- (6) `*.Z`用 `uncompress` 解压
- (7) `*.tar.Z` 用 `tar –xZf` 解压
- (8) `*.rar` 用 `unrar e` 解压
- (9) `*.zip` 用 `unzip` 解压
- (10) `*.xz` 用 `xz -d` 解压
- (11) `*.tar.xz` 用 `tar -zJf` 解压


文件压缩
- .tar 使用tar命令压缩或解压
- tar cvfz archive.tar.gz dir/
- tar xvfz. archive.tar.gz
- .bz2 使用bzip2命令操作
- .gz 使用gzip命令操作
- .zip 使用unzip命令解压
- .rar 使用unrar命令解压
- ![](https://p3-tt.byteimg.com/origin/pgc-image/0ffce7c93b324bed86a2e5dabdf92049?from=pc)

```sh
.bz2 
　　解压1：bzip2 -d FileName.bz2 
　　解压2：bunzip2 FileName.bz2 
　　压缩： bzip2 -z FileName 

.tar.bz2 
　　解压：tar jxvf FileName.tar.bz2        或 tar --bzip xvf FileName.tar.bz2 
　　压缩：tar jcvf FileName.tar.bz2 DirName 
```

### 中文乱码

linux 文件里中文乱码

```shell
echo "$LANG"
locale # 显示的字体中，没有zh cn，意味着没有中文语言
locale -a | grep "zh_CN"
# zh_CN
# zh_CN.gb18030
# zh_CN.gb2312
# zh_CN.gbk
# zh_CN.utf8

# 下载安装中文语言包
sudo yum groupinstall "fonts"
yum groupinstall chinese-support # 或
# 设置中文字体
LANG="zh_CN.UTF-8"
```

【2023-2-13】linux系统终端中文显示异常（方块或一堆？？），vim显示正常
- 修复方法
- 参考：[CentOS命令行中文显示方块](https://www.cnblogs.com/itfat/p/16009251.html)

```sh
echo 'export LC_ALL="zh_CN.UTF-8"' >> /etc/profile
source /etc/profile
echo 'LANG="zh_CN.UTF-8"' > /etc/locale.conf
source /etc/locale.conf
```

#### debian系统中文乱码

[Debian系统安装中文字体]()

以上方法在debian系统中无效，因为yum无法正常使用，总是提示libssl.so问题

```shell
# error: libssl.so.1.0.0: cannot open shared object file: No such file or directory
```

## 常用命令

- [linux常用命令脑图](https://www.cnblogs.com/hzg110/p/6914963.html)
- ![](https://images2015.cnblogs.com/blog/31127/201705/31127-20170530141401383-1329040140.png)

- [linux命令汇总](https://www.toutiao.com/w/i1694976027465741/)
- ![](https://p6.toutiaoimg.com/img/tos-cn-i-0022/057f03b362234ad5a702ad00c5f9f797~tplv-obj:975:1280.image?from=post)

### 账户管理

Linux 系统中，具有最高权限的用户——root。
- root 用户是系统中**唯一**的一个**超级**管理员，拥有了系统中的所有权限，可以执行任何想要执行的操作，也正因为如此，处于安全考虑，一般情况下不推荐使用 root 用户进行日常使用。
- root 用户所在的用户组称为 “root组”，处于 root 组的普通用户，能够通过 sudo 命令获取 root 权限。

Linux 将用户账号、密码等相关的信息分别存储在四个文件夹下：
- `/etc/passwd` —— 管理用户UID/GID重要参数
  - 账号名称 : 密码 : UID : GID : 用户信息说明列 : 主文件夹 : shell
  - root : x : 0 : 0 : root : /root : /bin/bash
  - 密码项显示 “x” 是出于安全考虑，Linux 将密码信息移到 /etc/shadow 进行存储；
- `/etc/shadow` —— 管理**用户密码**
  - 账号名称 : 密码 : 最近改动密码的日期 : 密码不可被改变的天数 : 密码需要重新更改的天数 : 更改提醒天数 : 密码过期后账号的宽限时间 : 账号失效日期 : 保留
  - root : (字符串，此处打码) : 200 : 0 : 99999 : 7 : : :
- `/etc/group` —— 管理**用户组**相关信息
  - 用户组名称 : 用户组密码 : GID : 此用户组包含的账号名称
  - root : x : 0 : root
- `/etc/gshadow` —— 管理用户组**管理员**相关信息
  - 用户组名 : 密码 : 用户组管理员账号 : 该用户组包含的账号名称
  - root : : : root

修改文件权限

```sh
# 格式
chown -R owner_name:group_name folder_name
chown -R new_owner_name directory1 directory2 directory3 # 多个目录
# 示例
sudo chown wqw test_dir # 修改文件所属权限（不含目录子文件）
sudo chown -R wqw test_dir # 递归修改文件所属权限
```

`adduser` 与 `useradd` 在一些方面存在不同。
- useradd 创建用户，但是不创建密码等其他用户信息，需要使用 passwd 设置密码才能使用；而 adduser 能通过交互界面，由用户直接输入密码等，设置用户信息。
- useradd 默认不在 /home 下创建用户同名的主文件夹，而 adduser 默认创建。
- useradd 是一个命令，而 adduser 被理解为一个 “简单的应用程序”。

```shell
# 查询用户信息
id <user> # 展示指定user的UID、GID、用户组信息等，默认为当前有效用户
who am i  # 等同于 who -m，仅显示当前登录用户相关信息
whoami    #   仅显示当前有效用户的用户名
w         # 展示当前正在登录主机的用户信息及正在执行的操作
who       # 展示当前正在登录主机的用户信息
last <user>  # 展示指定用户的历史登录信息，默认为当前有效用户
lastlog -u <user> # 展示指定用户最近的一次登录信息，默认显示所有用户

useradd # 新增用户，只是创建了一个用户名，如 （useradd  +用户名 ），它并没有在/home目录下创建同名文件夹，也没有创建密码，因此利用这个用户登录系统，是登录不了的
useradd -m wqw  # 添加用户：
useradd -g nginx -M nginx # -M 参数用于不为nginx建立home目录

passwd wqw # 设置密码
passwd -d wqw # root权限下清楚用户wqw的密码
passwd -l hadoop # 锁定用户hadoop不能更改密码；
passwd -u hadoop # 解除锁定用户hadoop不能更改密码；
passwd -S hadoop # 查询hadoop用户密码状态
# ------ 用户切换 -------
su wqw # 切换用户
sudo -i -u aisearch # 【2022-1-16】root下切换账户
userdel  -r  wqw # 删除用户
# 类似useradd，但adduser更实用，交互式创建用户
adduser tommy # 添加一个名为tommy的用户，
#passwd tommy  # 修改密码
# 赋予root权限： 修改 /etc/sudoers 文件，找到下面一行，把前面的注释(#)去掉
#    %wheel ALL=(ALL)    ALL
# 修改用户，使其属于root组(wheel)
usermod -g root tommy
# 用户组的添加和删除：
groupadd testgroup # 组的添加
groupdel testgroup # 组的删除
```

sudo
- 普通用户可以通过 sudo 命令，使用 root 用户权限来执行命令。
- 当然，不是所有的用户都能执行 sudo 命令的，而是在 /etc/sudoers 文件内的用户才能执行这个命令。

sudo 的执行流程大致为：
- 系统到 /etc/sudoers 下检查用户是否有执行 sudo 的权限
- 若有 sudo 权限，则需要输入本用户的密码（root 用户执行 sudo 不需要密码）
- 验证成功后执行命令
- 因此，关键在于执行 sudo 的用户是否存在于 /etc/sudoers 文件内

【2023-2-3】root 账户下输入 visudo 即可进入sudo配置，这个命令要比 vim /etc/sudoers 要好很多

```sh
# 找到这行
root  ALL=(ALL)    ALL
# 复制出来，改成新用户
wqw  ALL=(ALL)    ALL
# 保存，退出
# 测试
su liudiwei
cd ~
sudo mkdir test
```

[普通用户添加root权限方法总结](https://cloud.tencent.com/developer/article/1725832)
- 用adduser命令添加一个普通用户 tommy
- 赋予root权限
  - 方法一： 修改 /etc/sudoers 文件，找到下面一行，把前面的注释（#）去掉
    - \%wheel ALL=(ALL) ALL 
    - 修改用户，使其属于root组（wheel），命令如下：usermod -g root wqw 
    - 命令 su – ，即可获得root权限进行操作
  - 方法二： 修改 /etc/sudoers 文件，找到下面一行，在root下面添加一行
    -  tommy ALL=(ALL) ALL 
  - 方法三： 修改 /etc/passwd 文件，找到如下行，把用户ID修改为 0
    - tommy:x:500:500:tommy:/home/tommy:/bin/bash 
    - tommy:x:0:500:tommy:/home/tommy:/bin/bash 

su 是最简单的用户切换命令，通过该命令可以实现任何身份的切换，包括从普通用户切换为 root 用户、从 root 用户切换为普通用户以及普通用户之间的切换。
- 普通用户之间切换
- 普通用户切换至 root 用户，都需要知晓对方的密码，只有正确输入密码，才能实现切换；
- 从 root 用户切换至其他用户，无需知晓对方密码，直接可切换成功。

su \[选项] 用户名
1. -：当前用户不仅切换为指定用户的身份，同时所用的工作环境也切换为此用户的环境（包括 PATH 变量、MAIL 变量等），使用 - 选项可省略用户名，默认会切换为 root 用户。
1. -l：同 - 的使用类似，也就是在切换用户身份的同时，完整切换工作环境，但后面需要添加欲切换的使用者账号。--login加了这个参数之后，就似乎是重新登陆为该使用者一样，大部分环境变量（例如HOME、SHELL和USER等）都是以该使用者（USER）为主，并且工作目录也会改变。假如没有指定USER，缺省情况是root。
1. -p：表示切换为指定用户的身份，但不改变当前的工作环境（不使用切换用户的配置文件）。
1. -m：和 -p 一样；--preserve-environment：执行su时不改变环境变数。
1. -c 命令：仅切换用户执行一次命令，执行后自动切换回来，该选项后通常会带有要执行的命令。
1. -f ， --fast：不必读启动文件（如 csh.cshrc 等），仅用于csh或tcsh两种Shell。
1. -c command：变更账号为USER的使用者，并执行指令（command）后再变回原来使用者。
1. USER：欲变更的使用者账号，ARG传入新的Shell参数

```shell
su root # 切换到root，但是没有切换环境变量。注意：普通用户切换到root需要密码
su -root # "-"代表连带环境变量一起切换，不能省略
# 密码： <-- 输入 root 用户的密码
whoami # lamp 当前我是lamp
su - -c "useradd user1" root
# 不切换成root，但是执行useradd命令添加user1用户
grep "user1" /etc/passwd
# userl:x:502:504::/home/user1:/bin/bash
su - lamp1 # Password:   <--输入lamp1用户的密码 # 切换至 lamp1 用户的工作环境
whoami # lamp1
# 什么也不做，立即退出切换环境
exit # logout
whoami # lamp
```

su 命令时，有 - 和没有 - 是完全不同的
- \- 选项表示在切换用户身份的同时，连当前使用的环境变量也切换成指定用户的
- 不使用 su - 的情况下，虽然用户身份成功切换，但环境变量依旧用的是原用户的，切换并不完整。

echo \$PATH 命令看一下su和su -以后的环境变量有何不同
- su 后面不加用户是默认切到 root
- su username是不改变当前变量
- su - username是改变为切换到用户的变量

### 系统命令

- [系统常用命令](https://p6-tt.byteimg.com/origin/pgc-image/15e52c0fb24a444d99784798bbf6aba3?from=pc)
  - ![](https://p6-tt.byteimg.com/origin/pgc-image/15e52c0fb24a444d99784798bbf6aba3?from=pc)
  - ![](https://p1-tt.byteimg.com/origin/pgc-image/2107086df3244564a9ca41908b482da5?from=pc)
  - ![](https://p1-tt.byteimg.com/origin/pgc-image/300ef1e7824342afb93a24f988bd7151?from=pc)
- 快捷键
  - ![](https://p6-tt.byteimg.com/origin/pgc-image/4621e6095a834b078b0a6ced28ebf5cc?from=pc)

### 软件包

linux软件包：如yum、apt等

#### apt

```sh
# 指定软件包版本
apt-get install package=version 
sudo apt-get install python=2.7 
sudo apt-get install python3.10 # Ubuntu
brew install python@3.10 # Mac

```

#### yum

debian安装yum

```shell
# Debian 安装 yum
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install yum
sudo yum install python38 # [2023--3-2] 阿里云服务器上安装 python
```

软件包命令

```shell
apt install yum # 通过apt安装yum
# 或下载安装
wget http://yum.baseurl.org/download/3.2/yum-3.2.28.tar.gz
tar xvf yum-3.2.28.tar.gz
cd yum-3.2.28
sudo apt install yum
# 更新到新版
yum -y update # 升级所有包，改变软件设置和系统设置,系统版本内核都升级
yum -y upgrade # 升级所有包，不改变软件设置和系统设置，系统版本升级，内核不改变
yum check-update # 列出所有可更新的软件清单
yum update # 安装所有更新软件
yum update gcc # 安装gcc更新软件
yum -y update gcc # 安装gcc更新软件，自动yes
yum install gcc # 仅安装指定的软件
yum -y install gcc # 自动回答yes
yum list # 列出所有可安裝的软件清单
yum list pam* # pam开头的软件包
yum search samba # 查找
yum info samba # 显示软件信息
yum remove samba # 删除samba
# 清楚缓存
yum clean all
yum clean packages # 清除缓存目录下的软件包
yum clean headers # 清除缓存目录下的 headers
yum clean oldheaders # 清除缓存目录下旧的 headers
yum clean, yum clean all (= yum clean packages; yum clean oldheaders) # 清除缓存目录下的软件包及旧的 headers
yum makecache # 生成缓存
```


## linux工具

史上最全，[linux内核调试工具](https://www.toutiao.com/a1674325657904128)都在这里了，我们来看看：
1. 内存相关的：free, vmstate, slabtop
2. cpu相关的：top, ps, pidstat, mpstat
  - 【2021-8-23】根据关键词快速杀死进程：ps axu \| grep start_all \| awk '{print $2}' \| xargs kill
3. 块设备IO相关的：iostat, iotop, blktrace
4. 网络相关的：ping, tcpdump, traceroute, ip, nicstat, netstat
5. 系统调用相关的：strace, lstrace, sysdig, perf
6. linux内核调试和优化相关的：perf, dtrace, stap, lttng, ktap, sysdig

重点说一下perf，这个工具非常强大，可以说是做linux性能优化的首选工具，它可以：
1. 统计出你的程序是花在cpu计算上、还是IO上；
2. 统计出你的程序执行的时候经过了多少次进程切换。进程切换的多，说明系统的吞吐率较好，但是频繁的切换也会影响性能；
3. 统计出你的程序运行过程中的cache-misses的计数，我们知道cache-misses过多，则表示访问内存的性能不佳；
4. 统计出你的进程在运行过程中发生了多少次 CPU 迁移，即被调度器从一个 CPU 转移到另外一个 CPU 上运行；

这个工具简直就是做linux内核性能优化的”瑞士军刀“，有木有？

perf既然这么强大，那它的实现原理是什么呢？
- perf其实依赖的是内核里的Tracepoint。
- Tracepoint 是散落在内核源代码中的一些 hook，一旦使能，它们便可以在特定的代码被运行到时被触发，这一特性可以被各种 trace/debug 工具所使用。Perf 就是该特性的用户之一。假如您想知道在应用程序运行期间，内核内存管理模块的行为，便可以利用潜伏在 slab 分配器中的 tracepoint。当内核运行到这些 tracepoint 时，便会通知 perf。Perf 将 tracepoint 产生的事件记录下来，生成报告，通过分析这些报告，调优人员便可以了解程序运行时期内核的种种细节，对性能症状作出更准确的诊断。

总结：
- ![](https://p1-tt-ipv6.byteimg.com/img/tos-cn-i-0022/a75094f8b23645fdbc244851528c1c3b~tplv-obj:2664:1542.image?from=post)

- nl的功能和cat -n一样，同样是从第一行输出全部内容，并且把行号显示出来
- more的功能是将文件从第一行开始，根据输出窗口的大小，适当的输出文件内容。当一页无法全部输出时，可以用“回车键”向下翻行，用“空格键”向下翻页。退出查看页面，请按“q”键。另外，more还可以配合管道符“\|”（pipe）使用，例如:ls -al \| more
- less的功能和more相似，但是使用more无法向前翻页，只能向后翻。less可以使用【pageup】和【pagedown】键进行前翻页和后翻页，这样看起来更方便。
- cat的功能是将文件从第一行开始连续的将内容输出在屏幕上。当文件大，行数比较多时，屏幕无法全部容下时，只能看到一部分内容。所以通常使用重定向的方式，输出满足指定格式的内容
  - cat语法：cat [-n]  文件名 （-n ： 显示时，连行号一起输出）
- tac的功能是将文件从最后一行开始倒过来将内容数据输出到屏幕上。我们可以发现，tac实际上是cat反过来写。这个命令不常用。
  - tac语法：tac 文件名。


### 终端访问

终端客户端工具
- Xshellicon
- Mobaxterm
- FinalShell
- XTerminal 是一个功能强大的远程终端管理平台，支持多平台支持、安全、终端控制、远程监控、远程协作、脚本自动化、插件icon扩展等功能。



### 自动登录

- [2018-3-26]自动登录鲁班测试机
- 方法一：

```shell
#参考expect用法
passwd="***"
expect -c "
        spawn ssh user@host -p 8022
    expect {
        \"*assword:\" {send \"$passwd\r\"; exp_continue }
    }
"
```
- 方法二：
   - login.sh内容：

```shell
#!/usr/bin/expect -f
set host luban@10.84.176.174
set port 8022
set pwd M95B8RBR
 
spawn ssh "$host" -p $port
set timeout 30
expect "password:"
send "$pwd\r"
interact
```
   - 执行：expect login.sh
   - 自动登录, ~/.bash_profile里配置别名即可一直使用
   - alias luban='expect ~/login.sh'


### 日期

- 【2020-9-21】时间矫正

```shell
 sudo ntpdate cn.pool.ntp.org # 矫正系统时间
 ```

### 任务启动


#### 自定义批量启动

【2023-8-9】批量启动服务
- 若已有任务端口在跑，跳过(参数空)/杀死

```sh
#lsof -i:9001 | awk '{if($2=="PID")next;print $2}'
source common.sh # 定义彩色日志函数 log

run_cmd(){
	# 批量启动任务
	name=$1 # 任务名
	cmd=$2 # 命令
	port=$3 # 端口,用于已有任务检测重启
	[ $port ] && {
		log "INFO" "检测已有任务端口:$port"
		detect=`lsof -i:$port | awk '{if($2=="PID")next;print $2}'`
		[ $detect ] &&  { log "检测到已有任务, 关闭任务"; kill $detect; }
	}
	log "INFO" "开始执行 $cmd"
	eval $cmd
	[ $? -eq 0 ] && log "INFO" "服务 $name 启动完毕" || log "ERROR" "服务 $name 启动失败"
}

run_cmd "test" "ls" 9002
run_cmd "test" "ls" 9001
```

返回结果

```
 [2023-08-09 17:38:18] [INFO] 检测已有任务端口:9002 
 [2023-08-09 17:38:18] [INFO] 开始执行 ls 
a.sh  bak  bin	common.sh  files  log.txt  log_file.txt  start_all.sh  work
 [2023-08-09 17:38:18] [INFO] 服务 test 启动完毕 
 [2023-08-09 17:38:18] [INFO] 检测已有任务端口:9001 
 [2023-08-09 17:38:18] [INFO] 检测到已有任务, 关闭任务 
kill 2303865
 [2023-08-09 17:38:18] [INFO] 开始执行 ls 
a.sh  bak  bin	common.sh  files  log.txt  log_file.txt  start_all.sh  work
 [2023-08-09 17:38:18] [INFO] 服务 test 启动完毕
```


### md5

Mac下安装MD5工具
- 安装md5sum和sha1sum

```sh
brew install md5sha1sum
```


### curl 网络请求

curl功能非常强大，命令行参数多达几十种。如果熟练的话，完全可以取代 Postman 这一类的图形界面工具。
- curl支持包括HTTP、HTTPS、ftp等众多协议，还支持POST、cookies、认证、从指定偏移处下载部分文件、用户代理字符串、限速、文件大小、进度条等特征。
  - GET: 
    - curl http://127.0.0.1:8080/login?admin&passwd=12345678
  - POST
    - curl -d "user=admin&passwd=12345678" http://127.0.0.1:8080/login
    - curl -H "Content-Type:application/json" -X POST -d '{"user": "admin", "passwd":"12345678"}' http://127.0.0.1:8000/login
- [curl用法指南](https://blog.csdn.net/weixin_39715290/article/details/110611606)

```shell
# ------ GET --------
# 直接GET请求
curl https://www.example.com
# 指定客户端的用户代理表头（User-Agent）， -A参数； 等效于直接使用chrome浏览器
curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://google.com
curl -H 'User-Agent: php/1.0' https://google.com # -H 也可以直接指定标头，更改UA
curl -H 'Accept-Language: en-US' https://google.com # 添加 HTTP 请求的标头
curl -H 'Accept-Language: en-US' -H 'Secret-Message: xyzzy' https://google.com # 添加 HTTP 标头Accept-Language: en-US
curl -d '{"login": "emma", "pass": "123"}' -H 'Content-Type: application/json' https://google.com/login # 添加两个标头
# -i参数打印出服务器回应的 HTTP 标头
curl -i https://www.example.com
# -I参数向服务器发出 HEAD 请求，然会将服务器返回的 HTTP 标头打印出来
curl -I https://www.example.com
# --head参数等同于-I
curl --head https://www.example.com
# -k参数指定跳过 SSL 检测。不会检查服务器的 SSL 证书是否正确。
curl -k https://www.example.com
# -L参数会让 HTTP 请求跟随服务器的重定向。curl 默认不跟随重定向
curl -L -d 'tweet=hi' https://api.twitter.com/tweet
# --limit-rate用来限制 HTTP 请求和回应的带宽，模拟慢网速的环境
curl --limit-rate 200k https://google.com # 每秒 200K 字节
# -o参数将服务器的回应保存成文件，等同于wget命令
curl -o example.html https://www.example.com # 将http://www.example.com保存成example.html
# -O参数将服务器回应保存成文件，并将 URL 的最后部分当作文件名。
curl -O https://www.example.com/foo/bar.html # 将服务器回应保存成文件，文件名为bar.html
# -s参数将不输出错误和进度信息
curl -s https://www.example.com
curl -s -o /dev/null https://google.com # # 不产生任何输出
curl -s -o /dev/null https://google.com # -S参数指定只输出错误信息，通常与-o一起使用
# -u参数用来设置服务器认证的用户名和密码。
curl -u 'bob:12345' https://google.com/login
curl https://bob:12345@google.com/login # curl 能够识别 URL 里面的用户名和密码，将其转为上个例子里面的 HTTP 标头
curl -u 'bob' https://google.com/login # 只设置了用户名，执行后，curl 会提示用户输入密码
# -v参数输出通信的整个过程，用于调试。
curl -v https://www.example.com
# --trace参数也可以用于调试，还会输出原始的二进制数据。
curl --trace - https://www.example.com
# -x参数指定 HTTP 请求的代理。
curl -x socks5://james:cats@myproxy.com:8080 https://www.example.com # 指定 HTTP 请求通过http://myproxy.com:8080的 socks5 代理发出。如果没有指定代理协议，默认为 HTTP。
curl -x james:cats@myproxy.com:8080 https://www.example.com # 请求的代理使用 HTTP 协议。
# -X参数指定 HTTP 请求的方法。
curl -X POST https://www.example.com

# 移出UA标头
curl -A '' https://google.com
# 发送cookie给服务器，生成一个标头Cookie: foo=bar
curl -b 'foo=bar' https://google.com
curl -b 'foo1=bar' -b 'foo2=baz' https://google.com # 两个cookie
curl -b cookies.txt https://www.google.com # 本地文件cookies.txt
# 服务器端cookie写入本地文件cookies.txt
curl -c cookies.txt https://www.google.com 
# -e参数用来设置 HTTP 的标头Referer，表示请求的来源
curl -e 'https://google.com?q=example' https://www.example.com
curl -H 'Referer: https://google.com?q=example' https://www.example.com # -H参数可以通过直接添加标头Referer，达到同样效果

# ------ POST --------
# -d参数，HTTP请求会自动加上标头Content-Type : application/x-www-form-urlencoded。并且会自动将请求转为 POST 方法，因此可以省略-X POST。
curl -d 'login=emma＆password=123' -X POST https://google.com/login
curl -d 'login=emma' -d 'password=123' -X POST  https://google.com/login
curl -d '@data.txt' https://google.com/login # 省略-X POST； 读取data.txt文件的内容，作为数据体向服务器发送
# --data-urlencode参数等同于-d，发送 POST 请求的数据体，区别在于会自动将发送的数据进行 URL 编码
curl --data-urlencode 'comment=hello world' https://google.com/login


# -F参数用来向服务器上传二进制文件
curl -F 'file=@photo.png' https://google.com/profile # 给 HTTP 请求加上标头Content-Type: multipart/form-data，然后将文件photo.png作为file字段上传
# -F参数可以指定 MIME 类型
curl -F 'file=@photo.png;type=image/png' https://google.com/profile # 指定 MIME 类型为image/png，否则 curl 会把 MIME 类型设为application/octet-stream
curl -F 'file=@photo.png;filename=me.png' https://google.com/profile # -F参数也可以指定文件名，原始文件名为photo.png，但是服务器接收到的文件名为me.png
# -G参数用来构造 URL 的查询字符串
curl -G -d 'q=kitties' -d 'count=20' https://google.com/search #  GET 请求，实际请求的 URL 为https://google.com/search?q=k...。如果省略--G，会发出一个 POST 请求。如果数据需要 URL 编码，可以结合--data--urlencode参数。
curl -G --data-urlencode 'comment=hello world' https://www.example.com
```

### wget

【2022-11-16】wget用法：[wget用法详解](https://www.jianshu.com/p/59bb131bc2ab)

```python
# wget http://cn.wordpress.org/wordpress-3.1-zh_CN.zip
filename = 'http://cn.wordpress.org/wordpress-3.1-zh_CN.zip'

wget ${filename} # 下载单个文件, 以默认名字显示
wget -O wordpress.zip ${filename} # 下载并命名文件
wget -o download.log ${filename} # 下载日志
wget –limit-rate=300k ${filename} # 限速下载
wget –c ${filename} # 断点续传，下载大文件时突然由于网络等原因中断，不用重新下载
wget –b ${filename} # 后台下载
tail -f wget-log # 后台下载，查看进度
wget –user-agent="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16" ${filename} # 伪装代理下载
wget –spider  ${filename} # 测试下载链接
wget –tries=40 ${filename} # 设置重试次数
wget -i filelist.txt # 批量下载，filelist.txt 中一行一个链接
wget –mirror -p –convert-links -P ./LOCAL ${filename} # 使用镜像下载 
# –miror:开户镜像下载 
# -p:下载所有为了html页面显示正常的文件 
# –convert-links:下载后，转换成本地的链接 
# -P ./LOCAL：保存所有文件和目录到本地指定目录 
wget –reject=gif ${filename} # 过滤特定格式的文件
wget -Q5m -i filelist.txt # 递归下载时，限制文件大小 5m
wget -r -A.pdf ${filename} # 下载一个网站里指定格式的文件
wget ftp-url # ftp匿名下载
wget –ftp-user=USERNAME –ftp-password=PASSWORD ${filename} # ftp使用账户下载

```


### ssh

SSH连接服务器

SSH提供了两种级别的安全验证：
- 第一种级别是基于**密码**的**安全验证**，知道账号和密码就可以登陆到远程主机。
  - Team的开发工作使用这种方式登陆编译服务器，或者开发机器。因为是在内网中，这种级别的安全验证已经足够了。
- 第二种级别是基于 Public-key cryptography (公开密匙加密）机制的安全验证，原理如下图所示：
  - 其优点在于无需共享的通用密钥，解密的私钥不发往任何用户。即使公钥在网上被截获，如果没有与其匹配的私钥，也无法解密，所截获的公钥是没有任何用处的。
  - ![ssh](http://zuyunfei.com/images/public_key_cryptography.png)

#### sshkey-gen

【2022-11-01】sshkey-gen的作用
- 通过数字签名RSA或DSA让两个linux机器之间使用ssh，而不需要用户名和密码。

ssh-keygen 用于 生成、管理和转换认证密钥

常用参数
- -t type:指定要生成的**密钥类型**，有 rsa1(SSH1), dsa(SSH2), ecdsa(SSH2), rsa(SSH2) 等类型，较为常用的是 rsa类型
- -C comment：提供一个**新注释**
- -b bits：指定要生成的**密钥长度** (单位:bit)，对于RSA类型的密钥，最小长度768bits,默认长度为2048bits。DSA密钥必须是1024bits
- -f filename: 指定生成的密钥**文件**名字

```shell
ssh-keygen # [rsa|dsa]，默认生成密钥文件和私钥文件 id_rsa,id_rsa.pub或id_dsa,id_dsa.pub
# RSA身份认证，使用指定邮箱登录某机器
ssh-keygen -t rsa -C "wangqiwen.at@163.com"
# 生成 id_ras.pub 文件
cat ~/.ssh/id_rsa.pub # 查看公钥
# 添加pub key

```

本机生成一个公钥和一个私钥文件

```shell
ls ~/.ssh
```

注意
- `公钥`相当于**锁**，`私钥`相当于**钥匙**
- 这里相当于在客户端创建一对**钥匙**和**锁**，SSH免密码登录就相当于将锁分发到服务端并装锁，然后客户端就可以利用这个钥匙开锁。

ssh-copy-id命令将本机上的公钥文件拷贝到服务器上(服务器用户名比如为liujiakun，IP地址为192.168.3.105)

```shell
# 拷贝公钥文件到指定机器
ssh-copy-id -i ~/.ssh/id_ras.pub user@192.168.1.104
# 指定端口
ssh-copy-id -i ~/.ssh/id_ras.pub "-p 3300 user@192.168.1.104"
# ssh-add 指令将私钥 加进来
ssh-add ~/.ssh/id_rsa
# 服务器上查询~/.ssh/目录下多了一个文件:authorized_keys
```

【2024-1-29】 网页版（Github/GitLab）上添加key，网页地址：
- `user settings` → `user profile` → `SSH Keys`


**单向**登陆的操作过程：
- 1、登录A机器 
- 2、ssh-keygen -t [rsa\|dsa]，将会生成密钥文件和私钥文件 `id_rsa`, `id_rsa.pub` 或 `id_dsa`, `id_dsa.pub`
- 3、将 `.pub` 文件复制到B机器的 `.ssh` 目录， 并 `cat id_dsa.pub >> ~/.ssh/authorized_keys`
- 4、大功告成，从A机器登录B机器的目标账户，不再需要密码了；（直接运行 #ssh 192.168.20.60 ）

**双向**登陆的操作过程：
- 1、`ssh-keygen` 做密码验证可以使在向对方机器上ssh ,scp不用使用密码.具体方法如下:
- 2、两个节点都执行操作：# `ssh-keygen -t rsa`
  - 然后全部回车,采用默认值.
- 3、这样生成了一对密钥，存放在用户目录的 `~/.ssh` 下。
  - 将公钥考到对方机器的用户目录下 ，并将其复制到 `~/.ssh/authorized_keys` 中（操作命令：# `cat id_dsa.pub >> ~/.ssh/authorized_keys` ）。
- 4、设置文件和目录权限：
  - 设置 authorized_keys 权限: `chmod 600 authorized_keys`
  - 设置 .ssh 目录权限: `chmod 700 -R .ssh`
- 5、要保证 .ssh 和 `authorized_keys` 都只有用户自己有写权限。否则验证无效。（今天就是遇到这个问题，找了好久问题所在），其实仔细想想，这样做是为了不会出现系统漏洞。

[ssh-keygen使用及参数详解](https://www.jianshu.com/p/807ec99cea21)


#### ssh 隧道

`SSH隧道`（即SSH代理、端口转发），SSH隧道概念主要理解**映射**二字。
- 把**本地端口**映射到**远程机器端口**，然后访问远程端口就相当于访问的本地端口，这就是远程SSH隧道。
- [SSH隧道](https://blog.csdn.net/u010690647/article/details/78573963)

建立SSH隧道命令

```sh
ssh -C -f -N -L listen_port:DST_Host:DST_port user@Tunnel_Host 
ssh -C -f -N -R listen_port:DST_Host:DST_port user@Tunnel_Host 
ssh -C -f -N -D listen_port user@Tunnel_Host
```

参数

```sh
-L port:host:hostport #建立本地SSH隧道(本地客户端建立监听端口)
# 将本地机(客户机)的某个端口转发到远端指定机器的指定端口. 

-R port:host:hostport #建立远程SSH隧道(隧道服务端建立监听端口)
# 将远程主机(服务器)的某个端口转发到本地端指定机器的指定端口. 
# 有本地映射肯定有远程映射，就是把-L换成-R，这样我们访问远程主机的端口就相当于访问本地的端口，但感觉作用不大。

-D port 
# 指定一个本地机器 “动态的’’ 应用程序端口转发. 

-C 压缩数据传输。

-N Do not execute a shell or command. 
# 不执行脚本或命令，仅仅做端口转发。通常与-f连用。
-f Fork into background after authentication. 
# 后台认证用户/密码，不用登录到远程主机。
-L X:Y:Z的含义是，将IP为Y的机器的Z端口通过中间服务器映射到本地机器的X端口。把其他远程机器的端口通过中间服务器映射到本地端口上来。然后本地就能通过中间服务器访问了远程服务器了。

-R X:Y:Z 的含义就是把我们本地的Y机器的Z端口映射到远程机器的X端口上。把本地端口映射到远程机器的端口上去。然后远程机器访问X端口，就相当于访问的是本地机器了。前提是，本地到远程机器的网络是通的，才能把本地的端口映射到远程机器上去

```


### 文件服务

一行命令搭建文件服务

```shell
# python2
python -m SimpleHTTPServer 8001
# python3下直接执行以下命令即可
cd $your_dir # 要共享的目录
# 启动文件服务，ip填下本机ip，默认端口8000
python -m http.server
python -m http.server 8001 # 指定端口
nohup python -m http.server -b 10.200.24.101 &>log.txt & 
# 打开网页: http://10.200.24.101:8000/
```

注意：
- 当前目录下不要放index.html，会被服务识别为主页，自动加载
- http.server建的文件服务器是单线程的，意味着如果多个用户访问会被阻塞，同时只能一个用户访问

多线程改进方案

```python
import socket
import SocketServer
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class ForkingHTTPServer(SocketServer.ForkingTCPServer):

   allow_reuse_address = 1

   def server_bind(self):
       """Override server_bind to store the server name."""
       SocketServer.TCPServer.server_bind(self)
       host, port = self.socket.getsockname()[:2]
       self.server_name = socket.getfqdn(host)
       self.server_port = port

def test(HandlerClass=SimpleHTTPRequestHandler,
        ServerClass=ForkingHTTPServer):
   BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
   test()
```

代码命名为MultiHTTPServer.py 放置到 python的lib库里面, 如Python/2.7/lib/python/site-packages

```shell
# 多线程文件服务器版本
python -m MultiHTTPServer.py
```

### 邮件

【2021-11-19】[Linux 命令行发送邮件的 5 种方法](https://linux.cn/article-11663-1.html)

 Linux中邮件命令怎么把邮件传递给收件人的？
 - 邮件命令撰写邮件并发送给一个本地**邮件传输代理**（MTA，如 sendmail、Postfix）。邮件服务器和远程邮件服务器之间通信以实际发送和接收邮件。下面的流程可以看得更详细。
 - ![](https://img.linux.net.cn/data/attachment/album/201912/11/081830xntnd4iny5nl9ran.png)

最流行的 5 个命令行邮件客户端，你可以选择其中一个。这 5 个命令分别是：
- mail / mailx
  - 安装： yum install mailx
- mutt
  - 安装：yum install mutt
- mpack
  - 安装：yum install mpack
- sendmail
  - 安装：yum install sendmail
- ssmtp
  - ssmtp 是类似 sendmail 的一个**只发送不接收**的工具，可以把邮件从本地计算机传递到配置好的 邮件主机（mailhub）。用户可以在 Linux 命令行用 ssmtp 把邮件发送到 SMTP 服务器。可以运行下面的命令从官方发行版仓库安装 ssmtp 命令。
  - 安装：yum install ssmtp

```shell
# ------ mail ------
echo "This is the mail body" | mail -s "Subject" 2daygeek@gmail.com
# 带附件
# -a：用于在基于 Red Hat 的系统上添加附件。
# -A：用于在基于 Debian 的系统上添加附件。
# -s：指定消息标题。
echo "This is the mail body" | mail -a test1.txt -s "Subject" 2daygeek@gmail.com

# -------- mutt -------
echo "This is the mail body" | mutt -s "Subject" 2daygeek@gmail.com
# 带附件
echo "This is the mail body" | mutt -s "Subject" 2daygeek@gmail.com -a test1.txt

# -------- mpack ---------
echo "This is the mail body" | mpack -s "Subject" 2daygeek@gmail.com
# 附件
echo "This is the mail body" | mpack -s "Subject" 2daygeek@gmail.com -a test1.txt

# --------- sendmail ---------
# 准备邮件内容：
echo -e "Subject: Test Mail\nThis is the mail body" > /tmp/send-mail.txt
# 发送
sendmail 2daygeek@gmail.com < send-mail.txt
# ---------- ssmtp ------------
echo -e "Subject: Test Mail\nThis is the mail body" > /tmp/ssmtp-mail.txt
ssmtp 2daygeek@gmail.com < /tmp/ssmtp-mail.txt
```

#### Python自动发送多封邮件

【2022-1-25】[5个方便好用的Python自动化脚本](https://www.toutiao.com/i7056585992664269344)

自动发送多封邮件

这个脚本可以帮助我们批量定时发送邮件，邮件内容、附件也可以自定义调整，非常的实用。相比较邮件客户端，Python脚本的优点在于可以智能、批量、高定制化地部署邮件服务。

需要的第三方库：
- Email - 用于管理电子邮件消息
- Smtlib - 向SMTP服务器发送电子邮件，它定义了一个 SMTP 客户端会话对象，该对象可将邮件发送到互联网上任何带有 SMTP 或 ESMTP 监听程序的计算机
- Pandas - 用于数据分析清洗地工具

```python
import smtplib 
from email.message import EmailMessage
import pandas as pd

def send_email(remail, rsubject, rcontent):
    email = EmailMessage()                          ## Creating a object for EmailMessage
    email['from'] = 'The Pythoneer Here'            ## Person who is sending
    email['to'] = remail                            ## Whom we are sending
    email['subject'] = rsubject                     ## Subject of email
    email.set_content(rcontent)                     ## content of email
    with smtplib.SMTP(host='smtp.gmail.com',port=587)as smtp:     
        smtp.ehlo()                                 ## server object
        smtp.starttls()                             ## used to send data between server and client
        smtp.login("deltadelta371@gmail.com","delta@371") ## login id and password of gmail
        smtp.send_message(email)                    ## Sending email
        print("email send to ",remail)              ## Printing success message

if __name__ == '__main__':
    df = pd.read_excel('list.xlsx')
    length = len(df)+1

    for index, item in df.iterrows():
        email = item[0]
        subject = item[1]
        content = item[2]
        send_email(email,subject,content)
```

### tcpdump常用命令

- 用简单的话来定义tcpdump，就是：dump the traffic on a network，根据使用者的定义对网络上的数据包进行截获的包分析工具。 tcpdump可以将网络中传送的数据包的“头”完全截获下来提供分析。它支持针对网络层、协议、主机、网络或端口的过滤，并提供and、or、not等逻辑语句来帮助你去掉无用的信息。

实用命令实例
```shell
#将某端口收发的数据包保存到文件
sudo tcpdump -i any port 端口 -w 文件名.cap
# 打印请求到屏幕<br>
sudo tcpdump -i any port 端口 -Xnlps0
# 默认启动
tcpdump
# 普通情况下，直接启动tcpdump将监视第一个网络接口上所有流过的数据包。
#监视指定网络接口的数据包
tcpdump -i eth1
#如果不指定网卡，默认tcpdump只会监视第一个网络接口，一般是eth0，下面的例子都没有指定网络接口。
```

### 端口显示

#### lsof

lsof(list open files)是一个列出当前系统打开文件的工具。

lsof 查看端口占用语法格式：
- lsof -i:端口号

```shell
lsof -i:8080 # 查看8080端口占用（NAME字段就是端口）
# COMMAND   PID USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
# nodejs  26993 root   10u  IPv4 37999514      0t0  TCP *:8000 (LISTEN)
lsof abc.txt # 显示开启文件abc.txt的进程
lsof -c abc # 显示abc进程现在打开的文件
lsof -c -p 1234 # 列出进程号为1234的进程所打开的文件
lsof -g gid # 显示归属gid的进程情况
lsof +d /usr/local/ # 显示目录下被进程开启的文件
lsof +D /usr/local/ # 同上，但是会搜索目录下的目录，时间较长
lsof -d 4 # 显示使用fd为4的进程
lsof -i -U # 显示所有打开的端口和UNIX domain文件
```

#### netstat

netstat -tunlp 用于显示 tcp，udp 的端口和进程等相关情况

netstat 查看端口占用语法格式：
- netstat -tunlp \| grep 端口号
- 参数
  - -t (tcp) 仅显示tcp相关选项
  - -u (udp)仅显示udp相关选项
  - -n 拒绝显示别名，能显示数字的全部转化为数字
  - -l 仅列出在Listen(监听)的服务状态
  - -p 显示建立相关链接的程序名

```shell
netstat -tunlp | grep 8000
# tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      26993/nodejs   
netstat -ntlp   # 查看当前所有tcp端口
netstat -ntulp | grep 80   # 查看所有80端口使用情况
netstat -ntulp | grep 3306   # 查看所有3306端口使用情况
```

#### kill


命令杀死进程
- kill -9 26993

### java安装

- 【2021-1-20】
- 安装：先装[java](https://www.oracle.com/java/technologies/javase-jdk15-downloads.html), open JDK[清华源下载](https://mirror.tuna.tsinghua.edu.cn/AdoptOpenJDK/15/jdk/x64/linux/)
- 配置环境变量：vim /etc/profile
- 查看版本：java -version

```shell
export JAVA_HOME=/usr/local/src/jdk1.8.0_171 #根据自己的完整路径修改
export PATH=$PATH:$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
```

### wc

wc命令 统计指定文件中的字节数、字数、行数，并将统计结果显示输出

```sh
-c # 统计字节数，或--bytes：显示Bytes数。
-l # 统计行数，或--lines：显示列数。
-m # 统计字符数，或--chars：显示字符数。 中文
-w # 统计字数，或--words：显示字数。单词数, 一个字被定义为由空白、跳格或换行字符分隔的字符串。
-L # 打印最长行的长度，或--max-line-length。
-help     # 显示帮助信息。
--version # 显示版本信息。
```

示例

```sh
wc test.txt
# 输出结果
7     8     70     test.txt
# 行数 单词数 字节数  文件名
# ------------
wc -m # 字符数, 中文占3个字节(utf8), m可以统计中文
wc -l *       # 统计当前目录下的所有文件行数及总计行数。
wc -l *.js    # 统计当前目录下的所有 .js 后缀的文件行数及总计行数。
find  . * | xargs wc -l # 当前目录以及子目录的所有文件行数及总计行数。
```

### 录盘/gif

录屏


#### Gif

【2023-8-28】[Terminalizer](https://www.terminalizer.com/), [github](https://github.com/faressoft/terminalizer)
- ![](https://github.com/faressoft/terminalizer/raw/master/img/demo.gif?raw=true)

```sh
# Start recording your terminal using the record command.
terminalizer record demo
# A file called demo.yml will be created in the current directory. You can open it using any editor to edit the configurations and the recorded frames. You can replay your recording using the play command.
terminalizer play demo
# Now let's render our recording as an animated gif.
terminalizer render demo
```


### 聊天

#### smallchat 

【2023-11-15】 Redis创始人开源最小聊天服务器 [SmallChat](https://github.com/antirez/smallchat) ，C语言实现，仅200行代码
- [使用方法](https://github.com/antirez/smallchat/issues/3)

```sh
cd smallchat
# 编译
# gcc smallchat.c -o smallchat && ./smallchat
make
# 启动服务, 默认端口 SERVER_PORT 7711
./smallchat-server
# 启动客户端连接
/nick # 设置昵称
./smallchat-client 127.0.0.1 7711
```


### 文件传输

【2017-12-16】远程文件传输的几种方式：
- secureCRT、ftpxp客户端
- scp命令
- rsync命令
- ftp、http服务
  - 【2018-1-4】python搭建简易web服务，可以下载文件
      - 服务端：python -m SimpleHTTPServer 8088
      - 客户端浏览器：http://uemc-train-srv00.gz01:8088/
      - 参考：[三种Shell脚本编程中避免SFTP输入密码的方法](http://blog.csdn.net/hereiskxm/article/details/7861759)
- sftp服务
- szrz命令
- nc命令
  - Linux网络工具中的“瑞士军刀”盛誉的netcat,能通过TCP和UDP在网络中读写数据
  - (1) 检测端口是否可用：
      - nc -v www.thanks.live 80
  - （2）文件传输
      - 接收端：nc -l 9995 > tmp
      - 发送端：nc 10.200.0.79 9995 < send_file
      - 注：
        - 端口范围(1024,65535)
        - 发送、接收顺序不限
        - 传输目录
            - 接收端：nc -l 9995 \| tar xfvz -
            - 发送端：tar cfz - * \| nc 10.0.1.162 9995
  - （3）聊天功能
      - 类似文件传输操作步骤，去掉文件定向（<>）即可
      - A：nc -l 9995
      - B：nc 10.200.0.79 9995
  - （4）telnet服务器（远程登录）
      - 服务端：nc -l -p 9995 -e bash
      - 客户端：nc 10.200.0.79 9995
- samba
- Git LFS


#### nc（NetCat，瑞士军刀）

[NetCat](http://netcat.sourceforge.net/)（简称nc），在网络工具中有“**瑞士军刀**”美誉，其有Windows和Linux的版本。
- 因为它**短小精悍**（1.84版本也不过25k，旧版本或缩减版甚至更小）、**功能实用**，被设计为一个简单、可靠的网络工具，可通过TCP或UDP协议传输读写数据。
- 还是一个网络应用**Debug分析器**，因为它可以根据需要创建各种不同类型的网络连接。
- 参考：[nc命令详解](https://www.cnblogs.com/wenbiao/p/3375811.html)

【2021-12-8】亲测，使用nc命令局域网跨系统传输大文件夹（13G），mac → Ubuntu，Windows也可以安装，但安装包被win10拦截

安装：
- Windows系统安装：[nc下载链接](https://eternallybored.org/misc/netcat/)，把解压的文件存到c:\WINDOWS\system32路径下。
打开cmd 输入nc -help，查看命令使用方法。
- linux/mac一般自带，安装命令如下：

```shell
# linux yum
yum install -y nc
# linux rpm
rpm -q nc
```

参数：
- -g<网关> 设置路由器跃程通信网关，最多可设置8个。
- -G<指向器数目> 设置来源路由指向器，其数值为4的倍数。
- -h 在线帮助。
- -i<延迟秒数> 设置时间间隔，以便传送信息及扫描通信端口。
- -l 使用监听模式，管控传入的资料。
- -n 直接使用IP地址，而不通过域名服务器。
- -o<输出文件> 指定文件名称，把往来传输的数据以16进制字码倾倒成该文件保存。
- -p<通信端口> 设置本地主机使用的通信端口。
- -r 乱数指定本地与远端主机的通信端口。
- -s<来源地址> 设置本地主机送出数据包的IP地址。
- -u 使用UDP传输协议。
- -v 显示指令执行过程。
- -w<超时秒数> 设置等待连线的时间。
- -z 使用0输入/输出模式，只在扫描通信端口时使用。

注意：
  - 端口范围(1024,65535)
  - 发送、接收顺序不限

用法：

```shell
# （0）远程聊天：a与b两台机器
# --- 接收 ----
nc -l 1234  # a端开启监听
nc -lp 22222 # 或者
# --- 发送 ----
nc  192.168.200.27 1234 # b端开启
nc -nv 40.2.214.139 22222 # 或者

# （1）远程复制
#     s1(发送端) → s2(接收端)
nc -l 1234 > 1234.txt # s2上开通监听端口1234
nc -w 1 192.168.200.27 1234 < abc.txt # 发送端，传入文件abc.txt

nc -lp 22222 > log.rar # 接收端
nc -nc -vn 26.5.189.16 22222 < log.rar # 发送端

# 发送完后自动断开连接（超时3s）
nc –n ip port > yyy # 接收
nc –n –l –p port –vv –w 3 < xxx # 发送

# 传目录
nc -l 9995 | tar xfvz - # 发送端
tar cfz - * | nc 10.0.1.162 9995 # 发送端，当前目录

# （2）硬盘/分区 克隆
#     基本相似，由dd获得硬盘或分区的数据，然后传输即可。克隆硬盘或分区的操作，不应在已经mount的的系统上进行。
nc -l -p 1234 | dd of=/dev/sda # s2开启监听
dd if=/dev/sda | nc 192.168.200.27 1234 # s1上开始传输

# （3）端口扫描
nc -nvv 192.168.0.1 80 //扫描 80端口
nc -v www.thanks.live 80 # 检测端口80是否可用
nc -v -w 1 192.168.200.29 -z 20-30 # 从20依次扫描到30
nc -v -z -w2 192.168.0.3 1-100 # TCP端口扫描
nc -u -z -w2 192.168.0.1 1-1000 # UDP扫描192.168.0.3 的端口 范围是 1-1000

# （4）telnet服务器（远程登录）
nc -l -p 9995 -e bash # 服务端
nc 10.200.0.79 9995 # 客户端
```


#### 第三方工具

最强跨平台传输软件，速度快体积小，比苹果隔空传送好...

- syncthing和localsend都有用，localsend日常跨设备分享很方便， syncthing 偏向同步

##### reep.io 网页

- 【2018-6-21】webrtc peer to peer文件传输工具[reep.io](https://reep.io/)失效，[send-anywhere](https://send-anywhere.com/)全终端覆盖, 基于浏览器，直接选中本地文件，生成下载链接，速度400kb；[Snapdrop](Snapdrop.net),免软件免登录的一款工具，只需在同一WIFI环境下打开Snapdrop网页，就能侦测到彼此，并开始传输文件。知乎[大文件传输工具有哪些](https://www.zhihu.com/question/333234462), 示例：[mathematica下载](https://reep.io/d/9vsymkgm3e)，【2019-05-16】[mathematica快速入门](https://zhuanlan.zhihu.com/p/47896722)

##### LocalSend 开源

[LocalSend](https://localsend.org/#/) 是一款免费开源的跨平台文件传输工具
- 支持 Android、Windows、macOS、iOS、Linux等平台，安装后只需要在设置中打开快速保存开关即可使用。
- 速度快、支持跨平台传输，还能自定义保存目录。
- 电脑端安装包只有15MB，不会占用资源，可以在后台运行，需要时随时反应。

相比于苹果的隔空传送，LocalSend更方便快捷，适合办公人士使用。

##### syncthing

[syncthing](https://syncthing.net/)

Syncthing 是一个开源免费的数据同步神器，被称为 Resilio Sync 的替代品，支持 Android、Linux、Windows、Mac OS X 等系统
- 在 2 台任何系统任何设备之间，实现文件实时同步，很强大。
- 而且数据很安全，不会存储在你的设备以外的其他地方。
- 所有通信都使用 TLS 进行保护。
- 所使用的加密包括完美的前向保密，以防止窃听者获得对您的数据的访问权限。

很适合用来搭建私有同步网盘。


### 编译安装

编译安装常见命令

```sh
./configure # 配置
make # 构建
make install # 安装
```

整个过程分为三步：
1. `配置`
  - `configure` 脚本负责在系统软件构建环境。确保构建和安装过程所需要的依赖准备好，并且搞清楚使用这些依赖需要的东西。
  - Unix 程序一般是用 **C 语言**写，所以需要一个 C 编译器去构建。在这个例子中 configure 要做的就是确保系统中有 C 编译器，并确定它的名字和路径。
2. `构建`
  - 当 configure 配置完毕后，可以使用 `make` 命令执行构建。这个过程会执行在 Makefile 文件中定义的一系列任务将软件源代码编译成可执行文件。
  - 下载的源码包一般没有一个最终的 Makefile 文件，一般是一个模版文件 Makefile.in 文件，然后 configure 根据系统的参数生成一个定制化的 Makefile 文件。
3. `安装`
  - 软件已经被构建好且可执行，接下来将可执行文件复制到最终路径。
  - `make install` 命令将可执行文件、第三方依赖包和文档复制到正确路径。
  - 可执行文件被复制到某个 PATH 包含的路径，程序调用文档被复制到某个 MANPATH 包含的路径，还有程序依赖的文件也会被存放在合适的路径。
  - 因为安装这一步也是被定义在 Makefile 中，所以程序安装的路径可以通过 configure 命令的参数指定，或者 configure 通过系统参数决定。

如果要将可执行文件安装在系统路径，执行这步需要赋予相应的权限，一般是通过 sudo。


不直接写 configure 脚本文件，而是通过创建一个描述文件 `configure.ac` 来描述 configure 需要做的事情。
- `configure.ac` 使用 `m4sh` 写，m4sh 是 m4 宏命令和 shell 脚本的组合。

make 和 make install 区别
- make 用来编译，从Makefile中读取指令，然后编译。
- make install 用来安装，也从Makefile中读取指令，安装到指定的位置。

常见目标：
- make all：编译程序、库、文档等（等同于make）
- make install：安装已经编译好的程序。复制文件树中到文件到指定的位置
- make unistall：卸载已经安装的程序。
- make clean：删除由make命令产生的文件
- make distclean：删除由./configure产生的文件
- make check：测试刚刚编译的软件（某些程序可能不支持）
- make installcheck：检查安装的库和程序（某些程序可能不支持）
- make dist：重新打包成packname-version.tar.gz

【2024-4-20】[configure、 make、 make install 背后的原理](https://zhuanlan.zhihu.com/p/77813702)


## linux进程

### 进程查看

进程查看
- pstree 查看进程的树型结构
- tree 查看目录的树型结构

```sh
pstree # 查看进程树
pstree -p # 查看并打印进程树，含pid
pstree -p 123232 # 查看某个进程的树型结构
tree /tmp # 查看某个目录的目录树
tree -h /tmp # 查看某个目录的目录树，并打印文件大小
```

### fork

一个进程包括代码、数据和分配给进程的资源。fork（）函数通过**系统调用**创建一个与原来进程几乎完全相同的进程，也就是两个进程可以做完全相同的事，但如果初始参数或者传入的变量不同，两个进程也可以做不同的事。
- 一个进程调用fork（）函数后，系统先给新的进程分配资源，例如存储数据和代码的空间。
- 然后把原来的进程的所有值都复制到新的新进程中，只有少数值与原来的进程的值不同。相当于克隆了一个自己。

fork函数创建子进程

```c++
#include <unistd.h>  
#include <stdio.h>   
int main ()   
{   
    pid_t fpid; //fpid表示fork函数返回的值  
    int count=0;  
    fpid = fork();  // 创建子进程（克隆），返回0，错误时返回负数
    if (fpid < 0)  
        printf("error in fork!");   
    else if (fpid == 0) {  
        printf("i am the child process, my process id is %d\n", getpid());   
        printf("我是爹的儿子\n");//对某些人来说中文看着更直白。  
        count++;  
    }  
    else {  
        printf("i am the parent process, my process id is %d\n", getpid());   
        printf("我是孩子他爹\n");  
        count++;  
    }  
    printf("统计结果是: %d\n",count);  
    return 0;  
}
```

### top/htop

[htop官网](http://hisham.hm/htop/index.php)是Linux系统中的一个**互动**的进程查看器，一个文本模式的应用程序（在控制台orX终端中），需要ncurses。
- 与Linux传统的`top`相比，`htop`更加人性化。它可以让用户交互式操作，支持颜色主题，可横向或者纵向滚动浏览进程列表，并支持鼠标操作。

与top相比，htop有以下优点：
- 可以横向或纵向滚动浏览进程列表，以便看到所有的进程和完整命令行；
- 在启动时，比top要快；
- 杀进程时不需要输入进程号；
- htop支持鼠标操作；
- top已经很老了；



### crontab使用

- [Linux定时任务Crontab命令详解](https://www.cnblogs.com/intval/p/5763929.html)，[crontab在线测试](https://tool.lu/crontab/)
- 通过crontab 命令，我们可以在固定的间隔时间执行指定的系统指令或 shell script脚本。时间间隔的单位可以是分钟、小时、日、月、周及以上的任意组合。这个命令非常设合周期性的日志分析或数据备份等工作。
- 命令参数：
  - -u user：用来设定某个用户的crontab服务，例如，“-u ixdba”表示设定ixdba用户的crontab服务，此参数一般有root用户来运行。
  - file：file是命令文件的名字,表示将file做为crontab的任务列表文件并载入crontab。如果在命令行中没有指定这个文件，crontab命令将接受标准输入（键盘）上键入的命令，并将它们载入crontab。
  - -e：编辑某个用户的crontab文件内容。如果不指定用户，则表示编辑当前用户的crontab文件。
  - -l：显示某个用户的crontab文件内容，如果不指定用户，则表示显示当前用户的crontab文件内容。
  - -r：从/var/spool/cron目录中删除某个用户的crontab文件，如果不指定用户，则默认删除当前用户的crontab文件。
  - -i：在删除用户的crontab文件时给确认提示。

```shell
#安装crontab：
yum install crontabs
#服务操作说明：
/sbin/service crond start # 启动服务
/sbin/service crond stop # 关闭服务
/sbin/service crond restart # 重启服务
/sbin/service crond reload # 重新载入配置
/sbin/service crond status # 启动服务
# 查看
crontab [-u user] file
crontab [-u user] [ -e | -l | -r ] # l显示，e编辑
# 看日志
tail -n 2 /var/log/cron

# 更新系统时间
ntpdate time.windows.com
```

- 每一行都代表一项任务，每行的每个字段代表一项设置，它的格式共分为六个字段，前五段是时间设定段，第六段是要执行的命令段，格式如下：minute hour day month week command
  1. minute： 表示分钟，可以是从0到59之间的任何整数。
  1. hour：表示小时，可以是从0到23之间的任何整数。
  1. day：表示日期，可以是从1到31之间的任何整数。
  1. month：表示月份，可以是从1到12之间的任何整数。
  1. week：表示星期几，可以是从0到7之间的任何整数，这里的0或7代表星期日。
  1. command：要执行的命令，可以是系统命令，也可以是自己编写的脚本文件。
  - ![](https://images2015.cnblogs.com/blog/513841/201608/513841-20160812102124078-171184924.png)
- 示例

```shell
#分 时 天 月 周 命令
* * * * * cd /home/work/code/training_platform/web && python t.py

# 每一分钟执行一次 /bin/ls
* * * * * /bin/ls
# 12 月内, 每天的早上 6 点到 12 点，每隔 3 个小时 0 分钟执行一次 /usr/bin/backup
0 6-12/3 * 12 * /usr/bin/backup
# 周一到周五每天下午 5:00 寄一封信给 alex@domain.name：
0 17 * * 1-5 mail -s "hi" alex@domain.name < /tmp/maildata
# 每月每天的午夜 0 点 20 分, 2 点 20 分, 4 点 20 分....执行 echo "haha"：
20 0-23/2 * * * echo "haha"

0 */2 * * * /sbin/service httpd restart # 每两个小时重启一次apache 
50 7 * * * /sbin/service sshd start # 每天7：50开启ssh服务 
50 22 * * * /sbin/service sshd stop  # 每天22：50关闭ssh服务 
0 0 1,15 * * fsck /home  # 每月1号和15号检查/home 磁盘 
1 * * * * /home/bruce/backup  # 每小时的第一分执行 /home/bruce/backup这个文件 
00 03 * * 1-5 find /home "*.xxx" -mtime +4 -exec rm {} \; # 每周一至周五3点钟，在目录/home中，查找文件名为*.xxx的文件，并删除4天前的文件。
30 6 */10 * * ls # 每月的1、11、21、31日是的6：30执行一次ls命令

# 当程序在你所指定的时间执行后，系统会发一封邮件给当前的用户，显示该程序执行的内容，若是你不希望收到这样的邮件，请在每一行空一格之后加上 > /dev/null 2>&1 即可
20 03 * * * . /etc/profile;/bin/sh /var/www/runoob/test.sh > /dev/null 2>&1 

```

[crontab无法执行](https://www.runoob.com/linux/linux-comm-crontab.html)
- 用crontab来定时执行脚本无法执行，但是如果直接通过命令（如：./test.sh)又可以正常执行，这主要是因为**无法读取环境变量**。
- 解决方法：
  - 1、所有命令需要写成绝对路径形式，如: /usr/local/bin/docker。
  - 2、在 shell 脚本开头使用以下代码，. /etc/profile; . ~/.bash_profile
  - 3、在 /etc/crontab 中添加环境变量，在可执行命令之前添加命令 . /etc/profile;/bin/sh，使得环境变量生效
    - 20 03 * * * . /etc/profile;/bin/sh /var/www/runoob/test.sh


## linux I/O模式

【2021-12-17】[Linux 五种 IO 模式及 select、poll、epoll 详解](https://www.toutiao.com/i7042313859834724877)

从事 Web 服务器开发的后端程序员，必然绕不开**网络编程**，而其中最基础也是最重要的部分就是 Linux **I/O模式** 及 **Socket 编程**。

### 基础概念

基础概念
- 1.1、**用户**空间和**内核**空间
  - 对于32位操作系统而言，它的寻址空间是4G（2的32次方），注意这里的4G是**虚拟内存**空间大小。以 Linux 为例，它将最高的1G字节给内核使用，称为**内核空间**，剩下的3G给用户进程使用，称为**用户空间**。这样做的好处就是隔离，保证内核安全。
- 1.2、进程**切换**
  - 这是内核要干的事，字面意思很好理解，挂起正在运行的 A 进程，然后运行 B 进程，当然这其中的流程比较复杂，涉及到上下文切换，且非常消耗资源，感兴趣的同学可以去深入研究。
- 1.3、进程的**阻塞**
  - 进程阻塞是本进程的行为，比如和其他进程通信时，等待请求的数据返回；进程进入阻塞状态时不占用CPU资源的
- 1.4、文件描述符
  - 在 Linux 世界里，**一切皆文件**。怎么理解呢？当程序打开一个现有文件或创建新文件时，内核会向进程返回一个文件描述符，文件描述符在形式上是一个非负整数，其实就是一个索引值，指向该进程打开文件的记录表（它是由内核维护的）。
- 1.5、**缓存** I/O
  - 和标准 IO 是一个概念，当应用程序需要从内核读数据时，数据先被拷贝到操作系统的**内核缓冲区**（page cache），然后再从该缓冲区拷贝到应用程序的地址空间。

当应用程序发起一次 read 调用时，会经历以下两个阶段：
1. 等待数据准备 (Waiting for the data to be ready)
1. 将数据从**内核**拷贝到**进程**中 (Copying the data from the kernel to the process)
正式因为这两个阶段，Linux 系统产生了下述五种 IO 方式：
1. **阻塞** I/O（blocking IO）：blocking IO的特点就是在IO执行的两个阶段都被block了
1. **非阻塞** I/O（nonblocking IO）：non-blocking IO 的特点是用户进程需要不断的主动询问内核 “ 数据好了吗？”
1. **异步** I/O（asynchronous IO）
  - **同步**：synchronous IO做”IO operation”的时候会将process阻塞。之前所述的blocking IO，non-blocking IO，IO multiplexing 都属于 synchronous IO。各IO模式比较：
    - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/a5ccc4d198354858a16ab4994c20a3f7?from=pc)
    - 对于 non-blocking IO中，虽然进程大部分时间都不会被 block，但是它仍然要求进程去主动的 check，并且当数据准备完成以后，也需要进程主动的再次调用recvfrom来将数据拷贝到用户内存。
  - **异步**：asynchronous IO 完全不同于 no-blocking IO，它就像是用户进程将整个 IO 操作交给了内核完成，然后内核做完后发出信号通知。在此期间，用户进程不需要去检查 IO 操作的状态，也不需要主动的去拷贝数据。
1. I/O **多路复用**（ IO multiplexing）：
  - 通过一种机制一个进程能同时等待多个文件描述符，而这些文件描述符（套接字描述符）其中的任意一个进入读就绪状态，select()函数就可以返回。
  - select，poll，epoll 都是 IO 多路复用的机制，它们都需要在读写事件就绪后自己负责进行读写，也就是说这个读写过程是阻塞的。
1. **信号驱动** I/O（ signal driven IO）（很少见，可忽略）


## 网络编程（socket）

socket编程基于**传输层**，是应用层和传输层之间的一个抽象层。在使用socket API时，实际上每创建一个socket，都会分配两个**缓冲区**：**输入**缓冲区和**输出**缓冲区（大小一般是8K）
- Linux下**一切皆文件**的思想，两台主机在进行通信时，**write** 函数是向缓冲区里**写**，**read** 函数是从缓冲区里**读**，至于缓冲区里的数据什么时候被传输，有没有达到目标主机，这些都交给传输层的TCP/UDP来做。
- 但Windows中，将 **socket文件** 和 **普通文件** 分开，所以不能用write函数和read函数实现，而是用**send**函数和**recv**函数。

每次通信都打开了一个socket文件，所以通信结束后，在进程关闭前，要关闭所有的socket文件。

进程通信的概念最初来源于单机系统。由于每个进程都在自己的地址范围内运行，为保证两个相互通信的进程之间既互不干扰又协调一致工作，操作系统为进程通信提供了相应设施，如
- UNIX BSD有：**管道**（pipe）、**命名管道**（named pipe）**软中断信号**（signal）
- UNIX system V有：**消息**（message）、**共享存储区**（shared memory）和**信号量**（semaphore)等.
仅限于用在**本机**进程之间通信。**网间**进程通信要解决的是不同主机进程间的相互通信问题（同机进程通信是特例）。
- 同一主机上，不同进程可用**进程号**（process ID）唯一标识。
- 但在网络环境下，各主机独立分配的进程号不能唯一标识该进程。不同机器有相同进程号，另外，操作系统支持的网络协议众多，不同协议的工作方式不同，地址格式也不同。网间进程通信还要解决多重协议的识别问题。 
- TCP/IP协议族已经解决了这个问题，网络层的“**ip地址**”可以唯一标识网络中的主机，而传输层的“**协议**+**端口**”可以唯一标识主机中的应用程序（进程）。这样利用**三元组**（ip地址，协议，端口）就可以标识网络的进程了，网络中的进程通信就可以利用这个标志与其它进程进行交互。
TCP/IP协议的应用程序通常采用应用编程接口：UNIX  BSD的**套接字**（socket）和UNIX System V的**TLI**（已经被淘汰）来实现网络进程之间的通信。目前几乎所有的应用程序都是采用**socket**，而现在又是网络时代，网络中进程通信是无处不在，这就是我为什么说“**一切皆socket**”。

### TCP -- 三次握手、四次挥手

socket的API是在三次握手和四次挥手的基础上设置的接口
- 结构体：ip地址 + 端口号，如：sockaddr、sockaddr_in
总的来说，不管是 struct sockaddr 还是 struct sockaddr_in 都是存放了一个**ip地址**，一个**端口号**，和ip的**类型**(IPV4还是IPV6)

注意：
- 每次输入的ip要通过inet_addr(“127.0.0.1”)函数转化，将一个点分十进制ip转换成长无符号整形，头文件在<arpa/inet.h>中
- 端口号要转换成小端

三次握手
- 一个客户端只有一个sock（文件描述符），而一个服务器最少有两个（一个是自己创建socket时的sock，剩下的是每有一个客户端连接服务器就生成一个sock文件描述符）。数据传输过程相当于文件的读写操作
- ![img](https://img-blog.csdnimg.cn/20190406214540878.png)
- ![img](https://img-blog.csdnimg.cn/20190406214552329.png)
四次挥手
- 四次挥手在socket API上的接口表示为关闭各自拥有的文件描述符即可

### 什么是socket

什么是 Socket 呢？简单理解，就是： **ip地址** + **端口号**。

当两个进程间需要通信时，首先要创建**五元组**（源ip地址、目的ip地址、源端口号、目的端口号、协议），建立 tcp 连接，建立好连接之后，两个进程各自有一个 Socket 来标识，这两个 socket 组成的 socket pair 也就唯一标识了一个连接。有了连接之后，应用程序得要从 tcp 流上获取数据，然后再处理数据。

### socket工作原理

工作原理：“open—write/read—close”模式。
- 服务器端先**初始化**Socket，然后与端口**绑定**(bind)，对端口进行**监听**(listen)，调用accept**阻塞**，等待客户端连接。
- 这时如果有个客户端初始化一个Socket，然后连接服务器(connect)，如果连接成功，这时客户端与服务器端的连接就建立了。
- 客户端发送数据请求，服务器端接收请求并处理请求，然后把回应数据发送给客户端，客户端读取数据
- 最后关闭连接，一次交互结束。
涉及的函数
- （1）socket初始化：
  - int  socket(int protofamily, int type, int protocol); //返回sockfd
- （2）bind()函数把一个地址族中的特定地址赋给socket。
  - int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
- （3）listen()：调用listen()来监听这个socket，如果客户端这时调用connect()发出连接请求，服务器端就会接收到这个请求
  - int listen(int sockfd, int backlog); // backlog排队的最大连接个数
  - socket()函数创建的socket默认是一个**主动**类型的，listen函数将socket变为**被动**类型的，等待客户的连接请求。
- （4）connect()函数: 客户端通过调用connect函数来建立与TCP服务器的连接
  - int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
- （5）accept()函数
  - TCP服务器端依次调用socket()、bind()、listen()之后，就会监听指定的socket地址了。TCP客户端依次调用socket()、connect()之后就向TCP服务器发送了一个连接请求。TCP服务器监听到这个请求之后，就会调用accept()函数取接收请求，这样连接就建立好了。之后就可以开始网络I/O操作了，即类同于普通文件的读写I/O操作。
  - int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen); //返回连接connect_fd
- （6）read()、write()等函数：调用网络I/O进行读写操作
  - read()/write()
  - recv()/send()
  - readv()/writev()
  - recvmsg()/sendmsg() // 最通用的I/O函数
  - recvfrom()/sendto()
- （7）close()函数
  - 在服务器与客户端建立连接之后，会进行一些读写操作，完成了读写操作就要关闭相应的socket描述字，好比操作完打开的文件要调用fclose关闭打开的文件。
  - close一个TCP socket的缺省行为时把该socket标记为以关闭，然后立即返回到调用进程。该描述字不能再由调用进程使用，也就是说不能再作为read或write的第一个参数。
  - 注意：close操作只是使相应socket描述字的引用计数-1，只有当引用计数为0的时候，才会触发TCP客户端向服务器发送终止连接请求。

### socket 实现 TCP

参考
- [linux socket编程详解](https://www.cnblogs.com/jiangzhaowei/p/8261174.html)
- [Linux下简单socket编程](https://blog.csdn.net/weixin_41249411/article/details/89060985)


代码: 
- 客户端向服务器发送数据
- 服务器向客户端响应
- C编译：gcc  socket_test.cpp -o socket
- C++：g++  socket_test.cpp -o socket -std=c++11

```c++
// 一直监听本机的8000号端口，如果收到连接请求，将接收请求并接收客户端发来的消息，并向客户端返回消息。
#include<stdio.h>  
#include<stdlib.h>  
#include<string.h>  
#include<errno.h>  
#include<sys/types.h>  
#include<sys/socket.h>  
#include<netinet/in.h>  
#include <unistd.h> // fork/close

#define DEFAULT_PORT 8000  
#define MAXLINE 4096 

int main(int argc, char** argv)  
{  
    int    socket_fd, connect_fd;  
    struct sockaddr_in     servaddr;  
    char    buff[4096];  
    int     n;  
    //初始化Socket  
    if( (socket_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1 ){  
        printf("create socket error: %s(errno: %d)\n",strerror(errno),errno);  
        exit(0);  
    }  
    //初始化  
    memset(&servaddr, 0, sizeof(servaddr));  
    servaddr.sin_family = AF_INET;  
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY); //IP地址设置成INADDR_ANY,让系统自动获取本机的IP地址。  
    servaddr.sin_port = htons(DEFAULT_PORT); //设置的端口为DEFAULT_PORT  
  
    //将本地地址绑定到所创建的套接字上  
    if( bind(socket_fd, (struct sockaddr*)&servaddr, sizeof(servaddr)) == -1){  
        printf("bind socket error: %s(errno: %d)\n",strerror(errno),errno);  
        exit(0);  
    }  
    //开始监听是否有客户端连接  
    if( listen(socket_fd, 10) == -1){  
        printf("listen socket error: %s(errno: %d)\n",strerror(errno),errno);  
        exit(0);  
    }  
    printf("======waiting for client's request======\n");  
    while(1){  
//阻塞直到有客户端连接，不然多浪费CPU资源。  
        if( (connect_fd = accept(socket_fd, (struct sockaddr*)NULL, NULL)) == -1){  
            printf("accept socket error: %s(errno: %d)",strerror(errno),errno);  
            continue;  
        }  
        //接受客户端传过来的数据  
        n = recv(connect_fd, buff, MAXLINE, 0);  
        //向客户端发送回应数据  
        if(!fork()){ /*紫禁城*/  
            if(send(connect_fd, "Hello,you are connected!\n", 26,0) == -1)  
            perror("send error");  
            close(connect_fd);  
            exit(0);  
        }  
        buff[n] = '\0';  
        printf("recv msg from client: %s\n", buff);  
        close(connect_fd);  
    }  
    close(socket_fd);  
}
```

```c++
/* File Name: client.c */  
#include<stdio.h>  
#include<stdlib.h>  
#include<string.h>  
#include<errno.h>  
#include<sys/types.h>  
#include<sys/socket.h>  
#include<netinet/in.h>  
  
#define MAXLINE 4096  

int main(int argc, char** argv)  
{  
    int    sockfd, n,rec_len;  
    char    recvline[4096], sendline[4096];  
    char    buf[MAXLINE];  
    struct sockaddr_in    servaddr;  
  
    if( argc != 2){  
        printf("usage: ./client <ipaddress>\n");  
        exit(0);  
    }  
  
    if( (sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0){  
        printf("create socket error: %s(errno: %d)\n", strerror(errno),errno);  
        exit(0);  
    }  
  
    memset(&servaddr, 0, sizeof(servaddr));  
    servaddr.sin_family = AF_INET;  
    servaddr.sin_port = htons(8000);  
    // inet_pton 是Linux下IP地址转换函数，可以在将IP地址在“点分十进制”和“整数”之间转换 ，是inet_addr的扩展。
    if( inet_pton(AF_INET, argv[1], &servaddr.sin_addr) <= 0){  
        printf("inet_pton error for %s\n",argv[1]);  
        exit(0);  
    }  
    if( connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0){  
        printf("connect error: %s(errno: %d)\n",strerror(errno),errno);  
        exit(0);  
    }  
    printf("send msg to server: \n");  
    fgets(sendline, 4096, stdin);  
    if( send(sockfd, sendline, strlen(sendline), 0) < 0)  
    {  
        printf("send msg error: %s(errno: %d)\n", strerror(errno), errno);  
        exit(0);  
    }  
    if((rec_len = recv(sockfd, buf, MAXLINE,0)) == -1) {  
       perror("recv error");  
       exit(1);  
    }  
    buf[rec_len]  = '\0';  
    printf("Received : %s ",buf);  
    close(sockfd);  
    exit(0);  
}  
```

测试：

```shell
# 编译server.c
gcc -o server server.c
# 启动进程：
./server
# 显示结果并等待客户端连接。
# ======waiting for client's request======
# 编译 client.c
gcc -o client server.c
# 客户端去连接server：
./client 127.0.0.1 
# 等待输入消息
# 发送一条消息，输入：c++，服务端就能看到
# 可以不用client,可以使用telnet来测试：
telnet 127.0.0.1 8000
```

服务端：

```c++
/*serve_tcp.c*/
#include<stdio.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<stdlib.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<string.h>

int main(){
	//创建套接字
	int serv_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

	//初始化socket元素
	struct sockaddr_in serv_addr;
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
	serv_addr.sin_port = htons(1234);

	//绑定文件描述符和服务器的ip和端口号
	bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));

	//进入监听状态，等待用户发起请求
	listen(serv_sock, 20);
	//接受客户端请求
	//定义客户端的套接字，这里返回一个新的套接字，后面通信时，就用这个clnt_sock进行通信
	struct sockaddr_in clnt_addr;
	socklen_t clnt_addr_size = sizeof(clnt_addr);
	int clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_size);

	//接收客户端数据，并相应
	char str[256];
	read(clnt_sock, str, sizeof(str));
	printf("client send: %s\n",str);
	strcat(str, "+ACK");
	write(clnt_sock, str, sizeof(str));

	//关闭套接字
	close(clnt_sock);
	close(serv_sock);

	return 0;
}
```


客户端：

```c++
/*client_tcp.c*/
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>

int main(){
	//创建套接字
	int sock = socket(AF_INET, SOCK_STREAM, 0);
	//服务器的ip为本地，端口号1234
	struct sockaddr_in serv_addr;
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
	serv_addr.sin_port = htons(1234);
	//向服务器发送连接请求
	connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
	//发送并接收数据
	char buffer[40];
	printf("Please write:");
	scanf("%s", buffer);
	write(sock, buffer, sizeof(buffer));
	read(sock, buffer, sizeof(buffer) - 1);
	printf("Serve send: %s\n", buffer);
	//断开连接
	close(sock);

	return 0;
}
```

### Socket编程方法

三种高效的 Socket 编程方法：**select**、**poll** 和 **epoll**.

select，poll，epoll 都是 IO 多路复用的机制，它们都需要在读写事件就绪后自己负责进行读写，也就是说这个读写过程是阻塞的。select、poll、epoll 三者区别
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/38c2a3040b2046559f91e8872d0ebe7e?from=pc)

总结：
- epoll是 Linux 目前大规模网络并发程序开发的**首选**模型。在绝大多数情况下性能远超 select 和 poll。目前流行的高性能web服务器Nginx正式依赖于epoll提供的高效网络套接字轮询服务。
- 但是，在并发连接不高的情况下，多线程 + 阻塞 IO 方式可能性能更好。

### select -- 数组，O(N)

select 最多能同时监视 1024 个 socket（因为 fd_set 结构体大小是 128 字节，每个 bit 表示一个文件描述符）。用户需要维护一个临时数组，存储文件描述符。当内核有事件发生时，内核将 fd_set 中没发生的文件描述符清空，然后拷贝到用户区。select 返回的是整个数组，它需要遍历整个数组才知道谁发生了变化。
- ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/f22c3ae6f83a435196360e909f8891cf?from=pc)

代码：

```c++
#include<stdio.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<unistd.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<stdlib.h>
#include<string.h>
#include<sys/time.h>
static void Usage(const char* proc)
{
    printf("%s [local_ip] [local_port]\n",proc);
}
int array[4096];
static int start_up(const char* _ip,int _port)
{
    int sock = socket(AF_INET,SOCK_STREAM,0);
    if(sock < 0)
    {
        perror("socket");
        exit(1);
    }
    struct sockaddr_in local;
    local.sin_family = AF_INET;
    local.sin_port = htons(_port);
    local.sin_addr.s_addr = inet_addr(_ip);
    if(bind(sock,(struct sockaddr*)&local,sizeof(local)) < 0)
    {
        perror("bind");
        exit(2);
    }
    if(listen(sock,10) < 0)
    {
        perror("listen");
        exit(3);
    }
    return sock;
}
int main(int argc,char* argv[])
{
    if(argc != 3)
    {
        Usage(argv[0]);
        return -1;
    }
    int listensock = start_up(argv[1],atoi(argv[2]));
    int maxfd = 0;
    fd_set rfds;
    fd_set wfds;
    array[0] = listensock;
    int i = 1;
    int array_size = sizeof(array)/sizeof(array[0]);
    for(; i < array_size;i++)
    {
        array[i] = -1;
    }
    while(1)
    {
        FD_ZERO(&rfds);
        FD_ZERO(&wfds);
        for(i = 0;i < array_size;++i)
        {
            if(array[i] > 0)
            {
                FD_SET(array[i],&rfds);
                FD_SET(array[i],&wfds);
                if(array[i] > maxfd)
                {
                    maxfd = array[i];
                }
            }
        }
        switch(select(maxfd + 1,&rfds,&wfds,NULL,NULL))
        {
            case 0:
                {
                    printf("timeout\n");
                    break;
                }
            case -1:
                {
                    perror("select");
                    break;
                }
             default:
                {
                    int j = 0;
                    for(; j < array_size; ++j)
                    {
                        if(j == 0 && FD_ISSET(array[j],&rfds))
                        {
                            //listensock happened read events
                            struct sockaddr_in client;
                            socklen_t len = sizeof(client);
                            int new_sock = accept(listensock,(struct sockaddr*)&client,&len);
                            if(new_sock < 0)//accept failed
                            {
                                perror("accept");
                                continue;
                            }
                            else//accept success
                            {
                                printf("get a new client%s\n",inet_ntoa(client.sin_addr));
                                fflush(stdout);
                                int k = 1;
                                for(; k < array_size;++k)
                                {
                                    if(array[k] < 0)
                                    {
                                        array[k] = new_sock;
                                        if(new_sock > maxfd)
                                            maxfd = new_sock;
                                        break;
                                    }
                                }
                                if(k == array_size)
                                {
                                    close(new_sock);
                                }
                            }
                        }//j == 0
                        else if(j != 0 && FD_ISSET(array[j], &rfds))
                        {
                            //new_sock happend read events
                            char buf[1024];
                            ssize_t s = read(array[j],buf,sizeof(buf) - 1);
                            if(s > 0)//read success
                            {
                                buf[s] = 0;
                                printf("clientsay#%s\n",buf);
                                if(FD_ISSET(array[j],&wfds))
                                {
                                    char *msg = "HTTP/1.0 200 OK <\r\n\r\n<html><h1>yingying beautiful</h1></html>\r\n";
                                    write(array[j],msg,strlen(msg));

                                }
                            }
                            else if(0 == s)
                            {
                                printf("client quit!\n");
                                close(array[j]);
                                array[j] = -1;
                            }
                            else
                            {
                                perror("read");
                                close(array[j]);
                                array[j] = -1;
                            }
                        }//else j != 0  
                    }
                    break;
                }
        }
    }
    return 0;
}
```


### poll -- 链表，O(N)

poll 就是把 select 中的 fd_set 数组换成了链表，其他和 select 没什么不同。
- ![img](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/8b557aa29c4a430b9585e5e868e4932e?from=pc)

代码：
- poll()函数返回fds集合中就绪的读、写，或出错的描述符数量，返回0表示超时，返回-1表示出错；
- fds是一个struct pollfd类型的数组，用于存放需要检测其状态的socket描述符，并且调用poll函数之后fds数组不会被清空；
- nfds记录数组fds中描述符的总数量；
- timeout是调用poll函数阻塞的超时时间，单位毫秒；
- 一个pollfd结构体表示一个被监视的文件描述符，通过传递fds[]指示 poll() 监视多个文件描述符。其中，结构体的events域是监视该文件描述符的事件掩码，由用户来设置这个域，结构体的revents域是文件描述符的操作结果事件掩码，内核在调用返回时设置这个域。events域中请求的任何事件都可能在revents域中返回。

```c++
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<poll.h>
static void usage(const char *proc)
{
    printf("%s [local_ip] [local_port]\n",proc);
}
int start_up(const char*_ip,int _port)
{
    int sock = socket(AF_INET,SOCK_STREAM,0);
    if(sock < 0)
    {
        perror("socket");
        return 2;
    }
    int opt = 1;
    setsockopt(sock,SOL_SOCKET,SO_REUSEADDR,&opt,sizeof(opt));
    struct sockaddr_in local;
    local.sin_family = AF_INET;
    local.sin_port = htons(_port);
    local.sin_addr.s_addr = inet_addr(_ip);
    if(bind(sock,(struct sockaddr*)&local,sizeof(local)) < 0)
    {
        perror("bind");
        return 3;
    }
    if(listen(sock,10) < 0)
    {
        perror("listen");
        return 4;
    }
    return sock;
}
int main(int argc, char*argv[])
{
    if(argc != 3)
    {
        usage(argv[0]);
        return 1;
    }
    int sock = start_up(argv[1],atoi(argv[2]));
    struct pollfd peerfd[1024];
    peerfd[0].fd = sock;
    peerfd[0].events = POLLIN;
    int nfds = 1;
    int ret;
    int maxsize = sizeof(peerfd)/sizeof(peerfd[0]);
    int i = 1;
    int timeout = -1;
    for(; i < maxsize; ++i)
    {
        peerfd[i].fd = -1;
    }
    while(1)
    {
        switch(ret = poll(peerfd,nfds,timeout))
        {
            case 0:
                printf("timeout...\n");
                break;
            case -1:
                perror("poll");
                break;
            default:
                {
                        if(peerfd[0].revents & POLLIN)
                        {
                            struct sockaddr_in client;
                            socklen_t len = sizeof(client);
                            int new_sock = accept(sock,\
                                    (struct sockaddr*)&client,&len);
                            printf("accept finish %d\n",new_sock);
                            if(new_sock < 0)
                            {
                                perror("accept");
                                continue;
                            }
                            printf("get a new client\n");
                                int j = 1;
                                for(; j < maxsize; ++j)
                                {
                                    if(peerfd[j].fd < 0)
                                    {
                                        peerfd[j].fd = new_sock;
                                        break;
                                    }
                                }
                                if(j == maxsize)
                                {
                                    printf("to many clients...\n");
                                    close(new_sock);
                                }
                                peerfd[j].events = POLLIN;
                                if(j + 1 > nfds)
                                    nfds = j + 1;
                        }
                        for(i = 1;i < nfds;++i)
                        {
                            if(peerfd[i].revents & POLLIN)
                        {
                            printf("read ready\n");
                            char buf[1024];
                            ssize_t s = read(peerfd[i].fd,buf, \
                                    sizeof(buf) - 1);
                            if(s > 0)
                            {
                                buf[s] = 0;
                                printf("client say#%s",buf);
                                fflush(stdout);
                                peerfd[i].events = POLLOUT;
                            }
                        else if(s <= 0)
                            {
                                close(peerfd[i].fd);
                                peerfd[i].fd = -1;
                            }
                            else
                            {

                            }
                        }//i != 0
                        else if(peerfd[i].revents & POLLOUT)
                        {
                            char *msg = "HTTP/1.0 200 OK \
                                         <\r\n\r\n<html><h1> \
                                         yingying beautiful \
                                         </h1></html>\r\n";
                            write(peerfd[i].fd,msg,strlen(msg));
                            close(peerfd[i].fd);
                            peerfd[i].fd = -1;
                        }
                        else
                        {
                        }
                    }//for
                }//default
                break;
        }
    }
    return 0;
}

```

### epoll -- 哈希，O(1)，主流

epoll 是基于事件驱动的 IO 方式，它没有文件描述符个数限制，它将用户关心的文件描述符的事件存放到内核的一个事件表中（简单来说，就是由内核来负责存储（红黑树）有事件的 socket 句柄），这样在用户空间和内核空间的copy只需一次。优点如下：
- 没有最大并发连接的限制，能打开的fd上限远大于1024（1G的内存能监听约10万个端口）
- 采用回调的方式，效率提升。只有活跃可用的fd才会调用callback函数，也就是说 epoll 只管你“活跃”的连接，而跟连接总数无关；
- 内存拷贝。使用mmap()文件映射内存来加速与内核空间的消息传递，减少复制开销。
epoll 有两种工作方式：
- LT模式（水平触发）：若就绪的事件一次没有处理完，就会一直去处理。也就是说，将没有处理完的事件继续放回到就绪队列之中（即那个内核中的链表），一直进行处理。
- ET模式（边缘触发）：就绪的事件只能处理一次，若没有处理完会在下次的其它事件就绪时再进行处理。而若以后再也没有就绪的事件，那么剩余的那部分数据也会随之而丢失。
由此可见：ET模式的效率比LT模式的效率要高很多。只是如果使用ET模式，就要保证每次进行数据处理时，要将其处理完，不能造成数据丢失，这样对编写代码的人要求就比较高。

![img](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/e16129dbd4d844728257b8f32af1a558?from=pc)


```c++
#include<stdio.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<stdlib.h>
#include<string.h>
#include<sys/epoll.h>

static Usage(const char* proc)
{
    printf("%s [local_ip] [local_port]\n",proc);
}
int start_up(const char*_ip,int _port)
{
    int sock = socket(AF_INET,SOCK_STREAM,0);
    if(sock < 0)
    {
        perror("socket");
        exit(2);
    }
    struct sockaddr_in local;
    local.sin_family = AF_INET;
    local.sin_port = htons(_port);
    local.sin_addr.s_addr = inet_addr(_ip);
    if(bind(sock,(struct sockaddr*)&local,sizeof(local)) < 0)
    {
        perror("bind");
        exit(3);
    }
    if(listen(sock,10)< 0)
    {
        perror("listen");
        exit(4);
    }
    return sock;
}
int main(int argc, char*argv[])
{
    if(argc != 3)
    {
        Usage(argv[0]);
        return 1;
    }
    int sock = start_up(argv[1],atoi(argv[2]));
    int epollfd = epoll_create(256);
    if(epollfd < 0)
    {
        perror("epoll_create");
        return 5;
    }
    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.fd = sock;
    if(epoll_ctl(epollfd,EPOLL_CTL_ADD,sock,&ev) < 0)
    {
        perror("epoll_ctl");
        return 6;
    }
    int evnums = 0;//epoll_wait return val
    struct epoll_event evs[64];
    int timeout = -1;
    while(1)
    {
        switch(evnums = epoll_wait(epollfd,evs,64,timeout))
        {
            case 0:
     printf("timeout...\n");
     break;
            case -1:
     perror("epoll_wait");
     break;
default:
     {
         int i = 0;
         for(; i < evnums; ++i)
         {
             struct sockaddr_in client;
             socklen_t len = sizeof(client);
             if(evs[i].data.fd == sock \
                     && evs[i].events & EPOLLIN)
             {
                 int new_sock = accept(sock, \
                         (struct sockaddr*)&client,&len);
                 if(new_sock < 0)
                 {
                     perror("accept");
                     continue;
                 }//if accept failed
                 else 
                 {
                     printf("Get a new client[%s]\n", \
                             inet_ntoa(client.sin_addr));
                     ev.data.fd = new_sock;
                     ev.events = EPOLLIN;
                     epoll_ctl(epollfd,EPOLL_CTL_ADD,\
                             new_sock,&ev);
                 }//accept success

             }//if fd == sock
             else if(evs[i].data.fd != sock && \
                     evs[i].events & EPOLLIN)
             {
                 char buf[1024];
                 ssize_t s = read(evs[i].data.fd,buf,sizeof(buf) - 1);
                 if(s > 0)
                 {
                     buf[s] = 0;
                     printf("client say#%s",buf);
                     ev.data.fd = evs[i].data.fd;
                     ev.events = EPOLLOUT;
                     epoll_ctl(epollfd,EPOLL_CTL_MOD, \
                             evs[i].data.fd,&ev);
                 }//s > 0
                 else
                 {
                     close(evs[i].data.fd);
                     epoll_ctl(epollfd,EPOLL_CTL_DEL, \
                             evs[i].data.fd,NULL);
                 }
             }//fd != sock
             else if(evs[i].data.fd != sock \
                     && evs[i].events & EPOLLOUT)
             {
                 char *msg =  "HTTP/1.0 200 OK <\r\n\r\n<html><h1>yingying beautiful </h1></html>\r\n";
                 write(evs[i].data.fd,msg,strlen(msg));
                 close(evs[i].data.fd);
                 epoll_ctl(epollfd,EPOLL_CTL_DEL, \
                             evs[i].data.fd,NULL);
             }//EPOLLOUT
             else
             {
             }
         }//for
     }//default
     break;
        }//switch
    }//while
    return 0;
}
```

- epoll_create函数创建一个epoll句柄，参数size表明内核要监听的描述符数量。调用成功时返回一个epoll句柄描述符，失败时返回-1。
- epoll_ctl函数注册要监听的事件类型。四个参数解释如下： epfd表示epoll句柄； op表示fd操作类型：EPOLL_CTL_ADD（注册新的fd到epfd中），EPOLL_CTL_MOD（修改已注册的fd的监听事件），EPOLL_CTL_DEL（从epfd中删除一个fd）；fd是要监听的描述符； event表示要监听的事件，
- epoll_wait 函数等待事件的就绪，成功时返回就绪的事件数目，调用失败时返回 -1，等待超时返回 0。maxevents告诉内核events的大小，timeout表示等待的超时事件

epoll_event结构体定义如下：

```c++
struct epoll_event { 
  __uint32_t events; /* Epoll events */ 
  epoll_data_t data; /* User data variable */ 
}; 
typedef union epoll_data {
  void *ptr; 
  int fd; 
  __uint32_t u32;
  __uint64_t u64; 
} epoll_data_t;
```



# Shell语言

更多编程语言介绍：
- [编程语言发展历史]({{ site.baseurl}}{% post_url 2010-07-26-computer-history %}#编程语言变迁)
- 【2022-11-20】[linux bash shell 最常用的函数和指令](https://www.toutiao.com/article/7167905628231565827)
- 【2024-3-5】[Bash Shell脚本进阶](https://linuxstory.gitbook.io/advanced-bash-scripting-guide-in-chinese/zheng-wen/part1)

## Shell知识点

在 Linux 的基础上再度深入学习 Shell，可以极大的减少重复工作的压力。毕竟批量处理才是工作的常态呢~
- ![](https://raw.githubusercontent.com/woaielf/woaielf.github.io/master/_posts/Pic/1709/170920-1.png)
- ![](https://raw.githubusercontent.com/woaielf/woaielf.github.io/master/_posts/Pic/1709/170920-2.png)
- ![](https://raw.githubusercontent.com/woaielf/woaielf.github.io/master/_posts/Pic/1709/170920-3.png)


## 总结


### 经验

Bash Shell，使用反斜线时，中途注释语句无效!
- 【2024-4-11】 如下注释行无效

```sh
deepspeed --master_port 30001 ./llm/training/conversation_reward/main.py \
   --max_seq_len 2048 \
   --per_device_train_batch_size 1 \
   #--per_device_train_batch_size 2 \
   --per_device_eval_batch_size 2 \
   --weight_decay 0.01
```


## 常规语法

查看 Shell 版本

```sh
bash --version
echo "$BASH_VERSION"
```

### 执行shell

```sh
# ----- test.sh -----
#!/bin/bash
VAR="world"
echo "Hello $VAR!" # => Hello world!
# -------------------
# 执行
bash test.sh # 执行shell脚本
source "${0%/*}/../share/foo.sh" # 当前shell中执行
(cd somedir; echo "I'm now in $PWD") # 执行子shell
# 条件执行
git commit && git push # 成功才继续
git commit || echo "Commit failed" # 失败才继续
# 命令嵌入: ${}或``
echo "I'm in $(PWD)"
# Same as:
echo "I'm in `pwd`"
```

### 系统命令

```sh
history # 显示历史
sudo !! # 使用 sudo 运行上一个命令
shopt -s histverify # 不要立即执行扩展结果
!$ # 展开最新命令的最后一个参数
!* # 展开最新命令的所有参数
!-n # 展开第 n 个最近的命令
!n # 展开历史中的第 n 个命令
!<command> # 展开最近调用的命令 <command>
!! # 再次执行最后一条命令 
!!:s/<FROM>/<TO>/ # 在最近的命令中将第一次出现的 <FROM> 替换为 <TO> 
!!:gs/<FROM>/<TO>/ # 在最近的命令中将所有出现的 <FROM> 替换为 <TO> 
!$:t # 仅从最近命令的最后一个参数扩展基本名称 
!$:h # 仅从最近命令的最后一个参数展开目录 
# !! 和 !$ 可以替换为任何有效的扩展
# 切片 Slices
!!:n # 仅扩展最近命令中的第 n 个标记（命令为 0；第一个参数为 1） 
!^ # 从最近的命令展开第一个参数 
!$ # 从最近的命令中展开最后一个标记 
!!:n-m # 从最近的命令扩展令牌范围 
!!:n-$ # 从最近的命令中将第 n 个标记展开到最后
# 重定向
python hello.py > output.txt   # 标准输出到（文件）
python hello.py >> output.txt  # 标准输出到（文件），追加
python hello.py 2> error.log   # 标准错误到（文件）
python hello.py 2>&1           # 标准错误到标准输出
python hello.py 2>/dev/null    # 标准错误到（空null）
python hello.py &>/dev/null    # 标准输出和标准错误到（空null）
python hello.py < foo.txt      # 将 foo.txt 提供给 python 的标准输入
```

### 变量操作

sheel变量

```sh
# 默认值
${FOO:-val} # $FOO，如果未设置，则为 val
${FOO:=val} # 如果未设置，则将 $FOO 设置为 val
${FOO:+val} # val 如果设置了$FOO
${FOO:?message} # 如果 $FOO 未设置，则显示消息并退出

NAME="John"
echo ${NAME}    # => John (变量)
echo $NAME      # => John (变量)
echo "$NAME"    # => John (变量)
echo '$NAME'    # => $NAME (字符串原样输出)，单引号时，不解析变量
echo "${NAME}!" # => John! (变量)
NAME = "John"   # => 报错：Error (注意不能有空格)
# {}扩展
echo {A,B} # 与 A B 相同
echo {A..D}.js # 与 A.js B.js C.js D.js相同
echo {1..5} # 与 1 2 3 4 5 相同
# 数值计算
a=2
$((a + 200))      # Add 200 to $a
$(($RANDOM%200))  # 随机数 Random number 0..199
# 特殊变量
$? # 最后一个任务的退出状态
$! # 最后一个后台任务的 PID
$$ # shell PID
$0 # shell 脚本的文件名

# 注释：多行注释使用 :' 打开和 ' 关闭
: '
这是一个
非常整洁的
bash 注释
'
# Heredoc
cat <<END
hello world
END
```

特殊变量

```sh
#!/bin/bash
echo "Process ID: $$"
echo "File Name: $0"
echo "First Parameter : $1"
echo "Second Parameter : $2"
echo "All parameters 1: $@"
echo "All parameters 2: $*"
echo "Total: $#"
```

### 变量作用域

#### 变量的作用域（Scope）

Shell 变量作用域分三种：
- **全局变量**（global variable）: **当前 Shell 会话**中使用
- **局部变量**（local variable）: 只能在**函数内部**使用
- **环境变量**（environment variable）: 在**其它 Shell** 中使用。

解析
- **全局变量**：变量在当前的整个 Shell 会话中都有效。每个 Shell 会话都有自己的作用域，彼此之间互不影响。在 Shell 中定义的变量，默认就是全局变量。
- **局部变量**：Shell 函数中定义的变量默认是**全局变量**，它和在函数外部定义变量拥有一样的效果
- **环境变量**：环境变量被创建时所处的 Shell 被称为父 Shell，如果在父 Shell 中再创建一个 Shell，则该 Shell 被称作子 Shell。当子 Shell 产生时，它会继承父 Shell 的环境变量为自己所用，所以说环境变量可从父 Shell 传给子 Shell。
  - 注意，环境变量只能**向下传递**而不能向上传递，即“传子不传父”


```sh
a=3 # 全局变量
global a=3 # 报错，没有global关键词
export a # 将自定义变量设定为系统环境变量

fun f(){
    c='1' # 全局变量
    local t='2' # 局部变量,仅函数内使用
}
local t='2' # 报错，local必须出现在函数内
```


#### export

Linux export 命令用于设置/显示环境变量。

shell 中执行程序时，shell 会提供一组环境变量。export 可新增，修改或删除环境变量，供后续执行的程序使用。

export 命令的作用域：
> 当前终端中直接输入的 export 变量仅**当前shell终端**及其**子shell**可见，另起一个终端将无法访问。

注意
- 父shell中的export变量，子shell可读
- 子shell变量是父shell的一个拷贝，不影响父shell取值
- 子shell export变量，父shell读不到

```sh
export WORD="hello"

echo $WORD           # 可以看到输出 hello
env | grep WORD      # 可以看到有WORD变量
sh -c "echo $WORD"   # 子shell中执行，同样可以看到输出了 hello
```

如何保证其他终端可见？
- `~/.bashrc` 或者 `/etc/profile` 中使用 `export` 命令配置全局的环境变量，然后`source`，所有终端都可见

#### 变量传递

如何从子shell向父shell传递变量
- 命令传输
- 中间文件
- 管道
- here文档

```sh
# 命令传输
pvar=`subvar='hello shell'`
echo $pvar
# 文件传输
(
    subvar='hello shell'
    echo "$subvar" > tmp.txt
)
read pvar < tmp.txt
echo $pvar
# 管道传输
mkfifo -m 777 npipe # 创建管道 npipe
(
    subsend="hello world"
    echo "$subsend" > npipe &
)
read pread < npipe
echo "$pread"
# here 文档
read pvar <<HERE
`subvar="hello shell"
echo $subvar`
HERE
echo $pvar
```

### 函数参数

#### 函数

```sh
# function get_name() { # function 关键字可以省略
get_name() {
    echo "John $1"
}
echo "You are $(get_name)"
# 带返回值的函数
myfunc() {
    local myresult='some value'
    echo $myresult
}
result="$(myfunc)"

```

#### 参数

```sh
$0 # 脚本本身的名称
$1 … $9 # 参数 1 ... 9
$1 # 第一个参数
${10} # 位置参数 10
$# # 参数数量
$$ # shell 的进程 id
$* # 所有参数
$@ # 所有参数，从第一个开始
$- # 当前选项
$_ # 上一个命令的最后一个参数
```

### 控制

#### 操作系统差异


debain（乌班图）linux 下，字符串判断时，会出现以下错误
- 因为 ubuntu 默认 shell 使用 dash，dash 与 bash 一些指令上有些差异
- 解法: 改回 `/bin/sh -> bash`，修改默认sh
  - `sudo dpkg-reconfigure dash` 启动可视化编辑页面
  - 然后选 No，改回 `/bin/sh -> bash`
  - 把 == 改成 =

```sh
[: =~: binary operator expected
[[: =~: binary operator expected
```


#### if 条件判断

```sh
# 字符串比较
[[ -z STR ]] # 空字符串
[[ -n STR ]] # 非空字符串
[[ STR == STR ]] # 相等
[[ STR = STR ]] # 相等（同上）
[[ STR < STR ]] # 小于 (ASCII)
[[ STR > STR ]] # 大于 (ASCII)
[[ STR != STR ]] # 不相等
[[ STR =~ STR ]] # 正则表达式
# 整数比较
[[ NUM -eq NUM ]] # 等于 Equal
[[ NUM -ne NUM ]] # 不等于 Not equal
[[ NUM -lt NUM ]] # 小于 Less than
[[ NUM -le NUM ]] # 小于等于 Less than or equal
[[ NUM -gt NUM ]] # 大于 Greater than
[[ NUM -ge NUM ]] # 大于等于 Greater than or equal
(( NUM < NUM )) # 小于
(( NUM <= NUM )) # 小于或等于
(( NUM > NUM )) # 比...更大
(( NUM >= NUM )) # 大于等于
# 文件
[[ -e FILE ]] # 存在
[[ -d FILE ]] # 目录
[[ -f FILE ]] # 文件
[[ -h FILE ]] # 符号链接
[[ -s FILE ]] # 大小 > 0 字节
[[ -r FILE ]] # 可读
[[ -w FILE ]] # 可写
[[ -x FILE ]] # 可执行文件
[[ f1 -nt f2 ]] # f1 比 f2 新
[[ f1 -ot f2 ]] # f2 比 f1 新
[[ f1 -ef f2 ]] # 相同的文件
# 高级
[[ X && Y ]] # 条件组合
[[ "$A" == "$B" ]] # 是否相等
[[ -o noclobber ]] # 如果启用 OPTION
[[ ! EXPR ]] # 不是 Not
[[ X && Y ]] # 和 And
[[ X || Y ]] # 或者 Or
```

```sh
# 整型
if (( $a < $b )); then
   echo "$a is smaller than $b"
fi
# 字符串
if [[ -z "$string" ]]; then
    echo "String is empty"
elif [[ -n "$string" ]]; then
    echo "String is not empty"
fi
# 正则表达式
if [[ '1. abc' =~ ([a-z]+) ]]; then
    echo ${BASH_REMATCH[1]}
fi

# 文件是否存在
if [[ -e "file.txt" ]]; then
    echo "file exists"
fi
# 逻辑运算
if [ "$1" = 'y' -a $2 -gt 0 ]; then
    echo "yes"
fi
if [ "$1" = 'n' -o $2 -lt 0 ]; then
    echo "no"
fi
```

复合条件判断
- `&& ||-a –o` 处理

```sh
#!/bin/bash

# 等效表达: [[]] ＝ []
[  exp1  -a exp2  ] = [[  exp1 && exp2 ]] = [  exp1  ]&& [  exp2  ] = [[ exp1  ]] && [[  exp2 ]]
[  exp1  -o exp2  ] = [[  exp1 || exp2 ]] = [  exp1  ]|| [  exp2  ] = [[ exp1  ]] || [[  exp2 ]]

# 整型比较
count="$1"
if [ $count -gt 15 -o $count -lt 5 ];then
   echo right
fi
# 字符串
if [[ "a" == "a" ]] || [[ 2 -gt 1]] ;then
    echo "ok";
fi

```

实测
- `=` 和 `==` 等效
- `[]` 和 `test` 等效
-  `[[]]` 和 `[]`大体等效，但正则表达式只能用双括号
- `=` 两边要留空，否则结果错误

```sh
echo "单括号（识别错误）"
if [ "1"="" ] && [ "1"="1" ]; then echo A; else echo B; fi # A
if [ "1"="" -a "1"="1" ]; then echo A; else echo B; fi # A
echo "留空格（正确）"
if [ "1" = "" ] && [ "1" = "1" ]; then echo A; else echo B; fi # B
if [ "1" = "" -a "1" = "1" ]; then echo A; else echo B; fi # B
echo "双括号"
if [[ "1"="" ]] && [[ "1"="1" ]]; then echo A; else echo B; fi # A
if [[ "1" = "" ]] && [[ "1" = "1" ]]; then echo A; else echo B; fi # B
# if [[ "1"="" -a "1"="1" ]]; then echo A; else echo B; fi # 报错
echo "双等号（正确）"
if [ "1" == "" ] && [ "1" == "1" ]; then echo A; else echo B; fi # B
if [ "1" == "" -a "1" == "1" ]; then echo A; else echo B; fi # B
# 正则表达式需要双括号，否则报错
if [[ ${BASEDIR} =~ ^hdfs ]];then
    echo "y"
else
    echo 'n'
fi
# 组合条件中, 正则表达式单独使用[[]]括起来，不能混用！
# if [ $mode = 'local' -a ${BASEDIR} =~ ^hdfs ];then
if [ $mode = 'local' ] && [[ ${BASEDIR} =~ ^hdfs ]]; then
    echo "y"
else
    echo 'n'
fi
```

#### for 循环判断

```sh
# 基本 for 循环
for i in /etc/rc.*; do
    echo $i
done
# 类似 C 的 for 循环
for ((i = 0 ; i < 100 ; i++)); do
    echo $i
done
for i in `ls`;
do 
    echo $i is file name\! ;
done
# 字符串，[2023-2-4]注意：不能省略变量name_list，直接用字符串
name_list="httpd-init.service  httpd.service  httpd.socket  httpd@.service httpd.service.d";
for file in $name_list;
do
        echo "[$file]"
done
# 范围
for i in {1..5}; do
# for i in {5..50..5}; do # 设置步长
    echo "Welcome $i"
done
# awk版
awk 'BEGIN{for(i=1; i<=10; i++) print i}'
# 自动递增
i=1
while [[ $i -lt 4 ]]; do
    echo "Number: $i"
    ((i++))
done
# 自动递减
i=3
while [[ $i -gt 0 ]]; do
    echo "Number: $i"
    ((i--))
done
# Continue, break
for number in $(seq 1 3); do
    if [[ $number == 2 ]]; then
        continue;
        # break;
    fi
    echo "$number"
done
# Until
count=0
until [ $count -gt 10 ]; do
    echo "$count"
    ((count++))
done
# 死循环
# while :; do # 简写
while true; do
    # here is some code.
done
```

#### Case/switch

```sh
case "$1" in
    start | up)
    vagrant up
    ;;
    *)
    echo "Usage: $0 {start|stop|ssh}"
    ;;
esac
```

### 时间日期

[date用法](https://www.cnblogs.com/alsodzy/p/8403870.html)

```shell
cal # 日历

date +%Y%m%d 
date +%F
now=$(date +%y%m%d) # 获取今天时期
date +%Y%m%d%H%M%S # 当前时间，时分秒
date +%m%d%H%M%y.%S # 具体到毫秒
date +%w    # 今天是星期几
date +%W   # 当前为今年的第几周
# 时间戳
date +%s   # 获取时间戳
date -d @1521563928  # 将时间戳换算成日期
date +%s -d "2017-03-21 00:38:48" # 将日期换算成时间戳

# 相对时间
date -d 'now'    #显示当前时间
date -d tomorrow +%y%m%d # 明天
date -d yesterday +%Y%m%d # 获取昨天时期
date -d '30 second ago'    #显示30秒前的时间
date -d -2day +%Y%m%d # 获取前天日期
date -d '7 days ago' +%Y%m%d # 一星期前
date -d '1 weeks ago' +%Y%m%d # 一星期前
date -d '2 days ago'    #显示2天前的时间
date -d -10day +%Y%m% # 获取10天前的日期
date -d `date +%y%m01`"-1 day" # 上月最后一天
date -d '3 month 1 day'    # 显示3月零1天以后的时间
date -d "n days ago" +%y%m%d # 或n天前的
date -d '25 Dec' +%j    #显示12月25日在当年的哪一天

date -d "-3 day" # 3天前
date -d "+3 month"  # 3月后
date -d "-3 year" # 3年前，类似的，hour、minute、second
date -d `date -d "-3 month" +%y%m01`"-1 day" # 4个月前最后一天
date -d `date -d "+12 month" +%y%m01`"-1 day" # 11个月后第一天
date -d `date -d "+12 month" +%y%m01`"-1 day" +%Y%m%d # 11个月前最后一天
```

### 字符串

特殊的字符串处理方法
- #前 %后

```sh
# ----- 总结 -----
${FOO%suffix} # 删除后缀
${FOO#prefix} # 删除前缀
${FOO%%suffix} # 去掉长后缀
${FOO##prefix} # 删除长前缀
${FOO/from/to} # 替换第一个匹配项
${FOO//from/to} # 全部替换
${FOO/%from/to} # 替换后缀
${FOO/#from/to} # 替换前缀
echo ${food:-Cake}  #=> 如果没定义food变量，就赋默认值（Cake） $food or "Cake" 
${FOO:0:3} # 子串 (位置，长度)
${FOO:(-3):3} # 从右边开始的子串
${#FOO} # $FOO 的长度

# -------------
STR="/path/to/foo.cpp"
echo ${STR%.cpp}    # /path/to/foo 删短后缀
echo ${STR%.cpp}.o  # /path/to/foo.o
echo ${STR%/*}      # /path/to
echo ${STR##*.}     # cpp (extension)
echo ${STR##*/}     # foo.cpp (basepath)
echo ${STR#*/}      # path/to/foo.cpp
echo ${STR##*/}     # foo.cpp
echo ${STR/foo/bar} # /path/to/bar.cpp

url="http://c.biancheng.net/index.html"
echo ${url#*/}    # 结果为 /c.biancheng.net/index.html
echo ${url##*/}   # 结果为 index.html
str="---aa+++aa@@@"
echo ${str#*aa}   # 结果为 +++aa@@@
echo ${str##*aa}  # 结果为 @@@
echo ${url%/*}  # 结果为 http://c.biancheng.net
echo ${url%%/*}  # 结果为 http:
str="---aa+++aa@@@"
echo ${str%aa*}  # 结果为 ---aa+++
echo ${str%%aa*}  # 结果为 ---
# ---- 切片 -----
# 切片 Slicing
name="John"
echo ${name}           # => John
echo ${name:0:2}       # => Jo
echo ${name::2}        # => Jo
echo ${name::-1}       # => Joh
echo ${name:(-1)}      # => n 逆序
echo ${name:(-2)}      # => hn 逆序
echo ${name:(-2):2}    # => hn 逆序
length=2
echo ${name:0:length}  # => Jo
# 大小写转换：,小写 ^大写
STR="HELLO WORLD!"
echo ${STR,}      # => hELLO WORLD! 首字母小写
echo ${STR,,}     # => hello world! 全部小写
STR="hello world!"
echo ${STR^}      # => Hello world! 首字符大写
echo ${STR^^}     # => HELLO WORLD! 全部大写
ARR=(hello World)
echo "${ARR[@],}" # => hello world 数组元素首字母小写
echo "${ARR[@]^}" # => Hello World 数组元素首字母大写
```


### 数组

- 代码：

```shell
string="hello,shell,split,test" 
#将,替换为空格 
array=(${string//,/ })  # 空格区分，用()转数组
array=(`echo $string | tr ',' ' '` ) # 方法2
# 元素遍历
for var in ${array[@]} # 元素值遍历
do
   echo $var
done
for i in "${!array[@]}"; do # 下标遍历
  printf "%s\t%s\n" "$i" "${array[$i]}"
done

Fruits=('Apple' 'Banana' 'Orange') # 一次性定义
Fruits[0]="Apple" # 逐个赋值
Fruits[1]="Banana"
Fruits[2]="Orange"
# 批量定义
ARRAY1=(foo{1..2}) # => foo1 foo2
ARRAY2=({A..D})    # => A B C D
# 合并 => foo1 foo2 A B C D
ARRAY3=(${ARRAY1[@]} ${ARRAY2[@]})
# 声明构造
declare -a Numbers=(1 2 3)
Numbers+=(4 5) # 附加 => 1 2 3 4 5
# 索引含义
${Fruits[0]} # 第一个元素
${Fruits[-1]} # 最后一个元素
${Fruits[*]} # 所有元素
${Fruits[@]} # 所有元素 ""包围每个元素
${#Fruits[@]} # 总数
${#Fruits} # 第一节长度
${#Fruits[3]} # 第n个长度
${Fruits[@]:3:2} # 范围
${!Fruits[@]} # 所有 Key，索引index
# 数组操作
Fruits=("${Fruits[@]}" "Watermelon")         # 添加
Fruits+=('Watermelon')                       # 也是添加
Fruits=( ${Fruits[@]/Ap*/} )                 # 通过正则表达式匹配删除
unset Fruits[2]                              # 删除一项
Fruits=("${Fruits[@]}")                      # 复制
Fruits=("${Fruits[@]}" "${Veggies[@]}")      # 连接
lines=(`cat "logfile"`)                      # 从文件中读取
# 数组作为参数
function extract()
{
  local -n myarray=$1
  local idx=$2
  echo "${myarray[$idx]}"
}
Fruits=('Apple' 'Banana' 'Orange')
extract Fruits 2     # => Orangle
```

### 字典

```sh
declare -a sounds # 生命字典
# declare -A sounds # 生命字典, A在mac下执行失败
sounds[dog]="bark" # 赋值
sounds[cow]="moo"
# 取值
echo ${sounds[dog]} # Dog's sound
echo ${sounds[@]}   # All values 所有取值
echo ${!sounds[@]}  # All keys 所有key
echo ${#sounds[@]}  # Number of elements 元素个数
unset sounds[dog]   # Delete dog
# 遍历元素
for val in "${sounds[@]}"; do
    echo $val
done
for key in "${!sounds[@]}"; do
    echo $key
done
```

### 彩色日志

[shell彩色文字](https://blog.csdn.net/andylauren/article/details/60873400)
- 特效格式
  - \033[0m  关闭所有属性  
  - \033[1m   设置高亮度  
  - \03[4m   下划线  
  - \033[5m   闪烁  
  - \033[7m   反显  
  - \033[8m   消隐  
  - \033[30m ~ \033[37m   设置前景色  
  - \033[40m ~ \033[47m   设置背景色
- 光标位置
  - \033[nA  光标上移n行  
  - \03[nB   光标下移n行  
  - \033[nC   光标右移n行  
  - \033[nD   光标左移n行  
  - \033[y;xH设置光标位置  
  - \033[2J   清屏  
  - \033[K   清除从光标到行尾的内容  
  - \033[s   保存光标位置  
  - \033[u   恢复光标位置  
  - \033[?25l   隐藏光标  
  - \33[?25h   显示光标
- 特效可以叠加，需要使用“;”隔开
  - 例如：闪烁+下划线+白底色+黑字为 \033[5;4;47;30m闪烁+下划线+白底色+黑字为\033[0m

| 编码 | 颜色/动作 |
| --- | --- |
| 　　0 | 重新设置属性到缺省设置 |
| 　　1 | 设置粗体 |
| 　　2 | 设置一半亮度(模拟彩色显示器的颜色) |
| 　　4 | 设置下划线(模拟彩色显示器的颜色) |
| 　　5 | 设置闪烁 |
| 　　7 | 设置反向图象 |
| 　　22 | 设置一般密度 |
| 　　24 | 关闭下划线 |
| 　　25 | 关闭闪烁 |
| 　　27 | 关闭反向图象 |
| 　　30 | 设置黑色前景 |
| 　　31 | 设置红色前景 |
| 　　32 | 设置绿色前景 |
| 　　33 | 设置棕色前景 |
| 　　34 | 设置蓝色前景 |
| 　　35 | 设置紫色前景 |
| 　　36 | 设置青色前景 |
| 　　37 | 设置白色前景 |
| 　　38 | 在缺省的前景颜色上设置下划线 |
| 　　39 | 在缺省的前景颜色上关闭下划线 |
| 　　40 | 设置黑色背景 |
| 　　41 | 设置红色背景 |
| 　　42 | 设置绿色背景 |
| 　　43 | 设置棕色背景 |
| 　　44 | 设置蓝色背景 |
| 　　45 | 设置紫色背景 |
| 　　46 | 设置青色背景 |
| 　　47 | 设置白色背景 |
| 　　49 | 设置缺省黑色背景 |


```shell
# !/bin/bash

#【2021-12-28】
echo -e "\033[4;31m 下划线红字 \033[0m" 
echo -e "\033[5;34m 红字在闪烁 \033[0m" #闪烁
echo -e "\033[8m 消隐 \033[0m " #反影

# 彩色文字设置
prefix="\033["
Color_Off="0m" # Text Reset
# Bold High Intensty
BIBlack="30m" # "[1;90m" # Black
BIRed="31m" # "[1;91m" # Red
BIGreen="32m" # "[1;92m" # Green
BIYellow="33m" # "[1;93m" # Yellow
BIBlue="34m" # "[1;94m" # Blue
BIPurple="35m" # "[1;95m" # Purple
BICyan="36m" # "[1;96m" # Cyan
BIWhite="37m" # "[1;97m" # White
 
echo ${BRed} "===开始检测===!" ${Color_Off}
function log(){
    [ $# -eq 0 ]&& { echo "date [`"+%Y-%m-%d %H:%M:%S"`] 请输入要打印的日志！";exit 1; }
    [ $# -eq 1 ]&& { level="INFO";log_info=$1; }
    [ $# -gt 1 ]&& { level=$1;log_info=$2; }
    #echo "[`"+%Y-%m-%d %H:%M:%S"`] [$level] $log_info"
    cur_color="$BIWhite"
    case $level in
        "INFO") cur_color="$BIWhite";;
        "WARNING") cur_color="$BIYellow";;
        "ERROR") cur_color="$BIPurple";;
        "FETAL") cur_color="$BIRed";;
        *) cur_color="$BIWhite";;
    esac
	# echo -e "\033[4;31;42m 文字 \033[0m"
    echo -e  "${prefix}${cur_color} [`date "+%Y-%m-%d %H:%M:%S"`] [$level] $log_info ${prefix}${Color_Off}"
}
log "INFO" "TEST INFO"
log "WARNING" "TEST WARNING"
log "ERROR" "TEST ERROR"
log "FETAL" "TEST FETAL"

# ------- 失效 -------
【2018-10-12】
# 彩色文字设置
Color_Off="[0m" # Text Reset
# Bold High Intensty
BIBlack="[1;90m" # Black
BIRed="[1;91m" # Red
BIGreen="[1;92m" # Green
BIYellow="[1;93m" # Yellow
BIBlue="[1;94m" # Blue
BIPurple="[1;95m" # Purple
BICyan="[1;96m" # Cyan
BIWhite="[1;97m" # White
 
echo ${BRed} "===开始检测===!" ${Color_Off}
function log(){
    [ $# -eq 0 ]&& { echo "date [`"+%Y-%m-%d %H:%M:%S"`] 请输入要打印的日志！";exit 1; }
    [ $# -eq 1 ]&& { level="INFO";log_info=$1; }
    [ $# -gt 1 ]&& { level=$1;log_info=$2; }
    #echo "[`"+%Y-%m-%d %H:%M:%S"`] [$level] $log_info"
    cur_color="$BIWhite"
    case $level in
        "INFO") cur_color="$BIWhite";;
        "WARNING") cur_color="$BIYellow";;
        "ERROR") cur_color="$BIPurple";;
        "FETAL") cur_color="$BIRed";;
        *) cur_color="$BIWhite";;
    esac
    echo ${cur_color} "[`date "+%Y-%m-%d %H:%M:%S"`] [$level] $log_info" ${Color_Off}
}
```

### 随机抽奖

Shell随机创建手机号码与随机抽奖：
- 随机生成1000个以136开头的手机号码

```shell
#! usr/bin/bash

# 生成的手机号码存放到指定的目录的文件
filePath="/home/phoneNum.txt"

#(())语法类似C语法的括号
for((i=1;i<=1000;i++))
do
	# 取模
	num1=$[$RANDOM%10] # $RANDOM代表随机函数，是操作系统的全局变量
	num2=$[$RANDOM%10]
	num3=$[$RANDOM%10]
	num4=$[$RANDOM%10]
	num5=$[$RANDOM%10]
	num6=$[$RANDOM%10]
	num7=$[$RANDOM%10]
	num8=$[$RANDOM%10]
	num9=$[$RANDOM%10]
	# 将结果输到指定的文件里面
	echo "136$num1$num2$num3num4$num5$num6$num7$num8$num9" >> $filePath
done

# 寻找第100个的手机号码
head -100 phoneNum.txt | tail -1
# 查看是否有重复的手机号码
cat phoneNum.txt | sort -u|wc -l

# ================
# 抽取幸运的5位手机号码并去除已经抽取过的用户

#! usr/bin/bash
filePath="/home/phoneNum.txt"

# 循环读取5位用户手机号码
for((i=1;i<=5;i++))
do
	# 定位幸运观众所在行数
	#line=`wc -l $filePath | cut -d ' ' -f1`
  line=`wc -l $filePath | awk '{print $1}'
	#计算幸运行
	luck_line=$[RANDOM%line+1]
	#取出幸运观众所在行的电话号码,-1代表是一个
	luck_num=`head -$luck_line $filePath | tail -1` 
	#显示到屏幕,截取后位的号码数字
	echo "136****${luck_num:7:4}"
	# 将抽中的手机号码放到一个文本
	echo $luck_num >> luck.txt
	# 将抽中的手机号码在文本删除，防止下一次又抽中
	sed -i "/$luck_num/d" $filePath
done
# 查看还有多少行手机号码
wc -l /home/phoneNum.txt 

```


## 输出

### 系统输出

echo 和 printf

```sh
echo -n "Proceed? [y/n]: "
echo -e "a\tb" # 支持转移
read ans # 读入到变量 ans
read -n 1 ans    # 只有一个字符
echo $ans

printf
printf "Hello %s, I'm %s" Sven Olga #=> "Hello Sven, I'm Olga
printf "1 + 1 = %d" 2 #=> "1 + 1 = 2"
printf "Print a float: %f" 2 #=> "Print a float: 2.000000"
```

### 文件读取

```sh
cat file.txt | while read line; do
    echo $line
done
```

### 随机抽样


shell 中随机抽取数据，有多种方法

#### bash

bash 随机数

```sh
random=${RANDOM} # 25256
```


#### sort

「sort」命令的「-R」选项。

```sh
sort -R filename | head -n 100
```

例如，以下命令会随机抽取文件「data.txt」中的一行：


#### shuf

shuf 类似sort的命令行实用程序，包含在Coreutils中

Mac 需要单独安装

```sh
brew install coreutils
```

shuf 命令

```sh
shuf -n 100 data.txt
shuf -e line1 line2 line3 line4 line5 # 指定输入集合（字符串）
shuf -e 1 2 3 4 5 # 指定输入集合 1~5
shuf -n 3 -e 1 2 3 4 5 # 从指定集合中抽取3个
shuf -i 1-10 # 指定范围: 1~10
```

#### awk

或用「awk」命令，例如：

```sh
awk 'BEGIN{srand()} {if(rand()<0.01) print $0}' data.txt
awk 'BEGIN{srand()} {print rand()"\t"$0}' filename | sort -nk 1 | head -n100 | awk -F '\t' '{print $2}' # 假如输出的内容只有一列
```

这两个命令都可以随机地从文件中抽取一行数据。


```sh
#!/bin/bash

IN_FILE=$1
LINE_NUM=$2
awk -vN=${LINE_NUM} -vC="`wc -l ${IN_FILE}`" 'BEGIN{srand();while(n<N){i=int(rand()*C+1);if(!(i in a)){a[i]++;n++}}}NR in a' ${IN_FILE}
```

抽样

```sh
sh my_shuf.sh datas.txt 100 | awk '{print $1}' > random_data_100
```



### 三剑客

grep 、sed、awk被称为linux中的"三剑客"。
- grep 更适合单纯的查找或匹配文本
- sed 更适合编辑匹配到的文本
- awk 更适合格式化文本，对文本进行较复杂格式处理

## 编码转换

- 【2021-6-4】linux下转换文件编码格式，命令：

```shell
# 从gbk转utf8
iconv -f gbk -t utf8 pattern_0603.txt -o pattern.txt
# 上面命令失败的用下面
iconv -f gbk -t utf8 pattern_0603.txt > pattern.txt
```

## grep

文件内容查找

```sh
if grep -q 'foo' ~/.bash_history; then
    echo "您过去似乎输入过“foo”"
fi
# 文件内容查找: 目录wqw里查找包含yes的文件
grep yes /wqw

# 从文件内容查找与正则表达式匹配的行：
grep –e “^yes” myfile
# 查找时不区分大小写：
grep –i “yes” myfile
# 查找匹配的行数：
grep -c “yes” myfile
# 从文件内容查找不匹配指定字符串的行：
grep –v “yes” myfile
# 从根目录开始查找所有扩展名为.log的文本文件，并找出包含”ERROR”的行
find / -type f -name “*.log” | xargs grep “ERROR”
# 从当前目录开始查找所有扩展名为.in的文本文件，并找出包含”thermcontact”的行
find . -name “*.in” | xargs grep “thermcontact”
```

## awk

- awk是逐行处理的，逐行处理的意思就是说，当awk处理一个文本时，会一行一行进行处理，处理完当前行，再处理下一行，awk默认以"换行符"为标记，识别每一行，也就是说，awk跟我们人类一样，每次遇到"回车换行"，就认为是当前行的结束，新的一行的开始，awk会按照用户指定的分割符去分割当前行，如果没有指定分割符，默认使用空格作为分隔符。

### awk内建变量

变量
- $0 当前记录（这个变量中存放着整个行的内容）
- $1~$n 当前记录的第n个字段，字段间由FS分隔
- FS 输入字段分隔符 默认是空格或Tab
- NF 当前记录中的字段个数，就是有多少列，如果加上$符号，即$NF，表示一行的最后一个字段
- NR 已经读出的记录数，就是行号，从1开始，如果有多个文件话，这个值也是不断累加中。
- FNR 当前记录数，与NR不同的是，这个值会是各个文件自己的行号
- RS 输入的记录分隔符， 默认为换行符
- OFS 输出字段分隔符， 默认也是空格
- ORS 输出的记录分隔符，默认为换行符
- FILENAME 当前输入文件的名字
- ARGC 命令行参数个数
- ARGV 命令行参数排列
- ENVIRON 支持队列中系统环境变量的使用
- BEGIN{这里面放的是执行前的语句}
- END{这里面放的是处理完所有的行后要执行的语句}
- {这里面放的是处理每一行时要执行的语句}

![](https://community.linuxmint.com/img/screenshots/original-awk.png)

### 常用命令

```shell
awk '{print $1, $3}' netstat.txt
awk '{printf "%-8s %-8s %-18s %-22s %-15s\n",$1,$3,$4,$5,$6}' netstat.txt
awk '$3 == 0 && $6 == "LAST_ACK"' netstat.txt
awk '$3 > 0 && NR != 1 {print $3}' netstat.txt
awk 'BEGIN{FS=":"} {print $1,$3,$6}' semi_colon_FS #awk -F: '{print $1,$3,$6}' semi_colon_FS
awk '/WAIT/' netstat.txt
awk 'NR != 1 {print > $6}' netstat.txt
awk 'NR!=1{a[$6]++;} END {for (i in a) print i ", " a[i];}' netstat.txt
cat shuf.txt | awk 'BEGIN{srand()} {print rand() "\t" $0}' | sort -n | cut -f2- #shuffle一个文件
awk 'BEGIN{FS="  "}{if ($1 == "payment") {print;}}' /data/log/maui.data.log #抽出所有第一个字段是payment的行
awk 'BEGIN{FS="  "}$1 == "payment"' /data/log/maui.data.log #或者ACTION部分不要用花括号圈引，则自动打印符合条件的相应行
awk '$2 == "beat"{print $3}' /data/log/budweiser.data.log | sort | uniq -c #取出第二列等于beat的行的第3列，然后统计出现的数量
awk '$2 == "beat"{print $3}' logfile | sort | uniq -c
awk '{ print length, $0 }' file | sort -nrk1 -s | cut -d" " -f2- #根据文件的每行长度进行排序
```


### 字符串切割

```shell
test="cluster	8	平使用面积|你有啥用|使用多少？|使用年限|使用率|使用率多少|套内使用面积|车位使用权多久"
echo $test | awk '{split($3,a,"|");for(i in a) print $2"\t"a[i]}' > out.txt
# split用法，将真个字符串按照:切割，结果存入数组a中
echo "12:34:56" | awk '{split($0,a,":" ); print a[1]}'     # 输出 12

echo "123" | awk '{print length}' # 字符串长度
awk -F ',' '{print substr($3,6)}'  # 表示是从第3个字段里的第6个字符开始，一直到设定的分隔符","结束.
substr($3,10,8)  # 表示是从第3个字段里的第10个字符开始，截取8个字符结束.
substr($3,6)     # 表示是从第3个字段里的第6个字符开始，一直到结尾
awk '$0 ~ /abc/ {gsub("a\d+c", "def", $0); print $1, $3}' abc.txt # 字符串替换，正则模式
```

### 正则表达式

【2023-1-10】awk的正则表达式，是属于：`扩展的正则表达式`（Extended Regular Expression 又叫 Extended RegEx 简称 EREs），[详见](https://www.cnblogs.com/chengmo/archive/2010/10/11/1847772.html)

awk 常见调用正则表达式方法：
- ① 直接过滤：使用
- ② if条件判断
- ③ 正则函数

```sh
# ① 
awk '/REG/{action}'
# /REG/为正则表达式，可以将$0中，满足条件记录 送入到：action进行处理.
# ② 
# awk正则运算语句(~,~!等同!~)
awk 'BEGIN{info="this is a test";if( info ~ /test/){print "ok"}}'
# ok

#1：仿豆瓣电影微信小程序 
# https://github.com/zce/weapp-demo
#
#2：微信小程序移动端商城 
# https://github.com/liuxuanqiang/wechat-weapp-mall

# 两行合并，剔除空格
cat m.txt | awk '{if($1~/^[1-9]+/){gsub("\s+","",$1);printf "["$1"]"}else{gsub("\s+","",$1);if($1)printf "("$1")\n"}}'
```

③ awk内置使用正则表达式函数
- gsub( Ere, Repl, [ In ] ) 原地替换
- sub( Ere, Repl, [ In ] )
- match( String, Ere )
- split( String, A, [ Ere] )

```sh
# 将tab替换为 |
cat a.txt | awk -F'\t' '{gsub("\t"," | ",$0);print "|"$0"|"}'
```

详细函数使用，可以参照：[linux awk 内置函数详细介绍（实例）](http://www.cnblogs.com/chengmo/archive/2010/10/08/1845913.html)


### 多路输出

- 代码：
```shell
【2019-06-04】awk多路输出： 
head data_ivr_20190401_20190430.txt | awk -F'\t' '{if($2~/01:/){print $0>>"tmp_a.txt"}else{print $0>>"tmp_b.txt"}}'
head data_ivr_20190401_20190430.txt | awk -F'\t' 'BEGIN{a="tmp_a.txt";b="tmp_b.txt";system(">"a";>"b);}{if($2~/01:/){print $0>>a}else{print $0>>b}}'
# 文件分流示例
train_file='a.txt'
test_file='b.txt'
[ -e $train_file ] && > $train_file;
[ -e $test_file ] && > $test_file;
less error.txt | awk -v a=$train_file -v b=$test_file 'BEGIN {srand();OFS="\t";N=20} {r=int(rand()*N); if(r%N==1)print $0>>a; else{print $0>>b}}'
less error.txt | awk 'BEGIN {srand();OFS="\t"} {print $0,rand()*1000}' |sort -k2nr -k5n|awk 'BEGIN {OFS="\t"} {print}'
```

### 输出特殊字符

【2022-12-21】输出单引号、双引号

测试数据：

```sh
1.1 微客主页-个人主页
1.2 微客主页-热门资讯
1.3 微客主页-热门房源
1.4 微客主页-热门楼盘
1.6 获客宝主页-我的微店-个人主页
1.7 获客宝主页-我的微店-单个二手房
1.8 获客宝主页-我的微店-单个新房
2.1 二手房-详情页
2.2 二手房-列表页
2.3 二手房-详情页cpt
3.1 新房-楼盘详情页
3.2 新房-户型详情页
3.3 新房-项目资料详情页
3.4 新房-列表页
3.5 新房-详情页cpt
4.1 获客宝主页-资讯详情页(gid)
4.2 获客宝主页-获客资讯模块(gid)
4.3 获客宝主页-今日必推模块(gid)
4.4 获客宝主页-资讯详情页(h5)
4.5 获客宝主页-获客资讯模块(h5)
4.6 获客宝主页-今日必推模块(h5)
5.1 霸屏海报-海报
6.1 租赁-详情页
6.2 租赁-列表页
7.1 拉新工具-h5拉新链接
7.2 拉新工具-拉新海报
8.1 首页-好房分享-单个二手房
8.2 首页-好房分享-单个新房
8.3 首页-获客资讯(gid)
8.4 首页-获客资讯(h5)
9.9 幸福楼市
10.1 RGC经纪人
```

awk 命令
- 双引号：只需使用 \ 即可
- 单引号：需要额外用单引号围起来，再加转义符

```sh
# 双引号：
awk '{print "\""}'    # 放大：awk '{print "  \"  "}'
# 使用“”双引号把一个双引号括起来，然后用转义字符\对双引号进行转义，输出双引号。
# 单引号：
awk '{print "'\''"}'  # 放大: awk '{print  "  '  \  '  '   " }'
# 使用一个双引号“”，然后在双引号里面加入两个单引号‘’，接着在两个单引号里面加入一个转义的单引号\'，输出单引号。

cat share.txt | awk '{print "when substr(source_from,1,3)='\''" $1 "'\'' then '\''" $2"'\''"}'
# when substr(source_from,1,3)='1.1' then '微客主页-个人主页'
# when substr(source_from,1,3)='1.2' then '微客主页-热门资讯'
# when substr(source_from,1,3)='1.3' then '微客主页-热门房源'
# when substr(source_from,1,3)='1.4' then '微客主页-热门楼盘'
```


## sed

- sed是一款优秀的文本处理程序，但是其不同版本在用法和参数上存在着较大差异，建议大家在使用时一定要查询相关文档，以免出错。

```shell
# 删除只有空白字符行
sed -i -e '/^\s\+$/d' file #GNU

sed '1!G;h;$!d' pets.txt #反转一个文件的行
sed 'N; s/\n  /, /' pets.txt #将两行合并，并用逗号分开
sed -e 's/'$(echo -e "\x15")'//g' file # sed用于去除ascii不可打印的控制字符

# 常规的替换功能
sed "s/my/Hao Chen's/" pets.txt
sed "3s/my/your/" pets.txt
sed "3,6s/my/your/" pets.txt #只替换第3到第6行的文本

sed -n '/cat/,/fish/p' pets.txt # 只打印匹配cat和fish之前的行，-n表示不输出那些未匹配的行

sed -e 3,6{ -e /This/d -e } pets.txt
sed '3,6{/This/d;}' pets.txt #BSD sed, must add semi-colon

sed '3,6 {/This/{/fish/d;};}' pets.txt
sed '1,${/This/d;s/^ *//g;}' pets.txt
sed -E '/dog/{N;N;N;s/(^|\n)/&# /g;}' pets.txt #BSD sed
sed '/dog/,+3s/^/# /g' pets.txt #GNU sed
sed = pets.txt | sed 'N;s/\n/'$'\t''/' > line_num_pets.txt
sed = my.txt | sed 'N; s/^/    /; s/\(.\{5,\}\)\n/\1 /' #对文件中的所有行编号（行号在左，文字左端对齐）。
#sed = my.txt | sed -E 'N; s/(.*)\n/    \1 /' #貌似，我也可以这么写
sed '/'"$name"'/,/};/d' back_slash.txt
#实际应用，用来做代码重构时：(err) -> next err  =>   next
find . -name '*.coffee' | xargs sed -i '' -E '/\(err\) ->/{N;s/\(err\) ->\n +next err/next/g;}'
#在多行的时候，[[:space:]]才会匹配换行符\n，只有单行的时候，字符串尾部的换行符已经被sed截掉，所以匹配不到

#使用GNU sed去掉首行的BOM
find . -name '*.srt' -exec gsed -i -e '1s/^\xEF\xBB\xBF//' {} \;

gsed '1~2G' -i *.txt #奇数行后加空行
gsed -i -e '$a\' file #如果文件末尾没有换行符，则自动添加，解决"No newline at end of file"的问题，OSX sed中：sed -i '' -e '$a\'

# 在第1行插入内容
sed "1i\\"$'\n'"my monkey's name is wukong"$'\n' my.txt
# 在最后一行追加内容
sed "$ a \\"$'\n'"my monkey's name is wukong"$'\n' my.txt
# 在匹配行之前插入内容
sed "/fish/i\\"$'\n'"my monkey's name is wukong"$'\n' my.txt
# 在指定行修改为特定内容
sed "2c \\"$'\n'"my monkey's name is wukong"$'\n' my.txt

# 匹配行后追加内容
gsed -i '/matchpattern/a content' tmp.txt
# 如果content是以空白字符开头，比如tab或者空格，则用一个反斜线标记出来
gsed -i '/matchpattern/a \ content' tmp.txt
# 命令行中输入tab键：先按ctrl+v，然后再按tab
gsed -i '/matchpattern/a \	content' tmp.txt
# 匹配行后追加多行内容，可以把需要追加的内容写到一个文件中，然后使用r命令
gsed -i '/abcd/r otherfile.txt' tmp.txt

# 删除匹配行之前的内容，也就是保留匹配行之后的所有内容
sed -i '/^package /,$!d' *.go
# 显示一定范围内的行
sed -n '190,200p' tmp.txt
```


【2024-4-10】生成连续数字、字符串

```sh
# -f 或 --format=FORMAT：使用printf风格的浮点格式（使用%g或者%f占位，可指定宽度），可自定义格式输出序列。例如：
seq -f "ID-%05g" 3
# ID-00001
# ID-00002
# ID-00003

# -s 或 --separator=STRING：使用STRING分隔数字（默认值：\n）。例如：~$ 
seq -s , 3
# 1,2,3

# -w 或 --equal-width：使用前导零填充以均衡宽度。例如：~$ 
seq -w 8 10
# 08
# 09
# 10
```

## grep

- 待补充

## shell案例


### 自定义通用函数

common.sh包含的函数：
- 打日志
- 发邮件
- 发短信
- 多功能等待

```shell
#!/bin/bash
# -*- coding: utf-8 -*-
 
#===============================================================================
#            File:  common.sh
#           Usage:  sh common.sh
#     Description:  定义了常用函数
#    LastModified:  6/12/2012 16:28 PM CST
#         Created:  1/4/2012 11:06 AM CST
# 
#          AUTHOR:  wangqiwen(wangqiwen@*.com)
#         COMPANY:  baidu Inc
#         VERSION:  1.0
#            NOTE:  
#           input:  
#          output:  
#===============================================================================
 
ulimit -c unlimited
#init_log <log_file>
init_log()#清空log文件打一条日志
{
    >$LogFile # conf/var.sh中定义
    log "====================================="
    log "LogFile=$LogFile"
    log "\t\tshort-cut-pretreat"
    local day=`date "+%Y-%m-%d %H:%M:%S"`
    log "\t\t$day"
    log "====================================="
    declare -i log_count=0 # 整型局部变量
}
 
log()
{
    let log_count++
    echo -e "\n--------------------------[$log_count]th log--------------------------------\n"
    echo -e `date "+%Y-%m-%d %H:%M:%S"`"\t$@"
}
 
#read_mail <mail.conf> 结果在mail_receivers变量中
read_alarm_mail(){
    declare -i flag=0 # 整型局部变量
 
    if [ -f "$1" ];then
        cut -d "#" -f 1 "$1" |grep -v "^$" >tmp.$$
        while read line; do
            if [ $flag -eq 0 ];then
                mail_receivers=$line # 整型全局变量
                flag=1
            else
                mail_receivers="$mail_receivers,$line"
            fi
        done < tmp.$$
        rm -f tmp.$$
    else
        #设定一个默认值
        mail_receivers="-"
    fi
    echo "报警邮件接收人:$mail_receivers"
}
 
#向指定的邮件发送邮件告警
#$1:    告警主题
#$2:    需要被告警的详细内容
send_alarm_mail( )
{
        if [ $# -ne 2 ]; then
                return -1
        fi
    #获取收件人列表
        echo "$2" | mail -s "$1" "$mail_receivers"
        if [ $? -ne 0 ]; then
                log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] 发送到 $mail_receivers 的邮件($1)失败!"
        else
                log "[`date "+%Y-%m-%d %H:%M:%S"`] [NOTE] 成功将邮件($1---$2) 发送至 $mail_receivers !"
        fi
        return 0
}
#对所有手机报警
#$1:    报警内容
send_list_msgs( )
{ # 传入两个参数: $1 --> 报警短信内容  $n (n>=2) --> 报警接收人的手机号
        if [ $# -lt 2 ]; then
        echo "短信报警函数send_list_msgs参数不够!"
                return -1
        fi
    local i="-"
    local phone_number="-"
    for((i=2;i<=$#;i++))
    do
        eval "phone_number=\${$i}"
        # 向$phone_number发送报警信息$1
        gsmsend -s $GSMSERVER1:$GSMPORT1 -s $GSMSERVER2:$GSMPORT2 *$GSMPIORITY*"$phone_number@$1"
        if [ $? -ne 0 ];then
            log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] 报警短信发送失败 !"
        else
            log "[`date "+%Y-%m-%d %H:%M:%S"`] [NOTE] 报警信息 ($1) 成功发送到 $phone_number !"
        fi 
    done
}
#------------------------------------------------------
# 2012-2-25 PM 22:33   wangqiwen@*.com
# input: 每次等5min
# type=1 检测多个目录，各目录tag文件命名规则一致，且都在上一级目录
#(1) wait_hadoop_file   hadoop  time  1 tag_file   hadoop_dir1   hadoop_dir2   hadoop_dir3  
# 公用tag文件名（非绝对路径，tag文件默认在目录的上一层）
# 示例：wait_hadoop_file $hadoop 10   1  done        /a/b/c        /a/m/c       /a/m/d
# 或：  wait_hadoop_file $hadoop 10   1  finish.txt  /a/b/c        /a/m/c       /a/m/d
#   目录/a/b/c,/a/m/c,/a/m/d
#   若tag文件分别为:/a/b/c.done和/a/m/c.done和/a/m/d.done，那么，tag_file="done"
#   否则，所有目录的tag文件名相同，tag_file可自定义为某文件名
#
# type=2 检测多个目录，各目录的tag文件路径无规则，需直接指定其完整路径
#(2) wait_hadoop_file hadoop    time   2  hadoop_dir1 tag_file1  hadoop_dir2 tag_file2  # 私用tag文件名，绝对路径
# 示例：wait_hadoop_file $hadoop 10   2  /a/b/c      /a/b/c.done /a/m/c     /a/m/c.txt   /a/m/d     /a/m_d.txt 
# 目录与tag文件要依次成对出现
#
# type=3 检测多个集群文件（非目录），无须tag文件
#(3) wait_hadoop_file    hadoop    time   3 hadoop_file1    hadoop_file2   hadoop_file3   # 判断多个hadoop文件的存在性
# 示例：wait_hadoop_file $hadoop    10    3     /a/b/file1.txt  /a/b/file2.txt  /a/m/file3.log 
#
# output: 通过变量FILE_READY记录，返回状态值0~3 
#   0 : 检查完毕，或成功删除临时目录
#   1 : 参数输入有误：个数、奇偶性不对。type=2时要保证tag文件与目录依次成对出现
#   2 : 超时，停止检查
#   3 : _temporary目录删除失败,但不影响hadoop任务，属于成功状态
#   成功状态值: 0 和 3
#------------------------------------------------------
#shopt -s -o nounset  # 变量声明才能使用
wait_hadoop_file(){
    local FILE_READY=1 # 检查结果
    local ARG_NUM=$# # 参数个数
    [ $ARG_NUM -lt 4 ] && {  echo -e "input error ! $ARG_NUM < 4 , please check !\t参数有误，小于4个，请确认！";return $FILE_READY;} 
    local HADOOP=$1 # Hadoop集群客户端地址
    local HADOOP_CHECK_PATH="/" # 待检查的集群目录或文件
    local HADOOP_TEMP_PATH="/" # _temporary目录
    local HADOOP_CHECK_TAG="/"  # 待检查的tag文件
    local HADOOP_WATI_TIME=$2 # 最长等待时间（单位：分钟）
    local CURRENT_ERRORTIME=1 # 等待时间
    local CURRENT_PATH=1  # 当前遍历目录数
    local PATH_INDEX=0  # 当前检测目录所在的参数位置
    local TAG_INDEX=0  # 当前检测tag文件所在的参数位置
    local TAG_NAME="/"
    local DIR_NUM=0  # 待检测目录数
    local TYPE=$3  # type
    # 根据类型分别处理
    # type=1,2时，输入参数至少5个；type=3时，输入参数至少4个
    case $TYPE in
    1) 
        [ $ARG_NUM -eq 4 ] && {  echo -e "input error ! $ARG_NUM < 5 , please check !\t参数有误，小于5个，请确认！";return $FILE_READY;}
        DIR_NUM=$(($ARG_NUM-4));;  # 待检测的目录数
    2)
        [ $ARG_NUM -eq 4 ] && {  echo -e "input error ! $ARG_NUM < 5 , please check !\t参数有误，小于5个，请确认！";return $FILE_READY;}
        [ $((($ARG_NUM-3)%2)) -ne 0 ] && { FILE_READY=1; echo -e "Input error ! Dirs miss to match tags in pairs ...";return $FILE_READY;} # 目录和tag文件不成对，退出case
        DIR_NUM=$((($ARG_NUM-3)/2));;  # 待检测的目录数
    3)  
        DIR_NUM=$(($ARG_NUM-3));; # 待检测文件数
    *)
        echo "Input error ! Type value $TYPE illegal... type参数值错误，1-3，非$TYPE"
        return $FILE_READY;;
    esac
 
    while [ $CURRENT_PATH -le $DIR_NUM ]
    do
        # path/tag参数位置获取
        if [ $TYPE -eq 1 ];then
            PATH_INDEX=$((4+$CURRENT_PATH))
            TAG_INDEX=4
            eval "HADOOP_CHECK_PATH=\${$PATH_INDEX}"  # 待检查的集群目录
            eval "TAG_NAME=\${$TAG_INDEX}"
            if [ "$TAG_NAME" == "done" ];then #tag文件在上一级目录
                HADOOP_CHECK_TAG="${HADOOP_CHECK_PATH%/*}/${HADOOP_CHECK_PATH##*/}.$TAG_NAME" # tag文件名为：上一级目录名字.done
            else
                HADOOP_CHECK_TAG="${HADOOP_CHECK_PATH%/*}/$TAG_NAME" # 上一级目录自定义tag文件名
            fi
        elif [ $TYPE -eq 2 ];then
            PATH_INDEX=$((4+2*($CURRENT_PATH-1))) 
            TAG_INDEX=$(($PATH_INDEX+1))
            eval "HADOOP_CHECK_PATH=\${$PATH_INDEX}"  # 待检查的集群目录
            eval "HADOOP_CHECK_TAG=\${$TAG_INDEX}" # tag文件的绝对路径
        else
            PATH_INDEX=$((3+$CURRENT_PATH))
            eval "HADOOP_CHECK_PATH=\${$PATH_INDEX}"  # 待检查的集群文件
        fi
        while [ $CURRENT_ERRORTIME -le $HADOOP_WATI_TIME ]
        do
            $HADOOP fs -test -e $HADOOP_CHECK_PATH  # 检测path目录是否存在
            if [ $? -eq 0 ];then # 目录存在
                break
            else  # 目录不存在，等待生成
                CURRENT_ERRORTIME=$(($CURRENT_ERRORTIME+1))
                date "+%Y-%m-%d %H:%M:%S"
                sleep 5m
            fi
        done
        [ $CURRENT_ERRORTIME -gt $HADOOP_WATI_TIME ] && { FILE_READY=2; echo -e "Time out when checking dirs[$HADOOP_CHECK_PATH] ...\t等待超时，目录未检查完毕！" ;break;}
        if [ $TYPE -eq  3 ];then
            CURRENT_PATH=$(($CURRENT_PATH+1)) # 检查下一个目录
        else
            HADOOP_TEMP_PATH="${HADOOP_CHECK_PATH}/_temporary" # 临时目录
            # 检测tag文件，并删除临时目录
            while [ $CURRENT_ERRORTIME -le $HADOOP_WATI_TIME ]
            do
                $HADOOP fs -test -e $HADOOP_CHECK_TAG # 检测tag文件是否存在
                if [ $? -eq 0 ];then  # tag文件存在  [2012-12-4]停止临时文件删除
                    #$HADOOP fs -test -e $HADOOP_TEMP_PATH  # 检查临时目录是否存在
                    #if [ $? -eq 0 ];then  # 临时目录存在
                    #   $HADOOP fs -rmr $HADOOP_TEMP_PATH  # 删除临时目录
                    #   [ $? -ne 0 ] && { FILE_READY=3; echo -e "Failed to delete temp dir[$HADOOP_TEMP_PATH]...\t临时目录删除失败";} #break 2; } # 删除失败，退出2重循环 [2012-2-23]不退出，继续检查
                    #fi
                    CURRENT_PATH=$(($CURRENT_PATH+1)) # 检查下一个目录
                    break
                else  # tag文件不存在，错误次数自增，循环等待
                    CURRENT_ERRORTIME=$(($CURRENT_ERRORTIME+1))
                    date "+%Y-%m-%d %H:%M:%S"
                    sleep 5m
                fi
            done
        fi
    done
    [ $CURRENT_PATH -gt $DIR_NUM ] && { [ $FILE_READY -ne 3 ] && FILE_READY=0;  echo "All dirs ready ! 目录检查完毕！";} # 所有目录都准备好,新增成功状态3,[2012-2-23]
    return $FILE_READY
}
```

### 循环任务

从某个日期开始，往前递推N天，并启动任务

```shell
[ $# -ge 1 ] && date=$1 || date=`date -d "1 days ago" +%Y%m%d`
readonly rp_hadoop="/home/work/bin/hadoop-client-rp-product/hadoop/bin/hadoop"
i=1;n=3
while [ $i -le $n ]
do
    d=`date -d "${i} days ago $date" +%Y%m%d`
    echo "[`date "+%Y-%m-%d %H:%M:%S"`] 第 $i 天 ($d)"
    sh start.sh $d
    [ $? -ne 0 ] && { echo "[`date "+%Y-%m-%d %H:%M:%S"`] 第 $i 天 ($d) oneday-pretreat 执行失败...";exit -1; } || { echo "[`date "+%Y-%m-%d %H:%M:%S"`] 第 $i 天( $d ) oneday-pretreat 执行成功...";  }
    cd ../../short-cut-pretreat-v2/navigation
    sh start.sh $d
    [ $? -ne 0 ] && { echo "[`date "+%Y-%m-%d %H:%M:%S"`] 第 $i 天 ($d) short-cut-pretreat 执行失败...";exit -1; } || { echo "[`date "+%Y-%m-%d %H:%M:%S"`] 第 $i 天( $d ) short-cut-pretreat 执行成功..."; ((i++)); }
    cd -
done
```

### shell调度MapReduce任务

单次案例：

```shell
#!/bin/bash
# -*- coding: utf-8 -*-
 
#===============================================================================
#            File:  start_hadoop.sh [session]
#           Usage:  
#     Description:  pc端session日志的hadoop启动脚本 
#    LastModified:  2013-3-28 12:51 PM 
#         Created:  27/12/2012 11:17 AM CST
#          AUTHOR:  wangqiwen(wangqiwen@*.com)
#         COMPANY:  baidu Inc
#         VERSION:  1.0
#            NOTE:  
#           input:  
#          output:  
#===============================================================================
#:<<note
# online 
set -x
if [ $# -ne 9 ]; then
    echo "[$0] [ERROR] [`date "+%Y-%m-%d %H:%M:%S"`] [session] input error ! \$#=$# not 9"
    exit -1
fi
hadoop=$1;input=${2//;/ -input };output=$3
jobname=$4;main_dir=$5;date=$6;task_prefix=$7
map_con_num=$8;reduce_num=$9
#note

:<<note
# test
date="20130314"
jobname="session"
hadoop="/home/work/hadoop-rp-rd-nj/hadoop/bin/hadoop"
#input="/log/22307/nj_rpoffline_session_ting/$date/0000/szwg-ston-hdfs.dmop/0000"
input="/log/22307/nj_rpoffline_session_ting/$date/0000/szwg-ston-hdfs.dmop/0000/part-00000"
# baike http://cq01-test-nlp2.cq01.baidu.com:8130/table/view?table_id=347
output="/user/rp-rd/wqw/test/sm/$jobname/$date/0000"
map_con_num=200
reduce_num=200
main_dir="/home/work/wqw/sm-navi-data-cookie/new/bin"
note

echo "=========================$jobname start ============================="
done_file="${output%/*}/${output##*/}.done"
${hadoop} fs -test -e ${output} && ${hadoop} fs -rmr ${output}
${hadoop} fs -test -e ${done_file} && ${hadoop} fs -rm ${done_file}
echo "-------输出目录,标记文件清理完毕---------------------"
echo "[$0] [NOTE] [`date "+%Y-%m-%d %H:%M:%S"`] [$jobname] start to commit hadoop job"
${hadoop} streaming \
        -jobconf mapred.job.name="${task_prefix}" \
        -jobconf mapred.job.priority=HIGH \
        -jobconf mapred.task.timeout=600000 \
        -jobconf mapred.map.tasks=$map_con_num \
        -jobconf mapred.reduce.tasks=$reduce_num \
        -jobconf stream.memory.limit=1000 \
        -jobconf stream.num.map.output.key.fields=2 \
        -jobconf num.key.fields.for.partition=1 \
        -cacheArchive /user/rp-product/dcache/thirdparty/python2.7.tar.gz#py27 \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
        -jobconf mapred.job.map.capacity=$map_con_num -jobconf mapred.job.reduce.capacity=$reduce_num \
        -jobconf mapred.map.max.attempts=10 -jobconf mapred.reduce.max.attempts=10 \
        -file $main_dir/hadoop_jobs/session/*.py \
        -file $main_dir/tools/hadoop_tool/py27.sh \
        -file $main_dir/tools/url_normalize/m \
        -cmdenv date_of_data=$date \
        -output ${output} \
        -input ${input} \
        -mapper "sh py27.sh mapper.py" \
        -reducer "./m"
 
if [ $? -ne 0 ]; then
    echo "[$0] [Error] [`date "+%Y-%m-%d %H:%M:%S"`] [$jobname] job failed !"
    exit -1
fi
#${hadoop} fs -touchz ${done_file}
 
echo "[$0] [NOTE] [`date "+%Y-%m-%d %H:%M:%S"`] [$jobname] hadoop job finished"
echo "=========================$jobname end ============================="
exit 0
```

多任务调度

```shell
#!/bin/bash
# -*- coding: utf-8 -*-
#
#===============================================================================
#            File:  start.sh [oneday-pretreat]
#           Usage:  
#                运行指定日期：    sh start.sh  20120104
#        正常运行(昨天):   sh start.sh
#        查看运行日志：    tail -f ../log/20120104/run_log_20120103.txt
#     Description: oneday-pretreat总控脚本
#    LastModified:  12/13/2012 15:29 AM CST
#         Created:  1/4/2012 11:16 AM CST
# 
#          AUTHOR:  wangqiwen(wangqiwen@*.com)
#         COMPANY:  baidu Inc
#         VERSION:  1.0
#            NOTE: 
#       input:  mergeOneDay和dump
#      output:  作为short-cut-pretreat的输入
#===============================================================================
 
#搭建执行环境
source ./build.sh
#读入路径、时间配置
if [ $# -eq 1 ];then
    date_check=`echo "$1" | sed -n '/^[0-9]\{8\}$/p'`
    if [ -z $date_check ];then
        # 如果字符串为空,表明输入参数不当
        echo "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] date of start.sh input error ... 启动脚本的日期参数错误!"
        exit -1
    else
        source $ConfDir/vars.sh $1
    fi
else
    source $ConfDir/vars.sh
fi
 
#####################for mini#############################
export HADOOP_HOME=${rp_hadoop%/*/*}
export JAVA_HOME=${HADOOP_HOME%/*}/java6
# build.sh中读入BinDir
source $BinDir/oneday_onlyUrl_mini/mini/output/jjpack2text/conf/dlb_env.sh
export PATH=$PATH:$HADOOP_HOME/bin
##########################################################
 
#是否开启调试模式
if [ $debug_on -eq 1 ];then
        set -x
else
    set +x
fi
 
#导入公共函数
source ./common.sh #增加./,防止与环境变量重名
#日志初始化
init_log  #common.sh中定义
 
#重定向标准输入和输出到指定文件
exec 3<>$LogFile  #LogFile在conf/var.sh中定义
exec 1>&3 2>&1
 
log "$alarm_module_info" #模块信息
log "[`date "+%Y-%m-%d %H:%M:%S"`] [NOTE] load conf file 加载配置文件..."
#读入邮件配置
read_alarm_mail $ConfDir/mail.conf # read_alarm_mail源于common.sh
#读入短信配置
source $ConfDir/msg_conf.sh
#=========================hadoop任务函数封装===================
check_jobs_input()
{  # 参数: job type name warning msg_receiver 外部依赖才有短信报警
    [ $# -lt 5 ] && { echo "check_jobs_input input ($@) error ! ($#>= 5)";exit -1; }
    local my_job=$1
    local job_name="${my_job}-$date"
    local my_type=$2
    local hadoop_file="-"
    case $my_type in
    1)  # 内部依赖,超时仅发送邮件
        eval "hadoop_file=\$${my_job}_input_tag_in";;
    2)  # 外部依赖,超时发报警短信\短信，另外增加预警
        eval "hadoop_file=\$${my_job}_input_tag_out";;
    *)
        echo "check_jobs_input input error ! type=[1,2]"
        exit -1;;
    esac
    eval "local wait_time=\$${my_job}_wait_time" # 2012-5-22
    local name=$3
    local warning=$4  # 是否需要预警
    local msg_receiver=$5
    for((i=6;i<=$#;i++))
    do
        eval "msg_receiver=\"\$msg_receiver \${$i}\""
    done
    # 外部依赖，先等待，超时发出预警，继续等待最后时间
    if [ $warning -ne 0 ];then
        # 数据生成较晚，提醒相关人员关注
        eval "local wait_time_notice=\$${my_job}_wait_time_notice"
        # 验证${my_job}中是否定义提醒时间
        [ -e $wait_time_notice ] && { log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] $job_name ---[check_jobs_input] 未定义的变量: ${my_job}_wait_time_notice ";exit -1; }    
        wait_hadoop_file $rp_hadoop $wait_time_notice 3 $hadoop_file # 等待文件ready  2012-5-22
        return_value=$?
        if [ $return_value -ne 0 ];then
            rest_time=$(echo $wait_time_notice | awk '{print $0/12.0}')
            log "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] [返回值: $return_value] $job_name 上游数据 ($date,$name) 还没生成,存在风险...再等待 $rest_time 小时..... "
            [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [WARNING] $job_name 预警时间已到,请及时推进" "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] [返回值:$return_value] $job_name 预警时间已到,上游数据 ($date,$name) 还未生成,存在风险,再等待 $rest_time 小时...请 [$alarm_module_RP_rd] 及时跟进, $alarm_module_info" # 邮件报警
            [  $alarm_msg_off -eq 0 -a $my_type -eq 2 ] && send_list_msgs  "[oneday-pretreat] [WARNING] [返回值]:$return_value] $job_name 预警时间已到,上游数据 ($date,$name) 还未生成,存在风险,再等待 $rest_time 小时,请 [$alarm_module_RP_rd] 及时跟进." $msg_receiver 
        else
            return 0  # 预警时间内，数据ready，函数退出
        fi
        # 最晚抢救时间已到，当天挖掘无法更新，进入自动补数据阶段
        eval "local wait_time_warning=\$${my_job}_wait_time_warning"
        # 验证${my_job}中是否定义预警时间
        [ -e $wait_time_warning ] && { log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] $job_name --- [check_jobs_input] 未定义的变量: ${my_job}_wait_time_warning ";exit -1; } 
        wait_hadoop_file $rp_hadoop $wait_time_warning 3 $hadoop_file # 等待文件ready  2012-5-22
        return_value=$?
        if [ $return_value -ne 0 ];then
            rest_time=$(echo $wait_time_warning | awk '{print $0/12.0}')
            log "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] [返回值: $return_value ] $job_name 接口数据最晚等待时间已到! 上游数据 ($date,$name) 还没生成,当天挖掘赶不上,自动进入补数据阶段...再等待 $rest_time 小时...请及时处理."
            [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [WARNING] $job_name 预警时间已到,请及时推进..." "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] [返回值:$return_value] $job_name 接口数据最晚等待时间已到 !上游数据 ($date,$name) 还未生成,当天挖掘赶不上,自动进入补数据阶段,再等待 $rest_time 小时...请 [$alalarm_module_RP_rd] 及时跟进,$alarm_module_info" # 邮件报警
            [  $alarm_msg_off -eq 0 -a $my_type -eq 2 ] && send_list_msgs  "[oneday-pretreat] [WARNING] [返回值 $return_value ] $job_name 接口数据最晚等待时间已到 !,上游数据 ($date,$name) 还未生成,当天挖掘赶不上,自动进入补数据阶段,再等待 $rest_time 小时,请[ $alarm_module_RP_rd ]及时跟进." $msg_receiver
        else
            return 0   # 补数据成功，程序返回  
        fi
    fi
    # 补数据超时失败,程序退出
    wait_hadoop_file $rp_hadoop $wait_time 3 $hadoop_file # 等待文件ready  2012-5-22
    return_value=$?
    if [ $return_value -ne 0 ];then
        log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] [返回值: $return_value] $job_name 等待超时 ! 上游数据 ($date,$name) 未按时生成..."  # 打运行日志
        [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [ERROR] $job_name 等待超时!" " [`date "+%Y-%m-%d %H:%M:%S"`][ERROR][返回值: $return_value] $job_name 失败! 上游数据 ($date,$name) 未按时生成..请联系 [$alarm_module_RP_rd] 处理,$alarm_module_info" # 邮件报警
        [  $alarm_msg_off -eq 0 -a $my_type -eq 2 ] && send_list_msgs  "[oneday-pretreat] [ERROR] [返回值: $return_value] $job_name 等待超时!上游数据 ($date,$name) 未按时生成...请 [$alarm_module_RP_rd] 处理,$alarm_module_info" $msg_receiver # 短信报警 
        exit -1 # 超时等待，退出
    fi
}
 
hadoop_dir_search()
{   # 参数: job_name type  name 
    # 仅用于接口数据的自动查找,替换
    [ $# -lt 3 ] && echo "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] hadoop_dir_search input error ! ($# >= 3)"
    local job_name=$1
    local my_type=$2 # 区分正常产出数据(type=1)和转储日志(type非1)
    local name=$3
    local tmp_date='-'
    local tmp_path='-'
    local tmp_tag='-'
    eval "local days=\$${name}_findDays"
    eval "wait_hadoop_file \$rp_hadoop \$${name}_wait_time 3 \$${name}_tag"
    return_value=$?
    if [ $return_value -ne 0 ];then
        log "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] [$job_name] 当天目录 ${name}_dir/$date/0000.done 不存在,请核实 !"
        [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [WARNING] 上游数据 $name($date) 不存在!" "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] 上游数据 $name($date) 不存在...请联系 [$alarm_module_RP_rd] 追查原因,$alarm_module_info"
        # 当天数据超时未生成,common_query 需要自动搜索最近的数据
        for((i=1;i<=$days;i++))
        do
            tmp_date=`date -d "-$i day $date" +%Y%m%d` # 获取前i天日期
            if [ $my_type -eq 1 ];then
                eval "tmp_path=\"\${${name}_dir%/*/*}/$tmp_date/0000\"" # 拼接临时目录----正常产出数据
                eval "tmp_tag=\"\${${name}_dir%/*/*}/$tmp_date/0000.done\"" # 拼接临时目录----正常产出数据
            else
                eval "tmp_path=\"\${${name}_dir%/*/*/*}/$tmp_date/0000/0000\"" # 拼接临时目录----转储日志
                eval "tmp_tag=\"\${${name}_dir%/*/*/*}/$tmp_date/0000/@manifest\"" # 拼接临时目录----转储日志
            fi
            $rp_hadoop fs -test -e $tmp_tag  # 检查默认的目录标记文件 [20130218]
            if [ $? -eq 0 ];then
                eval "${name}_dir=\"$tmp_path\""  # 更改原目录值
                eval "${name}_tag=\"$tmp_tag\""   # 更改原标记文件
                break
            else
                log "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] [$job_name] $tmp_tag 不存在,请核实 !"
                [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [WARNING] 上游数据 $name($tmp_date) 不存在!" "[`date "+%Y-%m-%d %H:%M:%S"`] [WARNING] 上游数据 $name($d) 不存在...请联系 [$alarm_module_RP_rd] 追查原因,$alarm_module_info"
            fi
        done
        [ $i -ge $days ] && exit -1
    fi
}
start_hadoop_jobs()
{  # 参数: jobname arg1 arg2 ...  不包括基本参数
    [ $# -lt 1 ] && echo "start_hadoop_jobs input error ! ($# >= 1)"
    local myjob=$1
    local myjob_name="${1}-$date"
    local args=""
    if [ $# -ge 2 ];then
        # 获取额外参数
        for((i=2;i<=$#;i++))
        do
            eval "args=\"$args \${$i}\""
        done
    fi
    #启动任务
    eval "cd \$${myjob}_local_dir"
    eval "\$shellBin start_hadoop.sh \$rp_hadoop \$${myjob}_input \$${myjob}_output \$myjob_name \$${myjob}_map_con_num \$${myjob}_reduce_num \$args"
    return_value=$?
    if [ $return_value -eq 0 ];then
        log "[`date "+%Y-%m-%d %H:%M:%S"`] [NOTE] [返回值: $return_value] $myjob_name finished ! $myjob_name 执行成功..."
        eval output=\$${myjob}_output
        ${rp_hadoop} cr -register ${output} -cronID $cronID # zk注册数据状态
        if [ $? -ne 0 ];then
            log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] $myjob_name zk状态注册失败.."
            [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [ERROR] $myjob_name zk状态注册失败.."  " [`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] $myjob_name zk状态注册失败...请联系 $alarm_module_stra_rd 处理,谢谢! $alarm_module_info"
        fi
    else
        log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] [返回值: $return_value] $myjob_name failed ! $myjob_name 执行失败..."
        [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [ERROR] $myjob_name Failed !"  " [`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] $myjob_name failed when running ! $myjob_name 执行过程中失败...请联系 $alarm_module_stra_rd 处理,谢谢! $alarm_module_info"
        exit -1
    fi
    cd -
}
 
#=======================启动子任务==============================
 
#---------------oneday_onlyUrl----------------------
#  作用: 抽取URL,去重,方便下一步的网页库查询           |
#  输入: mergeOneDay和database_dump                    |
#  输出: oneday_onlyUrl                                       |
#-------------------------------------------------------
jobname1="oneday_onlyUrl"
oneday_onlyUrl()
{
    # 等待接口数据
    check_jobs_input $jobname1 2  "mergeOneDay&database_dump" 1 $MOBILE_LIST_ALL # 外部依赖,需要预警
    #从集群上下载记录mergeOneDay信息的xml文件
    local_xml_mergeOneDay_file="${DataDir}/${mergeOneDay_tag##*/}" #提取文件名
    [ -e $local_xml_mergeOneDay_file ] && rm $local_xml_mergeOneDay_file # 删除已有文件
    sleep 5 # 等待5S，防止原xml文件不完整
    $rp_hadoop fs -copyToLocal $mergeOneDay_tag $DataDir #复制xml文件到本地
    cd $CheckDir # 2012-12-11
    $pythonBin mergeOneDay_check.py $local_xml_mergeOneDay_file #检验mergeOneDay数据源是否满足要求
    cd - # 2012-12-11
    return_value=$?
    if [ $return_value -ne 0 ];then
        log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] [返回值:$return_value] $jobname1 失败!上游数据 mergeOneDay-$date 缺失过多,不满足要求..."
        [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [ERROR] [返回值:$return_value] $jobname1 失败!" " [`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] $jobname1 失败!上游数据 mergeOneDay-$date 数据源缺失过多,不满足要求...请联系 [$alarm_module_RP_rd] 追查原因,$alarm_module_info"
        [  $alarm_msg_off -eq 0 ] && send_list_msgs  "[oneday-pretreat] [ERROR] [返回值:$return_value] $jobname1 失败!上游数据 mergeOneDay-$date 数据源缺失过多,不满足要求...请 [$alarm_module_RP_rd] 追查原因,谢谢! $alarm_module_info" $MOBILE_LIST_ALL
        exit -1
    fi
    $rp_hadoop fs -touchz $mergeOneDay_ok # 数据验证通过，创建标记文件，通知下游模块启动 
    start_hadoop_jobs "oneday_onlyUrl"
}
if [ $oneday_onlyUrl_pass -eq 0 ];then
    oneday_onlyUrl
    $rp_hadoop fs -touchz $mergeOneDay_ok # 数据验证通过，创建标记文件，通知下游模块启动 
    ${rp_hadoop} cr -register $mergeOneDay_ok -cronID $cronID # 注册数据状态
    if [ $? -ne 0 ];then
        log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] mergeOneDay_ok zk状态注册失败.."
        [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [ERROR] mergeOneDay_ok zk状态注册失败.."  " [`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] mergeOneDay_ok zk状态注册失败...请联系 $alarm_module_stra_rd 处理,谢谢! $alarm_module_info"
        fi
fi
 
#-----------oneday_onlyUrl_mini-------------------------
#  作用: mini网页库查询                                |
#  输入: oneday_onlyUrl                                |
#  输出: oneday_onlyUrl_mini                           |
#-------------------------------------------------------
jobname2="oneday_onlyUrl_mini"
oneday_onlyUrl_mini()
{
     
    check_jobs_input $jobname2 1  "oneday_onlyUrl" 0 $MOBILE_LIST_ALL # 内部依赖
    cd $oneday_onlyUrl_mini_local_dir/mini/output
    # ----------通过vars.sh中的路径配置,python程序解析修改test.xml
    less $ConfDir/oneday_onlyUrl_mini_conf.xml | awk -v input=$oneday_onlyUrl_mini_hdfs_input -v output=$oneday_onlyUrl_mini_hdfs_output -v bin_path="$oneday_onlyUrl_mini_bin_path" '{
        if($0~/<hdfs_input>.*<\/hdfs_input>/)
            print "\t\t<hdfs_input>"input"</hdfs_input>"
        else if($0~/<hdfs_output>.*<\/hdfs_output>/)
            print "\t\t<hdfs_output>"output"</hdfs_output>"
        else if($0~/<bin_path>.*<\/bin_path>/)
            print "\t\t<bin_path>"bin_path"</bin_path>"
        else
            print $0
    }' > test.xml 
    echo "=======================mini网页库========================="
    $pythonBin Xml2stream.py test.xml  # 启动网页库查询,后台操作
    ${rp_hadoop} fs -test -e "${oneday_onlyUrl_mini_output}/part-00999" # part-00999存在才证明mini查询成功
    if [ $? -eq 0 ];then
        # 任务执行完毕后，创建便于检测的tag文件
        $rp_hadoop fs -touchz "${oneday_onlyUrl_mini_output%/*}/${oneday_onlyUrl_mini_output##*/}.done"
        ${rp_hadoop} cr -register ${oneday_onlyUrl_mini_output} -cronID $cronID # 注册数据状态
        if [ $? -ne 0 ];then
            log "[`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] oneday_onlyUrl_mini zk状态注册失败.."
            [  $alarm_mail_off -eq 0 ] && send_alarm_mail "[oneday-pretreat] [ERROR] oneday_onlyUrl_mini zk状态注册失败.."  " [`date "+%Y-%m-%d %H:%M:%S"`] [ERROR] oneday_onlyUrl_mini zk状态注册失败...请联系 $alarm_module_stra_rd 处理,谢谢! $alarm_module_info"
        fi
    fi
    # 删除多余的临时目录
    echo "----清除临时文件 $oneday_onlyUrl_mini_hdfs_tmp ------"
    #exec 1>/dev/null 2>&1 # 将以下删除信息扔到位桶里
    for dir in $oneday_onlyUrl_mini_hdfs_tmp
    do
 
        echo "删除临时目录:${oneday_onlyUrl_mini_output%/*}/$dir"
        $rp_hadoop fs -rmr "${oneday_onlyUrl_mini_output%/*}/$dir" &>/dev/null
    done
    #exec 1>&3 2>&1  # 恢复重定向到日志文件
    echo "========================结束============================"
    cd -
    log "[`date "+%Y-%m-%d %H:%M:%S"`] [NOTE] $jobname2 百灵库查询完毕..."
}
 
if [ $oneday_onlyUrl_mini_pass -eq 0 ];then
    oneday_onlyUrl_mini 
fi
#------------oneday_baiduid---------------------------------
#  作用:                                               |
#  输入: mergeOneDay和baiduid                          |
#  输出: oneday_baiduid                                |
#-------------------------------------------------------
jobname3="oneday_baiduid"
#-----------后台等待baiduid---------------------
oneday_baiduid(){
    check_jobs_input $jobname3 2  "mergeOneDay" 0 $MOBILE_LIST_ALL # 外部依赖
    start_hadoop_jobs $jobname3 $oneday_baiduid_max_freq $oneday_baiduid_min_time 
}
 
if [ $oneday_baiduid_pass -eq 0 ];then
    oneday_baiduid &  # 后台运行
fi
 
#------------oneday_onlyUrl_mini_plus------------------
#  作用: 网页库查询结果上附加unifyUrl和commonQuery     |
#  输入: oneday_onlyUrl_mini,urlunify,commonQuery      |
#  输出: oneday_onlyUrl_mini_plus                      |
#-------------------------------------------------------
jobname4="oneday_onlyUrl_mini_plus"
oneday_onlyUrl_mini_plus(){
    hadoop_dir_search $jobname4 1 "common_query" # 检查并查找可替代的commonQuery数据  统计产出(2013-5-15)
    hadoop_dir_search $jobname4 1 "oneday_onlyUrl_mini" # 检查并查找可替代的mini数据  原始日志
    #check_jobs_input $jobname4 1  "oneday_onlyUrl_mini" 0 $MOBILE_LIST_STRA  # 内部
    oneday_onlyUrl_mini_plus_input="$urlunify_dir $common_query_dir $oneday_onlyUrl_mini_dir"
    start_hadoop_jobs $jobname4 $oneday_onlyUrl_mini_plus_input_str1 $oneday_onlyUrl_mini_plus_input_str2 $oneday_onlyUrl_mini_plus_input_str3
    reset_common_query # 恢复common_query原始值
}
if [ $oneday_onlyUrl_mini_plus_pass -eq 0 ];then
    oneday_onlyUrl_mini_plus
fi
 
 
#------------oneday_baiduid_plus----------------------------
#  作用: oneday_baiduid附加URL信息                         |
#  输入: oneday_baiduid和oneday_onlyUrl_mini               |
#  输出: oneday_baiduid_plus                               |
#-------------------------------------------------------
jobname5="oneday_baiduid_plus"
oneday_baiduid_plus()
{
    check_jobs_input $jobname5 1  "oneday_baiduid|oneday_onlyUrl_mini_plus" 0 $MOBILE_LIST_STRA # 内部依赖
    start_hadoop_jobs $jobname5 $oneday_baiduid_plus_input_str1 $oneday_baiduid_plus_input_str2
}
 
if [ $oneday_baiduid_plus_pass -eq 0 ];then
    oneday_baiduid_plus
fi
 
#------------oneday_uid_plus----------------------------
#  作用: baiduid映射成uid                              |
#  输入: baiduid-uid-mapping和oneday_baiduid_plus      |
#  输出: oneday_uid_plus                           |
#-------------------------------------------------------
jobname6="oneday_uid_plus"
#-----------后台等待baiduid-uid-mapping-------------------
oneday_uid_plus(){
    hadoop_dir_search $jobname6 1 "baiduid_uid_mapping" # 检查并查找可替代的baiduid-uid数据---程序产出
    check_jobs_input $jobname6 1  "oneday_baiduid_plus" 0 $MOBILE_LIST_STRA # 内部依赖
    oneday_uid_plus_input="${baiduid_uid_mapping_dir} ${oneday_baiduid_plus_output}"
    start_hadoop_jobs $jobname6  $oneday_uid_plus_input_str1 $oneday_uid_plus_input_str2 
    reset_baiduid_uid_mapping # 恢复baiduid_uid_mapping原始值
}
 
if [ $oneday_uid_plus_pass -eq 0 ];then
    oneday_uid_plus  & # 后台运行
fi
 
#------------oneday_activeBaiduid_plus------------------
#  作用: baiduid映射成uid                              |
#  输入: activeBaiduid和oneday_baiduid_plus           |
#  输出: oneday_activeBaiduid_plus                     |
#-------------------------------------------------------
jobname7="oneday_activeBaiduid_plus"
#-----------后台等待 activeBaiduid-------------------
oneday_activeBaiduid_plus(){
    hadoop_dir_search $jobname7 1 "activeBaiduid" # 检查并查找可替代的baiduid-uid数据---程序产出
    check_jobs_input $jobname7 1  "oneday_baiduid_plus" 0 $MOBILE_LIST_STRA # 内部依赖
    oneday_activeBaiduid_plus_input="${activeBaiduid_dir} ${oneday_baiduid_plus_output}"
    start_hadoop_jobs $jobname7  $oneday_activeBaiduid_plus_input_str1 $oneday_activeBaiduid_plus_input_str2 
    reset_activeBaiduid # 恢复activeBaiduid原始值
}
 
if [ $oneday_activeBaiduid_plus_pass -eq 0 ];then
    oneday_activeBaiduid_plus
fi
 
#------------oneday_dump_urlUnify----------------------
#  作用: 用网页库查询结果归一化全库数据database_dump   |
#  输入: databse_dump和oneday_onlyUrl_mini             |
#  输出: oneday_dump_urlUnify                          |
#-------------------------------------------------------
jobname8="oneday_dump_urlUnify"
oneday_dump_urlUnify(){ # 后台运行
    check_jobs_input $jobname8 2  "database_dump" 0 $MOBILE_LIST_ALL # 外部依赖
    check_jobs_input $jobname8 1  "oneday_onlyUrl_mini_plus" 0 $MOBILE_LIST_STRA # 内部依赖
    start_hadoop_jobs $jobname8 $oneday_dump_urlUnify_input_str1 $oneday_dump_urlUnify_input_str2
}
 
if [ $oneday_dump_urlUnify_pass -eq 0 ];then
    oneday_dump_urlUnify  &
fi
 
#------------------end-----------------------
log "[`date "+%Y-%m-%d %H:%M:%S"`] [NOTE] oneday-pretreat success ! oneday-pretreat 模块执行完毕！"
 
#关闭重定向
exec 3<&-
```


## 批主机管理

pdsh、pssh 是之前运维管理人员的利器。

这俩工具已退出历史舞台，现在发光发热的已是 Ansible、Salt。
- 【2024-4-19】[参考](https://blog.opskumu.com/pdsh-pssh.html)

### pssh

pssh 是一个 python 编写可以在多台服务器上执行命令的工具，同时支持拷贝文件，是同类工具中很出色的，类似 pdsh 。为方便操作，使用前请在各个服务器上配置好密钥认证访问。
- 项目地址: [parallel-ssh](https://code.google.com/p/parallel-ssh)
- [总结](https://blog.opskumu.com/pdsh-pssh.html)

附加工具
- pscp 传输文件到多个 hosts，类似 scp
  - `pscp -h hosts.txt -l irb2 foo.txt /home/irb2/foo.txt`
- pslurp 从多台远程机器拷贝文件到本地
- pnuke 并行在远程主机杀进程
  - `pnuke -h hosts.txt -l irb2 java`
- prsync 使用rsync协议从本地计算机同步到远程主机
  - `prsync -r -h hosts.txt -l irb2 foo /home/irb2/foo`

### pdsh

pdsh (Parallel Distributed Shell) 可并行执行对目标主机的操作，对于批量执行命令和分发任务有很大的帮助，在使用前需要配置 ssh 无密码登录

pdsh 全称 parallel distributed shell
- 与pssh类似，pdsh可并行执行对远程目标主机的操作，在有批量执行命令或分发任务的运维需求时，使用这个命令可达到事半功倍的效果。
- 同时，pdsh还支持**交互模式**，当要执行的命令不确定时，可直接进入pdsh命令行，非常方便。

pdsh应用场景
- 基本上与pssh相同，都用于大批量服务器的配置、部署、文件复制等运维操作。
- 使用pdsh时，仍需要配置本地主机和远程主机间的单向ssh信任。
- 另外，pdsh还附带了pdcp命令，此命令可以将本地文件批量复制到远程的多台主机上，这在大规模的文件分发环境下是非常有用的。

pdsh可以通过多种方式在远程主机上运行命令
- 默认是rsh方式
- 另外也支持ssh、mrsh、qsh、mqsh、krb4、xcpu等多种rcmd模块，这个可以在运行命令时通过参数指定。


```sh
pdsh -h
Usage: pdsh [-options] command ...
-S                return largest of remote command return values
-h                output usage menu and quit                获取帮助
-V                output version information and quit       查看版本
-q                list the option settings and quit         列出 `pdsh` 执行的一些信息
-b                disable ^C status feature (batch mode)
-d                enable extra debug information from ^C status
-l user           execute remote commands as user           指定远程使用的用户
-t seconds        set connect timeout (default is 10 sec)   指定超时时间
-u seconds        set command timeout (no default)          类似 `-t`
-f n              use fanout of n nodes                     设置同时连接的目标主机的个数
-w host,host,...  set target node list on command line      指定主机，host 可以是主机名也可以是 ip
-x host,host,...  set node exclusion list on command line   排除某些或者某个主机
-R name           set rcmd module to name                   指定 rcmd 的模块名，默认使用 ssh
-N                disable hostname: labels on output lines  输出不显示主机名或者 ip
-L                list info on all loaded modules and exit  列出 `pdsh` 加载的模块信息
-a                target all nodes                          指定所有的节点
-g groupname      target hosts in dsh group "groupname"     指定 `dsh` 组名，编译安裝需要添加 `-g` 支持选项 `--with-dshgroups`
-X groupname      exclude hosts in dsh group "groupname"    排除组，一般和 `-a` 连用
available rcmd modules: exec,xcpu,ssh (default: ssh)        可用的执行命令模块，默认为 ssh
```

示例

```sh
# 单个主机测试
pdsh -w 192.168.0.231 -l root uptime
# 192.168.0.231:  16:16:11 up 32 days, 22:14, ? users,  load average: 0.10, 0.14, 0.16
# 多个主机测试
pdsh -w 192.168.0.[231-233] -l root uptime
# 192.168.0.233:  16:17:05 up 32 days, 22:17, ? users,  load average: 0.13, 0.12, 0.10
# 192.168.0.232:  16:17:05 up 32 days, 22:17, ? users,  load average: 0.45, 0.34, 0.27
# 192.168.0.231:  16:17:06 up 32 days, 22:15, ? users,  load average: 0.09, 0.13, 0.15
# 逗号分隔主机
pdsh -w 192.168.0.231,192.168.0.234 -l root uptime
# 192.168.0.234:  16:19:44 up 32 days, 22:19, ? users,  load average: 0.17, 0.21, 0.20
# 192.168.0.231:  16:19:44 up 32 days, 22:17, ? users,  load average: 0.29, 0.18, 0.16
#  -x 排除某个主机
pdsh -w 192.168.0.[231-233] -x 192.168.0.232 -l root uptime
# 192.168.0.233:  16:18:24 up 32 days, 22:19, ? users,  load average: 0.11, 0.12, 0.09
# 192.168.0.231:  16:18:25 up 32 days, 22:16, ? users,  load average: 0.11, 0.13, 0.15
```

【2024-4-20】pdsh 安装
- sudo apt-get install pdsh -- [错误](https://askubuntu.com/questions/590662/configure-error-invalid-variable-name-prefix-while-runing-configure)
- 源码安装
- [google code](https://code.google.com/archive/p/pdsh/downloads)


```sh
sudo apt-get install pdsh
# 错误
pdsh -v
# pdsh@mlxlabqcvytu4a66056efe-20240328132206-317dg9-nqi3xt-worker: module path "/usr/lib/x86_64-linux-gnu/pdsh" insecure.
# pdsh@mlxlabqcvytu4a66056efe-20240328132206-317dg9-nqi3xt-worker: "/": Owner not root, current uid, or pdsh executable owner
# pdsh@mlxlabqcvytu4a66056efe-20240328132206-317dg9-nqi3xt-worker: Couldn't load any pdsh modules

# 源码编译安装
wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pdsh/pdsh-2.29.tar.bz2
./configure --with-ssh --enable-static-modules --prefix=/home/wqw/bin && make && make install
# 问题: error: invalid variable name: –-prefix
# 解决: 复制过来的 -- 格式有问题, 重新输入
# 编译完后,生成 bin文件夹 /home/wqw/bin/pdsh/bin
# 修改配置 vim ~/.bashrc
export PATH=$PATH:/home/wqw/pdsh/bin

source ~/.bashrc

pdsh-2.29 (+static-modules)
# rcmd modules: ssh,rsh,exec (default: rsh)
# misc modules: (none)
```


# 本文编辑器

- [主流文本编辑器学习曲线](https://coolshell.cn/articles/3125.html)
- 几个经典的文本编辑器的学习曲线，不排除其中有调侃和幽默的味道

## 终端

- 【2022-4-8】[运维神器！一个可以通过Web访问Linux终端的工具](https://www.toutiao.com/article/7083860657581670951)——rtty
  - rtty由客户端和服务端组成。客户端采用纯C实现，服务端采用GO语言实现，前端界面采用vue实现。使用rtty可以在任何地方通过Web访问您的设备的终端，通过设备ID来区分您的不同的设备。rtty非常适合远程维护Linux设备。
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/ac2f8ae6dc5946f1b8ec4881d058a351?from=pc)
  - ![](https://p26.toutiaoimg.com/origin/tos-cn-i-qvj2lq49k0/ca37b04be909420cab976e1f998c0623?from=pc)
- 【2021-5-15】Next Terminal 是一款开源的远程登录工具，需要自己部署，可以在任何一个浏览器远程访问Windows/Linux/macOS系统，方便快捷。Next Terminal 基于 Apache Guacamole 开发，使用到了guacd 服务。在线[DEMO](https://next-terminal.typesafe.cn/)，即开即用,（用户名/密码 test/test），打开后就能看到后台了
- 具体功能如下：
  - 授权凭证管理（密码、密钥）
  - 资产管理（支持RDP、SSH、VNC、TELNET 协议）
  - 指令管理（预设命令行）
  - 批量执行命令
  - 在线会话管理（监控、强制断开）
  - 离线会话管理（查看录屏）
  - 双因素认证
  - 多用户登录
  - 资产授权
  - 用户分组
  - ![](https://img3.appinn.net/images/202101/vnc.jpg)
  - [Next Terminal – 用浏览器访问远程桌面，支持 RDP、SSH、VNC 和 Telnet](https://www.appinn.com/next-terminal/)
- 【2021-5-10】[terminus](https://eugeny.github.io/terminus/)，[下载地址](https://github.com/Eugeny/terminus/releases/tag/v1.0.138)
![](https://gitee.com/mirrors/terminus/raw/master/docs/readme.png)

- 【2020-9-1】[tmux](https://www.ruanyifeng.com/blog/2019/10/tmux.html)
- Tmux 就是会话与窗口的"解绑"工具，将它们彻底分离。
  - （1）它允许在单个窗口中，同时访问多个会话。这对于同时运行多个命令行程序很有用。
  - （2） 它可以让新窗口"接入"已经存在的会话。
  - （3）它允许每个会话有多个连接窗口，因此可以多人实时共享会话。
  - （4）它还支持窗口任意的垂直和水平拆分。

【2020-9-2】[Linux：在终端中查看图片和电影](https://blog.csdn.net/weixin_34072159/article/details/92473531)
- 安装工具(cacaview)：yum install caca-utils -y
- 查看图片：cacaview test.jpg
- 按d改变图片配色
- ![](https://static.xjh.me/wp-content/uploads/2017/11/www.xjh.me-2017-11-04_17-18-14_961742-2.png)


## Vim技能

### vim介绍

vim编辑器好处
- 不使用鼠标，完全用键盘操作。
- 系统资源占用小，打开大文件毫无压力。
- 键盘命令变成肌肉记忆以后，操作速度极快。
- 服务器默认都安装 Vi 或 Vim

- vi / vim是Linux上最常用的文本编辑器而且功能非常强大。只有命令，没有菜单，下图表示vi命令的各种模式的切换图。
  - ![](https://p3-tt.byteimg.com/origin/pgc-image/89e2d5d5a06e40d498f169c6bfde54fb?from=pc)
- 【2019-07-18】编辑器学习曲线:
  - ![](https://github.com/wqw547243068/wangqiwen/blob/master/other/figure/mmexport1563449034348.jpg?raw=true)
- [如何使用VIM搭建IDE？](http://harttle.com/2015/11/04/vim-ide.html),[vim键盘图大全](http://www.cnblogs.com/yu-lang/p/5413279.html),[所见即所得，像IDE一样使用vim](https://github.com/yangyangwithgnu/use_vim_as_ide)，![VIM键盘图](http://harttle.com/assets/img/blog/vim-key.png)
- ![vim命令图解](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1513414506184&di=5592bf051e8a3b337830632ac037b1c0&imgtype=jpg&src=http%3A%2F%2Fimg4.imgtn.bdimg.com%2Fit%2Fu%3D3339508074%2C1265491893%26fm%3D214%26gp%3D0.jpg)
- [台湾人总结的vim命令图解（pdf打印版）](http://img.my.csdn.net/uploads/201211/24/1353759337_6781.png)
- 【2017-12-14】[awk思维导图](http://s1.51cto.com/wyfs02/M01/7D/18/wKiom1bf0R6wMA_sABZGEQxE4yg982.png)，[sed思维导图](http://scc.qibebt.cas.cn/docs/linux/script/sed%CB%BC%CE%AC%B5%BC%CD%BC.jpg),[更多linux工具总结](http://scc.qibebt.cas.cn/docs/doc-main.php?dir=linux)
- pacvim，[vim学习游戏](https://linux.cn/article-9738-1.html)
  - 命令：git clone https://github.com/jmoon018/PacVim.git
  - ![](https://img.linux.net.cn/data/attachment/album/201806/12/104234m10a8uuhxh08kxx5.png)

### vim主题

- 【2021-1-12】vim配色，[大全](http://vimcolors.com/)
- 设置类似sublime的主题包：[vim-monokai](https://github.com/sickill/vim-monokai)
   - ![](https://camo.githubusercontent.com/b7d019bb849ebced5559fbde94e152f72b86855e07ab302c7ee27890f503674c/68747470733a2f2f692e696d6775722e636f6d2f4e5058324d584d2e706e67)


```shell
# 下载sublime主题
git clone https://github.com/sickill/vim-monokai.git
# 创建主题目录
mkdir -p ~/.vim/colors
# 复制主题
cp vim-monokai/colors/monokai.vim ~/.vim/colors
# 设置vim主题, ~/.vimrc
syntax enable
colorscheme monokai
```

【2022-11-9】monokai主题
- 去github上下载 [monokai.vim](https://github.com/sickill/vim-monokai/blob/6fb52e32863646e38cdebce57ae0d1688f334a79/colors/monokai.vim)文件
- 放到指定目录: ~/.vim/colors 中
- 开启主题

```shell
# 下载主题, 进入github中monokai.vim文件页面，点raw按钮
wget https://raw.githubusercontent.com/sickill/vim-monokai/6fb52e32863646e38cdebce57ae0d1688f334a79/colors/monokai.vim
mkdir -p ~/.vim/colors
mv monokai.vim ~/.vim/colors
# 编辑 vimrc 文件
syntax enable
colorscheme monokai
```

### vim 配置

Vim 的配置不太容易，它有自己的语法，许多命令

Vim 的全局配置一般在`/etc/vim/vimrc`或者`/etc/vimrc`，对所有用户生效。用户个人的配置在`~/.vimrc`。
- 如果只对**单次**编辑启用某个配置项，可以在命令模式下，先输入一个冒号，再输入配置。
- 如果是批量设置设置，详见：阮一峰的[Vim配置入门](https://www.ruanyifeng.com/blog/2018/09/vimrc.html)

精简

```python
set showmode " 在底部显示，当前处于命令模式还是插入模式
set number " 显示行号
syntax on " 打开语法高亮。自动识别代码，使用多种颜色显示
set cursorline " 光标所在的当前行高亮
set autoindent " 按下回车键后，下一行的缩进会自动跟上一行的缩进保持一致。
set tabstop=4 " 按下 Tab 键时，Vim 显示的空格数
set encoding=utf-8 " 编码，可以解决vim下的中文乱码问题
" colorscheme monokai " 配色
```

完整介绍

```python
" ========== 一次性 =========
" 打开
set number
" 关闭
set nonumber
" 查询某个配置项是打开还是关闭
:set number?
" 帮助
:help number

" ========== 永久 ===========
" ===== 外观 ======
set number " 显示行号
set nonumber " 关闭显示行号
set relativenumber " 显示光标所在的当前行的行号，其他行都为相对于该行的相对行号。

syntax on " 打开语法高亮。自动识别代码，使用多种颜色显示
syntax enable " 开启代码语法高亮
colorscheme monokai " 配色

set cursorline " 光标所在的当前行高亮

set textwidth=80 " 设置行宽，即一行显示多少个字符。
set wrap " 自动折行，即太长的行分成几行显示。
set nowrap " 关闭自动折行
set linebreak " 只有遇到指定的符号（比如空格、连词号和其他标点符号），才发生折行。也就是说，不会在单词内部折行。
set wrapmargin=2 " 指定折行处与编辑窗口的右边缘之间空出的字符数。
set scrolloff=5 " 垂直滚动时，光标距离顶部/底部的位置（单位：行）
set sidescrolloff=15 " 水平滚动时，光标距离行首或行尾的位置（单位：字符）。该配置在不折行时比较有用

set laststatus=2 " 是否显示状态栏。0 表示不显示，1 表示只在多窗口时显示，2 表示显示。
set  ruler " 在状态栏显示光标的当前位置（位于哪一行哪一列）

" ===== 缩进 ======
set autoindent " 按下回车键后，下一行的缩进会自动跟上一行的缩进保持一致。
set smartindent
set tabstop=4 " 按下 Tab 键时，Vim 显示的空格数
set shiftwidth=4 " 在文本上按下>>（增加一级缩进）、<<（取消一级缩进）或者==（取消全部缩进）时，每一级的字符数
set expandtab " 由于 Tab 键在不同的编辑器缩进不一致，该设置自动将 Tab 转为空格。
set softtabstop=2 " Tab 转为多少个空格。
" ===== 基本配置 ======
set showmode " 在底部显示，当前处于命令模式还是插入模式
set showcmd  " 命令模式下，在底部显示，当前键入的指令。比如，键入的指令是2y3d，那么底部就会显示2y3，当键入d的时候，操作完成，显示消失。
set mouse=a " 支持使用鼠标
set encoding=utf-8 " 编码，可以解决vim下的中文乱码问题
set fileencoding=utf-8 " 文件
set fileencodings=ucs-bom,utf-8,chinese,cp936
set guifont=Consolas:h15
language messages zh_CN.utf-8
" set lines=45 columns=100 # 这行不能加，否则按O进入编辑状态时，视觉错位

set foldmethod=manual

set nocompatible " 不与 Vi 兼容（采用 Vim 自己的操作命令）
set nobackup
filetype indent on " 开启文件类型检查，并且载入与该类型对应的缩进规则

" ===== 编辑 ======
set spell spelllang=en_us " 打开英语单词的拼写检查
set nobackup " 不创建备份文件。默认情况下，文件保存时，会额外创建一个备份文件，它的文件名是在原文件名的末尾，再添加一个波浪号（〜）。
set noswapfile " 不创建交换文件。交换文件主要用于系统崩溃时恢复文件，文件名的开头是.、结尾是.swp
set undofile " 保留撤销历史。Vim 会在编辑时保存操作历史，用来供用户撤消更改。默认情况下，操作记录只在本次编辑时有效，一旦编辑结束、文件关闭，操作历史就消失了。打开这个设置，可以在文件关闭后，操作记录保留在一个文件里面，继续存在。这意味着，重新打开一个文件，可以撤销上一次编辑时的操作。撤消文件是跟原文件保存在一起的隐藏文件，文件名以.un~开头
set backupdir=~/.vim/.backup//  
set directory=~/.vim/.swp//
set undodir=~/.vim/.undo// 
" 设置备份文件、交换文件、操作历史文件的保存位置。
" 结尾的//表示生成的文件名带有绝对路径，路径中用%替换目录分隔符，这样可以防止文件重名
set autochdir " 自动切换工作目录。这主要用在一个 Vim 会话之中打开多个文件的情况，默认的工作目录是打开的第一个文件的目录。该配置可以将工作目录自动切换到，正在编辑的文件的目录
set noerrorbells " 出错时，不要发出响声
set visualbell " 出错时，发出视觉提示，通常是屏幕闪烁
set history=1000 " Vim 需要记住多少次历史操作
set autoread " 打开文件监视。如果在编辑过程中文件发生外部改变（比如被别的编辑器编辑了），就会发出提示
set listchars=tab:»■,trail:■
set list " 如果行尾有多余的空格（包括 Tab 键），该配置将让这些空格显示成可见的小方块
set wildmenu
set wildmode=longest:list,full
" 命令模式下，底部操作指令按下 Tab 键自动补全。第一次按下 Tab，会显示所有匹配的操作指令的清单；第二次按下 Tab，会依次选择各个指令。

" ===== 搜索/查找 ======
set showmatch " 光标遇到圆括号、方括号、大括号时，自动高亮对应的另一个圆括号、方括号和大括号
set hlsearch " 搜索时，高亮显示匹配结果
set incsearch " 输入搜索模式时，每输入一个字符，就自动跳到第一个匹配的结果。
set ignorecase " 搜索时忽略大小写
set smartcase " 如果同时打开了ignorecase，那么对于只有一个大写字母的搜索词，将大小写敏感；其他情况都是大小写不敏感。比如，搜索Test时，将不匹配test；搜索test时，将匹配Test
```

缩进统一：tab -> 4个空格，只需在代码文件中加一行

```python
# */* vim: set expandtab ts=4 sw=4 sts=4 tw=400: */
```

### vim技巧

|命令|说明|备注|
|---|---|---|
|:s/searchStr/replaceStr/g	|替换当前行中的所有 searchStr 到 replaceStr||
|:s/searchStr/replaceStr/	|替换当前行中的第一个 searchStr 到 replaceStr||
|:%s/searchStr/replaceStr/	|替换每一行中的第一个 searchStr 到 replaceStr||
|:%s/searchStr/replaceStr/g	|替换每一行中的每一个 searchStr 到 replaceStr||
|h、j、k、l	|左下上右||
|i	|插入||
|A	|从末尾开始编辑||
|w / e|	下一个单词开头 / 结尾||
|b	|上一个单词||
|u	|撤消操作||
|x	|删除当前字符||
|H M L	|屏幕的上 / 中 / 下||

#### vim 疑难杂症

积累常见问题解决方法
1. vim粘贴多行文本时，编辑器自动换行，格式乱
  - 解决：粘贴前，使用命令：set paste即可, 如果想恢复自动换行，set nopaste
1. 【2022-11-16】web shell下打开vim，编辑后，无法退出
  - 原因：`esc` 退出这个是无法屏蔽的，chrome 等浏览器把 esc 作为逃逸键，没有信号可以拦截
  - 解法：vim 可以考虑使用 `ctrl`+`c` 代替 `esc`; 
    - ① Ctrl+C，vim就从编辑模式进入命令模式；Control + C 可以将代替 Esc 将 Vim 从 insert 模式切换到 normal 模式
    - ② 按大写的ZZ，退出
    - 参考：[ESC退出全屏模式和vi编辑模式的ESC键冲突](https://github.com/jumpserver/jumpserver/issues/4091)


# 项目

## python健康打卡

- 【2020-7-9】[python实现网页自动健康打卡以及腾讯文档打卡](https://blog.csdn.net/rglkt/article/details/105351363)



