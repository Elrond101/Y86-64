"""执行"""

from basic import *
def alu(alufun,aluA,aluB,set_cc,CC):
    ZF = CC[0]
    SF = CC[1]
    OF = CC[2]
    Stat = [0,0]
    if alufun.num == [0,0,0,0]: #加法
        result = add(aluB,aluA)
        if set_cc:
            ZF = (result[0].num == [0 for a in range(64)])
            SF = result[0].num[0]
            OF = result[1]
    elif alufun.num == [0,0,0,1]: #减法
        result = sub(aluB,aluA)
        if set_cc:
            ZF = (result[0].num == [0 for a in range(64)])
            SF = result[0].num[0]
            OF = result[1]
    elif alufun.num == [0,0,1,0]: #与
        result = and_bin(aluB,aluA)
        if set_cc:
            ZF = (result[0].num == [0 for a in range(64)])
            SF = result[0].num[0]
            OF = result[1]
    elif alufun.num == [0,0,1,1]: #异或
        result = xor_bin(aluB,aluA)
        if set_cc:
            ZF = (result[0].num == [0 for a in range(64)])
            SF = result[0].num[0]
            OF = result[1]
    else:
        result = (aluA,0)
        Stat = [1,1] #INS
    return Stat,result[0],[ZF,SF,OF]
def cond(CC,ifun): #用于计算是否传送
    ZF = CC[0]
    SF = CC[1]
    OF = CC[2]
    if ifun.num == [0,0,0,1]: #小于等于时跳转
        return ((SF != OF) or ZF == 1)
    elif ifun.num == [0,0,1,0]: #小于时跳转
        return (SF != OF)
    elif ifun.num == [0,0,1,1]: #相等时跳转
        return (ZF == 1)
    elif ifun.num == [0,1,0,0]: #不相等时跳转
        return (ZF == 0)
    elif ifun.num == [0,1,0,1]: #大于等于时跳转
        return (SF == OF)
    elif ifun.num == [0,1,1,0]: #大于时跳转
        return ((SF == OF) and ZF == 0)
    else: return 1
def execute(decode,CC): #decode为decode函数的返回值，内容为(Stat,icode,ifun,valC,valA,valB,dstE,dstM)
    Stat = decode[0]
    icode = decode[1]
    Cnd = 1
    valE =  Bin(64)
    valA = decode[4]
    dstE = decode[6]
    dstM = decode[7]

    ifun = decode[2]
    valC = decode[3]
    valB = decode[5]

    """设置aluA的值"""
    if icode.num in[[0,0,1,0],[0,1,1,0]]:
        aluA = valA
    elif icode.num in[[0,0,1,1],[0,1,0,0],[0,1,0,1]]:
        aluA = valC
    elif icode.num in [[1,0,0,1],[1,0,1,1]]:
        aluA = Bin(64)
        aluA.from_decimal(8) #将aluA设置为8
    elif icode.num in [[1,0,0,0],[1,0,1,0]]:
        aluA = Bin(64)
        aluA.from_decimal(-8)
    else:
        aluA = Bin(64)

    """设置aluB的值"""
    if icode.num in [[0,1,0,0],[0,1,0,1],[0,1,1,0],[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1]]:
        aluB = valB
    else:
        aluB = Bin(64)
    """设置alufun的值"""
    if icode.num == [0,1,1,0]:
        alufun = ifun
    else:
        alufun = Bin(4) #设置为add的fun

    """设置set_cc的值"""
    if icode.num == [0,1,1,0]:
        set_cc = True
    else:
        set_cc = False

    result = alu(alufun,aluA,aluB,set_cc,CC)
    if result[0] == [1, 1]:  # INS
        exit(0) #后期需修改这部分代码
    else:
        valE = result[1]
        if icode.num == [0,1,1,1]:
            Cnd = cond(CC, ifun)
        CC = result[2]
        """重设dstE"""
        if icode.num == [0,0,1,0] and (not Cnd): #cmovXX
            dstE = [1,1,1,1]
    return Stat, icode, Cnd, valE, valA, dstE, dstM, CC