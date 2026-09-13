
---
### 一、概念
#### 1.1 用途

提供与时间相关的函数和宏定义
#### 1.2 `time_t`

`time_t`是一个表示时间的类型，通常用于表示从某个特定时间点（通常是1970年1月1日00:00:00 UTC，即“Unix纪元”）开始的秒数，通常是`long`类型
#### 1.3 `clock_t`

`clock_t`是一个表示时钟周期的类型，通常用于测量程序的运行时间，通常是`long`类型
#### 1.4 `struct tm`

`struct tm`用于表示时间的各个组成部分，具体定义为
```c
struct tm {
    int tm_sec;    // 秒，范围为 0 到 59
    int tm_min;    // 分，范围为 0 到 59
    int tm_hour;   // 小时，范围为 0 到 23
    int tm_mday;   // 一个月中的第几天，范围为 1 到 31
    int tm_mon;    // 月份，范围为 0 到 11，其中 0 表示 1 月
    int tm_year;   // 年份，从 1900 年开始计算
    int tm_wday;   // 一周中的第几天，范围为 0 到 6，其中 0 表示星期日
    int tm_yday;   // 一年中的第几天，范围为 0 到 365
    int tm_isdst;  // 夏令时标志，非零表示夏令时，零表示非夏令时
};
```
#### 1.5 字符串格式化时间

| 格式化指令 | 含义                  |
| :---- | :------------------ |
| `%Y`  | 四位数的年份              |
| `%m`  | 两位数的月份（01到12）       |
| `%d`  | 两位数的日期（01到31）       |
| `%H`  | 两位数的小时（24小时制，00到23） |
| `%M`  | 两位数的分钟（00到59）       |
| `%S`  | 两位数的秒（00到59）        |
| `%a`  | 星期几的缩写              |
| `%A`  | 星期几的全称              |
| `%b`  | 月份的缩写               |
| `%B`  | 月份的全称               |
| `%w`  | 星期几（0到6，0表示星期日）     |
| `%j`  | 一年中的第几天（001到366）    |
| `%p`  | 上午或下午的标识（AM或PM）     |

---
### 二、时间函数
#### 2.1 `time()`

获取当前时间

函数接口
```c
time_t time(time_t *tloc);
```

>参数：
>`tloc`：指向`time_t`类型的指针，用于存储当前时间，如果为`NULL`，则不存储

>返回值：
>成功时返回当前时间的`time_t`值，失败时返回`(time_t)-1`
#### 2.2 `localtime()`

将`time_t`值转换为本地时间

函数接口
```c
struct tm *localtime(const time_t *timep);
```

>参数：
>`timep`：指向`time_t`类型的指针，表示要转换的时间

>返回值：
>成功时返回指向`struct tm`的指针，包含本地时间信息，失败时返回`NULL`
#### 2.3 `gmtime()`

将`time_t`值转换为UTC时间（格林威治时间）

函数接口
```c
struct tm *gmtime(const time_t *timep);
```

>参数：
>`timep`：指向`time_t`类型的指针，表示要转换的时间

>返回值：
>成功时返回指向`struct tm`的指针，包含UTC时间信息，失败时返回`NULL`
#### 2.4 `mktime()`

将`struct tm`结构转换为`time_t`值

函数接口
```c
time_t mktime(struct tm *timeptr);
```

>参数：
>`timeptr`：指向`struct tm`的指针，表示要转换的时间结构

>返回值：
>成功时返回对应的`time_t`值，失败时返回`(time_t)-1`
#### 2.5 `strftime()`

将时间格式化为字符串

函数接口
```c
size_t strftime(char *s, size_t maxsize, const char *format, const struct tm *timeptr);
```

>参数：
>`s`：目标字符串缓冲区
>`maxsize`：缓冲区的最大长度（以字节为单位）
>`format`：格式化字符串
>`timeptr`：指向`struct tm`的指针，表示要格式化的时间

>返回值：
>成功时返回写入的字符数（不包括结尾的`\0`），失败时返回`0`
#### 2.6 `asctime()`

将`struct tm`结构转换为字符串

函数接口
```c
char *asctime(const struct tm *timeptr);
```

>参数：
>`timeptr`：指向`struct tm`的指针，表示要转换的时间

>返回值：
>返回一个指向静态字符串的指针，包含时间信息
#### 2.7 `clock()`

获取程序运行时间

函数接口
```c
clock_t clock(void);
```

>参数：
>无

>返回值：
>返回从程序开始运行到当前的时钟周期数