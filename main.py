import time
from CLI.help import *
from CLI.list import *
from CLI.assemble import *
from assembler import assemble
from assembly_line import *
from Memory_to_hex import *
from open_file import open_file

title = r"""
══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════


    ██╗   ██╗███████╗████████╗ ██████╗███████╗██████╗ ███████╗    ██╗   ██╗ █████╗  ██████╗        ██████╗ ██╗  ██╗
    ██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔══██╗██╔════╝    ╚██╗ ██╔╝██╔══██╗██╔════╝       ██╔════╝ ██║  ██║
    ██║   ██║███████╗   ██║   ██║     █████╗  ██████╔╝███████╗     ╚████╔╝ ╚█████╔╝███████╗ █████╗███████╗ ███████║
    ██║   ██║╚════██║   ██║   ██║     ██╔══╝  ██╔══██╗╚════██║      ╚██╔╝  ██╔══██╗██╔═══██╗╚════╝██╔═══██╗╚════██║
    ╚██████╔╝███████║   ██║   ╚██████╗███████╗██║  ██║███████║       ██║   ╚█████╔╝╚██████╔╝      ╚██████╔╝     ██║
     ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝       ╚═╝    ╚════╝  ╚═════╝        ╚═════╝      ╚═╝
                                                                                                               
                                                                                            programmed by 张玮霖
══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""
print(title)
print("本程序用于计算机专业学生深入了解计算机的Y86-64系统，目前已模拟出了流水线的基本功能")
print("本项目的github仓库：https://github.com/Elrond101/USTCers_Y86-64")
print("如需帮助，请输入help")
"""操作标识"""
operate_tag = 0
hex_tag = 0
input_tag = 0
time_tag = 0
pc_tag = 0
reg_tag = 0
com_tag = 0
all_tag = 0
"""while True:
    command = input()
    if command == "help":
        help_all()
    elif command[:4] == "help":
        if command[-4:] == "list":
            help_list()
        elif command[-8:] == "assemble":
            help_assemble()
    elif command[:8] == "assemble":
        if "-no" in command:

    else:
        print("指令错误")"""
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
rsp.num = assemble().num  #初始化栈指针
convert_memory_file()
"""初始化流水线寄存器"""
begin_stat = [0, 0]
begin_code = Bin(4)
begin_code.num = [0, 0, 0, 1]
Cnd = 1
begin_num64 = Bin(64)
begin_reg = [1, 1, 1, 1]
begin_CC = [0, 0, 0]
D_data = (begin_stat, begin_code, begin_code, begin_reg, begin_reg, begin_num64, begin_num64)
E_data = (begin_stat, begin_code, begin_code, begin_num64, begin_num64, begin_num64, begin_reg, begin_reg)
M_data = (begin_stat, begin_code, Cnd, begin_num64, begin_num64, begin_reg, begin_reg, begin_CC)
W_data = (begin_stat, begin_code, begin_num64, begin_num64, begin_reg, begin_reg)
F_data = begin_stat
data = [D_data, E_data, M_data, W_data, F_data, PC, CC, Cnd, reg]
tag = [1]
#open_file("Assembly Language.txt")
while tag[0]:
    #i = input("Press enter to continue...")
    #if i == "q":
    #break
    print(f"rax.num = {rax.to_decimal()}")
    print(f"rdi.num = {rdi.to_decimal()}")
    print(f"rbx.num = {rbx.to_decimal()}")
    print(f"r12.num = {r12.to_decimal()}")
    print(''.join(map(str, rsp.num)))
    print(''.join(map(str, PC.num)))
    l = Lines(data)
    tag = l.one_step()
    data = tag[1][:]
print(f"rax.num = {rax.to_decimal()}")
print(f"rdi.num = {rdi.to_decimal()}")
print(f"rbx.num = {rbx.to_decimal()}")
print(f"rdx.num = {rdx.to_decimal()}")
