"""定义基本二进制移位运算与加减法"""
from unittest import result

from logic import *
"""二进制数"""
class Bin:
    def __init__(self,n):
        self.num=[0 for a in range(n)]#创建一个n位的二进制数
        self.n = n
    """求二进制位数"""
    def get_n(self):
        return self.n
    """左移操作"""
    def left_mov(self):
        for i in range(self.n - 2):
            self.num[i] = self.num[i+1]
        self.num[self.n - 1] = 0
        return self.num
    """逻辑右移"""
    def l_right_mov(self):
        for i in range(self.n - 2):
            self.num[self.n - 1 - i] = self.num[self.n - 2 - i]
        self.num[0] = 0
        return self.num
    """算数右移"""
    def c_right_mov(self):
        for i in range(self.n - 1):
            self.num[self.n - 1 - i] = self.num[self.n - 2 - i]
        self.num[0] = self.num[1]
        return self.num
    """补码"""
    def comp(self):
        for i in range(self.n):
            self.num[i] = not self.num[i]
    """十进制转二进制"""
    def from_decimal(self, decimal_num):
        if decimal_num == 0:
            self.num = [0] * self.n
            return self.num
        temp = decimal_num
        for i in range(self.n - 1, -1, -1):
            self.num[i] = temp % 2
            temp = temp // 2
        return self.num
    """二进制转十进制"""
    def to_decimal(self):
        result = 0
        for i in range(self.n):
            result = result * 2 + self.num[i]
        return result
"""寄存器"""
class Register(Bin):
    def __init__(self):
        super().__init__(64)
    def modify(self,bin):
        for i in range(64):
            self.num[i] = bin.num[i]


"""全加器"""
def full_add(bit1,bit2,co_in):
    return XOR(co_in,XOR(bit1,bit2)),OR(AND(co_in,XOR(bit1,bit2)),AND(bit1,bit2))

"""计算两个二进制数加法"""
def add(bin1,bin2):
    co = 0
    n = bin1.get_n()
    result = Bin(n)
    for i in range(n-1):
        result.num[n-1-i],co = full_add(bin1.num[n-1-i],bin2.num[n-1-i],co)
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
    n = bin1.get_n()
    result = Bin(n)
    for i in range(n-1, -1, -1):
        # 使用全减器计算当前位
        result.num[i], borrow = full_sub(bin1.num[i], bin2.num[i], borrow)
    return result, borrow


