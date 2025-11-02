"""定义基本二进制移位运算与加减法"""
from unittest import result

from logic import *
"""二进制数"""
class Bin:
    def __init__(self,n):
        self.num=[0 for a in range(n)]#创建一个n位的二进制数
        self.n = n
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

    """十进制转二进制（补码表示）"""

    def from_decimal(self, decimal_num):
        # 计算补码表示的范围
        min_val = -(2 ** (self.n - 1))
        max_val = (2 ** (self.n - 1)) - 1

        # 如果是非负数，直接转换
        if decimal_num >= 0:
            temp = decimal_num
            for i in range(self.n - 1, -1, -1):
                self.num[i] = temp % 2
                temp = temp // 2
        else:
            # 如果是负数，计算其补码
            # 先计算绝对值的二进制表示
            abs_value = -decimal_num
            abs_bin = [0] * self.n
            temp = abs_value
            for i in range(self.n - 1, -1, -1):
                abs_bin[i] = temp % 2
                temp = temp // 2

            # 取反
            for i in range(self.n):
                abs_bin[i] = 1 - abs_bin[i]  # 0变1，1变0

            # 加1
            carry = 1
            for i in range(self.n - 1, -1, -1):
                total = abs_bin[i] + carry
                abs_bin[i] = total % 2
                carry = total // 2

            self.num = abs_bin

        return self.num

    """二进制（补码表示）转十进制"""

    def to_decimal(self):
        # 检查符号位
        if self.num[0] == 0:
            # 正数，直接转换
            result = 0
            for i in range(self.n):
                result = result * 2 + self.num[i]
            return result
        else:
            # 负数，先取补码得到绝对值，再加负号
            # 复制当前值
            temp_bin = self.num.copy()

            # 减1
            borrow = 1
            for i in range(self.n - 1, -1, -1):
                if temp_bin[i] >= borrow:
                    temp_bin[i] -= borrow
                    borrow = 0
                    break
                else:
                    temp_bin[i] = 1
                    borrow = 1

            # 取反
            for i in range(self.n):
                temp_bin[i] = 1 - temp_bin[i]

            # 转换为十进制并加负号
            result = 0
            for i in range(self.n):
                result = result * 2 + temp_bin[i]
            return -result

    def modify(self, bin):
        for i in range(64):
            self.num[i] = bin.num[i]

"""寄存器"""
class Register(Bin):
    def __init__(self):
        super().__init__(64)


"""与操作"""
def and_bin(a,b):
    n = a.n
    result = Bin(n)
    for i in range(n):
        result.num[i] = a.num[i] and b.num[i]
    return result,0 #为了保持与加减法结果的一致

"""异或操作"""
def xor_bin(a,b):
    n = a.n
    result = Bin(n)
    for i in range(n):
        result.num[i] = a.num[i] ^ b.num[i]
    return result,0 #为了保持与加减法结果的一致

"""全加器"""
def full_add(bit1,bit2,co_in):
    return XOR(co_in,XOR(bit1,bit2)),OR(AND(co_in,XOR(bit1,bit2)),AND(bit1,bit2))

"""计算两个二进制数加法"""
def add(bin1,bin2):
    co = 0
    n = bin1.n
    result = Bin(n)

    # 保存最高位的进位输入，用于溢出检测
    co_in_msb = 0

    for i in range(n-1):
        result.num[n-1-i],co = full_add(bin1.num[n-1-i],bin2.num[n-1-i],co)
        # 记录进入最高位的进位
        if i == n-2:  # 即将计算最高位
            co_in_msb = co

    # 计算最高位
    result.num[0], co_out = full_add(bin1.num[0],bin2.num[0],co)

    # 检测有符号溢出：溢出发生在进入最高位的进位 != 从最高位的进位输出
    overflow = XOR(co_in_msb, co_out)

    return result, overflow  # 现在co表示是否有符号溢出

"""全减器"""
def full_sub(bit1, bit2, borrow_in):
    # 差 = bit1 XOR bit2 XOR borrow_in
    diff = XOR(borrow_in, XOR(bit1, bit2))
    # 借位 = (NOT(bit1) AND bit2) OR (NOT(bit1) AND borrow_in) OR (bit2 AND borrow_in)
    borrow_out = OR(OR(AND(NOT(bit1), bit2), AND(NOT(bit1), borrow_in)), AND(bit2, borrow_in))
    return diff, borrow_out

"""计算两个二进制数减法"""
def sub(bin1, bin2):
    borrow = 0
    n = bin1.n
    result = Bin(n)

    # 保存最高位的借位输入，用于溢出检测
    borrow_in_msb = 0

    for i in range(n-1, -1, -1):
        # 记录进入最高位的借位
        if i == 0:  # 即将计算最高位
            borrow_in_msb = borrow

        # 使用全减器计算当前位
        result.num[i], borrow = full_sub(bin1.num[i], bin2.num[i], borrow)

    # 检测有符号溢出：溢出发生在进入最高位的借位 != 从最高位的借位输出
    overflow = XOR(borrow_in_msb, borrow)

    return result, overflow  # 现在borrow表示是否有符号溢出


