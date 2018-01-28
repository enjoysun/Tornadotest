# coding:utf-8
import time
import thread

def testc(f):
    def wrapper(*args, **kwargs):
        cur_a = f() #返回testa的生成器
        cur_long = cur_a.next() # 返回io_long的生成器
        def fun(g):
            res = g.next() # 获取io_long生成器的yield返回值
            try:
                cur_a.send(res) # 将返回值有testa的生成器实例发送会去
            except StopIteration:
                pass
        thread.start_new_thread(fun, (cur_long,))
    return wrapper


def io_long():
    print "开始执行IO"
    time.sleep(5)
    yield "io 结果返回"
    print "执行完毕IO"

@testc
def testa():
    print "开始执行A"
    ret = yield io_long()
    print ret
    print "执行A完成"


def testb():
    print "开始执行B"
    print "执行B完毕"


if __name__ == "__main__":
    testa()
    testb()
    while 1:
        pass