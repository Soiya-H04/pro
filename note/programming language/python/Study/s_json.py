# json 文件在 Python 中运用
# 导入 json 库
import json

# Python 转换为 json 格式使用 json.dumps()
# 1. 字典
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

# 2. 列表
list1 = [1,2,3]
json_list = json.dumps(list1)
print("content:",json_list)
print("type:",type(json_list))

# 3. 元组
tuple1 =(1,2,)
json_tuple = json.dumps(tuple1)
print("content:",json_tuple)
print("type:",type(json_tuple))

# 4. 数值
num1 = 21
json_num = json.dumps(num1)
print("content:",json_num)
print("type:",type(json_num))

# 5. 字符串
str1 = "string"
json_str = json.dumps(str1)
print("content:",json_str)
print("type:",type(json_str))


# json 转换为 Python 格式使用 json.loads()
# 1. 字典
dict2 = json.loads(json_dict)
print("content:",dict2)
print("type:",type(dict2))

# 2. 列表
list2 = json.loads(json_list)
print("content:",list2)
print("type:",type(list2))

# 3. 元组
tuple2 = json.loads(json_tuple)
print("content:",tuple2)
print("type:",type(tuple2))

# 4. 数值
num2 = json.loads(json_num)
print("content:",num2)
print("type:",type(num2))

# 5. 字符串
str2 = json.loads(json_str)
print("content:",str2)
print("type:",type(str2))