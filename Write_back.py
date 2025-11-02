from basic import *
def write_back(memory,reg): #memory为memory函数的返回值，内容为(Stat, icode, valE, valM, dstE, dstM)
    Stat = memory[0]
    valE = memory[2]
    valM = memory[3]
    dstE = memory[4]
    dstM = memory[5]

    """将数据写回对应寄存器"""
    reg[tuple(dstE)].modify(valE)
    reg[tuple(dstM)].modify(valM)
