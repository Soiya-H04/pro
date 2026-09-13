#预定义变量 #动态输入
## 预定义变量
---
### 一、概念
#### 1.1 [Predefined variables](https://code.visualstudio.com/docs/reference/variables-reference#_predefined-variables)

使用预定义变量引用相关路径

| 常用变量                         | 描述                        |
| ---------------------------- | ------------------------- |
| `${workspaceFolder}`         | 由 Vscode 打开的文件夹名（全）       |
| `${fileDirname}`             | 活动文件的文件夹名（全）              |
| `${file}`                    | 活动文件名（全）                  |
| `${workspaceFolderBasename}` | 由 Vscode 打开的文件夹名（单）       |
| `${fileDirnameBasename}`     | 活动文件的文件夹名（单）              |
| `${fileBasename}`            | 活动文件名（单）                  |
| `${cwd}`                     | 启动 VS Code 时任务运行程序的当前工作目录 |
| `${fileBasenameNoExtension}` | 活动文件名，没有拓展（单）             |
| `${fileExtname}`             | 活动文件拓展名                   |
#### 1.2 [Environment variables](https://code.visualstudio.com/docs/reference/variables-reference#_environment-variables)

使用`${env：Name}`语法引用环境变量
#### 1.3 [Configuration variables](https://code.visualstudio.com/docs/reference/variables-reference#_configuration-variables)

使用`${config:Name}`引用 VS Code 设置
#### 1.4[Command variables](https://code.visualstudio.com/docs/reference/variables-reference#_command-variables)

通过`${command：commandID}`语法将任何 VS Code 命令用作变量
#### 1.5 [Input variables](https://code.visualstudio.com/docs/reference/variables-reference#_input-variables)

语法为`${input：variableID}`

