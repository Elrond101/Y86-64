from basic import *
from Fetch import add_PC
from pathlib import Path
def invalid_error():
    print("Your command is invalid.")
    exit(0)
"""将寄存器名翻译为编号"""
def translate_reg(reg):
    reg_list = {"%rax": "0000", "%rcx": "0001", "%rdx": "0010",
           "%rbx": "0011", "%rsp": "0100", "%rbp": "0101",
           "%rsi": "0110", "%rdi": "0111", "%r8": "1000",
           "%r9": "1001", "%r10": "1010", "%r11": "1011",
           "%r12": "1100", "%r13": "1101", "%r14": "1110"}
    return reg_list[reg]
"""将二进制指令写入内存"""
def write_in(PC,command,file):
    file.write(''.join(map(str,PC.num)),':',command,'\n')
def assemble():
    PC = Bin(64)
    need_regids = 0
    need_valC = 0
    try:
        with open('Memory.txt', 'w') as memory_file:
            pass
    except FileNotFoundError:
        print('The Memory.txt file was not found.')
        exit(0)
    else:
        with open('Memory.txt', 'w') as memory_file:
            try:
                with open('Assembly Language.txt', 'w') as file:
                    pass
            except FileNotFoundError:
                print('The Assembly Language.txt file was not found.')
                exit(0)
            else:
                with open('Assembly Language.txt', 'r') as file:
                    for line in file:
                        if line[0] == '#':
                            continue
                        else:
                            statement = line.split() #将指令以空格分隔开
                            if len(statement) == 0:
                                continue
                            elif len(statement) == 1:
                                need_regids = 0
                                need_valC = 0
                                if statement[0] == "halt":
                                    command = "00000000"
                                elif statement[0] == "nop":
                                    command = "00010000"
                                elif statement[0] == "ret":
                                    command = "10010000"
                                else:
                                    invalid_error()
                            elif len(statement) == 2:
                                if statement[0] in ["rrmovq","addq","subq",
                                                    "andq","xorq","cmovle",
                                                    "cmovl","cmove","cmovne",
                                                    "cmovge","comvg","pushq",
                                                    "popq"]:
                                    need_regids = 1
                                    need_valC = 0
                                    if statement[0] == "pushq":
                                        command = "1010" + translate_reg(statement[1]) + "1111"
                                    elif statement[0] == "popq":
                                        command = "1011" + translate_reg(statement[1]) + "1111"
                                    elif statement[0] == "rrmovq":
                                        command = "00100000" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                else:
                                    invalid_error()
                        write_in(PC,command,memory_file)
                        PC = add_PC(PC,need_regids,need_valC)