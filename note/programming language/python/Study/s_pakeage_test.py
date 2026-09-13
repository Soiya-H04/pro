# 导入这个包的 my_module1 所有函数
from my_pakeage.my_module1 import *
# 导入子包的 my_module3
from my_pakeage.sub_pakeage import my_module3

module1_hello()
module1_print()

my_module3.module3_hello()
my_module3.module3_print()