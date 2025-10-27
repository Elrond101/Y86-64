"""取指"""

"""从内存读取指令字节，地址为PC的值"""
from pathlib import Path
from basic import *
def predict_PC(PC,need_regids,need_valC):
    bits8 = Bin(64)
    bits64 = Bin(64)
    if need_regids:
        bits8.num = bits8.from_decimal(8)
    if need_valC:
        bits64.num = bits64.from_decimal(64)
    return add(PC, add(bits8, bits64)[0])[0]
"""这里在以后要加入溢出判断"""
def fetch(PC):
    Stat = [0,0]
    icode = Bin(4)
    ifun = Bin(4)
    rA = [1,1,1,1]
    rB = [1,1,1,1]
    val_C = Bin(64)
    val_P= PC
    instr_valid = 1 #是否合法
    need_regids = 0 #是否需要寄存器指示符
    need_valC = 0 #是否需要常数字
    try:
        with open('Memory.txt', 'r') as file:
            pass
    except FileNotFoundError:
        print('The Memory.txt file was not found.')
        exit(0)
    else:
        with open('Memory.txt', 'r') as file:
            """此处可用seek函数进行优化"""
            for line in file:
                if line[:64] == ''.join(map(str,PC.num)):  #寻找程序计数器对应的指令
                    command = list(line)
                    del command[:65] #提取出指令部分
                    command = list(map(int, command)) #将字符列表转化为整型列表
                    for i in range(4):
                        icode.num[i] = command.pop(0)

                    """提取指令中的信息"""
                    if icode.num in [[0,0,1,0],[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,0],[1,0,1,0],[1,0,1,1]]:
                        need_regids = 1
                    if icode.num in [[0,0,1,1],[0,1,0,0],[0,1,0,1],[0,1,1,1],[1,0,0,0]]:
                        need_valC = 1
                    if icode.num in [[1,1,0,0],[1,1,0,1],[1,1,1,0],[1,1,1,1]]:
                        instr_valid = 0
                    if instr_valid:
                        Stat = [0,0]
                    else:
                        Stat = [1,1]
                    ifun.num = command[:4]
                    if need_regids:
                        rA = command[4:8]
                        rB = command[8:12]
                        if need_valC:
                            val_C.num = command[12:]
                    elif need_valC:
                        val_C.num = command[4:]
                    val_P = predict_PC(PC,need_regids,need_valC)
                    return Stat,icode,ifun,rA,rB,val_C,val_P






