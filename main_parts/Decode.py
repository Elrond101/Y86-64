"""译码"""
from basic import *
def Select_A(icode,valA,valP):
    if icode.num in [[0,1,1,1],[1,0,0,0]]:
        return valP
    else:
        return valA
def decode(fetch,reg): #fetch为fetch函数的返回值，0为Stat，1为icode，2为ifun，3为rA，4为rB，5为valC,6为valP
    Stat = fetch[0]
    icode = fetch[1]
    ifun = fetch[2]
    rA = fetch[3]
    rB = fetch[4]
    valC = fetch[5]
    valP = fetch[6]
    valA = Bin(64)
    valB = Bin(64)
    srcA = [1,1,1,1]
    srcB = [1,1,1,1]
    dstE = [1,1,1,1]
    dstM = [1,1,1,1]
    """设置srcA的值"""
    if icode.num in [[0,0,1,0],[0,1,0,0],[0,1,1,0],[1,0,1,0]]:
        srcA = rA
    elif icode.num in [[1,0,0,1],[1,0,1,1]]:
        srcA = [0,1,0,0] #rsp
    """设置srcB的值"""
    if icode.num in [[0,1,0,0],[0,1,0,1],[0,1,1,0]]:
        srcB = rB
    elif icode.num in [[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1]]:
        srcB = [0,1,0,0] #rsp
    """设置dstE的值"""
    if icode.num in [[0,0,1,0],[0,0,1,1],[0,1,1,0]]:
        dstE = rB
    elif icode.num in [[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1]]:
        dstE = [0,1,0,0] #rsp
    """设置dstM的值"""
    if icode.num in [[0,1,0,1],[1,0,1,1]]:
        dstM = rA

    """设置valA的值"""
    valA.num = reg[tuple(srcA[:])].num
    valA = Select_A(icode,valA,valP)
    """设置valB的值"""
    valB.num = reg[tuple(srcB[:])].num
    return Stat,icode,ifun,valC,valA,valB,dstE,dstM
