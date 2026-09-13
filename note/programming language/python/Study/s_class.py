# Python 运用类

# 类定义
class MyClass1:
    # 属性
    # 方法
    pass

# 实例化
myclass1 = MyClass1()

# 属性
class MyClass2:
    # 类属性
    ID = 1
    # 私有类属性
    __PRIVATE_ID = 0

    def __init__(self,name,age):
        # 实例属性
        self.name = name
        self.age = age
        # 私有实例属性
        self.__private_pwd = 1222131

# 类属性赋值
MyClass2.NEWID = 21

# 实例化 MyClass2
# 位置传参与关键字传参
myclass2 = MyClass2("Tim", age=12)

# 实例属性赋值
myclass2.date = 22

print("--------------------------------------------------")
# 访问类属性
print("类访问类属性：MyClass2 的类属性 ID =",MyClass2.ID)
print("实例访问类属性：MyClass2 的类属性 ID =",myclass2.ID)
# 访问赋值类属性
print("赋值类属性：MyClass2 创建的新类属性 NEWID =", MyClass2.NEWID )
# 访问实例属性
print("实例访问实例属性：myclass2 的实例属性 name =",myclass2.name)
print("实例访问实例属性：：myclass2 的实例属性 age =",myclass2.age)
# 访问赋值实例属性
print("赋值实例属性：myclass2 创建的新实例属性 date =", myclass2.date)
print("--------------------------------------------------")

# 删除属性
del myclass2.date

# 方法
class MyClass3:
    # 实例方法
    def inst_print(self, msg):
        print("实例方法打印：", msg)

    # 类方法
    @classmethod
    def class_print(cls,msg):
        print("类方法打印：", msg)

    # 静态方法
    @staticmethod
    def static_method(msg):
        print("静态方法打印：",msg)

# 实例化 myclass3
myclass3 = MyClass3()

print("--------------------------------------------------")
# 调用实例方法
myclass3.inst_print("myclass3 打印的")
# 调用类方法
myclass3.class_print("myclass3 打印的")
MyClass3.class_print("MyClass3 打印的")
## 调用静态方法
myclass3.static_method("myclass3 打印的")
MyClass3.static_method("MyClass3 打印的")
print("--------------------------------------------------")

# 重写特殊方法（魔术方法）
class MyClass4:
    # 限制属性
    __slots__ = ['name', 'age', 'pid', 'time', 'desc']

    # 公开属性接口
    def __dir__(self):
        return ['name']

    # 重写 __new__()
    def __new__(cls, *args, **kwargs):
        print("执行 __new__()")
        # 必须调用 父类的 __new__(cls) 进行原来的操作
        instance = super().__new__(cls)
        return instance

    # 重写 __init__()
    def __init__(self, name, age, pid, time, desc):
        print("执行 __init__()")
        self.name = name
        self.age = age
        self.pid = pid
        self.time = time
        self.desc = desc

    # 重写 __str__()
    def __str__(self):
        return "执行 __str__()"

    # 重写 __del__()
    def __del__(self):
        print("执行 __del__()")

myclass4 = MyClass4("Tom", 22, 12111, 2022, "myclass4")

print(myclass4)
print(dir(myclass4))
del myclass4
print("--------------------------------------------------")

# 继承
# 单继承
# 父类
class People:
    # 父类属性
    ID = 1
    PID = 1001
    def __init__(self,name,age):
        self.name = name
        self.age = age

    # 父类方法
    def say(self):
        print("我是 People.")

    def hello(self):
        print("Hello!")

# 子类
class Adult(People):
    # 重写类属性
    PID = 1002
    # 添加类属性
    PPID = 1000000

    # 重写方法
    def __init__(self, name, age, addr, birth):
        # 继承父类的实例属性
        super().__init__(name,age)

        # 添加实例属性
        self.addr = addr
        self.birth = birth
    def say(self):
        print("我是 Adult.")


p = People("Tom", 12)
a = Adult("David", 11, "London", "2011-11-12")

# 多继承
class Women(People):
    GENDER = "female"

class Teacher(Adult, Women):
    # 添加属性
    TID = "T1"
    # 重写属性


    # 添加方法
    def teach(self):
        print("Lesson is on!")
    # 重写方法
    def say(self):
        # 使用父类方法
        print("我是 Teacher.")
        print("这是我的父类方法")
        super().say()
        Women.say(self)


t = Teacher("Amy", 22, "Shanghai", "2004-12-11")

print("--------------------------------------------------")
# 属性继承、添加、重写
print("People 属性：", People.ID, People.PID, p.name, p.age)
print("Adult 属性：", Adult.ID, Adult.PID, Adult.PPID, a.name, a.age, a.addr, a.birth)
print("Teacher 属性：", Teacher.ID, Teacher.PID, Teacher.PPID,t.name, t.age, t.addr, t.birth)
# 方法继承与重写
p.say()
p.hello()
a.say()
a.hello()
t.say()
t.hello()
t.teach()
print("--------------------------------------------------")

# 多态
from abc import ABC,abstractmethod
# 创建抽象类
class Animal(ABC):
    @abstractmethod
    def say(self):
        pass

# 实现抽象方法
class Cat(Animal):
    def say(self):
        print("Cat is say..")

class Dog(Animal):
    def say(self):
        print("Dog is say..")

class Bird(Animal):
    def say(self):
        print("Bird is say..")

def whosay(animal):
    animal.say()

cat = Cat()
dog = Dog()
bird = Bird()

print("--------------------------------------------------")
whosay(cat)
whosay(dog)
whosay(bird)
print("--------------------------------------------------")