"""取指"""
from xml.dom.pulldom import DOMEventStream

"""从内存读取指令字节，地址为PC的值"""
from pathlib import Path
from basic import *
def fetch(PC):
    icode = Bin(4)
    ifun = Bin(4)
    rA = [1,1,1,1]
    rB = [1,1,1,1]
    emp_bin = Bin(64)
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
                    if len(command) == 4 and\
                    (icode.num == [0,0,0,0]
                    or icode.num == [0,0,0,1]
                    or icode.num == [1,0,0,1]): #当代码为halt,nop或ret
                        if command == [0,0,0,0]:
                             return [0, 0], icode, ifun, rA, rB, emp_bin #输出AOK状态码及icode
                        else:
                             return [1, 1], icode, ifun, rA, rB, emp_bin #输出INS状态码
                    elif len(command) == 12 and\
                    (icode.num == [1,0,1,0]
                    or icode.num == [1,0,1,1]): #当代码为pushq或popq
                        if command[:4] == [0,0,0,0] and command[-4:] == [1,1,1,1]:
                            del command[:4]
                            del command[-4:] #剩余寄存器编号
                            rA = command
                            return [0, 0], icode, ifun, rA, rB, emp_bin #输出AOK状态码、icode和寄存器编号
                        else:
                            return [1, 1], icode, ifun, rA, rB, emp_bin #输出INS状态码
                    elif len(command) == 12 and\
                    icode.num == [0,0,1,0] and\
                    command[:4] == [0,0,0,0]: #rrmovq
                        rA = command[4:8]
                        rB = command[-4:]
                        return [0, 0], icode, ifun, rA, rB, emp_bin #输出AOK状态码、icode、rA和rB
                    elif len(command) == 76 and\
                    icode.num == [0,0,1,1]: #irmovq
                        imm = Bin(64) #储存立即数
                        if command[:4] != [0,0,0,0]:
                            return [1, 1], icode, ifun, rA, rB, imm #输出INS状态码
                        else:
                            del command[:8]
                            rB = command[:4]
                            imm.num = command[-64:]
                            return [0, 0], icode, ifun, rA, rB, imm #输出AOK状态码、icode、rB和立即数
                    elif len(command) == 76 and\
                    (icode.num == [0,1,0,0] or
                    icode.num == [0,1,0,1]): #rmmovq和mrmovq
                        des = Bin(64)
                        if command[:4] != [0,0,0,0]:
                            return [1, 1], icode, ifun, rA, rB, des #输出INS状态码
                        else:
                            rA = command[4:8]
                            rB = command[8:12]
                            des.num = command[-64:]
                            return [0, 0], icode, ifun, rA, rB, des #输出AOK状态码、icode、rA、rB和偏移量
                    elif len(command) == 68 and\
                    icode.num == [1,0,0,0]: #call
                        des = Bin(64)
                        if command[:4] != [0,0,0,0]:
                            return [1, 1], icode, ifun, rA, rB, des
                        else:
                            des.num = command[-64:]
                            return [0, 0], icode, ifun, rA, rB, des
                    elif len(command) == 12 and \
                    (icode.num == [0,0,1,0] or
                    icode.num == [0,1,1,0]): #OPq和cmovXX
                        ifun.num = command[:4]
                        rA = command[4:8]
                        rB = command[8:12]
                        return [0, 0], icode, ifun, rA, rB, emp_bin #输出AOK状态码、icode、ifun、rA和rB
                    elif len(command) == 68 and\
                    icode.num == [0,1,1,1]: #jXX
                        ifun.num = command[:4]
                        des = Bin(64)
                        des.num = command[-64:]
                        return [0, 0], icode, ifun, rA, rB, des #输出AOK状态码、icode、ifun和目标地址
                    else:
                        return [1, 1], icode, ifun, rA, rB, emp_bin #输出INS状态码





