
---
### 一、概念
#### 1.1 用途

处理字符串与内存的标准头文件
#### 1.2 `size_t`

`size_t` 是一种无符号整数类型，为`unsigned int`

---
### 二、字符串函数
#### 2.1 `strlen()`

计算字符串的长度，不包括结尾的空字符`\0`

函数接口
```c
size_t strlen(const char *s);
```

>参数：
>`s`：指向字符串的指针

>返回值：
>字符串的长度
#### 2.2 `strcpy()`

将字符串`src`拷贝到`dest`中，包括结尾的空字符`\0`

函数接口
```c
char *strcpy(char *dest, const char *src);
```

>参数：
> `dest`：目标字符串的指针
> `src`：源字符串的指针

>返回值：
>返回目标字符串的指针
#### 2.3 `strncpy()`

将字符串`src`的前`n`个字符拷贝到`dest`中
如果`src`的长度小于`n`，则在`dest`中填充空字符`\0`，直到总长度为`n`

函数接口
```c
char *strncpy(char *dest, const char *src, size_t n);
```

>参数：
>`dest`：目标字符串的指针
>`src`：源字符串的指针
>`n`：要拷贝的字符数

>返回值：
>返回目标字符串的指针

#### 2.4 `strcat()`

将字符串`src`连接到字符串`dest`的末尾

函数接口
```c
char *strcat(char *dest, const char *src);
```

>参数：
>`dest`：目标字符串的指针
>`src`：源字符串的指针

>返回值：
>返回目标字符串的指针
#### 2.5 `strncat()`

将字符串`src`的前`n`个字符连接到字符串`dest`的末尾

函数接口
```c
char *strncat(char *dest, const char *src, size_t n);
```

>参数：
>`dest`：目标字符串的指针
>`src`：源字符串的指针
>`n`：要连接的字符数

>返回值：
>返回目标字符串的指针
#### 2.6 `strcmp()`

比较两个字符串

函数接口
```c
int strcmp(const char *s1, const char *s2);
```

>参数：
>`s1`：第一个字符串的指针
>`s2`：第二个字符串的指针

>返回值：
>如果两个字符串相等，返回0
>如果`s1`小于`s2`，返回负值
>如果`s1`大于`s2`，返回正值
#### 2.7 `strncmp()`

比较两个字符串的前`n`个字符

函数接口
```c
int strncmp(const char *s1, const char *s2, size_t n);
```

>参数：
>`s1`：第一个字符串的指针
>`s2`：第二个字符串的指针
>`n`：要比较的字符数

>返回值：
>如果两个字符串的前`n`个字符相等，返回0
>如果`s1`小于`s2`，返回负值
>如果`s1`大于`s2`，返回正值
#### 2.8 `strstr()`

在字符串`haystack`中查找子字符串`needle`

函数接口
```c
char *strstr(const char *haystack, const char *needle);
```

>参数：
>`haystack`：主字符串的指针
>`needle`：子字符串的指针

>返回值：
>如果找到子字符串，返回子字符串的首字符指针
>如果未找到子字符串，返回`NULL`
#### 2.9 `strchr()`

在字符串`s`中查找字符`c`的第一次出现。

函数接口
```c
char *strchr(const char *s, int c);
```

>参数：
>`s`：字符串的指针
>`c`：要查找的字符

>返回值：
>如果找到字符，返回字符的指针
>如果未找到字符，返回`NULL`

---
### 三、内存函数
#### 3.1 `memset()`

将`s`指向的内存区域的前`n`个字节设置为`c`

函数接口
```c
void *memset(void *s, int c, size_t n);
```

>参数：
>`s`：指向内存区域的指针
>`c`：要设置的值

>返回值：
>无
#### 3.2 `memcpy()`

将`src`指向的内存区域的前`n`个字节复制到`dest`指向的内存区域

函数接口
```c
void *memcpy(void *dest, const void *src, size_t n);
```

>参数：
>`dest`：目标内存区域的指针
>`src`：源内存区域的指针
>`n`：要复制的字节数

>返回值：
>返回目标内存区域的指针

#### 3.3 `memmove()`

将`src`指向的内存区域的前`n`个字节移动到`dest`指向的内存区域
与`memcpy`不同的是，`memmove`可以处理内存区域重叠的情况

函数接口
```c
void *memmove(void *dest, const void *src, size_t n);
```

>参数：
>`dest`：目标内存区域的指针
>`src`：源内存区域的指针
>`n`：要移动的字节数

>返回值：
>返回目标内存区域的指针
#### 3.4 `memcmp()`

比较两个内存区域的前`n`个字节

函数接口
```c
int memcmp(const void *s1, const void *s2, size_t n);
```

>参数：
>`s1`：第一个内存区域的指针
>`s2`：第二个内存区域的指针
>`n`：要比较的字节数

>返回值：
>如果两个内存区域相等，返回`0`
>如果`s1`小于`s2`，返回负值
>如果`s1`大于`s2`，返回正值