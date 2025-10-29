from basic import *
def memory(execute): #execute为execute函数的返回值，内容为(Stat, icode, Cnd, valE, valA, dstE, dstM, CC)
    Stat = execute[0]
    icode = execute[1]
    valE = execute[3]
    valA = execute[4]
    dstE = execute[5]
    dstM = execute[6]
    """设置读写信号"""
    mem_read = (icode.num in [[0,1,0,1],[1,0,0,1],[1,0,1,1]])
    mem_write = (icode.num in [[0,1,0,0],[1,0,1,0],[1,0,0,0]])
    """设置内存地址"""
    if icode.num in [[0,1,0,0],[0,1,0,1],[1,0,0,0],[1,0,1,0]]:
        mem_addr = valE
    elif icode.num in [[1,0,0,1],[1,0,1,1]]:
        mem_addr = valA
    else:
        mem_addr = Bin(64)
    """设置内存内容"""
    if icode.num in [[0,1,0,0],[1,0,1,0]]:
        mem_data = valA
    elif icode.num == [1,0,0,0]:
        mem_data = valP
    else:
        mem_data = Bin(64)
    """更新Stat"""
    if icode.num == [0,0,0,0]:
        Stat = [0,1] #HLT
    elif mem_addr.num[0] == 1:
        Stat = [1,0] #ADR

    valM = Bin(64)
    if mem_read:
        with open('Memory.txt', 'r') as file:
            for line in file:
                """这里存在一个很大的问题，就是如果访问地址是在两个地址之间，无法读取，未来需要修复"""
                if line[:64] == ''.join(map(str,mem_addr.num)):  #寻找内存地址对应的指令
                    data = list(line)[65:129]
                    valM.num = data
    elif mem_write:
        with open('Memory.txt', 'w+r') as file:
            for line in file:
                if line[:64] == ''.join(map(str, mem_addr.num)):
                    line.replace(line[65:129],mem_data.num)
    return Stat, icode, valE, valM, dstE, dstM