"""定义基本二进制移位运算与加减法"""
from unittest import result

from logic import *
class Bin:
    def __init__(self):
        self.num=[0 for a in range(64)]#创建一个64位的二进制数
    """左移操作"""
    def left_mov(self):
        for i in range(62):
            self.num[i] = self.num[i+1]
        self.num[63] = 0
        return self.num
    """逻辑右移"""
    def l_right_mov(self):
        for i in range(62):
            self.num[63-i] = self.num[62-i]
        self.num[0] = 0
        return self.num
    """算数右移"""
    def c_right_mov(self):
        for i in range(63):
            self.num[63-i] = self.num[62-i]
        self.num[0] = self.num[1]
        return self.num
    """补码"""
    def comp(self):
        for i in range(64):
            self.num[i] = not self.num[i]
class Register(Bin):
    def __init__(self,No):
        super().__init__()
        self.No = No
    def modify(self,bin):
        for i in range(64):
            self.num[i] = bin.num[i]

"""全加器"""
def full_add(bit1,bit2,co_in):
    return XOR(co_in,XOR(bit1,bit2)),OR(AND(co_in,XOR(bit1,bit2)),AND(bit1,bit2))

"""计算两个二进制数加法"""
def add(bin1,bin2):
    co = 0
    result = Bin()
    for i in range(63):
        result.num[63-i],co = full_add(bin1.num[63-i],bin2.num[63-i],co)
    result.num[0] = full_add(bin1.num[0],bin2.num[0],co)[0]
    return result,co


"""半减器"""
def half_sub(bit1, bit2):
    # 差 = bit1 XOR bit2
    diff = XOR(bit1, bit2)
    # 借位 = NOT(bit1) AND bit2
    borrow = AND(NOT(bit1), bit2)
    return diff, borrow
"""全减器"""
def full_sub(bit1, bit2, borrow_in):
    diff1, borrow1 = half_sub(bit1, bit2)
    diff, borrow2 = half_sub(diff1, borrow_in)
    borrow_out = OR(borrow1, borrow2)
    return diff, borrow_out
"""计算两个二进制数减法"""
def sub(bin1, bin2):
    borrow = 0
    result = Bin()
    for i in range(63, -1, -1):
        # 使用全减器计算当前位
        result.num[i], borrow = full_sub(bin1.num[i], bin2.num[i], borrow)
    return result, borrow


