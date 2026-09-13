# 对象、值、类型
## 对象
对象是Python对于数据的**抽象化**
Python将各种各样的数据抽象成不同类型的对象**存储并操作**

Python中所有的数据都是通过**对象**以及**对象间关系**表示
如字面值也是对象
代码本身也是由对象表示
如之前的欢迎代码HelloWorld，`print()`是函数对象，`"HelloWorld!"`是字符串对象

每个对象有相应的**标识号**、**值**、**类型**

### 标识号
对象拥有唯一的**标识号**（十进制整数）且**绝对不会被改变**，这是判断对象是否相同的重要依据

使用`id()`可以查看对象标识号
返回结果：
- 对象标识号

假设对象为`<object>`，语法为
```python
id(<object>)
```

todo:
1. 使用`id()`查看对象标识号

创建code\check_id.py，输入
```python
# -*- coding:UTF-8-*-  
  
# 查看对象标识号
print("identifier value of 1000:", id(1000))
```

输出
![[check_id_output.png|1400]]

即整数对象1000的标识号为1482730877904

### 类型
所有对象都有类型

类型定义对象**支持的操作**，限定对象**可以取的值**，对象的类型一般**无法改变**
基于某些特定情况与特殊对象，对象类型可以改变，但一旦处理不当就会引发异常

使用`type()`可以查看对象类型
返回结果：
- 对象类型

假设对象为`<object->`，则使用方式为
```python
type(<object>)
```

在Python中对象都是以类（class）来进行管理创建
class是饼干模具，对象就是由模具烤出的饼干，所以当查看类型时会出现对象属于哪个类，表示的就是对象相应的类型

假设对象类型时`<object-type>`，则查询类型的结果为
```python
<class '<object-type>'>
```

todo:
1. 使用`type()`查看对象类型

创建code\check_type.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 查看对象类型  
print("the type of 1:", type(1))
```

输出
![[check_type_output.png|1400]]

即对象1的类型是int



### 对象比较
对象比较

使用`is`可以比较对象是否相同（实际比较的是标识号）
返回结果：
- True：比较对象是同一个对象
- False：比较对象是不同对象

假设对象分别为`<object-1>`，`<object-2>`，则使用方式为
```python
<object-1> is <object-2>
```

todo:
1. 查看对象标识号
2. 使用`is`比较对象

>True与None是Python两个不同的对象

创建code\compare_is.py，输入
 ```python
# -*- coding:UTF-8 -*-  
  
# 查看对象标识号  
print("identifier of True:", id(True))  
print("identifier of None:", id(None))  
  
# 比较对象
print("True is None:", True is None)
 ```

输出
![[compare_is_output.png|1400]]

即对象True与None的标识号不一样，表示不是同一个对象，所以`is`的比较结果为False

使用`is`比较字面值对象会引发警告SyntaxWarning，但依旧会返回比较结果
使用`is`比较字面值对象的标识符不会引发警告，但依旧不建议使用`is`比较字面值对象

todo:
1. 使用`is`比较字面值对象
2. 使用`is`比较字面值对象的标识符

创建code\compare_literal_is.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 比较字面值对象
print("13 is 'string':", 13 is "string")  
  
# 比较字面值对象的标识符
a = 13  
b = "string"  
print("a is b:", a is b)
```

输出
![[compare_literal_is_output.png|1400]]

即使用**is**比较字面值对象13，"string"会引发警告，但是使用`is`比较字面值对象的标识符a，b不会引发警告

### 对象清除
对象被创建后，大部分不会被显式清除掉

创建对象相当于在桌面新建文件，使用它进行相关操作后，不再需要使用它，它会被自动放到回收站，具体回收站什么时候清理，由程序自己决定
如创建字符串对象并添加标识符后，使用完将标识符指向别的对象，那么原先创建的字符串对象就会等待被清除

当然也有例外，对于有些对象，如文件对象，如果不显示清除，可能会造成程序由明显的延迟，所以有少部分对象会提供显式清除的方式

