
task.json 配置自动执行的任务

### version

指定任务配置文件的版本号，确保 VS Code 能够正确理解任务配置文件的格式和语法

>一般配置为 "2.0.0"

示例
```json
// task.json 配置版本号为 "2.0.0"
{
	"version" = "2.0.0"
}
```

### tasks
具体配置任务，可以配置多个任务

示例
```json
// 配置 tasks 里的具体任务
{
	"version" = "2.0.0",
	"tasks":[
		{
			// task_1
		},
		{
			// task_2
		}
	]
}
```

#### label
label 指定任务的名称
每个任务都要有唯一的任务名称

示例
```json
// 配置 label
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1"
		},
		{
			"label":"task_2"
		}
	]
}
```

#### type	

type 指定任务的执行类型，决定任务的执行方式以及如何解析任务的命令和参数
VSCode 允许两种主要的 type

| type    | 描述       |
| ------- | -------- |
| shell   | 在命令行运行命令 |
| process | 创建进程运行命令 |

示例

```json
// 配置 type
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			// 配置 shell type
			"type":"shell"
		},
		{
			"label":"task_2",
			// 配置 process type
			"type":"process"
		}
	]
}
```
#### command

command 指定需要在 shell 或 process 里执行的命令

>命令一般为可执行文件或相关命令行命令
>如果为可执行文件，最好配置完整地址，并使用`\\`隔开

示例
```json
// 配置 command
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			// 配置编译 C 程序的可执行文件
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe"
		}
	]
}
```

运行示例 task 
在 VSCode 命令行里自动执行
```bash
C:\\Program Files\\mingw64\\bin\\gcc.exe
```


#### args

args 指定传给 command 的参数
args 可以包含一个或多个参数，多个参数使用`[]`将其括起

示例
```json
// 配置 args
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			// 配置传递给编译 C 程序的可执行文件的参数
			"args":[
				// 输出彩色的调试信息
				"-fdiagnostics-color=always",
				// 输出调试信息，支持调试
				"-g",
				// 需要编译的程序代码的地址
				"${file}",
				// 输出标识，后接编译完生成的可执行文件名
				"-o",
				// 生成的可执行文件名
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			]
		}
	]
}
```

运行示例 task 
在 VSCode 命令行里自动执行
```bash
C:\\Program Files\\mingw64\\bin\\gcc.exe -fdiagnostics-color=always -g 需要编译的代码地址 -o 生成的可执行文件名
```

#### options

options 指定任务运行时的附加配置
VSCode 中能够使用的 options 配置有三种

| 配置    | 描述                              |
| ----- | ------------------------------- |
| cwd   | 配置工作目录，配置后可使用相对于工作目录的相对地址       |
| env   | 配置任务运行时的环境变量，配置后可使用相关环境变量       |
| shell | 配置任务运行时使用的 shell，配置后使用配置的 shell |
>一般只使用 cwd

示例
```json
// 配置 options
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			"args":[
				"-fdiagnostics-color=always",
				"-g",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options":
			{
				"cwd":"${fileDirname}",
				"env":"my_env",
				"shell":"shell"
			}
		}
	]
}
```

#### problemMatcher
problemMatcher 指定了匹配错误的匹配器
不同的错误匹配器用于匹配不同编译器的错误
VSCode 有很多语言的错误匹配器配置

| 配置（一部分）    | 描述                     |
| ---------- | ---------------------- |
| $gcc       | 指定为 GCC 编译器的错误输出       |
| $clang     | 指定为 Clang 编译器的错误输出     |
| $msCompile | 指定为 Microsoft 编译器的错误输出 |

示例
```json
// 配置 problemMatcher
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			"args":[
				"-fdiagnostics-color=always",
				"-g",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options":
			{
				"cwd":"${fileDirname}",
				"env":"my_env",
				"shell":"shell"
			},
			// 配置 GCC 编译器的错误匹配器
			"problemMatcher":[
				"$gcc"
			]
		}
	]
}
```
#### group

group 指定任务的组别，用于管理
VSCode 中，group 有两个配置

| 配置        | 描述                                                             |
| --------- | -------------------------------------------------------------- |
| kind      | 指定任务的组，可自定义（VSCode 中已有 build 与 test 组）                         |
| isDefault | 指定是否为组内的默认任务（ture 为默认，false 为非默认）<br>当任务为默认时，执行组任务会第一执行该任务<br> |
>一般只用 kind

