# 关于Python
Python是一门编程语言，用于编写应用程序以帮助完成日常工作与特定需求

Python的功能非常强大，最主要是简单易理解
Python具有良好的生态环境，即可以在Python社区或者其他有关编程的社区里找到几乎一切关于Python的问题的解决方案，如果没有找到，也会有广泛的coder愿意提供帮助

## 特点
作为一门主流的编程语言，Python的主要特点有：
- 解释性：Python不需要**编译与链接**生成二进制文件，可以跨平台（Mac、Linux、Windows）直接执行
> 编译（Compile）：将高级语言（C/C++、Rust等）翻译成汇编语言或及机器指令（CPU能够读懂的0和1）
> 链接（link）：将多个文件组合生成可执行文件

- 交互性：Python可以使用**cmd**（命令提示符）进行简单直接的代码执行，不需要单独编写成文件

- 简洁易懂：Python强制使用**缩进**表示是同一个代码块，不使用括号

- 动态类型：Python不需要明确表明变量类型，会**自动推测**变量类型，处理内存分配与释放

- 第三方库：Python具有强大丰富的**第三方库**，即下即用，Python 还可以作为“胶水”语言，轻松调用C/C++或Fortran写的底层库，实现高性能计算

- 可拓展性：Python可以在解释器中添加新的内置函数与模块

- 多重面向：Python既支持面向**过程编程**，也支持**面向对象**
> 面向过程：**以函数为中心**，数据与操作分离，通过函数的顺序调用来处理数据，解决问题
> 面向对象：**以对象为中心**，将数据（属性）和行为（方法）封装在一起，通过对象间的交互来解决问题

