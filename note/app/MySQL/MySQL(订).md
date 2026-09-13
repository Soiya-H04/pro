# MySQL

## 一、  SQL的基本概念

### 1.1 什么是SQL？

SQL是一种结构化查询语言，用来访问和操作数据库，但有许多版本，遵循的标准有SQL92、SQL99等。



### 1.2  SQL语言的分类

1. DDL : 数据定义语言。如`create`  \ `ALTER`  \ `DROP` 等，创建一些数据库对象，创建相应结构。
2. DML：数据操作语言。如`INSERT` \ `DELETE` \ `UPDATE` 等，对表中数据做一些操作的。
3. DCL：数据控制语言。如 `COMMIT` \ `GRANT`，对于一些操作进行管理，也可以对于访问权限与安全级别进行管理。

## 二、SQL的规则与规范

### 2.1  基本规则

- 可以写在一行或多行，子句可以分行写，必要时用缩进。 

- 每台命令要以 `;` 或 `\g` 或· `\G` 结束。
- 关键字编写时不能分行或漏写。
- 所有的括号与引号都要成对出现，



### 2.2 一些小规范

- 在 window 系统下，对于大小写是不敏感的，即小写与大写是一样的。
- 在 Linux 系统下，对于大小写是敏感的，即小写与大写不一样。但只是数据库名、表名、表的别名与变量名是敏感的。

所以在，MySQL 里建议数据库名、表名、表的别名、字段名与字段别名等都小写，关键字、函数名、绑定变量等大写。



### 2.3 注释