示例
```json
// 配置 group
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			"args":[
				"-fdiagnostics-color=always",
				"-g",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options":
			{
				"cwd":"${fileDirname}",
				"env":"my_env",
				"shell":"shell"
			},
			"group":
			{
				// 自定义 group
				"kind":"my_group",
				"isDefault":true
			}
		}
	]
}
```
#### presentation

presentation 指定任务运行时，终端窗口的显示行为
VSCode 的 presentation 有六种配置

| 配置               | 描述                                                                             |
| ---------------- | ------------------------------------------------------------------------------ |
| echo             | 指定是否在终端显示执行的命令<br>true：终端会显示实际执行的命令<br>false：终端不会显示实际执行的命令                     |
| reveal           | 指定是否显示终端<br>always（默认）：每次运行任务时都显示终端<br>never：不自动显示终端<br>silent：仅在任务出错时显示终端     |
| focus            | 指定是否聚焦到终端<br>true：运行任务时会自动将光标聚焦到终端，方便直接输入<br>false：运行任务时不会自动将光标聚焦到终端           |
| panel            | 指定终端面板的共享方式<br>share（默认）：多个任务共享一个终端<br>dedicated：每个任务使用独立终端<br>new：每次运行任务创建新终端 |
| showReuseMessage | 指定是否显示“终端将被重用”提示<br>true：终端会显示“终端将被重用”提示<br>false：终端不会显示“终端将被重用”提示             |
| clear            | 指定是否先清空终端再运行任务<br>true：终端会清空终端再运行任务<br>false：终端不会清空终端再运行任务                     |

示例
```json
// 配置 presentation
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			"args":[
				"-fdiagnostics-color=always",
				"-g",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options":
			{
				"cwd":"${fileDirname}",
				"env":"my_env",
				"shell":"shell"
			},
			"group":
			{
				"kind":"my_group",
				"isDefault":true
			},
			// 配置所有的 presentation
			"presentation":{
				"echo":true,
				"focus":true,
				"clear":true,
				"panel":"shared",
				"showReuseMessage":true,
				"reveal":"always"
			}
		}
	]
}
```

#### dependsOn

dependsOn 指定了任务依赖的其他任务，指定任务必须在另一个（或多个）任务完成后才能运行

>指定依赖任务时，指定任务的 label

示例
```json
// 配置 dependsOn
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			"args":[
				"-fdiagnostics-color=always",
				"-g",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options":
			{
				"cwd":"${fileDirname}",
				"env":"my_env",
				"shell":"shell"
			},
			"group":
			{
				"kind":"my_group",
				"isDefault":true
			},
			"presentation":{
				"echo":true,
				"focus":true,
				"clear":true,
				"panel":"shared",
				"showReuseMessage":true,
				"reveal":"always"
			},
			// 配置依赖的任务
			"dependsOn":["前置任务 1","前置任务 2"]
		}
	]
}
```

#### dependsOrder

dependsOrder 与 dependsOn 一起使用，指定依赖任务的执行顺序
VSCode 里，依赖任务的执行顺序有两种配置

| 配置         | 描述                          |
| ---------- | --------------------------- |
| sequential | 按数组顺序依次执行依赖任务（前一个完成后再执行下一个） |
| parallel   | 并行执行所有依赖任务（同时运行）            |

示例
```json
// 配置 dependsOrder
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			"args":[
				"-fdiagnostics-color=always",
				"-g",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options":
			{
				"cwd":"${fileDirname}",
				"env":"my_env",
				"shell":"shell"
			},
			"group":
			{
				"kind":"my_group",
				"isDefault":true
			},
			"presentation":{
				"echo":true,
				"focus":true,
				"clear":true,
				"panel":"shared",
				"showReuseMessage":true,
				"reveal":"always"
			},
			"dependsOn":["前置任务 1","前置任务 2"],
			// 配置依赖任务的顺序为顺序执行
			"dependsOrder":"sequential"
		}
	]
}
```

#### detail

detail 指定任务的详细说明，在命令面板上显示
不支持变量替换，且文本过长会被截断

