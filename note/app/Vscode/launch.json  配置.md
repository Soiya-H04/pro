
launch.json 配置代码调试器

### version
version 指定解析配置的版本

>一般使用"0.2.0" 版本，基本支持所有配置

示例
```json
// 配置 version
{
	// 配置 0.2.0 版本
	"version":"0.2.0"
}
```

### configurations

配置调试器的具体配置
可以配置多个调试器

示例
```json
// 配置 configurations	
{
	"version":"0.2.0",
	"configurations":[
		{
			// configuration_1
		},
		{
			// configuration_2
		}
	]
}
```


#### name

name 指定调试器的唯一名称
在 VSCode 的调试视图中可以选择调试器

示例
```json
// 配置 name	
{
	"version":"0.2.0",
	"configurations":[
		{
			// 配置调试器的 name
			"name":"my-cofiguration"
		}
	]
}
```

#### type

type 指定调试器的类型
VSCode 支持的调试器类型很多

| 调试器类型  | 描述                  |
| ------ | ------------------- |
| cppdbg | 用于调试 C/C++ 程序       |
| python | 用于调试 Python 脚本或应用程序 |
| node   | 用于调试 Node.js 应用程序   |
| java   | 用于调试 Java 应用程序      |
| go     | 用于调试 Go 程序          |

示例
```json
// 配置 type
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			// 配置调试器的 type 为 cppdbg
			"type":"cppdbg"
		}
	]
}
```

#### request

request 指定调试会话的启动方式

| 配置     | 描述                 |
| ------ | ------------------ |
| launch | 指定启动新的程序实例，并直接进入调试 |
| attach | 指定将调试器附加到已经运行的进程   |

示例
```json
// 配置 request
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			// 配置调试会话的启动方式为 launch
			"request":"launch"
		}
	]
}
```

#### externalConsole

externalConsole 仅在 request 为 launch 时使用，指定是否生成使用外部调试终端
为 true 时，生成并使用外部终端；为 false（默认） 时，不生成外部终端

>externalConsole 与 internalConsoleOptions：如果内部调试终端与外部调试终端同时使用会冲突，只能使用一个


示例
```json
// 配置 externalConsole
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			// 配置使用外部中断
			"externalConsole":true
		}
	]
}
```

#### internalConsoleOptions

internalConsoleOptions 指定内部调试终端的打开方式
internalConsoleOptions 有三个配置

| 配置                           | 描述              |
| ---------------------------- | --------------- |
| neverOpen                    | 指定禁用调试控制台（不显示）  |
| openOnFirstSessionStart（默认值） | 指定仅在第一次调试会话时打开  |
| openOnSessionStart           | 指定每次调试时都打开调试控制台 |

>externalConsole 与 internalConsoleOptions：如果内部调试终端与外部调试终端同时使用会冲突，只能使用一个


示例
```json
// 配置 internalConsoleOptions
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			// 配置不使用内部调试终端
			"internalConsoleOptions":"neverOpen"
		}
	]
}
```

#### logging

logging 指定将哪些类型的调试信息记录到调试终端

| 配置            | 描述                    | 默认   |
| ------------- | --------------------- | ---- |
| exceptions    | 用于确定是否应将异常消息记录到调试终端   | true |
| modleLoad     | 用于确定是否应将模块加载事件记录到调试终端 | true |
| programOutput | 用于确定是否应将程序输出记录到调试终端   | true |

示例
```json
// 配置 logging
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			// 配置不记录 exceptions
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			}
		}
	]
}
```
#### stopAtEntry

stopAtEntry 指定是否在程序的入口停下
为 true，调试器在目标的入口处停止(用于单步调试)；为 false（默认），调试器直接执行程序全部代码

示例
```json
// 配置 stopAtEntry
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			// 配置在程序入口停止
			"stopAtEntry":true
		}
	]
}
```

#### program

program 指定要调试的程序地址
程序以`\\`间隔

```json
// 配置 program
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			// 配置调试的程序地址
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe"
		}
	]
}
```
#### cwd

cwd 指定调试程序的工作目录
如果多个目录下有同名文件，确定是哪个目录的文件在工作

>一般采用变量替换，使用`${fileDirname}`来表示文件的工作目录

示例
```json
// 配置 cwd
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			// 配置工作目录
			"cwd":"${fileDirname}"
		}
	]
}
```


#### args

args 指定传递给 program 的参数

>在程序中，使用传入的 args：
  `${argc}` 为传入参数的数量
  `${char* argv[]}` 为传入参数
  `${argv[0]}` 为程序名
  `${argv[i]}` 为传入的第 i 个参数

示例 1
```json
// 配置 args
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			// 配置传递给 porgram 的参数
			"args":["参数 1", "参数 2", "参数 3]
			"cwd":"${fileDirname}"
		}
	]
}
```

示例 2
```json
// 使用 agrs
${argc} // 4
${argv} // 程序名 + 参数
${argv[0]} // 程序名
${argv[i]} // 第 i 个参数
```

#### environment

environment 指定程序使用的环境变量
环境变量采用`{ "name": "变量名","value": "变量值"}`的格式

