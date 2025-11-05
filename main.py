from Fetch import *
from Decode import decode
from Execute import execute
from Memory import *
from Write_back import write_back

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
D_data = fetch(PC)
D_data, E_data = fetch(PC), decode(D_data, reg)
D_data, E_data, M_data = fetch(PC), decode(D_data, reg), execute(E_data, CC)
CC = M_data[7]
D_data, E_data, M_data, W_data = fetch(PC), decode(D_data, reg), execute(E_data, CC), memory(M_data)
CC = M_data[7]
while True:
    print(rax.num)
    i = input("Press enter to continue...")
    if i == "q":
        break
    D_data, E_data, M_data, W_data, F_data= fetch(PC), decode(D_data, reg), execute(E_data, CC), memory(M_data), write_back(W_data,reg)
    CC = M_data[7]
    if W_data[0] == [0, 1]:
        break
print(f"rax.num = {rax.num}")
print(f"rcx.num = {rcx.num}")
