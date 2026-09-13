# Python 的闭包
# 基本闭包
# 外部函数参数与变量都能在内部函数使用
def outer_func(time):
    x = 20
    def inner_func(y):
        # 内部函数引用外部函数的变量 x 与 time
        return f"{time}-{x + y}"

    # 返回内部函数（未执行）
    return inner_func
# 不用定义一个全局变量
a = outer_func("12:00")

print("--------------------------------------------------")
print(a(2))
print("--------------------------------------------------")

# 修饰器