- 在语句前后加上 `\*` 与 `*\`  来表示多行注释。
- 在语句前加`-- ` 也是单行注释，注意 `--` 后有空格。

### 2.5 导入数据表及数据

- `source 文件的全路径名` （常用）
- 基于图形化的工具，可以直接拖到该SQL的存储表的位置

## 三、 select 语句基础

### 3.0 SELECT

``` mysql
SELECT 1;#没有任何子句
SELECT 9/2;#没有任何子句
```



### 3.1 SELECT...FROM...

``` mysql
SELECT 选择字段;（如果是*就是全部，字段用,隔开）
FROM 表名;
```



### 3.2 用 AS 给列加别名

``` mysql
SELECT 字段1 AS pp,字段2 AS  gg ;#将字段1的名字改为pp后显示，但在原表里还是字段1,字段2也是一样
FROM 表名;
```

在大部分情况下， `AS` 可以不加，即 

``` mysql
SELECT 字段1 pp,字段2 gg; #一样的效果，也可以加""将别名引起（在别名有空格隔开时使用），别用''
FROM 表名;
```

列的别名不能在 `WHERE` 中使用，但可以在 `ORDER BY` 中使用。



### 3.3 SELECT DISTINCT ... FROM 去除重复值

当只需要不重复值的时候，在 `SELECT` 后加上 `DISTINCT` 来去除重复值。当有多个字段需要去重，，那么就按照整体来对比。



### 3.4 空值参与运算

空值即  `null` 不等于 `0` ，不代表任何类型。空值参与运算，所得结果也为 `null` 。



### 3.5 着重号 `` 

用于当命名的字段等于关键字重合，用着重号来应用。



### 3.6 查询常数

``` mysql
SELECT 字符或汉字或数字,字符或汉字或数字 ,字段1,字段2 # 字符或汉字或数字为常数，会为每一个匹配到的值在前面加上该字符或汉字或数字;
FROM 表名 ;
```



### 3.7 DESCRIBE（DESC）显示表结构

``` mysql
DESCRIBE\DESC 表名; 
```

会显示该表的相关信息。



### 3.8 过滤信息

### SELECT...FROM...WHERE...

`WHERE`要声明在`FROM`后

``` mysql
SELECT * 
FROM 表名
WHERE 过滤条件;
```



## 四 、 运算符

### 4.1 算数运算符

- 加减运算 ：`+、-`

主要是针对数值类型，当用  `"122"+44` 时，会将 `"122"` 隐式转换，转换为数值类型进行运算。当不为数值时，会将其看为 0 。



- 乘除运算 ：`*、/(DIV)`

当进行乘除运算，得到的结果都是浮点型，且满足有限于加减运算。



- 取模运算 ： `%(MOD)`

当取模时，正负与模数无关，即与 `%` 后的数无关，只看被取模的数的正负。



### 4.2 比较运算符

- 等于 ： `=`

正确返回1，错误返回0。当是不能转换为数值的字符串，会拿ASCLL码的大小进行比较。



- 安全等于 ： `<=>`

其余情况与 `=` 相似，当两个操作数都为 `null` 时，返回1，只有一个为 `null` 时 ，返回 0。



- 不等于 ： `<>(!=)`

正确返回1，错误返回0.



- 大于 ： `>`

正确返回1，错误返回0.



- 小于 ： `<`

正确返回1，错误返回0.



- 为空，非空 ：  `IS NULL \ IS NOT NULL `

当为 `NULL` 时，用  `IS NULL` 时返回1。用 `IS NOT NULL` 返回 0。



-  最小 \ 最大 ： `LEAST() \ GREATEST() `

``` mysql
SELECT LEAST(比较的值)\GREATEST(比较的值) #获得比较的值的最大值与最小值。 
FROM 表名;
```



- 在 ... 与  ... 之间\不在 ... 与  ... 之间（包含前后两值） ： `BETREEN ...  AND ... `\ `NOT BETREEN ...  AND ...` 

```mysql
SELECT 	* 
FROM 表名
WHERE BETWEEN \NOT BETWEEN ... AND ...;
```



- 在范围里 ： `IN（...）\NOT IN(...)`

```mysql
SELECT *
FROM 表名
WHERE IN(...)\NOT IN(...);
```



- 模糊查询  （`%`代表一个或多个不确定的字符，`_`代表一个不确定的字符）：`LIKE\NOT LIKE`

```mysql
SELECT *
FROM  表名
WHERE 字段1 LIKE \ NOT LIKE "%a%"; #查询包含、不包含字符"a"的字段
\*
WHERE 字段1 LIKE \ NOT LIKE "_a"; #查询第二个字符是、不是a的字段.
#当想要用_时，就使用转义字符\
*\
```



- 正则表达式 ： `REGEXP` \ `RLIKE`

```mysql
SELECT 字段 REGEXP "匹配的值" #(匹配满足正常的正常的正则表达式)
FROM 表名;
```



### 4.3 逻辑运算符

- 或 ： `OR` \ `||`



- 非 ： `NOT `\ `!`



- 与 ： `AND` \ `&&`

优先级大于 `OR`。



- 异或 ： `XOR`

当给定的值有一个为 `null` 时，结果为 `null`



### 4.4 位运算符

- 按位与 ： `&`



- 按位或 ： `|`



- 按位异或 ：`^`



- 按位取反 ：`~`



- 按位右移 ：`>>`



- 按位左移 ：`<<`



## 五、 排序与分页

### 5.1 排序（升序、降序） : `ORDER BY ... (ASC\DESC) `

``` mysql
SELECT *
FROM 表名
ORDER BY 字段 (ASC\DESC); #没有指明排序方式，默认使用升序ASC ，可以使用别名
```

多级排序：如果是多字段，那么排序的优先级是：第一个>第二个>第三个···

```mysql
SELECT *
FROM 表名
ORDER BY 字段1 (ASC\DESC),字段2 (ASC\DESC),字段3 (ASC\DESC), ...; #先按字段1排序，再按字段2排序, ...
```



### 5.2 分页 ： `LIMIT `

在不同的DBMS中，排序关键字可能不一样。

```mysql
SELECT *
FROM 表名
LIMIT 0,20; #从第0条数据开始，每页有二十条数据，等价于"LIMIT 20;"下一页为 20,20
```



> PS: Mysql 8.0 新特性
>
> `LIMIT ... OFFSET ...`
>
> ```mysql
> SELECT *
> FROM 表名
> LIMIT 20 OFFSET 0;  #从第0条数据开始，每页有二十条数据
> ```



## 六、 多表查询

### 5.1 意义

防止表的冗余，大量的IO，导致效率低下。



### 5.2 实现方式（关联查询）

用表之间共有的字段来进行查询

```mysql
SELECT 字段1, 字段2 #建议也加上表名，表名1.字段1
FROM 表名1,表名2 #复杂时可用别名，但后续也得使用别名
WHERE 连接条件(表名1.`共有字段` = 表名2.`共有字段`);
```



### 5.3 非等值连接

当一个表的字段的值在另一个表的对应字段里不是一个确切唯一的值，用非等式连接，即用 `IN` 或者 `BETWEEN...AND ...`等范围的关键字进行检索。



### 5.4 自连接

即用两个相同的表，来进行连接。当需要表示一张表同一字段的不同的值的某种关系时，用两张表。



### 5.5 内连接

合并同一列的两个以上的表的行，结果集不包括两表之间不匹配的行。



#### 使用使用 `JOIN ... ON ... ` 实现内连接

不用`WHERE`来过滤,超过三个表不要用`JOIN ... ON ... `

``` mysql
SELECT 字段1, 字段2, ...
FROM 表1 
INNER JOIN 表2 #INNER可省略
ON 表1.`匹配字段` = 表2.`匹配字段`
INNER JOIN 表3
ON 表1.`匹配字段` = 表3.`匹配字段`
....
```





### 5.6 外连接

即，合并同一列的两个以上的表的行，结果集里有两表匹配的行，还查到了不匹配的行。

#### 5.6.1 外连接的分类

- 右外连接

两表之间，显示A表的包含的不含B表的匹配值的行。



- 左外连接

两表之间，显示B表的包含的不含A表的匹配值的行。





#### 5.6.2 使用 `JOIN ... ON ... ` 实现外连接

MySQL使用的是SQL99标准，超过三个表不要用`JOIN ... ON ... `

```mysql
SELECT 字段1, 字段2, ...
FROM 表1 
LEFT OUTER JOIN 表2 #左外连接，可以省略`OUTER`
ON 表1.`匹配字段` = 表2.`匹配字段`
RIGHT OUTER JOIN 表3 #右外连接,可以省略`OUTER`
ON 表1.`匹配字段` = 表3.`匹配字段`
....
```



 

### 5.7 满外连接

综合显示左外连接与右外连接的匹配与不匹配行。



### 5.8 使用`UNION` 

- `UNION` （会去重）

```mysql
结果集1
UNION
结果集2;
```



- `UNION ALL` （推荐，使用资源少，但不去重）

```mysql
结果集1
UNION ALL
结果集2;
```



## 六、 单行函数

### 6.1 数值函数

#### 6.1.1 基本函数

- `ABS(x)`

返回x的绝对值。



- `SIGN(x)`

当x为负数，返回 -1 ；当x为正数，返回 1。



- `pi()`

返回圆周率。



- `CEIL(x)` \ `CEILING(x)`

返回大于或等于某个值的最小整数。



- `FLOOR(x)`

返回大于或等于某个值的最大整数。



- `LEAST(x1,x2,...)`

返回x1，x2，x3，.... 中最小的值。



- `GREATEST(x1,x2,x3,...)`

返回x1，x2，x3，.... 中最大的值。



- `MOD(x,y)`

返回x对y取模的值。



- `RAND()`

返回一个0-1的随机数。



- `RAND(x)`

根据x，返回一个0-1的随机数，但x相同时，返回值相同。



- `ROUND(x)`

返回四舍五入后的值。



- `ROUND(x,y)`

也是返回四舍五入的值，但会保留y位小数。当y为负数时，保留从 `.` 往前数y位的数。



- `TRUNCATE(x,y)`

截断，类似于 `ROUND(x,y)` ，但不进行四舍五入，直接舍去。



- `SQRT(x)`

返回x的平方根。当x为负数时，返回 `null`。



#### 6.1.2 三角函数

**角度与弧度互换**

1. `PADIANNS(x)` 角度化为弧度。
2. `DEGREES(x) ` 弧度化为角度。



**当 x 为弧度值**

- SIN(x)

返回正弦值。



- ASIN(x)

返回反正弦值。



- COS(x)

返回余弦值。



- ACOS(x)

返回反余弦值。



- TAN(x)

返回正切值。



- ATAN(x)

返反正切值。



- ATAN2(m,n)

返回两个参数的反正切值。



- COT(x)

返回余切值。



#### 6.1.3 指数与对数函数

- `POW(x,y)` \ `POWER(x,y)`

返回x的y次方。



- `EXP(x)`

返回e的x次方。



- `LN(x)` \ `LOG(x)`

返回以e为底的x的对数，当x<=0时，返回 `null`。



- `LOG10(x)`

返回以10为底的x的对数，当x<=0时，返回 `null`。



- `LOG2(x)`

返回以2为底的x的对数，当x<=0时，返回 `null`。



#### 6.1.4 进制间转换

- BIN(x)

返回x的二进制编码。



- HEX(x)

返回x的十六进制编码。



- OCT(x)

返回x的八进制编码。



- CONV(x,f1,f2)

返回x的将f1进制的数换为f2进制的数，x为f1进制下的数。



### 6.2 字符串函数

- `CHAR_LENTH(s)`

返回字符的个数。



- `LENTH(s)`

返回字节的个数。



- `CONCAT(s1,s2,...)`

拼接。



- `CONCAT_WS(x,s1,s2,...)`

以 x 来进行拼接。



- `INSERT(str,index,len,replace_str)`

将 `str` 的第 `index` 个字符（包括）以后的 `len` 个字符 用 `replace_str`来替换（`len`为0时只插入），索引从1开始。



- `REPLACE(str,a,b)`

将 `str` 里的 a 换成 b。



- `UPPER(s)` \ `USACE(s)`

将s大写。



- `LOWER(s)` \ `LCACE(s)`

将s小写。



- `LEFT(str,n)`

去从左开始数的n个字符，超过全取。



- `RIGHT(str,n)`

去从右开始数的n个字符，超过全取。



- `LPAD(str,len,pad)`

若 `str` 位数不足 `len`  用 `pad` 在左边补足。



- `RPAD(str,len,pad)`

若 `str` 位数不足 `len`  用 `pad` 在右边补足。



- `LTRIM(s)`

去除字符串左边的空格。



- `RTRIM(s)`

去除字符串右边的空格。



- `TRIM(s)`

去除字符串左边与右边的空格。



- `TRIM(s1 FROM s)`

去除字符串开头与结尾的s1字符串。



- `TRIM(LEADING s1 FROM s)`

去除字符串开头的s1字符串。



- ``TRIM(TRAILING s1 FROM s)`

