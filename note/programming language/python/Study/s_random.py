# 随机数在 Python 的运用
import random

# 设置随机种子，可以使随机结果可重现
random.seed(12.221)

# 一、随机数生成
# 1. random() - 生成[0.0, 1.0)范围内的随机浮点数
print("random():", random.random())

# 2. uniform(a, b) - 生成[a, b]范围内的随机浮点数
print("uniform(1, 10):", random.uniform(1, 10))

# 3. randint(a, b) - 生成[a, b]范围内的随机整数
print("randint(1, 10):", random.randint(1, 10))

# 4. randrange(start, stop[, step]) - 从range(start, stop, step)中随机选择
print("randrange(0, 100, 5):", random.randrange(0, 100, 5))

# 二 、随机序列生成
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 1. choice(seq) - 从序列中随机选择一个元素
print("choice:", random.choice(my_list))

# 2. choices(seq, weights=None, k=1) - 从序列中随机选择k个元素（可重复）
print("choices with weights:", random.choices(my_list, k=3))

# 3. sample(seq, k) - 从序列中随机选择k个不重复的元素
print("sample:", random.sample(my_list, k=3))

# 4. shuffle(seq) - 将序列随机打乱（原地修改）
random.shuffle(my_list)
print("shuffled list:", my_list)