示例
```json
// 配置 detail
{
	"version" = "2.0.0",
	"tasks":[
		{
			"label":"task_1",
			"type":"shell",
			"command":"C:\\Program Files\\mingw64\\bin\\gcc.exe",
			"args":[
				"-fdiagnostics-color=always",
				"-g",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options":
			{
				"cwd":"${fileDirname}",
				"env":"my_env",
				"shell":"shell"
			},
			"group":
			{
				"kind":"my_group",
				"isDefault":true
			},
			"presentation":{
				"echo":true,
				"focus":true,
				"clear":true,
				"panel":"shared",
				"showReuseMessage":true,
				"reveal":"always"
			},
			"dependsOn":["前置任务 1","前置任务 2"],
			"dependsOrder":"sequential",
			// 配置任务相关的说明
			"detail":"任务的相关说明"
		}
	]
}
```


### input

task.json 中的 input 指定动态获取用户输入并传给任务

示例
```json
// 配置 input
{
	"version":"2.0.0",
	"tasks":[
		{
			// task_1
		},
		{
			// task_2
		}
	],
	"inputs":[
		{
			// input_1
		},
		{
			// input_2
		}
	]
}
```

#### id

id 指定每个输入的唯一名称

示例
```json
// 配置 id
{
	"version":"2.0.0",
	"tasks":[
		{
			// task_1
		},
		{
			// task_2
		}
	],
	"inputs":[
		{
			// 配置输入 1 的id
			"id":"input_1"
		},
		{
			// 配置输入 2 的id
			"id":"input_2"
		}
	]
}
```

#### type

type 指定输入方式
VSCode 能够配置两种输入方式

| 输入方式         | 描述                         |
| ------------ | -------------------------- |
| pickString   | 提供预定义选项列表供用户选择<br>选项能够添加说明 |
| promptString | 弹出文本框让用户输入任意文本             |
示例
```json
// 配置 type
{
	"version":"2.0.0",
	"task":[],
	"input":[
		{
			"id":"my_input_1",
			// 配置 type 为 pickString
			"type":"pickString"
		},
		{
			"id":"my_input_2",
			// 配置 type 为 promptString
			"type":"promptString"
		}
	]
}
```

#### options

options 与 type 里的 pickString 配套使用，指定输入的选项
选项能够添加解释

示例
```json
// 配置 options
{
	"version":"2.0.0",
	"task":[],
	"input":[
		{
			"id":"my_input_1",
			"type":"promptString"
			// 配置没有解释的 options
			"options":[
				"option_1",
				"option_2"
			]
		},
		{
			"id":"my_input_2",
			"type":"promptString"
			// 配置有解释的 options
			"options":[
				{
					"label":"option_1",
					"detail":"option_1 的解释"
				},
				{
					"label":"option_2",
					"detail":"option_2 的解释"
				}
			]
		}
	]
}
```

#### password

password 与 type 里的 promptString 配套使用，指定输入的文本是否被隐藏为`***`
当为 true 时，输入的内容被隐藏为`***`；当为 false 时，输入的内容正常显示

示例
```json
// 配置 password
{
	"version":"2.0.0",
	"tasks":[],
	"inputs":[
		{
			"id":"my_input",
			"type":"promptString",
			// 配置 password 为 true，隐藏输入内容
			"password":true
		}
	]
}
```

#### default

default 指定输入的默认值
当 type 为 pickString 时，指定默认选项；当 type 为 promptString 时，指定默认输入内容

示例
```json
// 配置 default
{
	"version":"2.0.0",
	"task":[],
	"input":[
		{
			"id":"my_input_1",
			"type":"pickString",
			"options":[
			"option_1",
			"option_2"
			],
			"default":"option_1"
		},
		{
			"id":"my_input_2",
			"type":"promptString",
			"default":"默认输入内容"
		}
	]
}
```

#### description

description 指定在输入弹窗或选项列表中显示提示的文本，说明需要输入什么
可以使用多行的解释，加`\n`即可

示例
```json
// 配置 description
{
	"version":"2.0.0",
	"task":[],
	"input":[
		{
			"id":"my_input_1",
			"type":"pickString",
			"options":[
			"option_1",
			"option_2"
			],
			"default":"option_1",
			"description":"my_input_1 的解释\n 第二行解释"
		},
		{
			"id":"my_input_2",
			"type":"promptString",
			"default":"默认输入内容",
			"description":"my_input_2 的解释\n 第二行解释"
		}
	]
}
```