去除字符串结尾的s1字符串。



- `REPEAT(Str,n)`

返回str重复n次的结果。



- `SPACE(n)`

返回n个空格。



- `SUBSTR(s,index,len)`

返回s的排序在 index 的字符（包括）往后 len-1 长度的字符串。



- `STRCMP(s1,s2)`

比较两个字符串的ASCLL码。



- `LOCATE(substr,str)`

返回 `substr` 在 `str` 里首次出现的位置，若没有，则返回0.



- `ELT(m,S1,s2,...)`

返回指定位置的字符串，m=1，则返回s1 。



- `FIELD(s,s1,s2,...)`

返回字符串s在字符串列表里第一次出现得到位置。



- `FIND_IN_SET(s1,s2)`

返回字符串s1在字符串s2中出现的位置。



### 6.3 日期与时间函数

#### 6.3.1 获取日期与时间

- `CURDATE()` \ `CURRENT_DATE()`

返回当前的年月日。



- `CURTIME()` \ `CURRENT_TIME()`

返回当前的时分秒。



- `NOW()`\ `LOCALTIME()` \ `SYSTIME()`

返回当前的系统日期与时间。



- `UTC_DATE()`

返回UTC（世界标准时间）日期



#### 6.3.2 日期与时间戳的转换

- `UNIX_TIMESTAMP()`

以时间戳的格式返回当前时间。



- `UNIX_TIMESTAMP(date)`

将时间 `date`以时间戳的格式返回。

 

- `FROM_UNIXTIME(timestamp)`

将 UNIX 时间戳的时间转换为一般格式的时间。



#### 6.3.3 获取月份、星期、星期数、天数

date 是以字符串的形式，如 '2004-10-11'。

- `YEAR(date)` \ `MONTH(date)` \ `DAY(date)`

返回具体的日期值。



- `HOUR(time)` \ `MINUTE(time)` \ `SECOND(time)`

返回具体的时间值。



- `MONTHNAME(date)`

返回月份。



- `DAYNAME(date)`

返回星期几。



- `WEEKDAY(date)`

返回周几。



- `QUARTER(date)`

返回季度。



- `WEEKOFYEAR(date)`

返回是一年的第几个星期。



- `DAYOFYEAR(date)`

返回时一年里的第几天。



- `DAYOFMONTH(date)`

返回是当月的第几天。



- `DAYOFWEEK(date)`

返回时周几。



#### 6.3.4 日期的操作函数

`EXTRACT(type FROM date)`

`type` 有多种选择，不再赘述。



#### 6.3.5 计算日期与时间

- `DARE_ADD(datetime,INTERVAL,expr type)`

有许多type可以选择。



- `ADDTIME(time1,time,2)`

将time1的时间加上time2的时间，当time2为数字时，表示的是秒。



- `SUBTIME(date1,date2)`

将time1的时间减去time2的时间，当time2为数字时，表示的是秒。



- `DATEDIFF(date1，date2)`

返回date1-date2，即相隔的天数。



- `PERIOD_ADD(time,n)`

返回date加上n后的时间。



#### 6.3.6 日期的格式化与解析

- `DATE_FORMAT(date,fmt)`

按fmt来格式化日期date。



- `TIME_FORMAT(time,fmt)`

按fmt来格式化时间time。



- `GET_FORMAT(date_type,format_type)`

返回字符串的显示格式。



- `STR_TO_DATE(str,fmt)`

按照字符串fmt对str进行解析，为一个日期。



|  %Y  | 年（四位） |  %m  |        月         |
| :--: | :--------: | :--: | :---------------: |
|  %d  |     日     |  %M  |        分         |
|  %H  |     时     |  %D  | 月中的天数（1st） |
|  %S  |     秒     |  %c  |       月份        |
|  %y  | 年（两位） |  %e  |  月中的天数（1）  |

​	

### 6.4 流程控制函数

- `IF(vlaue,value1,value2)`

如果value的值为TRUE，返回value1，否则返回value2。



- `IFNULL(value1,value2)`

如果value1不为`null`，返回value1，否则返回value2。



- `CASE WHEN 条件1 THEN 结果1 WHEN 条件2 THEN 结果2 ... [ELSE return] END`

没有`ELSE`时，若不符合上述条件，则返回 `null`。将`CASE`放在`SELECT`后，当作字段，建议给别名。



- `CASE expr WHEN 常量值1 THEN 值1 WHEN 常量值2 THEN 值2  ...[ELSE 值n] END`

​	`expr` 为表达式，其余同上。



### 6.5 加密函数

- `PASSWORD(str)` 

在MySQL8.0中已经弃用。



- `MD5(str)`

```mysql
SELECT MD5("mysql")
FROM DUAL;
```



- `SHA(str)`

```mysql
SELECT MD5("mysql")
FROM DUAL;
```



### 6.6 信息函数

- `VERSION()`

返回MySQL版本号。



- `CONNECTION_ID()`

返回当前MySQL服务器的连接数。



- `DATABASE()` \ `SCHEMA()`

返回当前命令行所在的数据库。



- `USER()` \ `CURRENT_USER()` \ `SYSTEM_USER()` \ `SESSION_USER()`

但会当前连接MySQL的用户名，格式为“主机名@用户名”



- `CHARSET(value)`

返回字符串value自变量的字符集。



- `COLLATION(value)`

返回字符串value的比较规则。



### 6.7 其他函数

- `CONV(value,from,to)`

不同进制的转换。



- `INET_ATON(ipvalue)`

将以点分隔的IP地址转换为数字。



- `INET_NTOA(value)`

将数字形式的IP地址转换为一般格式的IP地址



- `BENCHMARK(n,expr)`

让expr执行n次，测试MySQL的处理时间。





## 七、 聚合函数

多个输入参数，返回一个结果的函数。

### 7.1 常见的几个聚合函数

|      函数       |                结果                |
| :-------------: | :--------------------------------: |
|  `AVG(values)`  |               平均值               |
|  `SUM(values)`  |                 和                 |
|  `MAX(vakues)`  |               最大值               |
|  `MIN(values)`  |               最小值               |
| `COUNT(values)` | 计算指定字段在查询结构中出现的次数 |

> `COUNT()`的计算是不记录`null`。





### 7.2 `GROUP BY` 分组

```mysql
SELECT * 
FROM
WHERE ...
GROUP BY 字段... #按照字段来进行分组
```