在后面学习中会逐渐理解Python的相关特点
## 相关网站
关于Python的用法，永远先查询 **[官方文档](https://www.python.org/)**，它是最权威的Python使用文档

Python的官方文档使用英文编写，基本内容可以通过翻译进行学习，其次Python的官方文档有 **[中文版本](https://docs.python.org/zh-cn/3.12/)**，对于新手，建议在查阅官方文档时，同步参考 **[术语对照表](https://docs.python.org/zh-cn/3.12/glossary.html#glossary)** 这会帮助记忆关键词汇与主要作用

除官方文档外，还有许多国内的网站与论坛可以参考：
- **[CSDN](https://www.csdn.net)**：coder必备论坛，大部分编程问题都可以在这里得到解答
- **[知乎](https://www.zhihu.com)**：优秀的问答网站，如果有编程问题不能解决，可以发布问题寻求解答
- **[菜鸟教程](https://www.runoob.com)**：简单了解Python相关介绍与用法，如果简单语法忘却，可以来这里进行查找

## 下载
Python解释器最好是通过 **[官方网站](https://www.python.org)** 进行下载，但由于官方网站的服务器在国外，所以下载速度偶尔会高达几k或数十k
可以先访问官方网站进行下载，如果下载速度确实很慢的话，就使用镜像站
> 镜像站：国内的企业或相关部门搭建的服务器网站，将国外的部分软存储在国内，以获得更快的下载速度

比较知名的镜像站有：
- **[清华镜像站](https://www.python.org/ftp/python)**
- **[阿里镜像站](https://mirrors.aliyun.com/python-release)**

下载Python解释器会有多个可供选择的版本，版本分为预发行与稳定
预发行的版本相较之前的版本会有一定的更新，但可能引发相关问题；而当预发行版本在一定周期内经过用户与官方使用，没有发现问题，就会转成稳定的版本
### 官方网站

todo:
1. 使用官方网站下载Python解释器

打开官方网站
![[get_python_org.png|1400]]

将鼠标移至Downloads，选择需要下载到的操作系统
由于在Windows上进行下载，这里选择Windows，进入Windows的下载界面
![[on_downloads.png|1400]]

选择当前稳定的最新版本Python 3.13.15进行下载
![[on_windows_download.png|1400]]


![[download_in_org.png|1400]]

选择对应的系统（如果是macOS就选择macOS的版本），这里选择Windows的64bit版本进行下载
![[choose_os.png|1400]]

todo:
1. 安装Python

打开下载的Python文件
如果比较懒可以直接点击Install Now，会按照默认的安装配置进行安装，但针对于爱折腾的用户，或者说希望统一管理下载文件地址以及避免下一些可能很久都用不上的东西（避免全部堆积在C盘，导致C盘炸裂），一般都会选择自定义下载

选择自定义下载（Customize installation）
![[download_setup.png|900]]

简单介绍选项：
- [ ] Documentation：Python官方文档，下载后可以离线观看，但其实通过浏览器进行查看更加方便，且更新更及时，所以这个不需勾选
- [x] pip：Python的下载库的工具，如果想要下载一些第三方库，就需要使用它，如果不勾选，后面下载会很麻烦
- [ ] tcl/tk and IDLE：tcl/tk是Tkinter GUI库的底层依赖，简单来说就是图形化开发界面，IDLE是Python自带的简易集成开发环境（IDE），后面会使用PyCharm进行开发，所以这个不需勾选
- [ ] Python test suite：安装 Python 标准库的测试文件，如果需要自己编写Python的代码或编译（指Python语言本身的源代码），才需勾选
- [x] py launcher：用于在CMD中使用`py`启动python解释器，或使用其他版本的Python，这个会很方便在CMD中更换环境，如`py -3.13`选择打开Python3.13的版本
- [x] for all users：如果上面的py_launcher被勾选，才可以勾选该项，即为这台电脑上的**所有 Windows 用户**安装py_launcher，所有的用户都能使用`py`命令

按照勾选的选项配置即可，点击next
![[download_custom.png|900]]

简单介绍高级选项：
- [ ] Install Python 3.13 for all users：让这台电脑上的**所有 Windows 用户**都能使用 Python
- [x] Associate files with Python：双击py文件时，自动用Python解释器打开，而不是选择应用打开
- [ ] Create shortcuts for installed applications：在开始菜单中创建Python的快捷方式，这个并不必要，可以不勾选
- [x] Add Python to environment variables：添加到环境变量，这样在**任意目录下的命令行**中，直接输入`python`就能运行Python解释器
- [x] Precompile standard library：将Python标准库（Lib\目录）预编译成pyc字节码文件，加快 Python 启动速度
- [ ] Download debugging symbols：下载用于调试Python自身的符号文件，如果需要在Python崩溃时获取详细信息才勾选
- [ ] Download debug binaries：下载Python的调试版（Debug Build），包含额外的调试信息，是**实验性/开发用途**的选项，通常占用几百MB，且对于普通开发者用处不大
- [ ] Download free-threaded binaries：下载启用"自由线程"（Free-Threaded，允许Python在多核CPU上真正并行运行）的Python版本，这是实验性功能，可能导致兼容性问题
Customize install location决定Python安装在哪里，这是必须更改的，不然Python会默认下载到C盘

勾选上述选项，并选择安装地址后，点击install
![[download_custom_2.png|900]]

todo:
1. 检查Python是否添加进环境变量中

存在于环境变量的路径，里面的文件可以在任何文件夹中使用或指向
把下载好的Python的文件夹路径添加进环境变量中后，可以在任何位置使用Python

在开始菜单输入环境变量并进入，点击环境变量
![[add_vironment_varialbe.png|600]]

有两个区域：
- 用户变量：登录电脑的用户的环境变量，不与其他用户共享
- 系统变量：所有用户共同使用

在环境变量中找到**Path**，点击选中并点击编辑
![[add_vironment_varialbe_1.png|900]]

查看Python文件夹地址是否已经添加，如果没有添加则点击新建，将Python的文件夹地址输入
注意，是包含**python.exe**的文件夹地址，而不是exe文件本身的地址，如果python.exe文件的地址是C:\python.exe，那么填写的就是C:\，而不是C:\python.exe

一路点击确定
![[edit_path.png|900]]

todo:
1. 测试Python是否成功安装并添加进环境变量

打开CMD（通过开始菜单输入cmd打开或使用Win+R在文本输入框输入cmd打开）
![[open_cmd.png|1400]]

输入`python --version`，回车
![[check_python_version_in_cmd.png|1400]]

显示刚刚下载的Python版本，代表下载并成功添加进环境变量

---

# 使用Python
使用Python通常通过编写py文件（以.py结尾），然后使用Python解释器执行
对于较为简单的逻辑（甚至为其单独创建文件都觉得是浪费时间），可以通过CMD直接执行

下面将介绍几种使用Python的软件

在此之前，先认识一把打开所有编程语言的钥匙——**HelloWorld**
HelloWorld是一段代码，在coder必须知道的代码中，它绝对排第一（无论是什么语言）
具体代码如下
```python
print("HelloWorld!")
```

`print()`函数是用于将消息打印到终端界面
所以，这段代码的作用是在界面显示`HelloWorld!`这句话

只要在界面上成功显示HelloWorld!，就表明软件可以使用Python解释器运行代码，在此基础上就可以编辑运行其他代码

todo:
1. 创建py文件，输入HelloWorld代码

创建code\helloworld.py，在记事本中打开，输入代码
![[open_helloworld_in_notepad.png|900]]

## CMD
CMD使用Python有两种方式：
- 交互式
- py文件

### 交互式
CMD交互式使用Python，是通过直接运行Python解释器，然后直接编写代码进行执行

todo:
1. 打开CMD
2. 进入Python编辑器
3. 编写代码并执行

打开CMD
![[open_cmd.png|1400]]

在`>`后输入`python`（或py），进入Python解释器界面
![[open_python_in_cmd.png|1400]]

在`>>>`后输入代码，回车
![[print_helloworld_in_cmd.png|1400]]

成功显示

执行完这段代码后，Python会回到`>>>`等待下一段代码

如果代码很长，需要分行处理时，可以使用`\`在行末尾进行截断，在第二行接着编写

在`>>>`输入代码，使用`\`进行截断，回车
![[print_helloworld_in_cmd_1.png|1400]]

Python在截断后，原来的`>>>`会变为`...`，这个是省略号（后面会介绍），代表上一行的代码

接着输入剩余代码，回车
![[print_helloworld_in_cmd_2.png|1400]]

成功显示

### py文件
CMD使用py文件，是通过Python解释器直接执行已编写好的py文件

todo:
1. 打开CMD
2. 使用Python解释器执行已经编写好的py文件

打开CMD
![[open_cmd_1.png|1400]]

输入`python`，空一格，输入要执行的py文件地址（如果文件在当前文件夹内可直接输入文件名+`.py`，否则使用总地址），**双引号**括起，回车
![[print_helloworld_in_cmd_3.png|1400]]

成功显示

### 退出
使用完Python需要退出，可以直接关闭CMD，CMD会自动退出Python
如果还需要在CMD执行相关操作，可以在`>>>`后输入`quit`，退出Python

todo:
1. 退出Python

回到刚才的Python执行界面，输入`quit`，回车
![[quit_python.png|1400]]

成功退出Python界面，回到CMD

## PyCharm
PyCharm是Python的专用IDE（集成开发环境），是Python最完善专业的开发环境
PyCharm有两个版本**社区版**（完全免费）与**专业版**（需要支付费用），对于日常使用，社区版完全够用
PyCharm通常不是以单个文件进行编辑，而是以项目来编辑，可以理解为一个文件夹，里面可以存放多个py文件

todo:
1. 打开PyCharm
2. 创建项目
3. 创建py文件
4. 编写代码并执行

打开PyCharm（专业版略有不同）
![[open_pycharm.png|1400]]

点击新建项目
![[create_programme.png|1400]]

这里需要配置项目的存储位置、是否创建Git仓库、是否创建欢迎脚本与添加解释器
简单介绍选项：
- 位置：项目存储的位置
- 创造Git仓库：Git是版本控制系统，可以随时切换不同版本的文件
- 创建欢迎脚本：创建一个欢迎的文件
- 解释器类型：解释器的类型
- 环境：使用现有的解释器还是下载新的解释器
- 类型：解释器的具体类型
- Python路径：解释器的位置

Git仓库与欢迎脚本现在暂时不需要

选择自定义环境，选择现有，类型为Python，Python路径为下载的Python版本的exe文件路径，点击创建
![[create_programme_1.png|1400]]

如果指定文件夹不为空，PyCharm不会扫描文件夹查看是已经创建的项目还是未创建项目的文件夹，会弹出提示
如果是已经创建的项目，点击打开项目
如果是未创建项目的文件夹，点击从现有的源创建

点击从现有的源创建
![[create_programme_2.png|400]]

成功创建项目并进入项目界面，这里不介绍界面的不同区域（因为这是经过配置后的简洁版本第一次进入会有更丰富的功能）
![[open_pycharm_program.png|1400]]

创建py文件，在要创建文件的文件夹上点击右键>创建>py文件，输入文件名HelloWorld后，回车
![[create_pyfile.png|600]]

文件创建成功会弹出
![[create_pyfile_2.png|600]]

现在不需要使用Git进行版本管理

点击取消后进入py文件界面，在文件界面可以输入代码
![[create_programme_3.png|1400]]

输入代码，点击左上角的三角按钮
![[print_helloworld_in_pycharm.png|1400]]

输出
![[print_helloworld_in_pycharm_1.png|1400]]

成功显示

## VSCode
VSCode是轻量级的IDE，基本所有想要的功能都能通过下载插件进行配置使用，如果想要更加快速、更加自由的编写代码，这是不二选择
VSCode以单文件执行py文件
VSCode想要执行python文件需要下载启用对应的插件：
- Python
- Python Debugger

todo:
1. 打开VSCode
2. 下载对应的插件并启用（如果已经下载启用则跳过）
3. 创建py文件，已有的可以直接打开
4. 编辑并执行代码

打开VSCode界面
![[open_vscode.png|1400]]

点击右边的四个方块（有一个斜着）打开拓展，并在其中搜索python
![[set_expansion_in_vscode.png|1400]]

等待插件下载完成后启用

点击上方的文件>打开文件，打开使用PyCharm编辑的py文件
![[print_helloworld_in_vscode.png|1400]]

点击右上角的三角（第一次执行py文件需要指定Python解释器的位置，即Python的exe文件地址，之后就不需要再指定）
![[print_helloworld_in_vscode_1.png|1400]]

成功显示

---

# 总结
Python是一门极具特色的编程语言，使用广泛，简洁高效

使用Python的工具中：
- CMD：最为简易的工具，能够支持交互性使用与py文件使用
- PyCharm：最为专业的Python使用工具
- VSCode：最为全面的工具，支持Python所有的语法

继续探索Python的奇妙世界吧！