### 值
对象都有对应值
因为Python没有强制要求使用类型来创建对象，而是根据值来推定对象类型

### 可变性
对象的可变性是由其类型决定的，有些类型的对象的值可以改变，称为**可变对象**，有些不行，称为**不可变对象**

不可变对象并不是**完全不可变**
不可更改值的对象（假设为A），可以包含可以更改值的对象（假设为B），进而虽然A不能修改，但可以修改B的值
可以理解为A中存储了B的引用（或称为内存地址）。所以B的值修改不会影响A的**不可变性**

### 值比较
使用`==`可以比较对象的值是否相等
如数字字面值对象比较代表的数字是否相同，字符串字面值对象比较所有字符是否相同
返回结果：
- True：值相同
- False：值不相同

假设对象分别为`<object-1>`，`<object-2>`，则使用方式为
```python
<object-1> == <object-2>
```

todo:
1. 使用`==`比较对象的值

创建code\compare_eq.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 比较对象值  
print("11 == 'string':", 11 == 'string')
```

输出
![[compare_eq_output.png|1400]]



---
# 基本数据模型

## 基本概念
### 单例对象
**单例对象**是在程序运行期间只能存在一个的对象
无论如何获取单例对象，得到的都是同一个对象，不会创建新的对象

### 内置常量
内置常量是Python在启动

## NoneType
NoneType是None对象的类型

理解None对象需要知道一个概念

>内置常量：
>Python预先定义好的、在解释器启动时就创建的特殊对象，它们有固定的含义和用途

None对象是**单例对象**，也是**内置常量**
所以None对象是由Python在启动解释器时创建，并且在程序运行期间只能存在一个

NoneType类型可以取的值：
- None：代表**空值**，即没有值
所以None对象的取值是它本身

todo:
1. 查看None对象的类型

创建code\check_type_none.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 查看None对象类型  
print("type of None:", type(None))
```

输出
![[check_type_none_output.png|1400]]

即None对象的类型为NoneType

todo:
1. 证明None对象是否为单例对象

创建code\verify_none.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 尝试创建多个None对象  
a = None  
b = None  
c = None  
  
# 查看对象标识号  
print("identifier of a", id(a))  
print("identifier of b", id(b))  
print("identifier of c", id(c))
```

输出
![[verify_none_output.png|1400]]

即所有对象标识符相同，表示都是使用的同一个对象

None是Python定义的关键字，不能使用为标识符
且None对象为单例对象，要保持一致性
所以给None对象赋值是非法的，会引发SyntaxError异常（异常会导致程序无法正常运行）

todo:
1. 尝试给None对象赋值

创建code\try_none.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 尝试给None对象赋值  
None = 12
```

输出
![[try_none_output.png|1400]]

即给None对象赋值会引发SyntaxError异常，提示不能给None对象赋值

## NotImplementedType
NotImplementedType是NotImplemented对象的类型

NotImplemented用于运算符，当作返回值，表示不支持该运算，让Python去执行`__r*__()`函数（\*代表运算）
如`__add__()`函数实现两个对象相加，如果不满足相加条件且返回NotImplemented，则Python会去执行`__radd__()`函数
后面学习运算时就具体介绍

NotImplemented对象是**单例对象**，也是**内置常量**
所以NotImplemented对象是由Python在启动解释器时创建，并且在程序运行期间只能存在一个

NotImplementedType类型可以取的值：
- NotImplemented：代表没有实现，即没有实现相关逻辑
所以NotImplemented对象的取值是它本身

todo:
1. 查看NotImplemented对象的类型

创建code\check_type_notimplemented.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 查看NotImplemented对象类型  
print("type of NotImplemented:", type(NotImplemented))
```

输出
![[check_type_notimplemented_output.png|1400]]

即NotImplemented对象的类型是NotImplementedType

todo:
1. 证明NotImplemented对象是否为单例对象

创建code\verify_notimplemented.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 尝试创建多个NotImplemented对象  
a = NotImplemented  
b = NotImplemented  
c = NotImplemented  
  
# 查看对象标识号  
print("identifier of a", id(a))  
print("identifier of b", id(b))  
print("identifier of c", id(c))
```

 输出
 ![[verify_notimplemented_output.png|1400]]