分组没有先后顺序，`SELECT`中出现的非组函数的字段必须出现在 `GROUP BY`中，但 `GROUP BY`里出现的字段，可以不出现在 `SELECT`中。



### 7.3 `HAVING` 过滤

1. 如果过滤条件中使用了聚合函数，必须用`HAVING`来代替`WHERE`。但是，`HAVING`要写在`GROUP BY`后面（如果有的话）。
2. `WHERE`与`HAVING`同时可用的话，优先用 `WHERE`。



### 7.4 SQL的底层逻辑

#### 7.4.1 编写顺序

- 在 SQL92 里的语法

```mysql
SELECT ..., ..., ...
FROM ..., ..., ...
WHERE 多表的连接条件, 不包含聚合函数的过滤条件
GROUP BY ..., ...
HAVING 包含聚合函数的过滤条件
ORDER BY ..., ...(ASC,DESC)
LIMIT ..., ...
```

- 在 SQ99 里的语法

```mysql
SELECT ..., ..., ...
FROM ..., ..., ... 
(LEFT\RIGHT)JOIN .... 
ON...
WHERE 多表的连接条件, 不包含聚合函数的过滤条件
GROUP BY ..., ...
HAVING 包含聚合函数的过滤条件
ORDER BY ..., ...(ASC,DESC)
LIMIT ..., ...
```



#### 7.4.2 执行过程

1. 先找表（`FROM`）
2. 再过滤（`ON`，`LEFT\RIGHT`），多表连接时。
3. `WHERE`过滤
4. `GROUP  BY`分组
5. `HAVING`过滤
6. `SELECT`过滤字段, `DISTINCT` 去重。
7. `ORDER  BY` 顺序
8. `LIMIT`分页



## 八、 子查询

子查询指一个查询语句嵌套在另一个查询语句内部的查询。

如：

```mysql
#外查询
SELECT 查询字段
FROM 表名
WHERE (#内查询
    SELECT 查询字段
    FROM 表名
);#内查询的结果用于外查询的过滤
```

子查询分类：

- 单行子查询

>子查询返回结果只有一条

- 多行子查询

>子查询返回结果有多条

- 相关子查询

>外查询的内容与内查询的内容相关（外变内也变）

- 不相干子查询

>外查询的内容与内查询的内容不相关（外变内不变）



### 8.1 单行子查询

#### 单行子查询操作符

|  =   |  <>  |
| :--: | :--: |
|  >   |  <=  |
|  <   |  >=  |



例：

```mysql
SELECT 字段
FROM 表名
WHERE 字段的值 >/</... (
    SELECT 字段
    FROM 表名
    WHERE 过滤条件
);
```

**操作符后只能为单值！**



### 8.2 多行子查询

#### 多行子查询操作符

| 操作符 |                         含义                         |
| :----: | :--------------------------------------------------: |
|   IN   |                  等于列表里任意一个                  |
|  ANY   | 和单行操作符一起使用，与子查询返回的某一个值进行比较 |
|  ALL   |  需要和单行操作符一起使用，和子查询返回的所有值比较  |
|  SOME  |                    与ANY作用相同                     |

```mysql
SELECT 字段
FROM 表名
WHERE 字段的值 IN (
    SELECT 字段
    FROM 表名
    WHERE 过滤条件
)

AND ...;#可以加子查询
SELECT 字段
FROM 表名
WHERE 字段的值 </... ANY (#小于任一子查询返回值 ALL 小于所有的子查询返回值
    SELECT 字段
    FROM 表名
    WHERE 过滤条件
);
```

可以在`FROM/HAVING`后加子查询（子查询返回可为表格式）

### 8.3 相关子查询

在执行内查询（子查询）时，用到外查询（主查询）的条件，从而将内外查询关联起来。

```mysql
SELECT *
FROM table1,table2
WHERE 字段1 (
	SELECT *
    FROM table2	#将外查询的表传进来，从而实现内外的查询时相关联
    WHERE 过滤条件
);
```

不一定传表，也可以传字段等，进行多表查询。

在`FROM`中，可以传入我们通过`SELECT`返回的表，进而进行相关子查询。

**结论**：除了`GROUP BY`与`LIMIT`，其它的关键字都可以嵌入子查询语句（注意结构）。



#### `EXISTS`关键字

在表里找到匹配字段，返回TRUE，否则继续找，找完没有返回FALSE



## 九、 创建与管理

### 9.1 数据存储的过程

1. 创建数据库
2. 创建表（创建对应字段）
3. 插入数据



###  9.2 创建规则

- 数据库名与表名不能超过30个字符，变量名不能超过29个字符
- 只能包含A-Z、a-z、0-9，_共63个字符
- 最好不要使用关键字
- 表、字段、数据库不能重名
- 相同的字段最好在不同的表里的类型相同



### 9.3 创建、管理数据库

- 数据库的创建

```mysql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name #当不确定库是否存在时用IF NOT EXISTS
    [create_option] ... #一些选项，CHARSET gpk 即将编码方式定位gpk

create_option: [DEFAULT] {
    CHARACTER SET [=] charset_name
  | COLLATE [=] collation_name
  | ENCRYPTION [=] {'Y' | 'N'}
}
```

- 使用数据库

```mysql
USE db1；#使用数据库db1
```

- 查看当前数据库 

``` mysql
SELECT DATABASE();
```

- 查看当前(指定)数据库下的表

``` mysql
#查看当前库的表
SHOW TABLES;
# 查看指定数据库下的表：
SHOW TABLES FROM db1;
```

- 删除指定的库

```mysql
DROP DATABASE IF EXISTS ab1;
```



### 9.4 表操作

#### 9.4.1 字段类型

##### a. 整型

- 迷你整型：tinyint，使用**1个字节**存储整数，最多存储256个整数（-128~127）
- 短整型：smallint，使用**2个字节**存储整数
- 中整型：mediumint，使用**3个字节**存储整数
- 标准整型：int，使用**4个字节**存储整数
- 大整型：bigint，使用**8个字节**存储

数值型存储在MySQL中分为有符号（有负数）和无符号（纯正数）需要unsigned 修饰整型

``` mysql
create table t_7(
	age tinyint unsigned, # unsigned修饰整数，表示无符号（从0开始）
    haircount int unsigned
)charset utf8;
```



##### b. 小数型

**1、浮点型**：`FLOAT / DOUBLE`，存储不是特别精确的数值数据

- 浮点数又称之为精度数据，分为两种
  - 单精度：**FLOAT**，使用**4个字节**存储，精度范围为6-7位有效数字
  - 双精度：**DOUBLE**，使用**8个字节**存储，精度范围为14-15位有效数字
- 浮点数超过精度范围会自动进行**四舍五入**
- 精度可以指定整数和小数部分
  - 默认不指定，整数部分不超过最大值，小数部分保留2位
  - 可以指定：`float/double`(总长度,小数部分长度)
- 可以使用科学计数法插入数据：AEB，A * 10 ^ B
- 因为浮点数会自动四舍五入，所以不要使用浮点数来**存储对精度要求较高的数值**



**2、定点型**：`DECIMAL`，能够保证精度的小数

