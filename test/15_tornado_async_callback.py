# coding:utf-8
import time
import thread


def async(f):
    def fun(callback):
        print "开始执行A"
        time.sleep(5)
        print "执行A完毕"
        callback("异步调用完成")
    thread.start_new_thread(fun, (f,))


def on_finish(ret):
    print ret


def testa():
    async(on_finish)


def testb():
    print "开始执行B"
    print "执行B完毕"


if __name__ == "__main__":
    testa()
    testb()
    while 1:
        pass
    print "ok"