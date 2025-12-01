from basic import Register
from main_parts.Fetch import *
from main_parts.Decode import decode
from main_parts.Execute import execute
from main_parts.Memory import *
from main_parts.Write_back import write_back
from assembler import assemble
"""创建寄存器并定义其编号"""
rax = Register()
rcx = Register()
rdx = Register()
rbx = Register()
rsp = Register()
rbp = Register()
rsi = Register()
rdi = Register()
r8 = Register()
r9 = Register()
r10 = Register()
r11 = Register()
r12 = Register()
r13 = Register()
r14 = Register()
no_reg = Register()
reg = {(0, 0, 0, 0): rax, (0, 0, 0, 1): rcx, (0, 0, 1, 0): rdx, (0, 0, 1, 1): rbx,
       (0, 1, 0, 0): rsp, (0, 1, 0, 1): rbp, (0, 1, 1, 0): rsi, (0, 1, 1, 1): rdi,
       (1, 0, 0, 0): r8, (1, 0, 0, 1): r9, (1, 0, 1, 0): r10, (1, 0, 1, 1): r11,
       (1, 1, 0, 0): r12, (1, 1, 0, 1): r13, (1, 1, 1, 0): r14, (1, 1, 1, 1): no_reg}
"""零、符号和溢出条件码"""
ZF = 0
SF = 0
OF = 0
CC = [ZF, SF, OF]
Stat = [0, 0]  #状态码
PC = Bin(64)  #程序计数器
rax.from_decimal(0)
rcx.from_decimal(0)
rsp.num = assemble().num #初始化栈指针
"""寄存器重命名"""
P0 = Register()
P1 = Register()
P2 = Register()
P3 = Register()
P4 = Register()
empty_names = [P0,P1,P2,P3,P4] #空闲的物理寄存器
value_key = {} #寄存器与物理寄存器的对应关系
reg_renaming = [empty_names, value_key]
"""初始化流水线寄存器"""
begin_stat = [0,0]
begin_code = Bin(4)
begin_code.num = [0,0,0,1]
Cnd = 1
begin_num64 = Bin(64)
begin_reg = Bin(4)
begin_reg.num = [1,1,1,1]
begin_CC = [0,0,0]
D_data = (begin_stat, begin_code, begin_code, begin_reg, begin_reg, begin_num64, begin_num64)
E_data = (begin_stat,begin_code,begin_code,begin_num64,begin_num64,begin_num64,begin_reg.num,begin_reg.num)
M_data = (begin_stat, begin_code, Cnd, begin_num64, begin_num64, begin_reg.num, begin_reg.num, begin_CC)
W_data = (begin_stat, begin_code, begin_num64, begin_num64, begin_reg.num, begin_reg.num)
while True:
    print(f"rax.num = {rax.to_decimal()}")
    print(f"rdi.num = {rdi.to_decimal()}")
    print(f"rsi.num = {rsi.to_decimal()}")
    print(PC.num)
    #i = input("Press enter to continue...")
    #if i == "q":
        #break
    D_data, E_data, M_data, W_data, F_data = fetch(PC), decode(D_data, reg), execute(E_data, CC), memory(M_data), write_back(W_data,reg)
    """分支预测错误的处理"""
    CC = M_data[7]
    if W_data[0] == [0, 1]:
        break
    Cnd = M_data[2]
    if D_data[1].num == [1,0,0,1]: #ret
        """插入三个bubble"""
        for i in range(3):
            D_data, E_data, M_data, W_data, F_data = (begin_stat, begin_code, begin_code, begin_reg, begin_reg, begin_num64, begin_num64),\
            decode(D_data, reg), execute(E_data, CC), memory(M_data), write_back(W_data, reg)
    if (M_data[1].num == [0,1,1,1]) and (not Cnd):
        M_valA = M_data[4] #读出下一条指令的地址
        PC.modify(M_valA)
        D_data = fetch(PC)
        D_data, E_data = fetch(PC), decode(D_data, reg) #重新写入正确指令
    elif W_data[1].num == [1, 0, 0, 1]:
        W_valM = W_data[3]
        PC.modify(W_valM)
print(f"rax.num = {rax.to_decimal()}")
print(f"rdi.num = {rdi.to_decimal()}")
print(f"rsi.num = {rsi.to_decimal()}")
