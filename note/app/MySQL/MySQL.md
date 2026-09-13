# MySQL

## 一、MySQL 基础

### 1-0 数据库与 SQL

#### 1-0.1 数据库

##### 定义

​		数据库（Database）是按照某种特定的数据结构来组织、存储和管理数据的仓库。

​		数据库以一种系统化的方式存储数据，使得数据可以被高效地检索、更新和管理。



##### 数据模型

​		数据模型（Data Model）是数据库中数据组织和存储的抽象表示，规定了以什么模式来存储管理数据，即前面的数据库所遵循的特定的数据结构。

​		主要有三种常见的数据模型：

-   **层次模型**

​		层次模型将数据组织成一个树形结构，每个节点代表数据记录，节点之间存在一对多的父子关系。

​		例如，一个公司的组织架构数据库可以采用层次模型，公司是根节点，部门是子节点，员工是部门的子节点。

-   **网状模型**

​		网状模型允许数据记录之间存在多对多的复杂关系，数据结构像一张蜘蛛网。

​		网状模型比层次模型更灵活，但结构相对复杂，查询和维护难度也更大。

-   **关系模型**

​		关系模型是目前应用最广泛的数据模型。

​		关系模型将数据以表格的形式存储，每个表格称为关系。

​		表格的每一行代表一条记录，每一列代表记录的一个属性。

​		例如，一个学生选课数据库中，“学生”表可以有学号、姓名、性别等列，“课程”表可以有课程号、课程名、学分等列，“选课”表可以关联学生表和课程表，记录学生选课的情况，而每一行代表一个学生和一个课程。



##### 类型

​		数据库根据数据模型的区别大致可以分为两种类型：

-   **关系型数据库**

​		基于关系模型，使用结构化查询语言（SQL）进行数据操作。

​		关系型数据库适合处理结构化数据，如企业的财务数据、客户关系管理（CRM）数据等，这些数据通常具有明确的结构和关系，需要通过复杂的查询来获取信息。

-   **非关系型数据库**

​		不依赖于传统的关系模型，具有灵活的存储结构和高性能的读写能力。

​		主要有：**键值存储数据库**、**文档存储数据库**、**列存储数据库**、**图数据库**。

​		非关系型数据库用于处理非结构化或半结构化数据，如社交媒体数据、日志数据、物联网设备数据等，这些数据的结构灵活多变，需要快速的读写能力来应对高并发的场景。



##### 组成

-   **硬件**

​		包括服务器（用于存储和运行数据库的计算机）、存储设备（如硬盘、固态硬盘等，用于存储数据文件）、网络设备（用于数据库与其他计算机之间的通信）等。

-   **软件**

1.   **数据库管理系统（DBMS）**

​		数据库的核心软件，数据库管理系统为用户和应用程序提供访问数据库的接口，负责数据的存储、检索、更新和管理等操作。

​		例如，MySQL 提供了创建数据库、创建表、插入数据、查询数据等功能。

2.   **数据库应用程序**

​		用户与数据库交互的工具，如数据库客户端软件（用于连接和操作数据库）、数据库开发工具（用于开发数据库应用程序）等。

​		例如，Navicat 是一个数据库客户端软件，用户可以通过它方便地连接到 MySQL、Oracle 等数据库管理系统（DBMS），进行数据的增删改查操作。



##### 功能

​		数据库提供数据存储、数据查询、数据更新等核心功能。



#### 1-0.2 SQL

##### 定义

​		SQL（Struct Query Language，结构性查询语言）是一种声明式编程语言，专门用于管理关系型数据库系统（RDBMS）。

​		SQL 允许用户以简洁明了的方式描述所需的数据操作，而无需详细说明操作的具体步骤。

​		SQL 的核心功能包括数据查询、数据更新（插入、更新、删除数据）、数据定义（创建、修改、删除对象）以及数据控制（权限管理等）。



##### 语法结构

-   **数据定义语言（DDL，Data Definition Language）**

​		用于创建、修改与删除对象（库、表等）的结构。

-   **数据操作语言（DML，Data Manipulation Language）**

​		用于对表中的数据进行增删改。

-   **数据查询语言（DQL,，Data Query Language）**

​		用于检索数据。

-   **数据操控语言（DCL，Data Control Language）**

​		用于控制用户对数据库的访问权限，包括授权和撤销权限，还有对于事务（Transaction）的管理。



### 1-1 MySQL 相关概念

#### 1-1.0 定义

​		MySQL 是一种广泛使用的开源关系型数据库管理系统（RDBMS），基于 SQL 来管理和操作数据库。



#### 1-1.1 库

​		库是 MySQL 中的最高层次的逻辑结构，它是一个容器，用于存储和组织多个相关的数据表。



#### 1-1. 2 表

​		表是数据库中存储数据的基本单位，用来实际的存储数据。

​		表以表格的形式组织数据，即是以行与列的形式来存储数据。



#### 1-1.3 字段

​		字段（Field）是表中的列（Column）的别名（后面的列都用字段来代替），用于存储特定类型的数据，并通过数据类型、是否允许为空、默认值等属性与约束来定义其存储和行为方式。



#### 1-1.4 记录

​		记录（Record）是表中的行（Row）的别名。

​		记录是表中的基本数据单元，每条记录代表一条完整的数据，即在逻辑上需要操作的单个对象。

​		每条记录包含多个字段，可以将字段看为是记录的属性。

​		例如，班级、学号、姓名三种数据（每种数据一个字段）构成一个完整的表，那么一条记录可以代表一个学生，而每条记录都需要包含这三种数据。



#### 1-1.5 关键字

​		关键字（Keywords）就是数据库里不能随便用的“特殊词汇”，它们有固定的用途，比如创建表、查询数据等，不能用作普通的名字或内容。



#### 1-1.6 索引

​		索引（Index）是对表中字段（字段组合）的值进行排序的一种结构。

​		索引类似于书籍的目录，帮助快速定位到数据的存储位置，从而加快数据检索速度。



#### 1-1.7 主键

​		主键（Primary Key）是表中的字段（字段组合），即表内的字段（字段组合）都能充当表的主键。

​		主键的主要作用是用来唯一标识符来标识表中的每一条记录。

​		在表中，作为主键的字段（字段组合），值必须是唯一的，且不能为 Null（空值），即每条记录的主键的值不能重复。

​		例如，在一个学生信息表中，如果以学号作为主键，那么每个学生的学号都是独一无二的，不能有重复的学号，同时学号字段也不能没有值。



#### 1-1.8 外键

​		外键（Foreign Key）是表中的字段（字段组合），即表内的字段（字段组合）都能充当表的外键。

​		外键，就是与外界（别的表，后面统称为外表）有关联的键。

​		例如，有一个学生表（students）和一个班级表（classes），学生表中字段名班级编号的字段可以作为外键，连接到班级表中字段名班级编号的字段，从而建立学生和班级之间的关联。

​		外键必须是一一对应关系，即外键为字段（字段组合），那么与外键连接的也只能是字段（字段组合），且数据的类型也要一样，所以通常作为外键的是两个表都有的字段（字段意义相同）。

​		外键连接的外表的字段必须具有唯一性，即连接的外表的字段不能出现重复值。



### 1-2 数据类型

​		我们存储的每种数据都会有其相对应的数据类型（Data Type）。

​		例如，年龄一般都是整数类型，而名字一般是字符串类型。

​		只有为存储的数据设置了正确的数据类型才能进行数据的存储。

​		MySQL 基本上支持所有需要的数据类型。

#### 1-2.1 数值

​		用来存储数字类型的数据，有整数与浮点数两种数字类型。

##### 整数

​		整数类型有符号（Signed）与无符号（Unsugned）的区别。

​		有符号的整数可以存储负数，但是存储范围会减小；无符号的整数不存储负数，存储范围会更大。

​		下方是所有整数的类型：

|   整数类型    |          signed          |    unsigned    |     |
| :-------: | :----------------------: | :------------: | --- |
|  TINYINT  |        -128 ~ 127        |    0 ~ 255     |     |
| SMALLINT  |      -32768 ~ 32767      |   0 ~ 65535    |     |
| MEDIUMINT |    -8388608 ~ 8388607    |  0 ~ 16777215  |     |
|    INT    | -2147483648 ~ 2147483647 | 0 ~ 4294967295 |     |
|  BIGINT   |      -2^63 ~ 2^63-1      |   0 ~ 2^64-1   |     |



##### 浮点数

​		浮点数没有符号的区别。

​		下方是所有浮点数的类型：

|  浮点数类型  | 位数                               |
| :----------: | :--------------------------------- |
|    FLOAT     | 单精度浮点数，约7位有效数字        |
|    DOUBLE    | 双精度浮点数，约15位有效数字       |
| DECIMAL(m,n) | 精确浮点数，m为总位数，n为小数位数 |



#### 1-2.2 字符串

​		字符串类型用于存储文本数据，包括字符、数字（以文本形式）、符号等内容。

​		下方是基本的字符集类型：

| 字符串类型 | 长度                                                         |
| :--------: | :----------------------------------------------------------- |
|  CHAR(n)   | 定长字符串（尾部会用空格填充），最长 n 个字符（最大 255个）  |
| VARCHAR(n) | 可变字符串（不会填充），最长 n 个字符（65535字节，实际受行大小限制） |
|  TINYTEXT  | 短文本，最长255字节                                          |
|    TEXT    | 中等长度文本，最大 64 kb                                     |



#### 1-2.3 日期时间

​		日期与时间也是一种较为常用的数据种类。

​		下方是所有的日期时间类型：

| 日期时间类型 | 格式                                              |
| :----------: | ------------------------------------------------- |
|     DATE     | 形式为 'YYYY-MM-DD'，用来存储 年-月-日            |
|     TIME     | 形式为 'HH:MM:SS'，用来存储 时:分:秒              |
|   DATETIME   | 形式为 'YYYY-MM-DD HH:MM:SS' ，上两种类型结合起来 |



#### 1-2.4 枚举与集合

​		枚举与集合是只能存储特定的值（值为字符串类型）的类型。

##### 枚举

​		枚举（ENUM）类型用来存储特定的值中的一个。

|       枚举类型        | 类型及个数                                   |
| :-------------------: | :------------------------------------------- |
| ENUM(val1, val2, ...) | val 只能是字符串类型，最多可以包含 65,535 个 |



##### 集合

​		集合（SET）类型用来存储特定的组合，也可以是一个值。

|       集合类型       | 类型及个数                               |
| :------------------: | ---------------------------------------- |
| SET(val1, val2, ...) | val 只能是字符串类型，最多可以包含 64 个 |



#### 1-2.5 Null

​		Null 严格来说不能算一个数据类型，而是一个特殊的值。

​		Null 用来表示未知值，而不是表示空字符串 ' ' 或数字 0。



### 1-3 规范

​		使用 MySQL 来进行数据的管理需要遵守一定的规范，既是为了更好的理解 MySQL 的相关语法与逻辑，也是为了提高工作的效率。

#### 1-3.1 大小写

​		MySQL 对一般字母的大小写是不敏感的，库名与表名还有关键字都不会区分大小写。

​		例如，MySQL 与 mysql 在 MySQL 看来是完全一样的。

​		MySQL 只对字符串内的字母大小写进行区分。

​		下方是对 MySQL 中对于字母大小写的规范：

-   **关键字全大写**

​		例如，编辑关键字 SELECT。

-   **库名、表名、字段名全小写**

​		例如，编辑表名 mytb。

-   **函数名全大写**

​		函数也能算一种特殊的关键字，所以也需要全部大写。



#### 1-3.2 常数

​		编辑常数（字符串、数字、日期）也有规范。

​		下方是 MySQL 对于编辑常数的规范：

-   **字符串**

​		编辑字符串时使用英文的单引号。

​		例如，编辑字符串 'String'。

-   **数值**

​		直接编辑数值。

​		例如，编辑数值 13、15.232。

-   **日期与时间**

​		编辑日期时间时使用英文的单引号。

​		例如，编辑日期时间 '2024-12-09 11:21:31'。



#### 1-3.3 命名

​		在创建对象（库、表以及后面会学到的视图与存储过程）时，都需要给定一个唯一标识符来作为名字，也就是指定一个特定的名字来当作特定对象的代表。

​		命名需要一定的规范，下方是 MySQL 对于命名的规范：

-   **带有较强的描述性**

​		命名带有较强描述性的名字能够更好的理解与记忆创建逻辑。

​		例如，给学生的姓名字段命名为 name。

-   **在名称里加 _ 来连接多个单词**

​		创建名字时如果有多个单词 ，可以用 _ 进行分隔，但 _ 不能放在最前面。

​		例如，两个单词 person 与 id，可以命名为 person_id，但不能命名为 _person_id。

-   **不能重名**

​		不能创建同名的库，库名是使用库时的唯一标识符，同名就不知道使用哪个库。

​		在一个库里也不能创建同名的表，表名也是对表进行操作时唯一的标识符。

​		能在不同库里创建同名的表。

​		例如，不能创建两个名为 mydb 的库，也不能在一个库下创建两个名为 mytb 的表，但是能在 mydb1 与 mydb2 两个库中都创建一个 mytb 的表。

-   **特殊字符的字段名与表名用反引号**

​		如果要创建与关键字同名的字段与表名，需要用反引号将其括住，但这种命名方式建议不用。

​		例如，要创建一个名为 use 的表，但 use 是关键字，需要使用反括号 `` 将其括住。

-   **避免使用像 !、@ 等字符命名**

​		 !、@ 等字符会让名字难以理解，尽量不要使用。



#### 1-3.4 注释

​		编写 SQL 语句需要时常添加注释（Comment），既能理解代码也能提醒正在做的工作。

-   **单行注释**

​		使用两个减号 -- 后接一个空格，后面接注释的内容。

​		-- 前面的内容正常执行，-- 后面的内容会被忽略。

​		例如，

```mysql
这里没有被注释  -- 这里被注释 
```

-   **多行注释**

​		使用 /**/ 来注释多行内容。

​		所有被 /**/ 夹着的内容都会被忽略。

​		在 * 的前后不接内容。

​		例如，

```mysql
这里没有被注释
/*
这是一条
多行注释
*/
这里没有被注释
```



#### 1-3.5 结尾

​		SQL 语句使用英文的 ; 来结尾。

​		不用 ; 会默认是一条 SQL 语句，这样能将长的 SQL 语句分为多行。

​		例如，

```mysql
SQL 语句;  -- 以 ; 结尾
```



#### 1-3.6 括号与引号

​		所有的括号与引号都要成对出现，不能出现单个的括号与引号。

​		例如，

```mysql
((((SQL 语句))))  -- 括号必须封闭
```



### 1-4 约束

​		约束（Constraints） 是一种针对于字段（字段组合）的规则，为表中的字段（字段组合）设置约束可以限制字段（字段组合）。

#### 1-4.1 主键约束

​		为字段（字段组合）设置主键约束就是将该字段（字段组合）作为主键来进行管理。

​		

#### 1-4.2 外键约束

​		为字段（字段组合）设置外键约束就是将该字段（字段组合）作为外键来进行管理。



#### 1-4.3 唯一值约束

​		唯一值约束（Unique）用于限制表中的字段（字段组合）的值在表中不能重复。

​		为字段（字段组合）添加唯一值约束就是用来防止输入的记录在该字段（字段组合）有重复的值。

​		唯一约束允许 Null 值， 且一个表内能有多个唯一值约束。



#### 1-4.4 检查约束

​		检查约束（Check）用于限制表中的字段（字段组合）的值必须满足特定的条件。

​		例如，想要用户的年龄必须大于等于 1 ，就用检查约束来对年龄的字段进行限制，如果添加的记录的年龄小于 1 就无法添加该条记录。



### 1-5 属性

​		属性（Attribute）定义了字段的基本特性。

​		属性具有默认的设置，即就算不为字段指定，字段也会有相应的属性。

#### 1-5.1 可空

​		可空（Null）是字段的默认属性，即字段可以存储 Null。

​		如果想要字段不能存储 Null，就需要指定字段属性为非空（Not Null）。



