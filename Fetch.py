"""取指"""
"""从内存读取指令字节，地址为PC的值"""
from pathlib import Path
from basic import *
def fetch(PC):
    icode = Bin(4)
    ifun = Bin(4)
    try:
        with open('Memory.txt', 'r') as file:
            pass
    except FileNotFoundError:
        print('The Memory.txt file was not found.')
        exit(0)
    else:
        with open('Memory.txt', 'r') as file:
            for line in file:
                if line[:8] == ''.join(map(str,PC.num)):  #寻找程序计数器对应的指令
                    command = list(line)
                    del command[:9] #提取出指令部分
                    command = list(map(int, command)) #将字符列表转化为整型列表
                    for i in range(4):
                        icode.num[i] = command.pop(0)

                    """提取指令中的信息"""
                    if len(command) == 4 and\
                    (icode.num == [0,0,0,0]
                    or icode.num == [0,0,0,1]
                    or icode.num == [1,0,0,1]): #当代码为halt,nop或ret
                        if command == [0,0,0,0]:
                             return [0,0],icode.num #输出AOK状态码及icode
                        else:
                             return [1,1],icode.num #输出INS状态码
                    elif len(command) == 12 and\
                    (icode.num == [1,0,1,0]
                    or icode.num == [1,0,1,1]): #当代码为pushq或popq
                        rA = [1,1,1,1]
                        if command[:4] == [0,0,0,0] and command[-4:] == [1,1,1,1]:
                            del command[:4]
                            del command[-4:] #剩余寄存器编号
                            if command == [1,1,1,1]: #无寄存器
                                return [1, 1], icode.num, rA #输出INS状态码
                            else:
                                rA = command
                                return [0,0], icode.num, rA #输出AOK状态码、icode和寄存器编号
                        else:
                            return [1,1], icode.num, rA #输出INS状态码



