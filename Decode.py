"""译码"""
from basic import *
def decode(fetch): #fetch为fetch函数的返回值，0为Stat，1为icode，2为ifun，3为rA，4为rB，5为64位二进制数
    valA = Bin(64)
    valB = Bin(64)
    valC = Bin(64)
    if fetch[1] == [0,0,1,0] or\
    fetch[1] == [0,1,0,0] or\
    fetch[1] == [0,1,0,0]: #rrmovq,rmmovq,mrmovq

