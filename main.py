# main.py -- put your code here!
from machine import I2C
from lsm9ds1 import LSM9DS1
from bumpy import BumpCounter
from lora_send2 import LoraSender
import time
import _thread

# import lora_send2

# import read
#
# print("Waiting for TAG")
#
# read.do_read()
#
# print("Done")

def bumpytest():
    print("Bumpytest")
    lsm = LSM9DS1(I2C(0, I2C.MASTER))
    bumpy = BumpCounter(lsm)
    def foo():
        print("foo")
        bumpy.count_bumps()
    foo()
    # _thread.start_new_thread(foo)
    return bumpy

def loratest(bumpy):
    print("LoraTest")
    sender = LoraSender()
    while True:
        jdata = '[{"nodeID":"0002","msgID":%d,"bumpCount":%d}]' % (sender.msgCnt, bumpy.bumps)
        sender.send_msg(jdata)
        time.sleep(10)

if __name__ == "__main__":
    print("Starting main tests...")
    bumpy = bumpytest()
    while True:
        print("bumps:", bumpy.bumps)
        time.sleep(5)
    # _thread.start_new_thread(loratest, [bumpy])