- 定点数的存储模式**不是固定长度**，所以数据越大占用的存储空间越长

- 每9个数字使用**4个字节**存储

- 定点型可以

  指定

  整数部分长度和小数部分长度

  - 默认不指定，10位有效整数，0位小数
  - 可以指定：`DECIMAL`(有效数位,小数部分数位)
  - 有效数位不超过65个

- 数据规范

  - 整数部分超出报错
  - 小数部分超出四舍五入

  ```mysql
  create table t_12(
      money DECIMAL(14,2),#十四位有效数字,小数部分2位
      bet DECIMAL(10,2)
  )charset utf8;
  ```

  

##### c. 字符串型

**1、定长型**：char(L)，指定**固定长度的存储空间**存储字符串

- 定长是指定存储长度
- 定长的长度是字符而不是字节
  - L的最大值是255
  - 实际存储空间：**L字符数 \* 字符集对应字节数**
- 定长里存储的数据不能超过指定长度，但是可以小于指定长度
- 字符串数据使用单引号或者双引号包裹
- 定长的**访问效率较高**，但是**空间利用率较低**

```mysql
create table t_13(
	id_number char(18),
    phone_number char(11)
)charset utf8;
insert into t_13 values('440111999912120304','13512345678');
```



**2、变长型**：varchar(L)，根据实际存储的数据变化存储空间

- 变长型的存储空间是由**实际存储数据**决定的
- 变长型的L也是指字符而不是字节
  - L指定的是最大存储的数据长度
  - L最大值理论是65535
  - 变长需要额外产生1-2个字节，用来记录实际数据的长度
    - 数据长度小于256个，多1个字节
    - 数据长度大于256个，多2个字节
  - 实际存储空间：**实际字符数 \* 字符集对应字节数 + 记录长度**
- 变长数据不能超过定义的最大长度
- 变长字符串在读取时需要进行长度计算，所以效率没有定长字符串高
- 变长字符串能够更好的**利用存储空间**

```mysql
create table t_14(
	username varchar(50),#一定要指明
    password varchar(15),
    name varchar(10),
    id_number char(18)
)charset utf8;
```



**3、文本字符串**：text/blob，专门用来存储较长的文本

- 文本字符串通常在**超过255个字符**时使用

- 文本字符串包含两大类

  - text：

    普通字符

    - tinytext：迷你文本，不超过`2 ^ 8 -1`个字符
    - text：普通文本，不超过 `2 ^ 16 - 1`个字符
    - mediumtext：中型文本，不超过 `2 ^ 24 - 1` 个字符
    - longtext：长文本，不超过 `2 ^ 32 - 1` 个字符（4G）

  - blob：

    二进制字符

    （与text类似）

    - tinyblob
    - blob
    - mediumblob
    - longblob

- 文本字符串会**自动**根据文本长度选择适合的具体类型

- 一般在文本超过255个字符时，都会使用text（blob现在极少使用）

```mysql
create table t_15(
	author varchar(10),
    title varchar(50),
    content text
)charset utf8;
```

**4、枚举型**：enum, 一种**映射存储**方式，以较小的空间存储较多的数据

- 枚举是在定义时确定可能出现的可能，而后数据只能出现定义时其中的**一种**的数据类型
- 枚举类似一种**单选框**
- 枚举使用1-2个字节存储，最多可以设计65535个选项
- 枚举实际存储是**使用数值**，映射对应的**元素数据**，从1开始
- 枚举语法：`enum(元素1,元素2,...元素N)`
- 使用枚举的作用：
  - 规范数据模型
  - 优化存储空间

```mysql
create table t_16(
	type enum('小朋友','少年','青年','中年','老年')
)charset utf8;
```



**5、集合型**：set，一种**映射存储**方式，以较小的空间存储较多的数据

- 集合是在定义时确定可能出现的元素进行穷举，而后数据只能出现定义时其中的元素（可以是**多个**）
- 集合类似一种**多选框**
- 集合使用1-8个字节存储数据，最多可以设计64个元素
- 集合实际存储是使用数值（二进制位），映射对应的元素数据，每个元素对应一个比特位
  - 数据存在：对应位为 1
  - 数据不存在：对应位为 0
- 集合语法：`set(元素1,元素2,...元素N)`
- 使用集合的作用：
  - 规范数据模型
  - 优化存储空间

```mysql
create table t_17(
	hobby set('足球','篮球','羽毛球','网球','乒乓球','排球','台球','冰球')#可以使用索引来调用
)charset utf8;
```



##### d. 时间类型

**2、时间戳**：timestamp，基于格林威治时间的时间记录

- MySQL中时间戳表现形式不是秒数，而是年月日时分秒格式
  - **YYYY-MM-DD HH:II::SS**
  - **YYYYMMDDHHIISS**
- timestamp使用4个字节存储
  - 表示范围是 1971年1月1日0时0分0秒-2155年12月31日23是59分59秒
  - timestamp可以使用 0000-00-00 00:00:00
- 所对应的记录不论哪个字段被更新，该字段都会更新到当前时间
- 但在MySQL8中需要主动使用**on update current_timestamp**才会自动更新

```mysql
create table t_19(
	goods_name varchar(10),
    goods_inventory int unsigned,
    change_time timestamp
)charset utf8;
```



**3、日期**：date，用来记录年月日信息

- 使用**3个字节**存储数据
- 存储日期的格式为：**YYYY-MM-DD**
- 存储的范围跨度很大，存储区间是1000 - 9999年：1001-01-01~9999-12-31

```mysql
create table t_20(
	name varchar(10),
    birth date
)charset utf8;
```



#### 9.4.2 创建与管理

##### a. 查看表结构

```mysql
DESC tb1;
```



##### b. 查看创建表结构

``` mysql
SELECT CREATE TABLE tb1;
```



##### c. 查看表数据

``` mysql
SELECT * 
FROM tb1;
```



##### d. 创建表

```mysql
#普通创建新表
CREATE TABLE IF NOT EXISTS tb1;
#根据查询结果创建新表,会将数据移植到新表.还可以进行子查询等操作,将其返回记录移植至新表
CREATE TABLE 
AS
SELECT *
FROM tb1;# tb1已存在
#创建一个新表具有旧表的结构
CREATE TABLE 
AS
SELECT *
FROM tb1
WHERE 1=2;因为1不等于2,所以一条数据都不会传进新表里
#将另一数据库的表传入
CREATE TABLE 
AS
另一数据表.字段
```



##### e. 修改表

- 添加字段

``` mysql
ALTER TABLE tb1
ADD 字段名 字段类型;
#默认添加到最后的位置
ALTER TABLE tb1
ADD 字段名 字段类型
FIRST;
#放在第一位
ALTER TABLE tb1
ADD 字段名 字段类型
AFTER 字段1;
#放在字段1后
```

- 修改字段

```mysql
ALTER TABLE tb1
MODIFY 字段名 新字段类型;#一般不改字段类型,会改字段的长度等
ALTER TABLE tb1
MODIFY 字段名 新字段类型 DEFAULT 'aaa';#将其默认值改为aaa
```