即所有对象标识符相同，表示都是使用的同一个对象

虽然NotImplemented为单例对象，但NotImplemented不是Python关键字，所以Python支持将NotImplemented作为标识符添加给对象

todo:
1. 为NotImplemented对象赋值

创建code\verify_NotImplemented_1.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 为NotImplemented对象赋值  
NotImplemented = 12  
  
# 打印NotImplemented的值  
print("value of NotImplemented:", NotImplemented)
```

输出
![[verify_notimplemented_1_output.png|1400]]

即NotImplemented的被作为标识符添加给12这个对象

## Ellipsis
Ellipsis是只有一种取值的类型
取值：
- Ellipsis：表示省略

Ellipsis是Python内置的**常量对象**，可以赋值
Python使用Ellipsis表示某些被省略的对象，最常使用的形式是`...`，即Ellipsis对象与`...`为同一个对象

todo:
1. 查看Ellipsis对象与其符号形式`...`的类型
2. 查看Ellipsis对象与其符号形式`...`的标识符

创建code\check_type_id_ellipsis.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 查看Ellipsis对象与...的类型  
print("type of Ellipsis:", type(Ellipsis))  
print("type of ...:", type(...))  
  
# 查看Ellipsis对象与...的标识符  
print("identifier of Ellipsis:", id(Ellipsis))  
print("identifier of ...:", id(...))
```

输出
![[check_type_id_output.png|1400]]

即Ellipsis与`...`的类型都是ellpsis，且标识符都为140716714168864，表示为同一个对象

NotImplemented是具有此值的**单例对象**，即只能创建一个，后面如果需要使用会复用之前创建的NotImplemented对象

todo:
1. 证明Ellipsis与`...`为单例对象

创建code\verify_ellipsis.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 尝试创建多个Ellipsis与...对象  
a = Ellipsis  
b = Ellipsis  
c = ...  
d = ...  
  
# 查看对象标识符  
print("identifier of a:", id(a))  
print("identifier of b:", id(b))  
print("identifier of c:", id(c))  
print("identifier of d:", id(d))
```

输出
![[verify_ellipsis_output.png|1400]]

即所有Ellipsis对象的标识号相同，表示除了第一个创建了Ellipsis对象，其余都是复用第一个Ellipsis对象

---
# 数字
数字对象由 [[3-lexical analysis#数字|数字字面值]] 创建，是**不可变对象**，一旦创建其值就不再改变

数字对象一开始不存在，在第一次使用数字字面值时创建
如
```python
# 创建数字对象1，并使用标识符a表示
a = 1
```

创建数字对象`1`并使用标识符`a`表示

## 数字字符串
数字如果想要进行打印到终端界面进行显示，或者与文字一起使用，又或者存储到文件中，都需要转换为数字字符串
就像写数学题，数字在脑子里进行运算（使用数字），然后将结果写到纸上（展示数字）
所以能看得见的数字都是字符串，而数字字符串是根据数字对象创建的字符串

Python使用数字类型的**内置方法**`__repr__()`和`__str__()`提取**数字对象**的值，并创建对应的**字符串对象**

>内置方法：
>类型内部实现的函数，用于实现类型支持的一系列操作
>后面会详细介绍函数与方法

当使用`repr()`时，会执行`__repr__()`的逻辑
假设数字为`<num>`，则使用方式为
```python
repr(<num>)
```

使用`print()`打印相关信息到终端界面，实际是打印由`__str__()`生成的对应字符串
假设数字为`<num>`，则使用方式为
```python
print(<num>)
```

`print()`打印在终端界面的数字字符串与`repr()`生成的字符串格式是一样的
如果只是想显示数字对象的字符串，使用`print()`
如果想要通过数字字符串执行其他操作，使用`repr()`

todo:
1. 使用`repr()`通过数字对象创建数字字符串对象并使用`type()`查看类型
2. 使用`print()`打印数字对象

创建code\verify_number2string.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 使用repr()创建数字1的对应字符串并使用type()查看类型  
print("repr(1) is", repr(1))  
print("type of repr(1) is", type(repr(1)))  
  
# 使用print()直接打印数字1  
print(1)
```

