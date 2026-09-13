import time
# 当前目录下的 file_test.txt 文件路径
file_path = r"D:\a_Study Note\Planguage\Python\Study\file_test.txt"

# 打开文件写入
file = open(file_path,'w+',encoding="UTF-8")
# 查看指针位置
print(file.tell())

# 写入单行
file.write("hello,I'm Tom\n")

# 将内容先写进文件内
file.flush()
# 暂停 20 s
time.sleep(3)

# 写入列表，每元素一行
write_lines = ["first line\n", "second line\n", "third line\n"]
file.writelines(write_lines)

# 获得文件结尾位置
file_tail = file.tell()

# 移动指针位置到开头
file.seek(0)

# 重新写入(会替代 hell0,I'm Tom\n)，字符一样，其他地方不会更改
file.write("hello,I'm Amy\n")

# 移动到结尾
file.seek(file_tail)

# 继续写入
file.write("hello,I'm David\n")

# 关闭文件
file.close()


# 使用 with 打开文件读取
with open(file_path,'r',encoding="utf-8") as file:
    # 查看指针位置
    print(file.tell())

    # 读取指针后一个字符
    print(file.read(1))
    # 读取指针后一行字符
    print(file.readline())
    # 读取指针后所有行字符，组成列表
    print(file.readlines())

    # 回到文件开头
    file.seek(0)

    # 读取指针后所有字符
    print(file.read())