- 重命名字段

```mysql
ALTER TABLE tb1
CHANGE 字段名 新字段名 (新)字段类型;#可以同时修改字段名与字段类型
```

- 删除字段

```mysql
ALTER TABLE tb1
DROP COLUMN 字段名;
```

- 重命名表

``` mysql
#RENAME修改
RENAME TABLE tb1
TO 新表名;
```

- 删除表

```mysql
DROP TABLE IF EXISTS tb1;
```

- 清空表

```mysql
TRUNCATE TABLE tb1;#TRUNCATE 操作会导致隐式提交，因此不能回滚。
```

#### 9.4.3 `COMMIT`与`ROLLBACK`

`COMMIT`会提交最近的修改到数据库.

```mysql
COMMIT;#执行以后会保存当前修改,使用ROLLBACK只能回滚到当前状态
```

当执行了DML语句后,MySQL会自动提交,即当执行回滚时就不会得到之前的数据.所以如果想要在执行了DML语句后能回滚,就要执行

```mysql
SET autocommit = FALSE;
```

再

```mysql
ROLLBACK;
```

就可以回滚到上次修改的地方.

#### 9.4.4 数据处理

##### a. 添加数据

- 添加单条数据

```mysql
#方式一
INSERT INTO tb1
VALUES (
值一,值二,值三,值四...#没有指明添加字段,要按照声明时字段顺序进行添加
);
#方式二
INSERT INTO tb1(字段2,字段3,字段7,...)
VALUES (
值二,值三,值七,...#不用按照声明时的顺序,按照上面规定的字段顺序
);
```

- 同时添加多组数据

```mysql
INSERT INTO tb1
VALUES (
	值一,值二,值三,值四...,
),
(
	值一,值二,值三,值四...,
);
```

- 将查询结果添加进表内

```mysql
INSERT INTO tb1
SELECT *	#不需要加VALUES,但是要确保查询结果的字段顺序要与tb1一致,也可以用tb1(字段2,字段3,字段7,...)的形式
FROM tb1
WHERE 过滤条件;
```



##### b. 更新数据

更新数据通常会加上过滤条件(毕竟不是所有时候都要改所有人的数据),这也代表更新`UPDATE`是批量修改数据

```mysql
UPDATE tb1
SET 字段1 = 新值,字段2 = 新值	#可以一次修改多个字段
WHERE 过滤条件;
```

注意在修改数据时，要注意约束条件，即



##### c. 删除数据

```mysql
DELETE FROM tb1
WHERE 过滤条件;
#删除一行数据
```



## 十、 约束

对于字段进行一些限制与规范。

### 10.1 约束的分类

#### 10.1.1 按照约束的字段数

- 单列约束
- 多列约束



#### 10.1.2 按照约束的范围

- 列级约束

包括`NOT NULL` | `DEFAULT` | `PRIMARY KEY` | `UNIQUE` | `CHECK`

- 表级约束

包括`PRIMARY KEY` | `UNIQUE` | `CHECK` | `FOREIGN KEY`



#### 10.1.3 按照约束的作用

- NOT NULL：非空约束，用于约束该字段的值不能为空。比如姓名、学号等。
- DEFAULT：默认值约束，用于约束该字段有默认值，约束当数据表中某个字段不输入值时，自动为其添加一个已经设置好的值。比如性别。
- PRIMARY KEY：主键约束，用于约束该字段的值具有唯一性，至多有一个，可以没有，但是有的话非空。比如学号、员工编号等。
- UNIQUE：唯一约束，用于约束该字段的值具有唯一性，可以为空（为空时，可以多值）。比如座位号。
- CHECK：检查约束，用来检查数据表中，字段值是否有效。比如年龄、性别。
- FOREIGN KEY：外键约束，外键约束经常和主键约束一起使用，用来确保数据的一致性，用于限制两个表的关系，用于保证该字段的值必须来自于主表的关联列的值。在从表添加外键约束，用于引用主表中某列的值。比如学生表的专业编号，员工表的部门编号，员工表的工种编号。





### 10.2 约束的使用

#### 10.2.1 查看表中的约束

当我们想要查看表的约束时，用下面语句

```mysql
SELECT * 
FROM information_schema.table_constraints
WHERE table_name = '表名';
```



#### 10.2.2 约束的添加与删除

- 非空约束

赋值时不能为空，也不能不给赋值（如果没有默认值的时候），只能是单字段使用。

```mysql
#在创建表的时候声明
CREATE tb1(
	id INT NOT NULL,
    last_name CHAR(10) NOT NULL
);

#在更改字段声明
ALTER tb1
MODIFY 字段1 INT(任意类型) NOT NULL;

#删除约束
ALTER tb1
MODIFY 字段1 INT(任意类型) NULL;
```



- 唯一性约束

保证一个字段不会有相同的值（`NULL`除外），可以有多个字段唯一，也可以组合值唯一。

```mysql
#创建表时声明
##列级约束
CREATE TABLE tb1(
    id INT UNIQUE,
    last_name CHAR(10) UNIQUE,
);
##表级约束
CREATE TABLE tb1(
    id INT,
    last_name CHAR(10) UNIQUE,
    CONSTRAINT 约束名 UNIQUE(id)#在所有字段声明完后可以进行表约束，可以不起名，直接 UNIQUE(字段)，效果一样
);

#在更改字段时声明（在原本表数据里，字段没有重复时才能使用）
##方式一
ALTER TABLE tb1
MODIFY id INT UNIQUE;

##方式二
ALTER TABLE tb1
ADD CONSTRAINT 约束名 UNIQUE(字段1)
--------------------------------------------------------------------------------------------------
#针对于多字段的约束，即将两个字段的值当作一个整体
#创建时声明
CREATE TABLE tb1(
    id INT,
    last_name CHAR(10),
    CONSTRAINT 约束名 UNIQUE[KEY](id,last_name)#将两个字段当作整体，只要有一个值不一样就可以添加，KEY可加可不加
);
#在更改字段时声明
ALTER TABLE tb1
ADD CONSTRAINT 约束名 UNIQUE(id,last_name);
----------------------------------------------------------------------------------------------------
#删除唯一性约束
#在创建唯一性约束时自动创建了唯一性索引，要删除唯一性约束，就要删除唯一性索引，如果没有指定约束名，就是字段名。如果是多字段没有指定名，就与()里的第一个字段的字段名一样。
ALTER TABLE tb1
DROP INDEX id;
```



- PRIMARY KEY 约束

主键约束（非空且唯一），一个表里只能有一个主键约束。主键名只能是PRIMARY，不要修改主键字段的值。