#### 1-5.2 默认值

​		默认值（Default）属性是添加一条记录时，一个字段的值没有特殊指定值时，默认添加的值。

​		字段默认有默认值属性，字段的默认值为 Null。

​		如果字段设置了非空属性又没有设置自定义的默认值，在添加记录时，这个字段的值必须指定。



#### 1-5.3 自增长

​		自增长（AUTO_INCREMENT）属性是在添加记录时，不需要为自增长字段指定值，会自动的递增添加值（原来字段里最大的值加 1）。

​		字段默认没有自增长属性，且只有整数类型能指定自增长属性。

 

### 1- 6 范式

​		范式是用户设计存储逻辑中应该遵守的规范化原则。

​		常用的有三大范式（其实总共有六个，但后三个太难以完全实现，所以就只需要满足前三范式就够了）。

#### 1-6.1 第一范式（**1NF**）

​		第一范式是设计存储逻辑应该遵守的一个最基础的范式。

​		第一范式有两个性质：

-   **原子性**

​		原子性是指每个字段在表的存储逻辑上不可再分，即对于想要的存储逻辑来看，每个字段都是最小单位的数据种类。

​		例如，年级与班级在某些时候不能一起存储，需要拆分为年级与班级来分别存储；而有些时候年纪与班级可以一起存储，这取决于存储逻辑。

-   **唯一性**

​		唯一性是指同一表中不应存在多个含义相同的字段。

​		如果一条记录有多个相同含义的数据，应该拆分为不同的字段然后放进一个单独的表内进行存储。

​		例如，公司要存储员工的信息里有多个号码，应该单独做一个员工号码表，用来存储号码，而不应该在所有员工的信息的后面添加多个号码。



#### 1-6.2 第二范式（**2NF**）

​		第二范式是在第一范式的基础上，进一步要求表中的每个非主键字段都完全依赖于主键字段。

​		即第二范式要求表中的每个非主字段必须完全依赖于整个主键，而不是主键的一部分。

-   **完全依赖**

​		非主键字段由整个主键唯一确定。

-   **部分依赖**

​		非主键字段仅由主键的部分字段确定。

​		这个范式仅对使用字段组合作为主键的表有意义（单个字段主键的表自动满足 2NF）。

​		例如，表的主键为（订单ID, 产品ID），表中的字段就不能只跟其中一个有关，而是与这个组合有关。

​		推荐将单个字段作为主键，避免关系复杂。



#### 1-6.3 第三范式（3NF）

​		第三范式是在第二范式的基础上解决传递依赖的关系，进一步要求表中的每个非主键字段不仅完全依赖于主键字段，而且不依赖于其他非主键字段。

​		即非主键字段只与主键字段相关，与其他的非主键字段无关。

​		例如，表的主键字段为班级，学生、班主任与班级字段存在依赖关系：学生=>班主任=>班级，学生=>班级，班主任=>班级，这样就称为传递依赖。



### 1-7 字符集与排序规则

​		在 MySQL 中，字符集（Character Set）和排序规则（Collation）是处理文本数据时非常重要的概念。

#### 1-7.1 字符集

​		字符集（Character Set）是字符的集合，定义了可以使用的字符范围。

​		通过对库与表指定所需要的**字符集**，从而存储相应的数据内容。

​		MySQL 默认的字符集为 utf8mb4。

​		字符集是 MySQL 的关键字，需要大写。

​		下方是一些常用的字符集及其适用范围：

|     字符集      | 支持编码                                                     |
| :-------------: | ------------------------------------------------------------ |
| utf8mb4（默认） | 完整的 UTF-8 编码字符集，支持所有 Unicode 字符，包括 4 字节的字符（如表情符号），MySQL 5.5.3 之后引入的，是国际化应用的首选字符集 |
|     latin1      | 西欧字符集，支持拉丁字符，是最常用的字符集之一，使用单字节编码，存储效率高，但不支持非拉丁字符（如中文、日文等） |
|      ascii      | 美国标准信息交换码，只支持英文字符，使用单字节编码           |
|       GBK       | 双字节字符集，主要用于简体中文，支持大部分汉字               |
|      utf8       | UTF-8 编码的 Unicode 字符集，支持多种语言的字符，包括中文、日文、韩文等，只支持 3 字节的 UTF-8 编码，不支持 4 字节的字符（如部分表情符号） |



#### 1-7.2 排序规则

​		排序规则（Collation）定义了字符的比较和排序规则。

​		MySQL 默认的排序规则是 utf8mb4_0900_ai_ci。

​		不同的排序规则可能导致相同的字符在不同的上下文中有不同的比较结果（如区分大小写或不区分大小写）。

​		下方是 MySQL 常见的排序规则：

| 排序规则                   | 适用范围                                                     |
| -------------------------- | ------------------------------------------------------------ |
| utf8_general_ci            | 基于 utf8 字符集的通用排序规则，不区分大小写                 |
| utf8mb4_general_ci         | 基于 utf8mb4 字符集的通用排序规则，不区分大小写              |
| utf8mb4_0900_ai_ci（默认） | 基于 utf8mb4 字符集的排序规则，不区分大小写，更适合国际化应用 |
| utf8mb4_bin                | 基于 utf8mb4 字符集的二进制排序规则，区分大小写              |



## 二、基础 DDL

### 2-0 登录与退出

#### 2-0.1 登录

​		登录 MySQL 前，先确保已经下载 MySQL。

​		在终端执行下方命令

``` bash
mysql -V
```

​		如果返回类似下方信息

``` bash
mysql  Ver 8.0.38 for Win64 on x86_64 (MySQL Community Server - GPL)
```

​		说明已经下载了 MySQL。

​		在终端执行下方命令

```bash
mysql -h <hostname> -u <username> -p
# -h:后接登录主机名
# -u:后接 SQL 账户名
# -p:以密码方式登录
# <hostname>:登录主机名，本机登录可以省略
# <username>:SQL 账户名
```

​		会出现下方的密码提示

```bash
Enter password:
```

​		输入密码，正确就会返回下方界面

```bash
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 11
Server version: 8.0.38 MySQL Community Server - GPL

Copyright (c) 2000, 2024, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

​		提示符变为了 mysql>，表明已经处于 MySQL 的终端界面。

​		实例：

```bash
# 尝试登录 MySQL
C:\Users\smart dogs>MySQL -u root -p
Enter password: ********  # 输入密码
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.38 MySQL Community Server - GPL

Copyright (c) 2000, 2024, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>  # 登录成功
```



#### 2-0.2 退出

​		在 MySQL 的终端界面执行下方命令就可以退出 MySQL 的终端界面。

```mysql
EXIT;
```

​		实例：

```mysql
/*
退出 MySQL
*/
mysql> EXIT;
Bye  -- 退出成功
```



### 2-1 库

​		库的 DDL ，会涉及到库的结构查询、创建、修改、使用以及删除语法。

#### 2-1.0 信息查询

​		在 MySQL 里可以对库进行信息查询，来更好的管理库，提升工作效率。

##### 已创建库

​		在 MySQL 中可以创建并管理多个库。

​		当库多了，就需要时常查看已经创建的库来进行管理。

​		执行下方语法查询所有当前已经创建的库

```mysql
SHOW DATABASES;
```

​		实例：

```mysql
/*
查询当前所有已经创建的库
*/
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |  -- 已创建的库都在这里
| sakila             |
| smartdog           |
| sys                |
+--------------------+
6 rows in set (0.00 sec)
```

​		其中mysql，information_schema，performance_schema，sys 是 MySQL 自带的库，不要随意进行更改！



##### 结构

​		库的结构包括创建命令、字符集、排序规则。

​		执行下方语法查询库的结构

```mysql
SHOW CREATE DATABASE <db>;
/*
<db>:查询的库
*/
```

​		实例：

```mysql
/*
查询 mydb 库的结构
*/
mysql> SHOW CREATE DATABASE mydb;
| Database | Create Database
| mydb     | CREATE DATABASE `mydb`; /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */  -- 结构都会在这里显示
1 row in set (0.00 sec)
/*
创建命令:CREATE DATABASE `mydb`;
字符集:utf8mb4
排序规则:utf8mb4_0900_ai_ci
*/
```



##### 当前使用

​		在频繁切换库进行操作时，需要时常查看当前位置。

​		执行下方语法查询当前使用的库

```mysql
SELECT DATABASE();
```

​		实例：

```mysql
/*
查看当前使用的库
*/
mysql> SELECT DATABASE();
+------------+
| DATABASE() |
+------------+
| testdb     |  -- 当前在使用的库
+------------+
1 row in set (0.00 sec)
```



#### 2-1.1 创建

​		从前面查询库的结构可以知道，可以设置库的结构有字符集与排序结构。

​		MySQL 已经默认设置了一套库的结构，所以不需要自己设置库的字符集与排序规则。

​		使用默认设置结构的库称为**默认库**；使用了自己设置的结构创建的库称为**自定义库**。

​		此外，还有一种错误创建的情况需要注意。

##### 默认库

​		执行下方语法创建默认的库 

```mysql
CREATE DATABASE <db>;
/*
<db>:为我们所创建库的名称
*/
```

​		实例：

```mysql
/*
创建一个默认的库 mydb
*/
mysql> CREATE DATABASE mydb;
Query OK, 1 row affected (0.01 sec)  -- 创建成功


/*
验证是否创建
*/
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |  -- 库 mydb 已创建
| mysql              |
| performance_schema |
| sakila             |
| smartdog           |
| sys                |
+--------------------+
7 rows in set (0.00 sec)


/*
验证 MySQL 默认的字符集与排序规则
查询默认库 mydb 的结构
*/
mysql> SHOW CREATE DATABASE mydb;
| Database | Create Database                                                                 
| mydb     | CREATE DATABASE `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */ |  -- 默认的库结构
1 row in set (0.00 sec)
```



##### 自定义库

​		默认库的字符集与排序规则已经能够解决大部分的需求。

​		但是有时确实需要自定义库的字符集与排序规则。

​		执行下方语法创建自定义库

```mysql
CREATE DATABASE <db>
CHARACTER SET <character>
COLLATE <collate>;
/*
<db>:创建的表名
<character>:指定的字符集
<collate>:指定的排序规则
*/
```

​		实例：

```mysql
/*
创建自定义库 mydb_2，字符集为 utf8，排序规则为 utf8_general_ci 
*/
mysql> CREATE DATABASE mydb_2
    -> CHARACTER SET utf8
    -> COLLATE utf8_general_ci;
Query OK, 1 row affected, 2 warnings (0.01 sec)  -- 创建成功


/*
查看库 mydb_2 的结构是否被设置成功
*/
mysql> SHOW CREATE DATABASE mydb_2;
| Database | Create Database
| mydb_2   | CREATE DATABASE `mydb_2` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */  -- 确实修改，但 COLLATE 不会显示
1 row in set (0.00 sec)
```



##### 错误创建

​		如果创建一个已经存在的库，MySQL 会报错。

​		实例：

```mysql
/*
创建已存在的库 mydb
*/
mysql> CREATE DATABASE mydb;
ERROR 1007 (HY000): Can't create database 'mydb'; database exists  -- 报错
```

​		如果报错了，该条 SQL 语句不会被执行，库也不会被创建。

​		尽量避免报错，因为如果作为程序来运行会导致程序崩溃。

​		为了更安全的创建库，建议执行下面的语法来创建库

```mysql
CREATE DATABASE IF NOT EXISTS <db>;
/*
<db>:创建的库
*/
```

​		该语句的意思是如果不存在这个名字的库时再进行创建，当库没有创建成功的时候会警告但不会报错。

​		实例：

```mysql
/*
创建已存在的库 mydb
*/
mysql> CREATE DATABASE IF NOT EXISTS mydb;
Query OK, 1 row affected, 1 warning (0.01 sec)  -- 不报错，只会警告
```



#### 2-1.3 修改

​		库的修改针对于库的结构进行修改，也就是修改库的字符集与排序规则。

​		执行下方语法修改库的字符集与排序规则

```mysql
ALTER DATABASE <db>
CHARACTER SET <character>
COLLATE <collate>;
/*
<db>:修改的库
<character>:修改的字符集
<collate>:修改的排序规则
*/
```

​		实例：

​		

```mysql
/*
先查询库 mydb 原有的字符集与排序规则
*/
mysql> SHOW CREATE DATABASE mydb;
| Database | Create Database
| mydb     | CREATE DATABASE `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */ 
1 row in set (0.00 sec)


/*
修改 mydb 的字符集与排序规则为 utf8 与 utf8_general_ci
*/
mysql> ALTER DATABASE mydb CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected, 2 warnings (0.00 sec)  -- 修改成功


/*
查询库 mydb 现在的字符集与排序规则是否更改
*/
mysql> SHOW CREATE DATABASE mydb;
| Database | Create Database
| mydb     | CREATE DATABASE `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */  -- 已经修改为 utf8 与 utf8_general_ci
1 row in set (0.00 sec)
```



#### 2-1.4 使用

​		在对库内的表进行操作前，需要先使用相应的库。

​		执行下方语法使用库

```mysql
USE <db>;
/*
<db>:使用的库
*/
```

​		实例：

```mysql
/*
使用库 mydb
*/
mysql> USE mydb;
Database changed  -- 开始使用库 mytb


/*
查询当前使用的库验证
*/
mysql> SELECT DATABASE();
+------------+
| DATABASE() |
+------------+
| mydb       |  -- 正在使用库 mydb
+------------+
1 row in set (0.00 sec)
```



#### 2-1.5 删除

​		库的删除会有错误删除的情况。

##### 正常删除

​		执行删除库

```mysql
DROP DATABASE <db>;
/*
<db>:删除的库名
*/
```

​		实例：

```mysql
/*
删除库 mydb
*/
mysql> DROP DATABASE mydb;
Query OK, 0 rows affected (0.01 sec)  -- 删除成功


/*
验证是否删除成功
*/
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb_2             |
| mysql              |
| performance_schema |  -- 没有库 mydb
| sakila             |
| smartdog           |
| sys                |
+--------------------+
7 rows in set (0.00 sec)
```



##### 错误删除

​		当删除不存在的库时，MySQL 会报错。

​		实例：

```mysql
/*
删除不存在的库 mydb
*/
mysql> DROP DATABASE mydb;
ERROR 1008 (HY000): Can't drop database 'mydb'; database doesn't exist  -- 报错
```

​		如果报错，这条 SQL 语句不会被执行。

​		安全删除库与安全创建库时的语法类似，推荐执行下面的语法删除库

```mysql
DROP DATABASE IF EXISTS <db>;
```

​		实例：

```mysql
/*
删除不存在的库 mydb
*/
mysql> DROP DATABASE IF EXISTS mydb;
Query OK, 0 rows affected, 1 warning (0.00 sec)  -- 无报错，只有警告
```



###  2-2 表

​		表的 DDL，会涉及表的查询、创建、修改、删除操作。

#### 2-2.1 信息查询

​		在 MySQL 里，通过对创建的表进行信息查询，可以更好的管理表。

##### 已创建表

​		使用库后，可以查看该库里所有的表。

​		执行下方语法查看库内所有的表

```mysql
SHOW TABLES;
```

​		实例：

```mysql
/*
使用库 mydb_2
*/
mysql> USE mydb_2;
Database changed

/*
查看库 mydb_2 内所有的表
*/
mysql> SHOW TABLES;
Empty set (0.00 sec)  -- 空的库，因为库 mydb_2 刚刚创建，所以库还是空的，没有表


/*
使用 sakila 库
*/
mysql> USE sakila;
Database changed

/*
查看库 sakila 里所有的表
*/
mysql> SHOW TABLES;
+----------------------------+
| Tables_in_sakila           |
+----------------------------+
| actor                      |
| actor_info                 |
| address                    |
| category                   |
| city                       |
| country                    |
| customer                   |
| customer_list              |
| film                       |
| film_actor                 |
| film_category              |
| film_list                  |  -- sakila 库里所有的表
| film_text                  |
| inventory                  |
| language                   |
| nicer_but_slower_film_list |
| payment                    |
| rental                     |
| sales_by_film_category     |
| sales_by_store             |
| staff                      |
| staff_list                 |
| store                      |
+----------------------------+
23 rows in set (0.00 sec)
```



