# JSON  文件(json)

## 一、概念

**JSON（JavaScript Object Notation）是一种轻量级的数据交换格式**。

 **JSON** 文件的合法内容可以是：

-   **单个值**（字符串、数字、布尔值、null）
-   **数组** `[]`
-   **对象** `{}`（键名必须有""括起）
-   **任何有效的 JSON 值**

例1： json 对象

```json
{
  "字符串": "Hello World",
  "数字": 42,
  "布尔值": true,
  "null": null,
  "数组": [1, 2, 3],
  "对象": {
    "嵌套键": "值"
  }
}
```

例2：json 数组

```json
["苹果", "香蕉", "橙子"]
```

例3：数值

```json
12
ture
null
"hello"
```

## 二、与 Python 关系

在 Python 中 json 文件的格式为字符串 `string`，相互转换使用 `json `库

```python
import json
```

### 2.1 Python 转 json

```python
# Python 转换为 json 格式使用 json.dumps()
# 1. 字典 -> str
dict1 = {
  "字符串": "Hello World",
  "数字": 42,
  "布尔值": True,
  "null": None, # Python 中 Null 为 None
  "数组": [1, 2, 3],
  "对象": {
    "嵌套键": "值"
  }
}
json_dict = json.dumps(dict1)
print("content:",json_dict)
print("type:",type(json_dict))

# 2. 列表 -> str
list1 = [1,2,3]
json_list = json.dumps(list1)
print("content:",json_list)
print("type:",type(json_list))

# 3. 元组 -> str
tuple1 =(1,2,)
json_tuple = json.dumps(tuple1)
print("content:",json_tuple)
print("type:",type(json_tuple))

# 4. 数值 -> str
num1 = 21
json_num = json.dumps(num1)
print("content:",json_num)
print("type:",type(json_num))

# 5. 字符串 -> str
str1 = "string"
json_str = json.dumps(str1)
print("content:",json_str)
print("type:",type(json_str))
```

## 2.2 json 转 Python

```python
# json 转换为 Python 格式使用 json.loads()
# 1. str -> 字典
dict2 = json.loads(json_dict)
print("content:",dict2)
print("type:",type(dict2))

# 2. str -> 列表
list2 = json.loads(json_list)
print("content:",list2)
print("type:",type(list2))

# 3. str -> 列表
tuple2 = json.loads(json_tuple)
print("content:",tuple2)
print("type:",type(tuple2))

# 4. str -> 数值
num2 = json.loads(json_num)
print("content:",num2)
print("type:",type(num2))

# 5. str -> 字符串
str2 = json.loads(json_str)
print("content:",str2)
print("type:",type(str2))
```

## 2.3 总结

json 在 Python 里是 string 类型，但注意元组转换为 json 再转换回的是列表