```mysql
#创建表时声明
##列级约束
CREATE TABLE(
    id INT PRIMARY KEY,#只能添加一个
    last_name VARCHAR(15),
    salary DECIMAL(10,2),
);
##表级约束
CREATE TABLE(
    id INT,
    last_name VARCHAR(15),
    salary DECIMAL(10,2),
    PRIMARY KEY(id)
);
#两者效果一样
#更改字段时声明
##方式一
ALTER TABLE tb1
ADD PRIMARY KEY(id);
##方式二
ALTER TABLE tb1
MODIFY id INT PRIMARY KEY;
---------------------------------------------------------------------------------------------------
#复合主键约束
CREATE TABLE(
    id INT,
    last_name VARCHAR(15),
    salary DECIMAL(10,2),
    PRIMARY KEY(id，last_name)
);
#当id与last_name不完全一样就可以添加，但是一个都不能为空

ALTER TABLE tb1
ADD  PRIMARY KEY(id，last_name);
#一样的效果
---------------------------------------------------------------------------------------------------
#删除主键约束（大概率用不上）
ALTER TABLE tb1
DROP PRIMARY KEY;
```



- AUTO_INCREMENT 自增列

一张表里只能有一个自增列，必须是数值类型，在添加字段时，会自动将对应字段的值加1

```mysql
#在创建表的时候声明
CREATE TABLE tb1 (
id INT AUTO_INCREMENT,
name VARCHAR(15)
)
#在添加数据时就不需要给其赋值
#在更改表的时候声明
ALTER TABLE tb1
MODIFY id AUTO_INCREMENT;
#添加数据时一定要指明字段
INSERT INTO test(name,age)
VALUES('LIG',9),
('dasd',45);

#删除AUTO_INCREMENT约束
mysql> ALTER TABLE test
    -> MODIFY id INT;
```

- FOREIGN KEY

外键约束，限定每个表的的外表必须存在且唯一（即，在外表里，对应的字段要么是主键约束，要么是唯一性约束）。

```mysql
#创建表时声明（先创建主表）
mysql> CREATE TABLE test1(
    -> id INT PRIMARY KEY,#创建外表，且为主键
    -> name VARCHAR(15),
    -> age INT NOT NULL);
#再创建从表
mysql> CREATE TABLE test2(
    -> id INT,
    -> name VARCHAR(15),
    -> age INT,
    -> CONSTRAINT fk_id FOREIGN KEY (id) REFERENCES test1(id));
#会返回
Query OK, 0 rows affected (0.05 sec)
--------------------------------------------------------------------------------------------------------
#在更改字段时声明
mysql> ALTER TABLE test2
    -> ADD CONSTRAINT fk_age FOREIGN KEY(age) REFERENCES test1(age);
#返回结果
Query OK, 0 rows affected (0.09 sec)
Records: 0  Duplicates: 0  Warnings: 0
#一般键的增加用ADD比较好
--------------------------------------------------------------------------------------------------------
#第一步：删除外键约束
mysql> ALTER TABLE test2
    -> DROP FOREIGN KEY fk_age;
#返回	
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0
#指明外键名
#第二步：再去删除索引
mysql> ALTER TABLE test2
    -> DROP INDEX fk_age;
#返回
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

提供外键，但是一般是在应用层面去进行更新，只能在低并发的时候才好用，对于高并发的集群，会引起更新风暴。

- CHECK 约束

只有满足CHECK条件的才能添加

```mysql
#创建表
mysql> CREATE TABLE test4(
    -> id INT ,
    -> name VARCHAR(15),
    -> salary DECIMAL(10,2) CHECK(salary>2000));
#返回
Query OK, 0 rows affected (0.05 sec)
#此时添加值
mysql> INSERT INTO test4
    -> VALUES(11,'mmas',1222);
#返回
ERROR 3819 (HY000): Check constraint 'test4_chk_1' is violated.
#这是CHECK的作用，输入如下数据，
mysql> INSERT INTO test4
    -> VALUES(11,'mmas',5555);#只改了5555
#返回
Query OK, 1 row affected (0.03 sec)
#成功添加
```

- DEFAULT约束

```mysql
#创建新表
mysql> CREATE TABLE test5
    -> (
    -> id INT,
    -> name VARCHAR(15),
    -> salary DECIMAL(10,2) DEFAULT 5000#设置默认值为5000
    -> );
#返回
Query OK, 0 rows affected (0.04 sec)
#添加数据
mysql> INSERT INTO test5(id,name)#就像之前AUTO_INCREMECT一样，要添加顺序
    -> VALUES(5,'LUCY');
#返回
Query OK, 1 row affected (0.03 sec)
#再检查一下
mysql> SELECT *
    -> FROM test5;
+------+------+---------+
| id   | name | salary  |
+------+------+---------+
|    5 | LUCY | 5000.00 |
+------+------+---------+
1 row in set (0.00 sec)
------------------------------------------------------------------------------------------------------
#在ALTER时修改
mysql> ALTER TABLE test5
    -> MODIFY salary DECIMAL(10,2) DEFAULT 3000;
#返回，即已经将默认值改为3000
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0
#再添加数据
mysql> INSERT INTO test5(id,name)
    -> VALUES(5,'smomm');
Query OK, 1 row affected (0.03 sec)
#查看默认值
mysql> SELECT *
    -> FROM test5;
+------+-------+---------+
| id   | name  | salary  |
+------+-------+---------+
|    5 | LUCY  | 5000.00 |
|    5 | smomm | 3000.00 |
+------+-------+---------+
2 rows in set (0.00 sec)
--------------------------------------------------------------------------------------------------------
#删除默认值，也是用ALTER
mysql> ALTER TABLE test5
    -> MODIFY salary DECIMAL(10,2);
