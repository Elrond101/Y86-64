import time
from CLI.help import *
from CLI.list import *
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
operate_tag = 1
hex_tag = 0
input_tag = 0
time_tag = 0
pc_tag = 0
reg_tag = 0
com_tag = 0
open_file("Assembly Language.txt")
while True:
    command = input(">>")
    if command == "help":
        help_all()
    elif command[:4] == "help":
        if command[-4:] == "list":
            help_list()
        elif command[-8:] == "assemble":
            help_assemble()
    elif command[:4] == "list":
        list()
    elif command[:8] == "assemble":
        if "-no" in command:
            operate_tag = 0
        if "-h" in command:
            hex_tag = 1
        if "-i" in command:
            input_tag = 1
        if "-pc" in command:
            pc_tag = 1
            if "-t" in command:
                time_tag = 1
                time_str = command.split("-t")[1].split()[0]
                s_time = float(time_str)
        if "-r" in command:
            reg_tag = 1
            if "-t" in command:
                time_tag = 1
                time_str = command.split("-t")[1].split()[0]
                s_time = float(time_str)
        if "-c" in command:
            com_tag = 1
            if "-t" in command:
                time_tag = 1
                time_str = command.split("-t")[1].split()[0]
                s_time = float(time_str)
        break
    elif command[:7] == "operate":
        if "-h" in command:
            hex_tag = 1
        if "-i" in command:
            input_tag = 1
        if "-t" in command:
            time_tag = 1
            time_str = command.split("-t")[1].split()[0]
            s_time = int(time_str)
        if "-pc" in command:
            pc_tag = 1
        if "-r" in command:
            reg_tag = 1
        if "-c" in command:
            com_tag = 1
        break
    else:
        print("指令错误")
"""创建寄存器并定义其编号"""
rax = Register("rax")
rcx = Register("rcx")
rdx = Register("rdx")
rbx = Register("rbx")
rsp = Register("rsp")
rbp = Register("rbp")
rsi = Register("rsi")
rdi = Register("rdi")
r8 = Register("r8")
r9 = Register("r9")
r10 = Register("r10")
r11 = Register("r11")
r12 = Register("r12")
r13 = Register("r13")
r14 = Register("r14")
no_reg = Register("no")
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
if hex_tag:
    convert_memory_file()
    open_file("Memory_Hex.txt")
if not operate_tag:
    open_file("Memory.txt")
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
if operate_tag:
    while tag[0]:
        if input_tag:
            i = input("Press enter to continue...\n")
            if i == "q":
                break
        if time_tag:
            time.sleep(s_time)
        if reg_tag:
            for r in reg.values():
                if r.to_decimal():
                    print(f"%{r.name} = {r.to_decimal()}")
        if pc_tag:
            print(f"PC:{PC.to_hex()} ")
        l = Lines(data)
        tag = l.one_step()
        data = tag[1][:]
    for r in reg.values():
        if r.to_decimal():
            print(f"%{r.name} = {r.to_decimal()}")