##### 结构

​		表的结构包括：字段结构（字段、数据类型、约束、属性）、创建命令、基本结构（字符集、排序规则、存储引擎）

>   **存储引擎（Engine）**
>
>   MySQL 的存储引擎（Engine）是数据库的核心组件之一，它定义了数据的存储方式、索引机制、事务支持、锁定机制等。
>
>   通过使用不同的存储引擎，MySQL 可以根据不同的应用场景提供不同的功能和性能优化。
>
>   常见的存储引擎有：
>
>   InnoDB（默认）：支持事务处理（ACID），提供行级锁定，适合高并发的读写操作。
>
>   支持外键约束，确保数据的参照完整性。
>
>   MyISAM：不支持事务处理，但支持全文索引，适合全文搜索。
>
>   MEMORY：数据存储在内存中，访问速度快，但数据在服务器重启后会丢失。
>
>   ARCHIVE：用于存储大量不频繁更新的数据，如日志信息。
>
>   BLACKHOLE：数据写入后会被丢弃，不存储任何数据。
>
>   NDB (Cluster)：支持高可用性和分布式存储，适合集群环境。

​		查看表的结构会有简单查询与细致查询两种语法。

-   **简单查询**

​		简单查询只会查到字段结构，即字段名、数据类型、约束、属性。

​		简单查询查到的信息易于理解，且对于一般情况来说足够。

​		执行下方语法对表进行简单查询

```mysql
DESC <tb>;
/*
<tb>:查询的表
*/
```

​		实例：

```mysql
/*
在库 sakila 里简单查询表 store
*/
mysql> DESC store;
-- 字段名			   字段的数据类型		    可空   键     默认值              其他属性
| Field             | Type              | Null | Key | Default           | Extra             
| store_id         | tinyint unsigned  | NO   | PRI | Null              | auto_increment
| manager_staff_id | tinyint unsigned  | NO   | UNI | Null              |                   
| address_id       | smallint unsigned | NO   | MUL | Null              |
| last_update      | timestamp         | NO   |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
4 rows in set (0.00 sec)
```

-   **详细查询**

​		详细查询会查询到上方提到的所有结构。

​		详细查询其实是查询表的完整的创建命令（有些使用默认值的语法也会显示出来）。

​		执行下方语法对表进行详细查询

```mysql
SHOW CREATE TABLE <tb>;
/*
<tb>:查询的表
*/
```

​		实例：

```mysql
/*
详细查询库 sakila 里表 store
*/
mysql> SHOW CREATE TABLE store;
| Table | Create Table
| store | CREATE TABLE `store` (
  `store_id` tinyint unsigned NOT Null AUTO_INCREMENT,
  `manager_staff_id` tinyint unsigned NOT Null,
  `address_id` smallint unsigned NOT Null,
  `last_update` timestamp NOT Null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`store_id`),
  UNIQUE KEY `idx_unique_manager` (`manager_staff_id`),
  KEY `idx_fk_address_id` (`address_id`),
  CONSTRAINT `fk_store_address` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_store_staff` FOREIGN KEY (`manager_staff_id`) REFERENCES `staff` (`staff_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)  -- 所有的结构都有，这就是这个表创建的完整语法
```



#### 2-2.2 创建

​		与库一样，表也有字符集与排序规则的默认设置。

​		库的字符集与排序规则会成为库里的表的默认字符集与排序规则，使用默认设置创建的表称为默认表。

​		此外，还可以更改表的存储引擎，而更改这三个结构创建的表，称为自定义表。

##### 默认表

​		默认结构的表，可以进行字段名、数据类型、属性、约束、描述的设置。

​		字段名与数据类型是在创建表时必须设置的，其余结构都是根据存储逻辑进行设置。

###### 数据类型

​		MySQL 支持的数据类型就是创建字段时可以使用的数据类型。

​		执行下方语法创建只有数据类型与字段名的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1>,  -- 用 , 来分割两个字段
    <column2> <type2>,
    <column3> <type3>,
    <column4> <type4>   -- 最后一个字段不加 ,
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
*/
```

​		需要注意的是，每两个字段之间用英文的 ,  隔开，最后一个字段后面不加。

​		实例：

```mysql
/*
创建库 tb_test
*/
mysql> CREATE DATABASE IF NOT EXISTS tb_test;
Query OK, 1 row affected (0.01 sec)

/*
使用库 tb_test
*/
mysql> USE tb_test;
Database changed

/*
创建包含所有数据类型的默认表 mytb
*/
mysql> CREATE TABLE IF NOT EXISTS mytb (
    -> num1 INT UNSIGNED,  -- 这里的 UNSIGNED 就是前面介绍的无符号
    -> num2 BIGINT,        -- 默认为有符号
    -> num3 FLOAT,
    -> num4 DOUBLE,
    -> num5 DECIMAL(10,5),
    -> str1 CHAR(10),
    -> str2 VARCHAR(20),
    -> str3 TEXT,
    -> date1 DATE,
    -> date2 TIME,
    -> date3 DATETIME,
    -> enum1 ENUM('a','b','c'),
    -> set1 SET('a','b','c')  -- 注意没有 , 
    -> );
Query OK, 0 rows affected (0.03 sec)  -- 创建成功 


/*
查询表 mytb 的字段结构验证
*/
mysql> DESC mytb;
+-------+-------------------+------+-----+---------+-------+
| Field | Type              | Null | Key | Default | Extra |
+-------+-------------------+------+-----+---------+-------+
| num1  | int unsigned      | YES  |     | Null    |       |
| num2  | bigint            | YES  |     | Null    |       |
| num3  | float             | YES  |     | Null    |       |
| num4  | double            | YES  |     | Null    |       |
| num5  | decimal(10,5)     | YES  |     | Null    |       |
| str1  | char(10)          | YES  |     | Null    |       |
| str2  | varchar(20)       | YES  |     | Null    |       |
| str3  | text              | YES  |     | Null    |       |
| date1 | date              | YES  |     | Null    |       |
| date2 | time              | YES  |     | Null    |       |
| date3 | datetime          | YES  |     | Null    |       |
| enum1 | enum('a','b','c') | YES  |     | Null    |       |
| set1  | set('a','b','c')  | YES  |     | Null    |       |
+-------+-------------------+------+-----+---------+-------+
13 rows in set (0.00 sec)
```



###### 描述

​		对于一般的字段其实并不需要加描述（Comment）。

​		例如，name 这种描述性强的字段名，就不需要添加描述。

​		描述的数据类型是字符串。

​		描述是有默认值的，默认值为 ''，即空字符串。

​		添加描述会将原来的描述覆盖，可以视为另一种形式的设置。

​		描述细分为表描述与字段描述。

​		执行下面的语法为表与字段添加描述

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1> COMMENT <comment1>, 
    <column2> <type2> COMMENT <comment2>,
    <column3> <type3> COMMENT <comment3>,
    ...
) COMMENT <tb_comment>; 
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<comment>:字段描述，字符串格式
<tb_comment>:表描述，字符串格式
*/
```

​		添加的描述都是字符串，不能添加其他数据类型的描述。

​		实例：

```mysql
/*
创建带有字段描述与表描述的表 mytb_2
*/
mysql> CREATE TABLE IF NOT EXISTS mytb_2 (
    -> id INT COMMENT 'id的描述',  -- 设置字段描述
    -> name VARCHAR(20) COMMENT 'name的描述'
    -> ) COMMENT '表的描述';  -- 设置表描述
Query OK, 0 rows affected (0.02 sec)  -- 创建成功
```



###### 约束

​		MySQL 一共提供了四种约束（Constraint）：主键约束、外键约束、唯一值约束、检查约束。

​		约束需要进行命名，以便进行相关的管理。

​		约束只能对字段（字段组合）进行设置。

​		执行下方语法创建设置约束的表

```mysql
CREATE TABLE <tb> (
	<column1> <type1>,
    <column2> <type2>,
    <constraint3>,
    <constraint4>
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<constrain>：字段的约束
*/
```

-   **主键约束**

​		因为一张表里只能设置一个主键约束，主键约束名就被 MySQL 固定为 PRIMARY，所以不需要对主键约束进行命名。

​		执行下方语法创建设置主键约束的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1>,
    <column2> <type2>
    PRIMARY KEY (<column1>,<column2>)
);
/*
<tb>:创建的表
<column>:创建的字段
(<column>,<column>):主键字段（字段组合）
<type>:字段的数据类型
*/
```

​		实例：

```mysql
/*
创建主键为 id 的表 pk_tb
*/
mysql> CREATE TABLE IF NOT EXISTS pk_tb (
    -> id INT PRIMARY KEY
    -> );
Query OK, 0 rows affected (0.05 sec)  -- 创建成功


/*
查询表 pk_tb 的 id 字段是否被设置为主键
*/
mysql> DESC pk_tb;
+-------+------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+------+------+-----+---------+-------+
| id    | int  | NO   | PRI | Null    |       |  -- KEY 为 PRI
+-------+------+------+-----+---------+-------+
1 row in set (0.00 sec)
```

-   外键约束

​		一个表里能有多个外键，即可以设置多个外键约束

​		执行下面语法创建设置外键约束的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1>,
    <column2> <type2>,
    CONSTRAINT <fk_name> FOREIGN KEY (<column1>,<column2>) REFERENCES <f_tb> (<f_column1>,<f_column2>)
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<fk_name>:外键约束名
(<column>,<column>):外键字段（字段组合）
<f_tb>:外表
<f_column>:外表的字段（具有唯一性）
*/
```

​		注意外键字段的数量与顺序与相应的数据结构要一样。

​		实例：

```mysql
/*
创建含无唯一性的字段 id 与 name 的外表 fk_tb
*/
mysql> CREATE TABLE IF NOT EXISTS fk_tb (
    -> id INT,
    -> name VARCHAR(10)
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
创建主键为 id 与 name 的外表 fk_tb2
*/
mysql> CREATE TABLE IF NOT EXISTS fk_tb2 (
    -> id INT,
    -> name VARCHAR(10),
    -> PRIMARY KEY (id,name)
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
创建与 fk_tb 以 (id,name) 进行外键关联的表 fk_mytb_1
*/
mysql> CREATE TABLE IF NOT EXISTS fk_mytb_1 (
    -> id INT,
    -> name VARCHAR(10),
    -> CONSTRAINT fk_idname FOREIGN KEY (id,name) REFERENCES fk_tb (id,name)
    -> );
ERROR 1822 (HY000): Failed to add the foreign key constraint. Missing index for constraint 'fk_idname' in the referenced table 'fk_tb'  -- 报错，无法创建

/*
创建与 fk_tb2 以 (id,name) 进行外键关联的表 fk_mytb_2
*/
mysql> CREATE TABLE IF NOT EXISTS fk_mytb_2 (
    -> id INT,
    -> name VARCHAR(10),
    -> CONSTRAINT fk_idname FOREIGN KEY (id,name) REFERENCES fk_tb2 (id,name)
    -> );
Query OK, 0 rows affected (0.05 sec)  -- 创建成功
```

​		最后强调一次，外键要数据类型（长度）一致，顺序一致，数量一致！

-   唯一值约束

​		一个表里能有多个唯一值，即可以设置多个唯一值约束。

​		执行下面语法创建设置唯一性约束的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1>,
    <column2> <type2>,
    CONSTRAINT <uni_name> UNIQUE (<column1>,<column2>)
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<uni_name>:唯一值约束名
(<column>,<column>):唯一值字段（字段组合）
*/
```

​		实例

```mysql
/*
创建一个 id 与 name 字段为组合的唯一值的表 uni_tb
*/
mysql> CREATE TABLE IF NOT EXISTS uni_tb (
    -> id INT,
    -> name VARCHAR(10),
    -> CONSTRAINT uni_idname UNIQUE (id,name)
    -> );
Query OK, 0 rows affected (0.05 sec)  -- 创建成功
```

-   检查约束

​		检查约束确保符合条件的值才会被加入到表内，而条件是一个具有真值的布尔表达式。

>   布尔表达式
>
>   布尔表达式是一种表达逻辑关系的表达式，它的结果是一个布尔值，即 true（真）或 false（假）。

​		一个表里能设置多个检查约束。

​		执行下面语法创建设置检查约束的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1>,
    <column2> <type2>,
    CONSTRAINT <chk_name> CHECK (<condition1>,<condition2>)
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<chk_name>:检查约束名
<condition>:布尔条件式
*/
```

​		实例：

```mysql
/*
创建一个 age 需要大于18的表 chk_tb
*/
mysql> CREATE TABLE IF NOT EXISTS chk_tb (
    -> age INT,
    -> CONSTRAINT chk_age CHECK (age > 18)
    -> );
Query OK, 0 rows affected (0.02 sec)  -- 创建成功
```



###### 属性

​		字段的常用属性有三种：可空、默认值、自增长。

-   **可空（Null）**

​		段默认可空，创建表时可以不写。

​		执行下方语法可以创建一个字段可空的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1> Null
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
*/
```

​		与执行下方语法k'yi创建一个字段可空的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1>
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
*/
```

​		两个语法效果一样。

​		想要字段不能接收 Null 的话，需要设置字段属性为非空。

​		执下方语法创建字段不可空的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1> NOT Null
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
*/
```

​		实例：

```mysql
/*
创建一个 id 字段可空的表 null_tb
*/
mysql> CREATE TABLE IF NOT EXISTS null_tb (
    -> id INT
    -> );
Query OK, 0 rows affected (0.03 sec)  -- 创建成功

/*
查询 id 字段是否可空
*/
mysql> DESC null_tb;
+-------+------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+------+------+-----+---------+-------+
| id    | int  | YES  |     | Null    |       |  -- Null 的值为 YES，即字段允许为空
+-------+------+------+-----+---------+-------+
1 row in set (0.00 sec)


/*
创建一个 id 字段不可空的表 notnull_tb
*/
mysql> CREATE TABLE IF NOT EXISTS notnull_tb (
    -> id INT NOT Null
    -> );
Query OK, 0 rows affected (0.02 sec)  -- 创建成功

/*
查询 id 字段是否可空
*/
mysql> DESC notnull_tb;
+-------+------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+------+------+-----+---------+-------+
| id    | int  | NO   |     | Null    |       |  -- Null 的值为 NO，即字段不允许为空
+-------+------+------+-----+---------+-------+
1 row in set (0.00 sec)
```

-   **默认值（DEFAULT）**

​		默认值的数据类型应该与字段相同。

​		执行下方语法创建设置默认值的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1> DEFAULT <df_value> 
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<df_value>:字段的默认值
*/
```

​		实例：

```mysql
/*
创建含有字段 id 的表 df_tb，并指定默认值为 Q000000
*/
mysql> CREATE TABLE IF NOT EXISTS df_tb (
    -> id VARCHAR(10) DEFAULT 'Q000000'
    -> );
Query OK, 0 rows affected (0.03 sec)  -- 创建成功

/*
查询 id 的默认值
*/
mysql> DESC df_tb;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | varchar(10) | YES  |     | Q000000 |       |  -- DEFAULT 为 Q000000
+-------+-------------+------+-----+---------+-------+
1 row in set (0.00 sec)
```

-   **自增长（AUTO_INCREMENT）**

​		自增长字段有一个初始值，默认是 1。

​		每次插入新记录时，字段值会自动递增 1。

​		例如，如果初始值是 1，步长是 1，那么插入的第一条记录的值是 1，第二条记录的值是 2，依此类推。

​		自增长字段的值是连续的，但删除记录后，自增长值不会回退。

​		例如，如果插入了 3 条记录后删除了其中一条，自增长值仍然会继续递增，不会重新使用被删除的值。

​		自增长有一个要求，其必须有唯一性（主键或唯一值）