输出
![[verify_number2string_output.png|1200]]

即`repr(1)`生成1的类型为str

创建字符串对象遵循以下规则：
- 数字字符串是有效的数字字面值，被传给数字的类构造器时，将会产生具有原数字值的对象
将数字字符串传给数字的类构造器都能产生**原来数字值**的对象
如传进"12.12"不会生成12.12000的数字对象

数字的类构造器用于生成数字对象，常见的有：
- `int()`：整型类构造器，将传进的对象转变为整型，即int类型，数字字符串**必须原本为整型**
- `float()`：浮点型类构造器，将传进的对象转变为浮点型，即float类型，数字字符串**必须原本为浮点型**

假设数字字符串为`<num-string>`，则使用方法为
```python
# 转换为整型
int(<num-string>)

# 转换为浮点型
float(<num-string>)
```

- 表示形式会在可能的情况下采用 10 进制
数字字符串默认为十进制，不会出现二进制或其他进制

- 开头的零，除小数点前可能存在的单个零之外，将不会被显示
数字前面不会出现多余的0，唯一的情况是小数出现在小数点前的0

- 末尾的零，除小数点后可能存在的单个零之外，将不会被显示
小数部分末尾的0会被去除，唯一的情况数字的小数部分为0时，会留有一个0表示为小数

- 正负号仅在当数字为负值时会被显示
正数的数字字符串不会在数字前加上+，负数的数字字符串会在数字前加上-

todo:
1. 使用类构造器创建数字字符串对象对应的数字对象并使用`type()`查看类型
2. 使用`print()`打印小数点前为0的小数
3. 使用`print()`打印小数点后有多余0的小数
4. 使用`print()`打印带符号的正负数

创建code\verify_number2string_rule.py，输入
```python
# -*- coding:UTF-8 -*-  
  
# 使用类构造器创建数字字符串"1"与"21.12"对应的数字对象并使用type()查看类型  
print("int('1') is", int('1'))  
print("float('21.12') is", float('21.12'))  
print("type os int('1') is", type(int('1')))  
print("type os float('1') is", type(float('1')))  
  
# 使用print()打印0.12  
print(0.12)  
  
# 使用print()打印12.10000  
print(12.10000)  
  
# 使用print()打印+31，-22  
print(+31)  
print(-22)
```

输出
![[verify_number2string_rule_output.png|1200]]

即类构造器创建了int类型对象1与float类型对象21.12
小数点前的0没有省略，小数点后多余的0被省略
正数的+被省略，负数的-被保留

## int
int是表示数学中整数集合的元素（包括正数和负数），所以Python中所有的整数都是int类型
如
```python
1
21
-12
```

### 类型转换
使用之前提到的类构造器`float()`可以创建以**int类型对象的值**或**整数字面值**为整数部分的浮点数，默认小数点后有一个0

假设int类型对象为`<int-object>`，整数字面值为`<int-literal-value>`，则使用方式为
```python
float(<int-object>)
float(<int-literal-value>)
```

### bool
bool类型是int类型的分支，属于int类型的子类型（Python明确规定）
bool类型有两个取值：True、False

bool值本质上就是真与假，在计算机中表示1与0
True对应整数1，False对应整数0
True/False可以参与数学运算，等价于1/0

True/False跟1/0不是完全等同，它们的类型分别bool与int
使用`print()`进行打印时，True显示True，False显示False

todo:
1. 使用`type()`查看正负整数类型
2. 使用`float()`创建int类型对象与数字字面值为整数部分的浮点型对象
3. 查看`type()`查看True与False类型
4. 使用`print()`打印True与False

创建code\verify_int.py，输入
```python

```