Query OK, 0 rows affected (0.04 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

## 十一、 视图

### 10.1 数据库对象

- 表：基本的数据存储对象 以行和列的方式存在  列就是字段  行就是记录

- 约束：执行数据的校验 保存数据的完整性

- 数据字典：系统表  存放数据库的相关信息

- 视图：一个或者多个数据表的逻辑显示

- 索引：用于提高查询的性能
- ...



### 10.2 视图概述

当只想给用户看指定的数据，就用视图来实现。即，给用户指定的视图来对表进行操作。视图不存储数据，占用很少的空间。从视图来查询、修改数据是直接在原表上操作。

视图的删除不会让基表（视图时的SELECT获得的表）的数据删除。



### 10.3 创建视图

```mysql
#对于单表创建VIEW
mysql> CREATE OR REPLACE VIEW shitu#shitu为VIEW的别名,当视图存在就替代掉
    -> AS
    -> SELECT id,salary,name
    -> FROM test4;
#返回
Query OK, 0 rows affected (0.04 sec)

#给字段加别名
mysql> CREATE VIEW shitu1(id,NAME,sal)
    -> AS
    -> SELECT id,name,salary
    -> FROM test4;
#返回
Query OK, 0 rows affected (0.03 sec)

#加上限定条件
mysql> CREATE VIEW shitu2(id,NAME,sal)
    -> AS
    -> SELECT id,name,salary
    -> FROM test4
    -> WHERE salary > 2000;
#返回
Query OK, 0 rows affected (0.03 sec)
------------------------------------------------------------------------------------------------------
#查询VIEW字段
mysql> SELECT *
    -> FROM shitu2;
#返回
+------+------+---------+
| id   | NAME | sal     |
+------+------+---------+
|   11 | mmas | 5555.00 |
+------+------+---------+
1 row in set (0.00 sec)

-----------------------------------------------------------------------------------------------------
#视图可以包含基表里没有的字段
mysql> CREATE VIEW shitu3(id,name,avg_sal)
    -> AS
    -> SELECT id,name,AVG(salary)
    -> FROM test4
    -> ORDER BY id;
#返回
Query OK, 0 rows affected (0.01 sec)
--------------------------------------------------------------------------------------------------------
#可以基于多表创建视图
mysql> CREATE VIEW shitu4(id,name,salary)
    -> AS
    -> SELECT test4.id, test5.name, test4.salary
    -> FROM test4, test5;
#成功返回
Query OK, 0 rows affected (0.03 sec)
#但我这里会返回笛卡尔积，不过就是这个流程。
-------------------------------------------------------------------------------------------------------
#基于视图创建视图
#流程一样
----------------------------------------------------------------------------------------------------
#查看视图
mysql> SHOW TABLES;
+--------------------+
| Tables_in_smartdog |
+--------------------+
| emp                |
| service_password   |
| shitu              |
| shitu1             |
| shitu2             |
| shitu4             |
| test               |
| test1              |
| test2              |
| test4              |
| test5              |
+--------------------+
11 rows in set (0.00 sec)

#查看视图结构
mysql> DESCRIBE shitu4;
+--------+---------------+------+-----+---------+-------+
| Field  | Type          | Null | Key | Default | Extra |
+--------+---------------+------+-----+---------+-------+
| id     | int           | YES  |     | NULL    |       |
| name   | varchar(15)   | YES  |     | NULL    |       |
| salary | decimal(10,2) | YES  |     | NULL    |       |
+--------+---------------+------+-----+---------+-------+
3 rows in set (0.00 sec)

#查看视图属性
mysql> SHOW TABLE STATUS LIKE 'shitu4';
+--------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+-----------+----------+----------------+---------+
| Name   | Engine | Version | Row_format | Rows | Avg_row_length | Data_length | Max_data_length | Index_length | Data_free | Auto_increment | Create_time         | Update_time | Check_time | Collation | Checksum | Create_options | Comment |
+--------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+-----------+----------+----------------+---------+
| shitu4 | NULL   |    NULL | NULL       | NULL |           NULL |        NULL |            NULL |         NULL |      NULL |           NULL | 2024-09-05 21:53:29 | NULL        | NULL       | NULL      |     NULL | NULL           | VIEW    |
+--------+--------+---------+------------+------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+-------------+------------+-----------+----------+----------------+---------+
1 row in set (0.00 sec)

#加\G
mysql> SHOW TABLE STATUS LIKE 'shitu4' \G;
*************************** 1. row ***************************
           Name: shitu4
         Engine: NULL
        Version: NULL
     Row_format: NULL
           Rows: NULL
 Avg_row_length: NULL
    Data_length: NULL
Max_data_length: NULL
   Index_length: NULL
      Data_free: NULL
 Auto_increment: NULL
    Create_time: 2024-09-05 21:53:29
    Update_time: NULL
     Check_time: NULL
      Collation: NULL
       Checksum: NULL
 Create_options: NULL
        Comment: VIEW
1 row in set (0.00 sec)
-----------------------------------------------------------------------------------------------------------
```



### 10.4 更改与删除视图

在更改视图时，会同时更改基表的对应值（需要一对一关系，如果是更改多条记录，就需满足所有的记录都在视图）。

```mysql
mysql> SELECT *
    -> FROM shitu2;
+------+-------+----------+
| id   | NAME  | sal      |
+------+-------+----------+
|   11 | mmas  | 12000.00 |
|   13 | affad |  5557.00 |
+------+-------+----------+
2 rows in set (0.00 sec)

mysql> UPDATE shitu2
    -> SET sal = 24444
    -> WHERE id = 11;
Query OK, 1 row affected (0.03 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT *
    -> FROM shitu2;
+------+-------+----------+
| id   | NAME  | sal      |
+------+-------+----------+
|   11 | mmas  | 24444.00 |
|   13 | affad |  5557.00 |
+------+-------+----------+
2 rows in set (0.00 sec)
#已经更改
```

在删除视图的数据时，基表里的数据也会被删除

```mysql
mysql> DROP VIEW shitu1;
Query OK, 0 rows affected (0.03 sec)
#更安全的做法就加IF EXISTS
mysql> DROP VIEW IF EXISTS shitu1;
Query OK, 0 rows affected (0.03 sec)
```

## 十二、 存储过程与函数

### 12.1 存储过程

#### 12.1.1 理解

一组预先编译的SQL语句的封装。存储过程存储在服务器上，需要执行时，就向服务器发送调用命令，服务器就将一系列SQL语句执行。



#### 12.1.2 分类

- 没有参数（无参数无返回）
- 带IN（有参数）
- 带OUT（有返回）
- 带IN与OUT（有参数有返回）



#### 12.1.3 创建存储方式（调用）

- 无参数

```mysql
mysql> DELIMITER $#将结束符换位$，否则无法在下面用;
mysql> CREATE PROCEDURE select_data()
    -> BEGIN
    -> SELECT *
    -> FROM test4;
    -> END $
#请求成功！
Query OK, 0 rows affected (0.04 sec)
mysql> DELIMITER ;
```

- 带OUT

```mysql
mysql> DELIMITER $
mysql> CREATE PROCEDURE show_min_sal()
    -> BEGIN
    -> ^C
mysql> CREATE PROCEDURE show_min_sal(OUT mn DECIMAL(10,2))#传参时要将其类型传入
    -> BEGIN
    -> SELECT MIN(salary) INTO mn #将MIN传进去
    -> FROM test4;
    -> END $
Query OK, 0 rows affected (0.03 sec)
#请求成功！
#查看
```

- 带IN

```mysql
mysql> DELIMITER $
mysql> CREATE PROCEDURE find_sal(IN username VARCHAR(15))
    -> BEGIN
    -> SELECT salary
    -> FROM test4
    -> WHERE name = username;
    -> END $
Query OK, 0 rows affected (0.03 sec)
#创建成功
#调用
mysql> CALL find_sal('affad')$
+---------+
| salary  |
+---------+
| 5557.00 |
+---------+
1 row in set (0.00 sec)
Query OK, 0 rows affected (0.00 sec)
----------------------------------------------------------------------------------------------------------
#用变量调用
mysql> SET @name = 'mmas'$#设置变量name
Query OK, 0 rows affected (0.00 sec)

mysql> CALL find_sal(@name)$ # 用CALL调用
+----------+
| salary   |
+----------+
| 24444.00 |
+----------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)
```

- 带IN与OUT

```mysql
mysql> CREATE PROCEDURE show_salary(IN username VARCHAR(10) ,OUT sal DECIMAL(10,2))
    -> BEGIN
    -> SELECT salary INTO sal
    -> FROM test4
    -> WHERE name = username;
    -> END $
Query OK, 0 rows affected (0.03 sec)
```



### 12.2 存储函数

用户的自定义函数

#### 12.2.1 创建函数