​		执行下方语法来创建一个字段具有自增长属性的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1> AUTO_INCREMENT 
);
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
*/
```

​		实例：

```mysql
/*
创建一个含有设置自增长属性的唯一值字段 id 的表 autoadd_tb
*/
mysql> CREATE TABLE IF NOT EXISTS autoadd_tb (
    -> id INT AUTO_INCREMENT,
    -> CONSTRAINT uni_id UNIQUE (id)
    -> );
Query OK, 0 rows affected (0.03 sec)  -- 创建成功
```



##### 自定义表

​		默认创建的表的字符集与排序规则与库的一致，也就是说，表会沿用库的对应设置。

​		默认表的搜索引擎为 InnoDB。

​		执行下方语法创建自定义的表

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1>,
    <column2> <type2>,
) ENGINE=<engine> CHARACTER SET <character> COLLATE <collate>;
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<engine>:表的存储引擎
<character>:表的字符集
<collate>:表的排序规则
*/
```

​		实例：

```mysql
/*
创建一个搜索引擎为 MyISAM，字符集为 utf8，排序规则为 utf8_general_ci 的表 custom_tb
*/
mysql> CREATE TABLE IF NOT EXISTS custom_tb (
    -> id Int
    -> ) ENGINE MyISAM CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 0 rows affected, 2 warnings (0.01 sec)   -- 创建成功

/*
查询表 custom_tb 的详细结构
*/
mysql> SHOW CREATE TABLE custom_tb;
| Table  | Create Table                                                                     
| mytb_7 | CREATE TABLE IF NOT EXISTS `mytb_7` (
  `id` int DEFAULT Null
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3  -- 修改成功
1 row in set (0.00 sec)
```



##### 错误创建

​		创建一个存在的表，MySQL 会报错。

​		实例：

```mysql
/*
查询当前存在的表
*/
mysql> SHOW TABLES;
+-------------------+
| Tables_in_tb_test |
+-------------------+
| chk_tb            |
| df_tb             |
| fk_mytb_2         |
| fk_tb             |
| fk_tb2            |
| mul_pk_tb         |
| mytb              |
| mytb_10           |
| mytb_11           |
| mytb_12           |
| mytb_13           |
| mytb_2            |
| mytb_3            |
| mytb_4            |
| mytb_5            |
| mytb_6            |
| mytb_7            |
| mytb_8            |
| mytb_9            |
| notNull_tb        |
| Null_tb           |
| pk_tb             |
| uni_tb            |
| uni_tb2           |
+-------------------+
24 rows in set (0.00 sec)

/*
创建存在的表 mytb
*/
mysql> CREATE TABLE mytb (
    -> id INT
    -> );
ERROR 1050 (42S01): Table 'mytb' already exists  -- 报错
```

​		为了避免 MySQL 报错，建议执行下面的语法创建表。

```mysql
CREATE TABLE IF NOT EXISTS <tb>(
	...
);
```

​		实例：

```mysql
/*
创建存在的表 mytb
*/
mysql> CREATE TABLE IF NOT EXISTS mytb (
    -> id INT
    -> );
Query OK, 0 rows affected, 1 warning (0.01 sec)  -- 不报错，只有警告
```



##### 总结

​		创建表的时候有很多结构可以设置。

​		但表的结构的设置是有顺序的。

​		下方是整个创建表的顺序：

```mysql
CREATE TABLE IF NOT EXISTS <tb> (
	<column1> <type1> <attribute1> COMMENT '<comment1>',
    <column2> <type2> <attribute2> COMMENT '<comment2>',
    <constrain1>,
    <constrain2>,
) ENGINE <engine> CHARACTER SET <character> COLLATE <collate> COMMENT '<tb_comment>';
/*
<tb>:创建的表
<column>:创建的字段
<type>:字段的数据类型
<attribute>:字段的属性
<constraint>:字段的约束
<comment>:字段的描述
<tb_comment>:表的描述
*/
```



#### 2-2.4 修改

​		表的结构非常复杂，所以对应的修改也很复杂。

​		可以将修改概括为三个情况：添加、修改、删除。

##### a.添加

​		能够添加的结构有：字段、约束。



###### 字段

​		对已存在的表添加字段时，也可以像在创建表时一样，为字段设置属性、描述与约束。

​		但在设置字段的约束时，不能设置添加字段与其他已存在字段组合约束，因为 MySQL 只能为已经在表内的字段添加字段组合约束。

​		添加字段需要考虑对已有的记录的影响，即记录的对应字段的取值。

​		如果不设置非空属性，那么每一条记录的添加字段的值都会默认设为 Null；而如果设置了默认值，就会使用默认值来作为每条记录的值。

​		简而言之，若是为新字段设置非空属性，就需要设置非空的默认值，否则可以不用设置。

​		下方是不加约束的添加字段的语法

```mysql
ALTER TABLE <tb>
ADD COLUMN <column1> <type1> <attribute1> COMMENT <comment1>;
/*
<tb>:添加的表
<column>:添加的字段
<type>:字段的数据类型
<attribute>:字段的属性
<comment>:字段的描述
*/
```

​		实例：

```mysql
/*
创建表 add_tb
*/
mysql> CREATE TABLE IF NOT EXISTS add_tb (
    -> id INT
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
为表 add_tb 添加 name 字段并设置默认值与描述
*/
mysql> ALTER TABLE add_tb
    -> ADD COLUMN name VARCHAR(20) DEFAULT '空' COMMENT 'name的描述';
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功

/*
查看 name 字段是否添加成功
*/
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int         | YES  |     | Null    |       |
| name  | varchar(20) | YES  |     | 空      |       |  -- 确实添加正确
+-------+-------------+------+-----+---------+-------+
2 rows in set (0.00 sec)
```

​		下方是添加字段时同时设置添加字段约束的基本语法

```mysql
ALTER TABLE <tb>
ADD COLUMN <column1> <type1> <attribute1> COMMENT <comment>,
ADD <constraint1>; 
/*
<tb>:添加的表
<column>:添加的字段
<type>:字段的数据类型
<attribute>:字段的属性
<comment>:字段的描述
<constraint>:添加的约束
*/
```

-   主键约束

​		与创建时设置一样，不需要为其指定约束名。

​		执行下方语法添加设置主键约束的字段

```mysql
ALTER TABLE <tb>
ADD COLUMN <column1> <type1>,
PRIMARY KEY (<pk_column1>);
/*
<tb>:添加的表
<column>:添加的字段
<type>:字段的数据类型
<pk_column>:主键字段
*/
```

​		实例：

```mysql
/*
为 add_tb 表添加带有主键约束的 age 字段
*/
mysql> ALTER TABLE add_tb
    -> ADD COLUMN age INT. 
    -> PRIMARY KEY (age);
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功

/*
查看字段 age 是否具有主键约束
*/
mysql> DESC add_tb;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int         | YES  |     | Null    |       |
| name  | varchar(20) | YES  |     | 空      |       |
| age   | int         | NO   | PRI | Null    |       |  -- 确实设置了主键约束
+-------+-------------+------+-----+---------+-------+
3 rows in set (0.00 sec)
```

​		主键约束只能添加一次。

-   外键约束

​		添加字段时设置外键约束需要指定外键约束名。

​		执行下方语法添加设置外键约束的字段

```mysql
ALTER TABLE <tb>
ADD COLUMN <column1> <type1>,
ADD CONSTRAINT <fk_name> FOREIGN KEY (<fk_column1>) REFERENCES <f_tb> <f_column>;
/*
<tb>:添加的表
<column>:添加的字段
<type>:字段的数据类型
<fk_name>:外键约束名
<fk_column>:外键字段
<f_tb>:外表
<f_column>:外表的字段
*/
```

​		实例：

```mysql
/*
给表 add_tb 添加 fk_id 字段并外键关联到 mytb_8 的 id 字段
*/
mysql> ALTER TABLE add_tb
    -> ADD COLUMN fk_id INT,
    -> ADD CONSTRAINT fk FOREIGN KEY (id) REFERENCES mytb_8 (id);
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功
```

-   唯一值约束

​		添加字段时设置唯一值约束需要指定唯一值约束名。

​		执行下方语法添加设置唯一值约束的字段

````mysql
ALTER TABLE <tb>
ADD COLUMN <column1> <type1>,
ADD CONSTRAINT <uni_name> UNIQUE (<uni_column1>);
/*
<tb>:待添加的表
<column>:添加的字段
<type>:字段的数据类型
<uni_name>:唯一值约束名
<uni_column>:唯一值字段
*/
````

​		实例：

```mysql
/*
为表 add_tb 添加设置唯一值约束的 class 字段
*/
mysql> ALTER TABLE add_tb
    -> ADD COLUMN class VARCHAR(20),
    -> ADD CONSTRAINT uni_class UNIQUE (class);
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功

/*
查询是否添加了唯一值的 class 字段
*/
mysql> DESC add_tb;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int         | YES  | MUL | Null    |       |
| name  | varchar(20) | YES  |     | 空      |       |
| age   | int         | NO   | PRI | Null    |       |
| fk_id | int         | YES  |     | Null    |       |
| class | varchar(20) | YES  | UNI | Null    |       |  -- 确实设置了唯一值约束
+-------+-------------+------+-----+---------+-------+
5 rows in set (0.00 sec)
```

-   检查约束

​		添加字段时设置检查约束需要指定检查约束名。

​		执行下方语法添加设置检查约束的字段

```mysql
CREATE TABLE IF NOT EXISTS <tb>
ADD COLUMN <column1> <type1>,
ADD CONSTRAINT <chk_name> CHECK (<condition1>);
/*
<tb>:添加的表
<column>:添加的字段
<type>:字段的数据类型
<chk_name>:检查约束名
<condition>:检查条件
*/
```

​		添加的字段默认会添加在表的最后。

​		下方的语法可以指定其添加的位置。

​		执行下方语法将添加的字段添加到原有字段的后面

```mysql
ALTER TABLE <tb>
ADD COLUMN <column1> <type1> AFTER <ori_column>;
/*
<tb>:添加的表
<column>:添加的字段
<type>:字段的数据类型
<ori_column>:原有的字段
*/
```

​		实例：

```mysql
/*
在 mytb_8 表里添加 age 字段，并将其添加在字段 id 的后面
*/
mysql> ALTER TABLE mytb_8
    -> ADD COLUMN age INT NOT Null DEFAULT 1 COMMENT 'age在id的后面' AFTER id;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功

/*
查看表 mytb_8 字段顺序
*/
mysql> DESC mytb_8;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | int         | YES  |     | Null    |       |
| age   | int         | NO   |     | 1       |       |  -- 在 id 的后面
| name  | varchar(10) | YES  |     | 空      |       |
+-------+-------------+------+-----+---------+-------+
3 rows in set (0.00 sec)
```

​		还有一个位置，靠上方的语法是不能指定到的，那就是第一个位置。

​		如果想要将字段指定到表的第一个位置，就执行下方语法添加字段并将其指定到表的第一个位置

```mysql
ALTER TABLE <tb>
ADD COLUMN <column1> <type1> FIRST;
/*
<tb>:添加的表
<column>:添加的字段
<type>:字段的数据类型
*/
```

​		实例：

```mysql
/*
为表 mytb_8 添加字段 class 并指定在第一个位置
*/
mysql> ALTER TABLE mytb_8
    -> ADD COLUMN class INT NOT Null DEFAULT 0 COMMENT 'class在最前面' FIRST;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

/*
查询表 mytb_8 字段顺序
*/
mysql> DESC mytb_8;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+ 
| class | int         | NO   |     | 0       |       |  -- class 在第一个位置
| id    | int         | YES  |     | Null    |       |  
| age   | int         | NO   |     | 1       |       |
| name  | varchar(10) | YES  |     | 空      |       |
+-------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```



###### 约束

​		所有约束都能添加给已存在的表。

-   主键约束

​		添加主键约束依旧不需要指定约束名。

​		执行下方语法给表中的字段（字段组合）添加主键约束。

```mysql
ALTER TABLE <tb>
ADD PRIMARY KEY (<column1>,<column2>);
/*
<tb>:添加的表
<column>:添加约束的字段
*/
```

​		实例：

```mysql
/*
为 mytb_8 的 id 字段添加主键约束
*/
mysql> ALTER TABLE mytb_8
    -> ADD PRIMARY KEY (id);
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功

/*
查看主键约束是否添加成功
*/
mysql> DESC mytb_8;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| class | int         | NO   |     | 0       |       |
| id    | int         | NO   | PRI | Null    |       |  -- 添加成功
| age   | int         | NO   |     | 1       |       |
| name  | varchar(10) | YES  |     | 空      |       |
+-------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```



-   外键约束

​		添加外键约束需要知道外键约束名。

​		执行下方语法给表中的字段（字段组合）添加外键约束

```mysql
ALTER TABLE <tb>
ADD CONSTRAINT <fk_name>
FOREIGN KEY (<ori_column1>，<ori_column2>)
REFERENCES <foreign_tb> (<foreign_column1>,<foreign_column2>);
/*
<tb>:添加的表
<fk_name>:外键约束名
<ori_column>:添加外键约束的原表字段
<foreign_tb>:外键连接的外表
<foreign_column>:连接的外表字段
*/
```

​		实例：

```mysql
/*
创建一个具有主键 id 的外表 mytb_9
*/
mysql> CREATE TABLE IF NOT EXISTS mytb_9 (
    -> id int PRIMARY KEY
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
给 mytb_8 表的 id 字段添加外键约束关联到 mytb_9 的 id 字段
*/
mysql> ALTER TABLE mytb_8
    -> ADD CONSTRAINT fk_id
    -> FOREIGN KEY (id)
    -> REFERENCES mytb_9 (id);
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功
```

-   唯一值约束

​		添加唯一值约束约束需要知道唯一值约束名。

​		执行下方语法给表中的字段（字段组合）添加唯一值约束

```mysql
ALTER TABLE <tb>
ADD CONSTRAINT <uni_name>
UNIQUE (<column1>,<column2>);
/*
<tb>:添加的表
<uni_name>:唯一值约束名
<column>:添加唯一值约束的字段
*/
```

​		实例：

```mysql
/*
给表 mytb_8 的 name 字段添加唯一值约束
*/
mysql> ALTER TABLE mytb_8
    -> ADD CONSTRAINT uni_name
    -> UNIQUE (name);
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功

/*
查询唯一值约束是否添加成功
*/
mysql> DESC mytb_8;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| class | int         | NO   |     | 0       |       |
| id    | int         | NO   | PRI | Null    |       |
| age   | int         | NO   |     | 1       |       |
| name  | varchar(10) | YES  | UNI | 空      |       |  -- 添加成功
+-------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

-   检查约束

​		添加检查约束需要知道检查约束名。

​		执行下方语法给表里的字段（字段组合）添加检查约束

```mysql
ALTER TABLE <tb>
ADD CONSTRAINT <chk_name>
CHECK (<condition>);
/*
<tb>:添加的表
<chk_name>:检查约束名
<condition>:检查条件
*/
```

​		实例：

```mysql
/*
给表 mytb_8 的 age 字段添加检查约束
*/
mysql> ALTER TABLE mytb_8
    -> ADD CONSTRAINT ck_age
    -> CHECK (age > 0);