示例
```json
// 配置 environment
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			"args":["参数 1", "参数 2", "参数 3],
			"cwd":"${fileDirname}"
			// 配置 program 使用的相关 environment
			"environment":[
			{
				"name":"环境变量名 1",
				"value":"环境变量值 1"
			},
			{
				"name":"环境变量名 2",
				"value":"环境变量值 2"
			}
			]
		}
	]
}
```

#### MIMode

MIMode 指定调试器是否使用 MI（Machine Interface）模式与 VSCode 通信
gdb 或 lldb：使用 MI 模式（结构化数据交换，适合 IDE 集成）
none：禁用 MI 模式，直接使用调试器的命令行接口（不推荐）

>与 type 的 cppdbg 配套使用

示例
```json
// 配置 MIMode
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			"args":["参数 1", "参数 2", "参数 3],
			"cwd":"${fileDirname}"
			"environment":[
			{
				"name":"环境变量名 1",
				"value":"环境变量值 1"
			},
			{
				"name":"环境变量名 2",
				"value":"环境变量值 2"
			}
			]
			// 配置调速器与 VSCode 的通信模式为 gdb
			"MIMode":"gdb"
		}
	]
}
```

#### miDebuggerPath

与 MIMode 配套使用，miDebuggerPath 指定调试器（GDB/LLDB）的完整路径

示例
```json
// 配置 miDebuggerPath
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			"args":["参数 1", "参数 2", "参数 3],
			"cwd":"${fileDirname}"
			"environment":[
			{
				"name":"环境变量名 1",
				"value":"环境变量值 1"
			},
			{
				"name":"环境变量名 2",
				"value":"环境变量值 2"
			}
			]
			"MIMode":"gdb",
			// 配置 gdb 的完整地址
			"miDebuggerPath":"C:\\Program Files\\mingw64\\bin\\gdb.exe"
		}
	]
}
```

#### SetupCommands

与 miDebuggerPath 配套使用，SetupCommands 指定传给 gdb 或 lldb 的命令，用于设置输出格式

| 配置             | 描述                                                                               |
| -------------- | -------------------------------------------------------------------------------- |
| description    | 指定相关配置的描述                                                                        |
| text           | 指定调试信息输出的格式<br>-enable-pretty-printing：指定启用整齐打印<br>set print pretty on：指定启用格式化打印 |
| ignoreFailures | 指定配置失败后是否停止调试<br>true：指定配置失败后停止调试<br>false：指定配置失败后不停止调试                          |

示例
```json
// 配置 SetupCommands
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			"args":["参数 1", "参数 2", "参数 3],
			"cwd":"${fileDirname}"
			"environment":[
			{
				"name":"环境变量名 1",
				"value":"环境变量值 1"
			},
			{
				"name":"环境变量名 2",
				"value":"环境变量值 2"
			}
			]
			"MIMode":"gdb",
			"miDebuggerPath":"C:\\Program Files\\mingw64\\bin\\gdb.exe",
			"SetupCommands":[
				{
					"description": "漂亮打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures":true
				}
			]
		}
	]
}
```


#### preLaunchTask

preLaunchTask 指定在调试前需要执行的 task

>preLaunchTask 指定 task 的 label 来使用 task

示例
```json
// 配置 preLaunchTask
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			"args":["参数 1", "参数 2", "参数 3],
			"cwd":"${fileDirname}"
			"environment":[
			{
				"name":"环境变量名 1",
				"value":"环境变量值 1"
			},
			{
				"name":"环境变量名 2",
				"value":"环境变量值 2"
			}
			]
			"MIMode":"gdb",
			"miDebuggerPath":"C:\\Program Files\\mingw64\\bin\\gdb.exe",
			"SetupCommands":[
				{
					"description": "漂亮打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures":true
				}
			],
			// 配置调试前的 task
			"preLaunchTask":"task 的 label"
		}
	]
}
```
#### postDebugTask

postDebugTask 指定在调试后执行的 task

>postDebugTask 指定 task 的 label 来使用 task

```json
// 配置 preLaunchTask
{
	"version":"0.2.0",
	"configurations":[
		{
			"name":"my-cofiguration",
			"type":"cppdbg",
			"request":"launch",
			"externalConsole":true,
			"internalConsoleOptions":"neverOpen",
			"logging":{
				"exceptions":false,
				"modelLoad":true,
				"programOutput":true
			},
			"stopAtEntry":true,
			"program":"${fileDirname}\\${fileBasenameNoExtension}(Debug).exe",
			"args":["参数 1", "参数 2", "参数 3],
			"cwd":"${fileDirname}"
			"environment":[
			{
				"name":"环境变量名 1",
				"value":"环境变量值 1"
			},
			{
				"name":"环境变量名 2",
				"value":"环境变量值 2"
			}
			]
			"MIMode":"gdb",
			"miDebuggerPath":"C:\\Program Files\\mingw64\\bin\\gdb.exe",
			"SetupCommands":[
				{
					"description": "漂亮打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures":true
				}
			],
			"preLaunchTask":"调试前的 task 的 label",
			// 配置调试后的 task
			"postDebugTask":"调试后的 task 的 label",
		}
	]
}
```