
import datetime

# print(datetime.datetime.now)


def wapper(func):
    print("jinruwapper")
    def inner():
        print("inner1")
        func()
        print("inner2")
        return "asd"
    return inner


@wapper
def a():
    print("a")

def b():
    print("b")

s = a()
print(s)
print("aaaaaaaaaaaaaaaaa")
ret = wapper(b)
s = ret()
print(s)