Query OK, 0 rows affected (0.06 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 添加成功
```



##### b.修改

​		除了表名（不能更改）与约束（只能添加与删除），其他的表结构都能修改。

​		下方是能够修改的结构：

###### 字段名

​		修改字段名的情况很少见。

​		修改字段名的情况很复杂，需要先将该字段的约束先全部删除，再将字段的全部属性与描述重新编辑一遍，最后再将

​		约束给新的字段名添加上去。

​		执行下方语法为字段更改名字，假设现在字段已经没有任何属性

```mysql
ALTER TABLE <tb>
CHANGE COLUMN <old_column> <new_column> <type1> <attribute1> COMMENT <comment1>;
/*
<tb>:修改的表
<old_column>:旧字段名
<new_column>:新字段名
<type1>:字段的数据类型
<attribute>:字段的属性
<comment1>:字段的描述
*/
```

​		实例：

```mysql
/*
创建一个含 name 字段的表 chname_tb 并添加默认值
*/
mysql> CREATE TABLE IF NOT EXISTS chname_tb (
    -> name VARCHAR (20) DEFAULT '空'
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
修改字段名为 new_name
*/
mysql> ALTER TABLE chname_tb
    -> CHANGE name new_name VARCHAR(20) DEFAULT '空';
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 修改成功

/*
查询表 chname_tb 里的字段
*/
mysql> DESC chname_tb;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| new_name | varchar(20) | YES  |     | 空      |       |  -- 正确修改
+----------+-------------+------+-----+---------+-------+
1 row in set (0.00 sec)
```



###### 数据类型

​		修改数据类型之前要确保类型兼容。

>   **兼容性**
>
>   指新的数据类型是否能够容纳现有数据，以及是否会对现有数据的存储、查询和完整性产生影响。
>
>   如果新的数据类型与现有数据不兼容，可能会导致数据丢失、错误或无法执行修改操作。
>
>   兼容范围：
>
>   -   小范围  ->大范围：如从 VARCHAR(50) -> VARCHAR(255)，TINYINT -> INT。
>   -   数值 -> 字符串：通常兼容，因为数字可以完整地存储为字符串格式。
>   -   字符串 -> 数值：如果字符串字段中包含非数字字符（如字母、空格等），修改后会导致错误。
>   -   日期 ->字符串：通常兼容，因为日期可以完整地存储为字符串格式。
>   -   浮点 ->整数：小数部分会被截断，导致数据丢失。
>   -   字符串 -> 日期：如果字符串字段中包含非日期格式的内容（如纯文本、不规范的日期格式等），修改后会导致错误。

​		修改字段的数据类型，可以使用两种语法 CHANGE 与 MODIFY。

​		修改数据类型时，也是需要先将该字段的约束先全部删除，再将字段的全部属性与描述重新编辑一遍，最后再将

​		约束给新的字段名添加上去。

-   **CHANGE**

​		执行下方语法修改字段的数据类型，注意要写两遍字段名

```mysql
ALTER TABLE <tb>
CHANGE COLUMN <column1> <column1> <new_type> <attribute1> COMMENT <comment>;
/*
<tb>:修改的表
<column>:修改的字段
<new_type>:修改的数据类型
<attribute>:字段的属性
<comment>:字段的描述
*/
```

​		实例：

```mysql
/*
创建包含字段 id 的表 chtype_tb，并添加默认值
*/
mysql> CREATE TABLE IF NOT EXISTS chtype_tb (
    -> id INT DEFAULT 99
    -> );
Query OK, 0 rows affected (0.03 sec)

/*
将字段 id 的数据类型修改为 BIGINT
*/
mysql> ALTER TABLE chtype_tb
    -> CHANGE COLUMN id id BIGINT DEFAULT 99;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 修改成功

/*
查看字段 id 的数据类型
*/
mysql> DESC chtype_tb;
+-------+--------+------+-----+---------+-------+
| Field | Type   | Null | Key | Default | Extra |
+-------+--------+------+-----+---------+-------+
| id    | bigint | YES  |     | 99      |       |  -- 确实修改为 BIGINT
+-------+--------+------+-----+---------+-------+
1 row in set (0.01 sec)
```

-    **MODIFY**

​		执行下方语法修改字段的数据类型，注意只要写一遍字段名

```mysql
ALTER TABLE <tb>
MODIFY COLUMN <column1> <new_type> <attribute1> COMMENT '<comment1>';
/*
<tb>:修改的表
<column>:修改的字段
<new_type>:修改的数据类型
<attribute>:字段的属性
<comment>:字段的描述
*/
```

​		实例：

```mysql
/*
将表 chtypr_tb 的字段 id 的数据类型修改为 VARCHAR(20)
*/
mysql> ALTER TABLE chtype_tb
    -> MODIFY COLUMN id VARCHAR(20) DEFAULT '90';
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0

/*
查看字段 id 的数据类型
*/
mysql> DESC chtype_tb;
+-------+-------------+------+-----+---------+-------+
| Field | Type        | Null | Key | Default | Extra |
+-------+-------------+------+-----+---------+-------+
| id    | varchar(20) | YES  |     | 90      |       |  -- 确实修改为 VARCHAR(20)
+-------+-------------+------+-----+---------+-------+
1 row in set (0.00 sec)
```

​		这里有一点要注意，默认值要符合修改的数据类型。



###### 属性

​		修改属性的时候需要考虑到原表已经有的记录，如果原有字段的数据中含有 Null，那么字段就不能设置为非空。

​		而如果为一个字段设置为默认值，字段里所有为 Null 的值都会修改为默认值。

​		修改字段的属性也有 CHANGE 与 MODIFY 两种语法。

-   **CHANGE**

​		执行下方语法修改字段属性

```mysql
ALTER TABLE <tb>
CHANGE COLUMN <column1> <column1> <type1> <new_attribute> COMMENT '<comment1>';
/*
<tb>:修改的表
<column>:修改的字段
<new_type>:字段的数据类型
<new_attribute>:修改的属性
<comment>:字段的描述
*/
```

​		实例：

```mysql
/*
创建一个含有非空字段 id 的表 chattr_tb
*/
mysql> CREATE TABLE IF NOT EXISTS chattr_tb (
    -> id INT NOT Null
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
将 id 字段的属性修改为可空并添加默认值
*/
mysql> ALTER TABLE chattr_tb
    -> CHANGE id id INT Null DEFAULT 14;
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0

/*
查看一下 id 字段的非空属性
*/
mysql> DESC chattr_tb;
+-------+------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+------+------+-----+---------+-------+
| id    | int  | YES  |     | 14      |       |  -- 成功修改为可空且默认值为14
+-------+------+------+-----+---------+-------+
1 row in set (0.00 sec)
```



###### 描述

​		修改字段描述与表描述可以分为 CHANGE 与 MODIFY 两种语法。

-   **字段描述**

​		执行下方语法

```mysql
-- CHANGE 语法
ALTER TABLE <tb>
CHANGE COLUMN <column1> <column1> <type1> <attribute> COMMENT <new_comment>;
/*
<tb>:修改的表
<column>:字段名
<new_type>:字段的数据类型
<attribute>:字段的属性
<new_comment>:修改的描述
*/

-- MODIFY 语法
CHANGE COLUMN <column1> <type1> <attribute> COMMENT <new_comment>;
/*
<tb>:修改的表
<column>:修改的字段
<new_type>:字段的数据类型
<attribute>:字段的属性
<new_comment>:修改的描述
*/
```

​		实例：

```mysql
/*
创建表 chcom_tb 并添加描述
*/
mysql> CREATE TABLE IF NOT EXISTS chcom_tb (
    -> id INT COMMENT '未修改'
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
分别用 CHANGE 与 MODIFY 修改描述
*/
mysql> ALTER TABLE chcom_tb
    -> CHANGE COLUMN id id INT COMMENT 'CHANGE 修改';
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 修改成功

mysql> ALTER TABLE chcom_tb
    -> MODIFY COLUMN id INT COMMENT 'MODIFY 修改';
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 修改成功
```

-   **修改表描述**

​		执行下方语法修改表描述

```mysql
ALTER TABLE <tb>
COMMENT <new_tb_comment>;
/*
<tb>:修改的表
<new_tb_comment>: 修改的表描述
*/
```

​		实例：

```mysql		
/*
修改 chcom_tb 的表描述
*/
mysql> ALTER TABLE chcom_tb
    -> COMMENT '修改表描述';
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 成功修改
```



###### 基本结构

​		下方是基本结构包括：存储引擎、字符集、排序结构

​		不建议在已经存储数据后再进行修改总结构，否则数据的完整性与正确性可能会被破坏。

​		执行下方语法修改表的存储引擎、字符集与排序结构

```mysql
ALTER TABLE <tb> ENGINE <engine>;
ALTER TABLE <tb> CONVERT TO CHARACTER SET <character> COLLATE <collate>;
/*
<tb>:修改的表
<engine>:修改的存储引擎
<character>:修改的字符集
<collate>:修改的排序规则
*/
```

​		实例：

```mysql
/*
创建一个默认表 chbase_tb
*/
mysql> CREATE TABLE IF NOT EXISTS chbase_tb (
    -> id INT
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
查询表 chbase_tb 原来的基本结构
*/
mysql> SHOW CREATE TABLE chbase_tb;
| Table   | Create Table                                                                    
| chbase_tb | CREATE TABLE `chbase_tb` (
  `id` int DEFAULT Null
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
1 row in set (0.00 sec)

/*
修改表 chbase_tb 的搜索引擎
*/
mysql> ALTER TABLE chbase_tb ENGINE MyISAM;
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 修改成功

/*
修改表 chbase_tb 的字符集与排序规则
*/
mysql> ALTER TABLE chbase_tb
    -> CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 0 rows affected, 2 warnings (0.03 sec)
Records: 0  Duplicates: 0  Warnings: 2  -- 修改成功

/*
查看表 chbase_tb 现在的基本结构
*/
mysql> SHOW CREATE TABLE chbase_tb;
| Table   | Create Table
| chbase_tb | CREATE TABLE `chbase_tb` (
  `id` int DEFAULT Null
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3  -- 修改成功
1 row in set (0.00 sec)
```



###### 总结

​		CHANGE 与 MODIFY 的功能区别只有更改字段名的时候会体现。

​		更常使用 MODIFY 的语法来进行表的修改，因为可以少写一个无用的字段名。

​		一次可以同时修改多个结构，可以一次直接修改全部的需要修改的结构。



##### c.删除

​		能够删除的表的结构和能够添加的一样，就是字段与约束。

​		删除字段之前需要将添加给字段的约束先删除，例如外键约束等，才能进行字段的删除。

###### 约束

-   主键约束

​		因为每个表只能有一个主键约束，就不需要通过约束名来进行删除。

​		使用下方语法删除主键约束。

```mysql
ALTER TABLE <tb>
DROP PRIMARY KEY;
/*
<tb>:删除的表
*/
```

​		实例：

```mysql
/*
创建字段 id 为主键的表 dpk_tb
*/
mysql> CREATE TABLE IF NOT EXISTS dpk_tb (
    -> id INT PRIMARY KEY
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
删除 id 的主键约束
*/
mysql> ALTER TABLE dpk_tb
    -> DROP PRIMARY KEY;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 删除成功

/*
查询主键约束是否删除
*/
mysql> DESC dpk_tb;
+-------+------+------+-----+---------+-------+
| Field | Type | Null | Key | Default | Extra |
+-------+------+------+-----+---------+-------+
| id    | int  | NO   |     | Null    |       |  -- 删除成功
+-------+------+------+-----+---------+-------+
1 row in set (0.00 sec)
```

-   外键约束

​		删除外键约束需要外键约束名，执行下方的语法删除外键约束

```mysql
ALTER TABLE <tb> 
DROP FOREIGN KEY <fk_name>;
/*
<tb>:删除的表
<fk_name>:外键约束名
*/
```

​		实例：

```mysql
/*
创建外表 fk_tb3 并将字段 id 设为唯一值
*/
mysql> CREATE TABLE IF NOT EXISTS fk_tb3 (
    -> id INT,
    -> CONSTRAINT uni_id UNIQUE (id)
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
创建表 dfk_tb 并关联外表 fk_tb3 的 id 字段
*/
mysql> CREATE TABLE IF NOT EXISTS dfk_tb (
    -> id INT,
    -> CONSTRAINT foreignk_id FOREIGN KEY (id) REFERENCES fk_tb3 (id)
    -> );
Query OK, 0 rows affected (0.03 sec)

/*
删除 dfk_tb 的字段 id 的外键
*/
mysql> ALTER TABLE dfk_tb
    -> DROP FOREIGN KEY foreignk_id;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 删除成功
```

-   唯一值约束

​		删除唯一值约束需要唯一值约束名，执行下方语法删除唯一值约束

```mysql
ALTER TABLE <tb>
DROP INDEX <uni_name>;
/*
<tb>:删除的表
<uni_name>:唯一值约束名
*/
```

​		实例：

```mysql
/*
创建表 duni_tb 并给当中的 id 与 name 字段添加唯一值约束 
*/
mysql> CREATE TABLE IF NOT EXISTS duni_tb (
    -> id INT,
    -> name VARCHAR(20),
    -> CONSTRAINT uni_idname UNIQUE (id,name)
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
删除 id 与 name 的唯一值约束
*/
mysql> ALTER TABLE duni_tb
    -> DROP INDEX uni_idname;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0  --- 删除成功
```

-   检查约束

​		删除检查约束需要检查约束名，执行下方语法删除检查约束

```mysql
ALTER TABLE <tb>
DROP CHECK <chk_name>;
/*
<tb>:删除的库
<chk_name>:检查约束名
*/
```

​		实例：

```mysql
/*
创建表 dchk_tb 并为字段 id 添加检查约束
*/
mysql> CREATE TABLE IF NOT EXISTS dchk_tb (
    -> id INT,
    -> CONSTRAINT chk_id CHECK (id > 0)
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
删除 id 的检查约束
*/
mysql> ALTER TABLE dchk_tb
    -> DROP CHECK chk_id;
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 删除成功
```



###### 字段

​		在删除字段前，要检查与其相关的约束是否完全删除（包括自己的约束与外表对它的外键）。

​		删除字段前最好确认当中数据确实不再需要，且删除了不会造成影响。

​		如果表内只有一个字段，就直接删除表。

​		执行下方语法删除字段。

```mysql
ALTER TABLE <tb>
DROP COLUMN <column1>;
/*
<tb>:删除的表
<column>:删除的字段
*/
```

​		实例：

```mysql
/*
创建含有字段 id、name 的表 dcol_tb
*/
mysql> CREATE TABLE IF NOT EXISTS dcol_tb (
    -> id INT
    -> name VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
删除 name 字段 
*/
mysql> ALTER TABLE dcol_tb
    -> DROP COLUMN name;
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0  -- 删除成功
```



#### 2-2.5 删除

​		表的删除很简单，但是需要注意表的依赖关系。

​		删除表前，我们需要将表之间的依赖关系全部删除。

​		如果删除的表，是与其他表关联的外表，就需要先将其他表对于要删除的表的外键删除，不然表无法删除。

##### 正常删除

​		删除表的操作是不可逆的，只要删除，表内所有的数据都会消失。

​		执行下方语法删除表

```mysql
DROP TABLE <tb>;
/*
<tb>:删除的表
*/
```

​		实例：

```mysql
/*
创建表 drop_tb
*/
mysql> CREATE TABLE IF NOT EXISTS drop_tb (
    -> id INT
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
删除表 drop_tb
*/
mysql> DROP TABLE drop_tb;
Query OK, 0 rows affected (0.04 sec)  -- 删除成功
```



##### 错误删除

​		删除不存在的表，MySQL 会报错。

​		实例：

```mysql
/*
删除不存在的表 drop_tb
*/
mysql> DROP TABLE drop_tb;
ERROR 1051 (42S02): Unknown table 'tb_test.drop_tb'  -- 报错
```

​		为了避免报错，执行下方语法删除表

```mysql
DROP TABLE IF EXISTS <tb>;
/*
<tb>:删除的表
*/
```

​		实例：

```mysql
/*
删除不存在的表 drop_tb
*/
mysql> DROP TABLE IF EXISTS drop_tb;
Query OK, 0 rows affected, 1 warning (0.03 sec)  -- 没有报错，只有警告
```



## 三、运算符

​		MySQL 支持多种运算符，用于在操作中进行数学运算、逻辑判断、位操作等。

​		运算符根据作用分为三类：

| 运算符种类 | 作用                   |
| :--------: | ---------------------- |
| 算术运算符 | 对数值类型进行数学计算 |
| 比较运算符 | 进行比较               |
| 逻辑运算符 | 组合或修改布尔表达式   |

​		下方是使用运算符并查询返回结果的语法

```mysql
SELECT <expression>;
/*
<expression>:使用运算符的表达式
*/
```

#### 3-0 布尔表达式

##### 定义

​		布尔表达式是用于计算并返回真值的表达式。

​		布尔表达式是控制程序流程、过滤数据、定义逻辑规则的核心工具。



##### 真值

​		布尔表达式的返回值称为真值。

​		真值只有两个取值：真（True）与假（False）

​		非 0 值视为真（True），0 值与 Null 视为假（False）。



##### 组成

​		布尔表达式由操作数（Operands）与操作符（Operators）两部分组成。

|  组成  | 含义                             |
| :----: | -------------------------------- |
| 操作数 | 参与运算的变量、常量或函数返回值 |
| 操作符 | 连接操作数的符号，决定运算逻辑   |



#### 		3-1 算术运算符

​		算术运算符是以数值类型为操作数的运算符。

​		MySQL  支持基础的加减乘除等运算符，即 MySQL 能够充当简单的计算器使用。

​		所有的算术运算符遇到 Null 值其结果都为 Null。

​		下方是 MySQL 支持的算术运算符：

| 算术运算符 | 作用     |      |
| :--------: | -------- | ---- |
|     +      | 加法运算 |      |
|     -      | 减法运算 |      |
|     *      | 乘法运算 |      |
|     /      | 除法运算 |      |
|     %      | 取模运算 |      |
|     -      | 取反运算 |      |
|    DIV     | 整除运算 |      |



##### 		3-1.1 运算优先级

​		运算符优先级决定了计算顺序（从高到低）：

1.  括号 ()：强制改变优先级，括号内的优先级更高 。
2.  单目负号 -：如 -5。
3.  乘法 \、除法 /、整除 DIV、取模 %。
4.  加法 +、减法 -。

##### 3-1.2 使用

​		在 MySQL 里，只要是字段为数值类型的都能使用算术运算符进行计算。

​		字段使用算术运算符的语法与常数使用算术运算符的语法一样，所以可以使用算术运算符操作常数的语法理解算术运算符如何操作数值类型的字段。

-   **+（加法）**

​		+ 为二元运算符，即需要两个操作数来进行运算。

​		使用 + 会将两个操作数相加。

​		实例：

```mysql
/*
计算 1 + 1.1 的值
*/
mysql> SELECT 1 + 1.1;
+---------+
| 1 + 1.1 |  -- 计算表达式
+---------+
|     2.1 |  -- 计算结果
+---------+
1 row in set (0.00 sec)
```

-   **-（减法）**

​		 - 为二元运算符，即需要两个操作数来进行运算。

​		使用 - 会用前一个操作数减去后一个操作数。

​		实例：

```mysql
/*
计算 2.13 - 0.22
*/
mysql> SELECT 2.13 - 0.22;
+------------+
| 2.13 - 0.22 |
+------------+
|       1.91 |
+------------+
1 row in set (0.00 sec)
```

-   ***（乘法）**

​		* 为二元运算符，即需要两个操作数来进行运算。

​		使用 * 会将两个操作数相乘。

​		实例：

```mysql
/*
计算 2 * 4.33
*/
mysql> SELECT 2 * 4.33;
+--------+
| 2 * 4.33|
+--------+
|   8.66 |
+--------+
1 row in set (0.00 sec)
```

-   **/（除法）**

​		**/** 为二元运算符，即需要两个操作数来进行运算。

​		使用 **/** 会用前一个操作数除以够一个操作数，返回一个浮点数类型。

​		如果后一个操作数为 0，结果为 Null。

​		实例：

```mysql
/*
计算 7 / 4.33
*/
mysql> SELECT 7 / 4.33;
+----------+
| 7 / 4.33 |
+----------+
|   1.6166 |
+----------+
1 row in set (0.00 sec)

/*
计算 7 / 0
*/
mysql> SELECT 7 / 0;
+-------+
| 7 / 0 |
+-------+
|  NULL |  -- 结果为 NULL
+-------+
1 row in set, 1 warning (0.00 sec)
```

-   **DIV（整除）**

​		DIV 为二元运算符，即需要两个操作数来进行运算。

​		使用 DIV 会用前一个操作数整除后一个操作数。

​		如果后一个操作数为 0，结果为 Null。

​		实例：

```mysql
/*
计算 7 整除 3
*/
mysql> SELECT 7 DIV 3;
+---------+
| 7 DIV 3 |
+---------+
|       2 |
+---------+
1 row in set (0.00 sec)

/*
计算 7 DIV Null
*/
mysql> SELECT 7 DIV Null;
+------------+
| 7 DIV Null |
+------------+
|       NULL |  -- 结果为 NULL
+------------+
1 row in set (0.00 sec)
```

-   **%（取模）**

​		% 为二元运算符，即需要两个操作数来进行运算。

​		使用 % 会用前一个操作数对后一个操作数取模。

​		如果后一个操作数为 0，结果为 Null。

​		实例：

```mysql
/*
计算 7 对 3 取模
*/
mysql> SELECT 7 % 3;
+-------+
| 7 % 3 |
+-------+
|     1 |
+-------+
1 row in set (0.00 sec)

/*
计算 7 对 0 取模
*/
mysql> SELECT 7 % 0;
+-------+
| 7 % 0 |
+-------+
|  NULL |  -- 结果为 Null
+-------+
1 row in set, 1 warning (0.00 sec)
```

-   **-（取反）**

​		- 为一元运算符，即只需要一个操作数来进行运算。

​		使用 - 会将该操作数的符号取反。

​		实例：

```mysql
/%
对 -7 取反
%/
mysql> SELECT - -7 ;
+------+
| - -7 |
+------+
|    7 |
+------+
1 row in set (0.00 sec)
```



##### 3-1.3 类型转换

​		数值的字符串格式能够正确被 MySQL 识别为数值，非数值字符串会被转换为 0。

​		实例：

```mysql
/*
计算 13 + '12'
*/
mysql> SELECT 13 + '12';
+-----------+
| 13 + '12' |
+-----------+
|        25 |
+-----------+
1 row in set (0.00 sec)

/*
计算 12 + 'a'
*/
mysql> SELECT 12 + 'a';
+----------+
| 12 + 'a' |
+----------+
|       12 |
+----------+
1 row in set, 1 warning (0.00 sec)
```



#### 3-2 比较运算符

​		MySQL 中的比较运算符用于比较两个表达式（可以为常数、变量、函数返回值以及另一个表达式），并返回布尔值（TRUE、FALSE或UNKNOWN）。

​		所有比较运算符遇到 Null，返回的值都为 Null。

​		由比较运算符连接的两个表达式就是一个典型的布尔表达式。

​		下方是 MySQL 提供的比较运算符：

|   比较运算符   | 作用                   |
| :------------: | ---------------------- |
| 基本比较运算符 | 进行基本的比较         |
| 范围检查运算符 | 检查值是否处于某一范围 |
| 集合检查运算符 | 检查值是否处于某一集合 |
| 模式匹配运算符 | 使用指定文本匹配字符串 |

​		下方是使用比较运算符可以返回的值：

| 返回结果 | 含义                     |
| :------: | ------------------------ |
|    1     | True，即比较的逻辑正确   |
|    0     | False，即比较的逻辑错误  |
|   NULL   | Unknow，即比较的逻辑未知 |

##### 		3-2.1 基本比较

​		基本比较运算符可以比较数值、字符串以及日期时间。

​		基本比较运算符包含下方五种：

|    算术运算符     |                             作用                             |
| :---------------: | :----------------------------------------------------------: |
|         >         | 大于运算符，判断前一个值是否大于后一个值，大于返回 1，小于返回 0 |
|         <         | 小于运算符，判断前一个值是否大于后一个值，大于返回 1，小于返回 0 |
|     <>（!=）      | 不等运算符，判断前一个值是否不等后一个值，不等于返回 1，等于返回 0 |
|         =         | 等于运算符，判断前一个值是否等于后一个值，等于返回 1，不等于返回 0 |
| **IS [NOT] NULL** | 比较空值，判断数值是否为 Null，是返回 1，不是返回 0，加上 NOT 反之 |

###### 比较规则

​		比较数值时，只需注意比较支持类型转换，即字符串格式的数值也能被正常比较。

​		比较字符串时，会依次从第一个字符开始进行比较，比较的是字符的 ASCLL 码（每一个字符会拥有一个 ASCLL 码，A-Z的 ASCLL 码依次增加）。

​		MySQL 根据字段的字符集和排序规则，将字符串转换为 ASCLL码 后按字典顺序比较。

​		比较日期时间时，会比较时间的早与晚，大于代表晚于另一时间，小于代表早于另一时间。

​		日期时间的比较必须是同样格式的，如果是年月日就只能比较年月日。

​		只能使用 IS NULL 或 IS NOT NULL 来比较空值。



###### 使用

​		根据比较规则进行使用。

-   **数值比较**

​		实例：

```mysql
/*
使用 >
*/
mysql> SELECT 1 > 2;
+-------+
| 1 > 2 |  -- 比较表达式
+-------+
|     0 |  -- 比较结果
+-------+
1 row in set (0.00 sec)

/*
使用 <
*/
mysql> SELECT 1 < 2.22;
+----------+
| 1 < 2.22 |
+----------+
|        1 |
+----------+
1 row in set (0.00 sec)

/*
使用 <>（!=）
*/
mysql> SELECT 1 <> 2.22;
+-----------+
| 1 <> 2.22 |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)


/*
使用 =
*/
mysql> SELECT 1 = 2.22;
+----------+
| 1 = 2.22 |
+----------+
|        0 |
+----------+
1 row in set (0.00 sec)


/*
比较数值与字符串的数值
*/
mysql> SELECT 1 = '2.22';
+------------+
| 1 = '2.22' |
+------------+
|          0 |
+------------+
1 row in set (0.00 sec)

mysql> SELECT 1 = '1';
+---------+
| 1 = '1' |
+---------+
|       1 |
+---------+
1 row in set (0.00 sec)
```

-   **字符串比较**

​		实例：

```mysql
/*
比较字符串
*/
mysql> SELECT 'a' > 'b';
+-----------+
| 'a' > 'b' |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)

mysql> SELECT 'a' < 'b';
+-----------+
| 'a' < 'b' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)

mysql> SELECT 'ab' < 'baa';  -- 第一位小于就不往后比较
+--------------+
| 'ab' < 'baa' |
+--------------+
|            1 |
+--------------+
1 row in set (0.00 sec)

mysql> SELECT 'a' = 'A';
+-----------+
| 'a' = 'A' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

-   **日期时间比较**

​		实例：

```mysql
/*
比较日期时间
*/
mysql> SELECT '2014-11-12' < '2013-2-4';
+---------------------------+
| '2014-11-12' < '2013-2-4' |
+---------------------------+
|                         0 |
+---------------------------+
1 row in set (0.00 sec)

mysql> SELECT '2014-11-12' < '2015-2-4';
+---------------------------+
| '2014-11-12' < '2015-2-4' |
+---------------------------+
|                         1 |
+---------------------------+
1 row in set (0.00 sec)
```

-   **空值比较**

​		实例：

```mysql
/*
非空值与空值比较
*/
mysql> SELECT 1 < Null;
+----------+
| 1 < Null |
+----------+
|     NULL |
+----------+
1 row in set (0.00 sec)

mysql> SELECT 'a' < Null;
+------------+
| 'a' < Null |
+------------+
|       NULL |
+------------+
1 row in set (0.00 sec)

mysql> SELECT '2014-11-12' < Null;
+---------------------+
| '2014-11-12' < Null |
+---------------------+
|                NULL |
+---------------------+
1 row in set (0.00 sec)


/*
进行空值比较
*/
mysql> SELECT null IS NULL;
+--------------+
| null IS NULL |
+--------------+
|            1 |
+--------------+
1 row in set (0.00 sec)

mysql> SELECT null IS NOT NULL;
+------------------+
| null IS NOT NULL |
+------------------+
|                0 |
+------------------+
1 row in set (0.00 sec)

mysql> SELECT 1 IS NULL;
+-----------+
| 1 IS NULL |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)

mysql> SELECT 1 IS NOT NULL;
+---------------+
| 1 IS NOT NULL |
+---------------+
|             1 |
+---------------+
1 row in set (0.00 sec)
```



##### 3-2.2 范围检查

​		在 MySQL 中，范围检查主要用于判断值是否落在指定区间（闭区间）内，可以是字符串、数值、日期时间。

​		下面对值进行范围检查的基本语法

```mysql
<expression> BETWEEN <min> AND <max>;
/*
<expression>:表达式
<min>:表达式的最小值
<max>:表达式的最大值
*
```

​		下方是范围检查能够返回的结果：

| 返回值 | 含义                               |
| :----: | :--------------------------------- |
|   1    | True，即检查值在范围里             |
|   0    | False，即检查值不在范围里。        |
|  NULL  | Unknow，即未知检查值在不在范围里。 |



###### 检查规则

​		检查数值，即检查是否其在最大值与最小值之间，不会注意精确值，但最大值、最小值需要都是数值。

​		检查日期时间，即检查是否在给定的两个日期时间之间，但需要检查的日期时间与最大值、最小值的格式一致。

​		例如，检查年月日就设置年月日的最大值与最小值，不然没有比较意义。

​		检查字符串，即检查对应字符串的 ASCLL 码是否在其最大值与最小值之间，但是这个检查不会对字符串的个数进行限制。

​		MySQL 根据字段的字符集和排序规则，将字符串转换为 ASCLL码 后按字典顺序进行检查。

​		例如，aaa 在 a 与 b 之间，因为 aaa 的第一个字符 a 在 a 与 b 之间，而 aab 在 aaaaa 与 aabaa 之间，因为前两个字符一样，而第三个字符 b 正在 a 与 b 之间，虽然 aab 只有三位，而检查范围为5位。

​		即字符串的范围检查规则为：不同字符个数的字符串进行比较时，只比较到较少字符个数的字符串，而每个对应顺序的字符串比较遵循字符的 ASCLL 码。

​		加上 NOT 可以取反，即不包含在范围里。



###### 使用

​		根据检查规则使用范围检查

-   **数值检查**

​		实例：

```mysql
/*
对数值使用范围检查
*/
mysql> SELECT 3 BETWEEN 1 AND 10;
+--------------------+
| 3 BETWEEN 1 AND 10 |  -- 检查表达式
+--------------------+
|                  1 |  -- 检查结果
+--------------------+
1 row in set (0.00 sec)

mysql> SELECT 3 BETWEEN 1 AND NUll;
+----------------------+
| 3 BETWEEN 1 AND NUll |
+----------------------+
|                 NULL |  -- 结果为 NULL
+----------------------+
1 row in set (0.00 sec)
```

-   **日期时间检查**

​		实例：

```mysql
/*
对日期时间使用范围检查
*/
mysql> SELECT '2011-11-12' BETWEEN '2002-2-11' and '2019-2-11';
+--------------------------------------------------+
| '2011-11-12' BETWEEN '2002-2-11' and '2019-2-11' |
+--------------------------------------------------+
|                                                1 |
+--------------------------------------------------+
1 row in set (0.00 sec)
```

-   **字符串检查**

​		实例：

```mysql
/*
对字符串进行范围检查
*/
mysql> SELECT 'aabb' BETWEEN 'aaaaaa' and 'aabaa';
+-------------------------------------+
| 'aabb' BETWEEN 'aaaaaa' and 'aabaa' |
+-------------------------------------+
|                                   0 |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'aabb' BETWEEN 'aaaaaa' and 'aabba';
+-------------------------------------+
| 'aabb' BETWEEN 'aaaaaa' and 'aabba' |
+-------------------------------------+
|                                   1 |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'aa' BETWEEN 'a' and 'b';
+--------------------------+
| 'aa' BETWEEN 'a' and 'b' |
+--------------------------+
|                        1 |
+--------------------------+
```



##### 3-2.3 集合检查

​		在 MySQL 中，集合检查主要用于判断值是否属于指定集合中的元素，可以是字符串、数值、日期时间。

​		集合约束包含 Null 仍可以进行检查。

​		下方是对值进行集合检查的基本语法

```mysql
<expression> IN (<value1>,<value2>,<value3>);
/*
<expression>:表达式
<value>:检查的值
*/
```

​		下方是集合检查能够返回的结果：

| 返回结果 | 含义                             |
| -------- | -------------------------------- |
| 1        | True，即检查值在指定集合里       |
| 0        | False，即检查值不在集合里        |
| NULL     | Unknow，即未知检查值在不在集合里 |

###### 使用

​		实例：

```mysql
/*
对数值、字符串与日期时间使用集合检查
*/
mysql> SELECT 1 in (0,2,1,4,5,6,2);
+----------------------+
| 1 in (0,2,1,4,5,6,2) |  -- 检查表达式
+----------------------+
|                    1 |  -- 检查结果
+----------------------+
1 row in set (0.00 sec)

mysql> SELECT 1 in (0,2,1,4,5,6,Null);  -- 包含 Null
+-------------------------+
| 1 in (0,2,1,4,5,6,Null) |
+-------------------------+
|                       1 |  -- 仍可以检查
+-------------------------+
1 row in set (0.00 sec)

mysql> SELECT '2022-11-11' in ('2111-11-11','2012-12-11','2022-11-11');
+----------------------------------------------------------+
| '2022-11-11' in ('2111-11-11','2012-12-11','2022-11-11') |
+----------------------------------------------------------+
|                                                        1 |
+----------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'aa' in ('aa','ss','ad','asdc');
+---------------------------------+
| 'aa' in ('aa','ss','ad','asdc') |
+---------------------------------+
|                               1 |
+---------------------------------+
1 row in set (0.00 sec)
```



##### 3-2.4 模式匹配

​		在 MySQL 中，模式匹配用于根据特定规则筛选字符串数据。

​		模式匹配基于通配符。

>   通配符
>
>   通配符指可以替代其他字符的符号。

​		模式匹配分为简单匹配与正则匹配，正则匹配可以控制更精细的匹配条件。

​		模式匹配不会区分字符串的大小写。

​		下面是模式匹配能够返回的结果：

| 返回值 | 含义                |
| :----: | :------------------ |
|   1    | True，即匹配成功    |
|   0    | False，即匹配不成功 |

​		

###### 简单匹配

​		简单匹配可以分为三类：

| 匹配类型 | 作用                                   |
| -------- | -------------------------------------- |
| 前缀匹配 | 匹配的字符串在所要进行匹配的字符的前方 |
| 后缀匹配 | 匹配的字符串在所要进行匹配的字符的后方 |
| 中间匹配 | 匹配的字符串在所要进行匹配的字符的中间 |

​		使用下方语法进行简单匹配并查询匹配的结果

```mysql
SELECT <match_str> LIKE <format_str>
/*
<match_str>:待匹配字符串
<format_str>:匹配的字符串格式
*/
```

​		下方是简单匹配能够使用到的通配符：

| 通配符 | 含义                             |
| :----: | :------------------------------- |
|   %    | 匹配任意多个字符（包括零个字符） |
|   _    | 匹配任意一个字符                 |

​		实例：
```mysql
/*
使用通配符实现前缀匹配
*/
mysql> SELECT 'I love you' LIKE 'I Lov%';
+----------------------------+
| 'I love you' LIKE 'I Lov%' |  -- 匹配表达式
+----------------------------+
|                          1 |  -- 匹配结果
+----------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' LIKE 'I Lov_';
+----------------------------+
| 'I love you' LIKE 'I Lov_' |
+----------------------------+
|                          0 |
+----------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' LIKE 'I Lov_____';
+--------------------------------+
| 'I love you' LIKE 'I Lov_____' |
+--------------------------------+
|                              1 |
+--------------------------------+
1 row in set (0.00 sec)


/*
使用通配符实现后缀匹配
*/
mysql> SELECT 'I love you' LIKE '%you';
+--------------------------+
| 'I love you' LIKE '%you' |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' LIKE '__you';  -- 前面只有两个字符，不匹配
+---------------------------+
| 'I love you' LIKE '__you' |
+---------------------------+
|                         0 |
+---------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' LIKE '_______you';
+--------------------------------+
| 'I love you' LIKE '_______you' |
+--------------------------------+
|                              1 |
+--------------------------------+
1 row in set (0.00 sec)


/*
使用通配符实现中间匹配
*/
mysql> SELECT 'I love you' LIKE '%love%';
+----------------------------+
| 'I love you' LIKE '%love%' |
+----------------------------+
|                          1 |
+----------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' LIKE '__love___';
+-------------------------------+
| 'I love you' LIKE '__love___' |
+-------------------------------+
|                             0 |
+-------------------------------+
1 row in set (0.00 sec
```



###### 正则匹配

​		正则匹配能够实现精确的匹配依赖于其通配符。

​		正则匹配不区分字符串的大小写。

​		下方是正则匹配能够使用的通配符：

| **通配符** | **作用**                           |
| :--------: | :--------------------------------- |
|     .      | 匹配任意单个字符（除换行符）       |
|     ^      | 匹配字符串开头                     |
|     $      | 匹配字符串结尾                     |
|   [abc]    | 匹配字符 a、b 或 c                 |
|   [a-z]    | 匹配任意小写字母                   |
|   [0-9]    | 匹配任意数字                       |
|     *      | 匹配前一个字符零次或多次           |
|     +      | 匹配前一个字符一次或多次           |
|    {n}     | 匹配前一个字符恰好 n 次            |
|   {n,m}    | 匹配前一个字符至少 n 次，至多 m 次 |

​		使用下方语法进行正则匹配并查询匹配的结果

```mysql
SELECT <match_str> RLIKE <format_str>
/*
<match_str>:待匹配字符串
<format_str>:匹配的字符串格式
*/
```

​		实例：

```mysql
/*
使用正则匹配
*/
mysql> SELECT 'I love you' RLIKE '.......you';
+---------------------------------+
| 'I love you' RLIKE '.......you' |
+---------------------------------+
|                               1 |
+---------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' RLIKE '^I';
+-------------------------+
| 'I love you' RLIKE '^I' |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' RLIKE 'you$';
+---------------------------+
| 'I love you' RLIKE 'you$' |
+---------------------------+
|                         1 |
+---------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' RLIKE 'I [a-z]ove you';
+-------------------------------------+
| 'I love you' RLIKE 'I [a-z]ove you' |
+-------------------------------------+
|                                   1 |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love you' RLIKE 'I [mln]ove you';
+-------------------------------------+
| 'I love you' RLIKE 'I [mln]ove you' |
+-------------------------------------+
|                                   1 |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love youuuuu' RLIKE 'I love you*';
+--------------------------------------+
| 'I love youuuuu' RLIKE 'I love you*' |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love youuuuu' RLIKE 'I love you+';
+--------------------------------------+
| 'I love youuuuu' RLIKE 'I love you+' |
+--------------------------------------+
|                                    1 |
+--------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love youuuuu' RLIKE 'I love you{5}';
+----------------------------------------+
| 'I love youuuuu' RLIKE 'I love you{5}' |
+----------------------------------------+
|                                      1 |
+----------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT 'I love youuuuu' RLIKE 'I love you{5,10}';
+-------------------------------------------+
| 'I love youuuuu' RLIKE 'I love you{5,10}' |
+-------------------------------------------+
|                                         1 |
+-------------------------------------------+
1 row in set (0.00 sec)
```



#### 3-3 逻辑运算符

​		MySQL 的逻辑运算符用于组合或修改条件的逻辑结果。

​		下方是 MySQL 的逻辑运算符种类。

| 运算符 | 作用                           |
| :----: | :----------------------------- |
|  AND   | 与，两条件都为真时，返回真     |
|   OR   | 或，两条件只要一个为真，返回真 |
|  NOT   | 非，对于一个条件取它的真值的反 |

​		下方是逻辑运算返回能够返回的值：

| 返回值 | 含义               |
| :----: | :----------------- |
|   1    | True，即逻辑为真   |
|   0    | False，即逻辑为假  |
|  NULL  | Unknow，即逻辑未知 |

##### 3-3.1 逻辑与

​		逻辑与仅当所有条件为 TRUE 时返回 TRUE，否则返回 FALSE，若含 NULL，则按三值逻辑处理。

​		下方是进行逻辑与运算的语法：

```mysql
<condition1> AND <condition2>
/*
<condition>:条件
*/
```

​		下方是进行逻辑与运算返回结果遵循规则：

| 条件1 | 条件2 | 返回结果 |
| :---: | :---: | :------: |
| TRUE  | TRUE  |   TRUE   |
| TRUE  | FALSE |  FALSE   |
| TRUE  | NULL  |   NULL   |
| FALSE | NULL  |  FALSE   |
| NULL  | NULL  |   NULL   |

​		实例：

```mysql
/*
使用逻辑与运算
*/
mysql> SELECT 2 > 1 AND 5;
+-------------+
| 2 > 1 AND 5 |
+-------------+
|           1 |
+-------------+
1 row in set (0.00 sec)

mysql> SELECT 2 < 1 AND 5;
+-------------+
| 2 < 1 AND 5 |
+-------------+
|           0 |
+-------------+
1 row in set (0.00 sec)

mysql> SELECT Null AND 1;
+------------+
| Null AND 1 |
+------------+
|       NULL |
+------------+
1 row in set (0.00 sec)

mysql> SELECT Null AND Null;
+---------------+
| Null AND Null |
+---------------+
|          NULL |
+---------------+
1 row in set (0.00 sec)

mysql> SELECT Null AND 1 > 2;
+----------------+
| Null AND 1 > 2 |
+----------------+
|              0 |
+----------------+
1 row in set (0.00 sec)
```



##### 3-3.2 逻辑或

​		任一条件为 TRUE 时返回 TRUE，否则返回 FALSE，若含 NULL，则按三值逻辑处理。

​		下方是进行逻辑或运算的语法：

```mysql
<condition1> OR <condition2>
/*
<condition>:条件
*/
```

​		下方是进行逻辑或运算返回结果遵循规则：

| 条件1 | 条件2 | 返回结果 |
| :---: | :---: | :------: |
| FALSE | FALSE |  FALSE   |
| FALSE | TRUE  |   TRUE   |
| FALSE | NULL  |   NULL   |
| TRUE  | NULL  |   TRUE   |
| NULL  | NULL  |   NULL   |

​		实例：

```mysql
/*
使用逻辑或运算
*/
mysql> SELECT 1 > 2 OR 1 > 2;
+----------------+
| 1 > 2 OR 1 > 2 |
+----------------+
|              0 |
+----------------+
1 row in set (0.00 sec)

mysql> SELECT 1 > 2 OR 1 < 2;
+----------------+
| 1 > 2 OR 1 < 2 |
+----------------+
|              1 |
+----------------+
1 row in set (0.00 sec)

mysql> SELECT 1 > 2 OR Null;
+---------------+
| 1 > 2 OR Null |
+---------------+
|          NULL |
+---------------+
1 row in set (0.00 sec)

mysql> SELECT 1 < 2 OR Null;
+---------------+
| 1 < 2 OR Null |
+---------------+
|             1 |
+---------------+
1 row in set (0.00 sec)

mysql> SELECT Null OR Null;
+--------------+
| Null OR Null |
+--------------+
|         NULL |
+--------------+
1 row in set (0.00 sec)
```



##### 3-3.3 逻辑非

​		反转条件的布尔值，若条件为 NULL，结果仍为 NULL。

​		下方是进行逻辑非运算的语法：
```mysql
NOT <condition1>
/*
<condition>:条件
*/
```

​		下方是进行逻辑非运算返回结果遵循规则：

| 条件  | 返回结果 |
| :---: | :------: |
| TRUE  |  FALSE   |
| FALSE |   TRUE   |
| NULL  |   NULL   |

​		实例：

```mysql
/*
使用逻辑非
*/
mysql> SELECT NOT 1 > 2;
+-----------+
| NOT 1 > 2 |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)

mysql> SELECT NOT 1 < 2;
+-----------+
| NOT 1 < 2 |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)

mysql> SELECT NOT Null;
+----------+
| NOT Null |
+----------+
|     NULL |
+----------+
1 row in set (0.00 sec)
```



##### 3-3.4 优先级

​		对于多个逻辑运算符组合使用，需要注意其执行的优先级。

​		NOT 的优先级最高，其次是 AND，最后是 OR。



##### 3-3.5 短路求值

​		MySQL对逻辑运算符采用短路求值：

| 运算符 | 短路求值                         |
| :----: | -------------------------------- |
|  AND   | 若左条件为 FALSE，右条件不执行。 |
|   OR   | 若左条件为 TRUE，右条件不执行。  |



## 四、基础 DML

​		DML 主要用来对表进行数据的添加、更新与删除，是最常使用的语言。

​		我们会在介绍前，先介绍查询表的每条记录的语法。

​		然后再分为记录的添加、更新、与删除是三部分来进行介绍。

### 4-0 基础

​		在正式了解 DML 之前，首先要了解怎样查询与过滤表内的记录。

​		执行下方语法把记录对应的字段值全部显示

```mysql
SELECT * 
FROM <tb>;
/*
<tb>:查询的表
*/
```

​		执行下方语法过滤记录

```mysql
WHERE <condition1>
/*
<condition>:过滤条件
*/
```

​		过滤条件为布尔表达式，即过滤出满足使该布尔表达式值为 True 的记录。



### 4-1 添加

​		为表内添加记录需要遵循一定的规则，而这会在语法上有一定的体现。

​		前面提到的所有的对字段的设置（数据类型、属性、约束）都会在这里有所体现。

​		我们会分为添加数据类型、属性、约束以及添加顺序四部分来进行对表的添加记录的规范进行介绍。

​		针对与不同的规范，我们添加记录的语法都是一样的。

​		执行

```mysql
INSERT INTO <tb> (<column1>,<column2>,<column3>)
VALUES 
(value11,value12,value13),
(value21,value22,value23),
(value21,value22,value23);
/*
<tb>:添加的表
<column>:字段
<value>:添加的数据
(value,value,value):添加的单条记录
*/
```

​		来添加记录。



#### 4-1.1 数据类型规范

​		我们添加记录需要满足表的每个字段的数据类型，不然无法添加成功。

​		实例：

```mysql
/*
创建一个含有所有类型的表 type_tb
*/
mysql> CREATE TABLE IF NOT EXISTS type_tb (
    -> num1 TINYINT,
    -> num2 SMALLINT,
    -> num3 MEDIUMINT,
    -> num4 INT,
    -> num5 BIGINT,
    -> num6 FLOAT,
    -> num7 DOUBLE,
    -> num8 DECIMAL(10,5),
    -> str1 CHAR(10),
    -> str2 VARCHAR(10),
    -> str3 TINYTEXT,
    -> str4 TEXT,
    -> date1 DATE,
    -> time1 TIME,
    -> datetime1 DATETIME,
    -> enum1 ENUM('red','blue','green'),
    -> set1 SET('a','b','c')
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
给表 type_tb 添加记录
*/
mysql> INSERT INTO type_tb
    -> (num1, num2, num3, num4, num5, num6, num7, num8, str1, str2, str3, str4, date1, time1, datetime1, enum1, set1)
    -> VALUES
    -> (1, 1, 1, 1, 1, 1.1, 1.1111, 131.312, 'a', 'a', 'a', 'a', '2021-11-21', '12:21:21', '2201-12-13 21:21:33', 'red', 'a,b'),  -- 集合以逗号隔开
    -> (2, 2, 2, 2, 2, 2.2, 2.2222, 2.2222, 'b', 'b', 'b', 'b', '2022-12-22', '13:22:22', '2202-12-14 22:22:34', 'green', 'b,c'),
    -> (3, 3, 3, 3, 3, 3.3, 3.3333, 3.3333, 'c', 'c', 'c', 'c', '2023-01-23', '14:23:23', '2203-12-15 23:23:35', 'blue', 'a,c');
Query OK, 3 rows affected (0.03 sec)
Records: 3  Duplicates: 0  Warnings: 0  -- 添加成功

/*
查询表 type_tb 的所有记录
*/
mysql> SELECT * FROM type_tb;
| num1 | num2 | num3 | num4 | num5 | num6 | num7   | num8      | str1 | str2 | str3 | str4 | date1      | time1    | datetime1           | enum1 | set1 |
|    1 |    1 |    1 |    1 |    1 |  1.1 | 1.1111 | 131.31200 | a    | a    | a    | a    | 2021-11-21 | 12:21:21 | 2201-12-13 21:21:33 | red   | a,b  |
|    2 |    2 |    2 |    2 |    2 |  2.2 | 2.2222 |   2.22220 | b    | b    | b    | b    | 2022-12-22 | 13:22:22 | 2202-12-14 22:22:34 | green | b,c  |
|    3 |    3 |    3 |    3 |    3 |  3.3 | 3.3333 |   3.33330 | c    | c    | c    | c    | 2023-01-23 | 14:23:23 | 2203-12-15 23:23:35 | blue  | a,c  |
3 rows in set (0.00 sec)  -- 添加成功
```

​		

#### 4-1.2 属性规范

​		当字段设置了默认值，该字段就可以不指定值，会自动用默认值来填充。

​		而字段默认是可空，且默认值为 Null。这就代表当我们没有设置非空属性，又没有指定默认值，那么不给字段指定值就会用 Null 来当字段值。

​		而当字段属性为非空的话，就必须指定该字段的值，且不能为 Null，但指定了默认值（不是 Null）就不需要。

​		实例：

```mysql
/*
创建表 attr_tb 来检验属性的规范
*/
mysql> CREATE TABLE IF NOT EXISTS attr_tb (
    -> id INT NOT Null DEFAULT 13,
    -> class INT,
    -> name VARCHAR(20) NOT Null
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
不指定 id 与 class 字段的值
*/
mysql> INSERT INTO attr_tb
    -> (name)
    -> VALUES
    -> ('TOM');
Query OK, 1 row affected (0.03 sec)  -- 添加成功

/*
不指定 name 字段的值
*/
mysql> INSERT INTO attr_tb
    -> (id,class)
    -> VALUES
    -> (14,15);
ERROR 1364 (HY000): Field 'name' doesn't have a default value  -- 添加失败

/*
查询表 attr_tb 的记录
*/
mysql> SELECT * FROM attr_tb;
+----+-------+------+
| id | class | name |
+----+-------+------+
| 13 |  Null | TOM  |
+----+-------+------+
1 row in set (0.00 sec)
```



#### 4-1.3 约束规范

​		由于每个约束都有特性，所以添加记录时要遵循约束的规范

-   主键约束规范

​		主键约束有两个要求：非空与唯一。

​		所以添加主键字段的数据时不能重复且不能为空。

​		实例：

```mysql
/*
创建表 pk_tb1 并设置 id 字段为主键
*/
mysql> CREATE TABLE IF NOT EXISTS pk_tb1 (
    -> id INT PRIMARY KEY
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
测试非空
*/
mysql> INSERT INTO pk_tb1
    -> (id)
    -> VALUES
    -> (Null);
ERROR 1048 (23000): Column 'id' cannot be Null  -- 不能添加

/*
测试唯一
*/
mysql> INSERT INTO pk_tb1
    -> (id)
    -> VALUES
    -> (1),
    -> (1);
ERROR 1062 (23000): Duplicate entry '1' for key 'pk_tb1.PRIMARY'  -- 不能添加

/*
正常添加
*/
mysql> INSERT INTO pk_tb1
    -> (id)
    -> VALUES
    -> (1),
    -> (2);
Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0  -- 添加成功
```

-   外键约束规范

​		字段通过建立外键约束连接到外表，当外表没有该条记录对应的外键字段的值，是无法添加记录的。

​		实例：

```mysql
/*
创建外表 fk_tb4 并指定字段 id 为主键
*/
mysql> CREATE TABLE IF NOT EXISTS fk_tb4 (
    -> id INT PRIMARY KEY
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
创建表 mytb_14 并将字段 id 外联到 fk_tb4 的id 字段
*/
mysql> CREATE TABLE IF NOT EXISTS mytb_14 (
    -> id INT,
    -> CONSTRAINT FOREIGN KEY (id) REFERENCES fk_tb4 (id)
    -> );
Query OK, 0 rows affected (0.06 sec)

/*
在外表没有 id 为 1 的记录时给 mytb_14 添加 id 为 1 的字段
*/
mysql> INSERT INTO mytb_14
    -> (id)
    -> VALUES
    -> (1);
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`tb_test`.`mytb_14`, CONSTRAINT `mytb_14_ibfk_1` FOREIGN KEY (`id`) REFERENCES `fk_tb4` (`id`))  -- 无法添加

/*
先给外表添加 1 的 id 再给 mytb_14 添加 1 的id
*/
mysql> INSERT INTO fk_tb4
    -> (id)
    -> VALUES
    -> (1);
Query OK, 1 row affected (0.03 sec)

mysql> INSERT INTO mytb_14
    -> (id)
    -> VALUES
    -> (1);
Query OK, 1 row affected (0.03 sec)  -- 添加成功
```

-   唯一值约束规范

​		唯一值约束限制不能添加重复的值。

```mysql
/*
创建字段 id 为唯一值的表 test_uni_tb
*/
mysql> CREATE TABLE IF NOT EXISTS test_uni_tb (
    -> id INT,
    -> CONSTRAINT uni_id UNIQUE (id)
    -> );
Query OK, 0 rows affected (0.05 sec)

/*
添加两个 id 为 1 的记录
*/
mysql> INSERT INTO test_uni_tb
    -> (id)
    -> VALUES
    -> (1),
    -> (1);
ERROR 1062 (23000): Duplicate entry '1' for key 'test_uni_tb.uni_id'  -- 添加失败

/*
添加 id 分别为 1,2 的记录
*/
mysql> INSERT INTO test_uni_tb
    -> (id)
    -> VALUES
    -> (1),
    -> (2);
Query OK, 2 rows affected (0.03 sec)
Records: 2  Duplicates: 0  Warnings: 0  -- 添加成
```

-   检查约束规范

​		当添加的记录不符合检查条件时，就不能成功添加数据。

```mysql
/*
创建字段 age 不能小于 18 的表 test_chk_tb
*/
mysql> CREATE TABLE IF NOT EXISTS test_chk_tb (
    -> age INT,
    -> CONSTRAINT check_age CHECK (age > 18)
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
添加 age < 18 的记录
*/
mysql> INSERT INTO test_chk_tb
    -> (age)
    -> VALUES
    -> (11);
ERROR 3819 (HY000): Check constraint 'check_age' is violated.  -- 添加失败

/*
添加 age > 18 的记录
*/
mysql> INSERT INTO test_chk_tb
    -> (age)
    -> VALUES
    -> (22);
Query OK, 1 row affected (0.01 sec)  -- 添加成功
```



#### 4-1.4 顺序问题

​		添加记录时可以不按顺序来添加，只需要将前面指定的字段变换一下。

​		执行下方语法以自定义的字段顺序添加记录。

```mysql
INSERT INTO <tb>
(<column1>,<column3>,<column2>)
VALUES
(<value11>,<value13>,<value12>),
(<value21>,<value23>,<value22>),
(<value31>,<value33>,<value32>);
/*
<tb>:添加的表
<column>:字段
<value>:添加的数据
(value,value,value):添加的单条记录
*/
```



### 4-2 更新

​		更新是指对表内的记录进行更改。

​		更新需要遵循添加记录时需要遵循的规范。

​		结合过滤语法与运算符，执行下方语法更新表中特定的记录

```mysql
UPDATE <tb>
SET <column1> = <new_value>
WHERE <condition1>
/*
<tb>:更新的表
<column>:更新的字段
<new_value>:更新的值
<condition>:过滤条件（没有代表全部更新）
*/
```

​		实例：

```mysql
/*
创建含有字段 id 与 name 的表 update_tb
*/
mysql> CREATE TABLE IF NOT EXISTS update_tb (
    -> id INT,
    -> name VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
添加几条记录
*/
mysql> INSERT INTO update_tb
    -> (id,name)
    -> VALUEs
    -> (1,'TOM'),
    -> (2,'AMY'),
    -> (3,'David');
Query OK, 3 rows affected (0.01 sec)
Records: 3  Duplicates: 0  Warnings: 0

/*
更新 name 为 AMY 与 TOM 的值为 Amy 与 Tom
*/
mysql> UPDATE update_tb
    -> SET name = 'Amy'
    -> WHERE name = 'AMY';
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> UPDATE update_tb
    -> SET name = 'Tom'
    -> WHERE name = 'TOM';
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

/*
更新所有记录的 id 为 1
*/
mysql> UPDATE update_tb
    -> SET id = '1';
Query OK, 2 rows affected (0.01 sec)
Rows matched: 3  Changed: 2  Warnings: 0

/*
查询是否更新成功
*/
mysql> SELECT * FROM update_tb;
+------+-------+
| id   | name  |
+------+-------+
|    1 | Tom   |  -- 更新成功
|    1 | Amy   |
|    1 | David |
+------+-------+
3 rows in set (0.00 sec)
```

​		



### 4-3 删除

​		删除与更新类似，需要结合过滤语句对特定记录进行删除。

​		执行下方语句删除表中特定的记录

```mysql
DELETE FROM <tb>
WHERE <condition1>
/*
<tb>:删除的表
<condition>:过滤条件（没有代表全部删除）
*/
```

​		实例：

```mysql
/*
创建含有字段 id 与 name 的表 delete_tb
*/
mysql> CREATE TABLE IF NOT EXISTS delete_tb (
    -> id INT,
    -> name VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.02 sec)

/*
添加几条记录
*/
mysql> INSERT INTO delete_tb
    -> (id,name)
    -> VALUES
    -> (1,'Tom'),
    -> (2,'Amy'),
    -> (3,'David'),
    -> (4,'Frank');
Query OK, 4 rows affected (0.03 sec)
Records: 4  Duplicates: 0  Warnings: 0

/*
删除 name 为 Amy 的记录
*/
mysql> DELETE FROM delete_tb
    -> WHERE name = 'Amy';
Query OK, 1 row affected (0.01 sec)

/*
查询是否删除
*/
mysql> SELECT * FROM delete_tb;
+------+-------+
| id   | name  |
+------+-------+
|    1 | Tom   |  -- 删除成功
|    3 | David |
|    4 | Frank |
+------+-------+
3 rows in set (0.00 sec)

/*
删除所有记录
*/
mysql> DELETE FROM delete_tb;\
Query OK, 3 rows affected (0.00 sec)

/*
查询是否删除
*/
mysql> SELECT * FROM delete_tb;
Empty set (0.00 sec)  -- 删除成功
```



## 四、基础 DQL

​		DQL 是 MySQL 最核心也是最常使用的功能。

​		DQL 设计单表查询以及多表查询。

### 4-0 SELECT

​		SELECT 语句是 SQL 的核心命令，用于从数据库中检索数据。

​		SELECT 主要用于从表中提取符合条件的数据。



### 4-1 基础查询

​		使用 SELECT 能够查询表中的每条记录的相关数据。

-   **一般查询**

​		执行下方语法能够查询表中记录的对应字段

```mysql
SELECT <column1>,<column2>,<column3>
FROM <tb>;
/*
<column>:查询的字段
<tb>:查询的表
*/
```

​		实例：

```mysql
/*
创建一个含字段 id 与 name 的表 select_tb 并添加数据
*/
mysql> CREATE TABLE IF NOT EXISTS select_tb (
    -> id INT,
    -> name VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO select_tb
    -> (id,name)
    -> VALUES
    -> (1,'Tom'),
    -> (2,'Amy'),
    -> (3,'Candy'),
    -> (4,'Salina');
Query OK, 4 rows affected (0.01 sec)
Records: 4  Duplicates: 0  Warnings: 0

/*
查询表 select_tb 所有记录的 id 字段
*/
mysql> SELECT id
    -> FROM select_tb;
+------+
| id   |  -- 查询成功
+------+
|    1 |
|    2 |
|    3 |
|    4 |
+------+
4 rows in set (0.00 sec)
```

-   **泛查询**

​		泛查询是指查询表中记录的所有字段

​		执行下方语法查看记录的所有字段

```mysql
SELECT *
FROM <tb>;
/*
<tb>:查询的表
*/
```

​		实例：

```mysql
/*
泛查询表 select_tb 记录的所有字段
*/
mysql> SELECT *
    -> FROM select_tb;
+------+--------+
| id   | name   |  -- 查询成功
+------+--------+
|    1 | Tom    |
|    2 | Amy    |
|    3 | Candy  |
|    4 | Salina |
+------+--------+
4 rows in set (0.00 sec)
```



### 4-2 条件过滤

​		大多数情况不需要查询所有记录，所以通过条件过滤来进行筛选记录。

​		条件是个布尔表达式，只有使这个布尔表达式为真的记录，才能被查询到。

​		在过滤记录时可以使用到所有运算符。

​		执行下方语法在查询时筛选特定记录

```mysql
SELECT <column1>,<column2>,<column3>
FROM <tb>
WHERE <expression>
/*
<column>:查询的字段
<tb>:查询的表
<expression>:过滤条件
*/
```

​		实例：

```mysql
/*
创建含有字段 id 与 name 的表 select_tb 并添加几条记录
*/
mysql> CREATE TABLE IF NOT EXISTS select_tb (
    -> id INT,
    -> name VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO select_tb
    -> (id,name)
    -> VALUES
    -> (1,'Amy'),
    -> (2,'Tom'),
    -> (3,'Candy'),
    -> (4,'Linda');
Query OK, 4 rows affected (0.01 sec)
Records: 4  Duplicates: 0  Warnings: 0

/*
查询表中 id 为 1 的记录的 name
*/
mysql> SELECT name
    -> FROM select_tb
    -> WHERE id = 1;
+------+
| name |
+------+
| Amy  |  -- 查询成功
+------+
1 row in set (0.00 sec)

/*
 查询表中是否有 id 为 3，name 为 David 的记录
*/
mysql> SELECT *
    -> FROM select_tb
    -> WHERE id = 3 AND name = 'David';
Empty set (0.00 sec)  -- 查询失败

/*
查询表中所有 id 大于等于 3 的记录的name
*/
mysql> SELECT name
    -> FROM select_tb
    -> WHERE id >= 3;
+-------+
| name  |
+-------+
| Candy |  -- 查询成功
| Linda |
+-------+
2 rows in set (0.00 sec)
```



### 4-3 分组

​		在查询记录时，可以对指定的列进行分组，即每个分组包含具有相同列值的行。

​		MySQL 规定，分组必须在条件过滤之后进行，而如果不进行条件过滤则可以直接进行分组。

#### 直接分组

​		直接分组不会在之前对记录进行条件过滤。

​		对记录进行分组需要在查询时带上用于分组的字段。

​		执行下面语法对记录进行直接分组

```mysql
SELECT <group_column>,<column1>,<column2>
FROM <tb>
GROUP BY <group_column>;
/*
<group_column>:用于分组的字段
<column>:查询的字段
<tb>:查询的表
*/
```

​		实例：

```mysql
/*
创建用于分组的表 group_tb 并添加记录
*/
mysql> CREATE TABLE IF NOT EXISTS group_tb (
    -> class INT,
    -> id INT,
    -> name VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO group_tb
    -> (class,id,name)
    -> VALUES
    -> (1,1,'Tom'),
    -> (2,1,'David'),
    -> (1,2,'Amy'),
    -> (1,3,'Han'),
    -> (2,3,'Louis'),
    -> (2,2,'Candy'),
    -> (2,4,'Kobe'),
    -> (1,4,'James');
Query OK, 8 rows affected (0.01 sec)
Records: 8  Duplicates: 0  Warnings: 0

/*
根据 class 进行分组并查询 name
*/

```



### 4-4 分组过滤

### 4-5 排序

### 4-6 关联查询





## 触发器

## 函数

## 视图 -> 子查询

## 事务

## 存储过程

## 权限控制
