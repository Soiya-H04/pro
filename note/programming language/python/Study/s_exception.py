# Python 中的异常捕获
# 基本捕获
try:
    1/0
except:
    print("1发生异常")

# 顶级捕获
try:
    1/0
except Exception:
    print("2发生异常")

# 捕获特定异常
try:
    1/0
except ZeroDivisionError:
    print("3发生异常")

# 无异常处理
try:
    1/1
except:
    print("4发生异常")
else:
    print("4未发生异常")

# 绝对处理
try:
    1/1
except:
    print("5发生异常")
else:
    print("5未发生异常")
finally:
    print("我管你有没有异常")