#C #switch #control_statement 

## Switch 语句
---
### 一、概念

#### 1.1 用途

Switch 语句为表达式匹配**常量**
匹配到就执行相关语句
#### 1.2 break

在每个`case`里加上`break`才能匹配到后退出
#### 1.3 default

在`Switch` 结尾加上`default`匹配所有常量都匹配的情况
#### 1.4 语法

使用`switch`的语法为
```
switch(表达式)
{
	case 常量1:
		语句1
		break;
	case 常量2:
		语句2
		break;
	case 常量3:
		语句3
		break;
	default:
		语句4
		break;
}
```