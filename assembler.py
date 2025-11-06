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
    file.write(''.join([''.join(map(str,PC.num)),':',command,'\n']))
def assemble():
    PC = Bin(64)
    need_regids = 0
    need_valC = 0
    label = {} #用于记录函数开头和跳转标签
    address = {} #用于记录label在文件中的位置
    try:
        with open('Memory.txt', 'w') as memory_file:
            pass
    except FileNotFoundError:
        print('The Memory.txt file was not found.')
        exit(0)
    else:
        with open('Memory.txt', 'w') as memory_file:
            try:
                with open('Assembly Language.txt', 'r') as file:
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
                            statement = line.strip().split() #将指令以空格分隔开
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
                                elif statement[0][-1:] == ':':
                                    label[statement[0].rstrip().rstrip(':')] = ''.join(map(str,PC.num))
                                    continue
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
                                    elif statement[0] == "addq":
                                        command = "01100000" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "subq":
                                        command = "01100001" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "andq":
                                        command = "01100010" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "xorq":
                                        command = "01100011" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "cmovle":
                                        command = "00100001" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "cmovl":
                                        command = "00100010" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "cmove":
                                        command = "00100011" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "cmovne":
                                        command = "00100100" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "cmovge":
                                        command = "00100101" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    elif statement[0] == "comvg":
                                        command = "00100110" + translate_reg(statement[1].split(',')[0])\
                                                  + translate_reg(statement[1].split(',')[1])
                                    else:
                                        invalid_error()
                                elif statement[0] in ["jmp","jle","jl","je",
                                                      "jne","jge","jg","call"]:
                                    need_valC = 1
                                    need_regids = 0
                                    if statement[0] == "call":
                                        command = "10000000"
                                    elif statement[0] == "jmp":
                                        command = "01110000"
                                    elif statement[0] == "jle":
                                        command = "01110001"
                                    elif statement[0] == "jl":
                                        command = "01110010"
                                    elif statement[0] == "je":
                                        command = "01110011"
                                    elif statement[0] == "jne":
                                        command = "01110100"
                                    elif statement[0] == "jge":
                                        command = "01110101"
                                    elif statement[0] == "jg":
                                        command = "01110110"
                                    else:
                                        invalid_error()
                                    memory_file.write(''.join([''.join(map(str, PC.num)), ':', command]))
                                    position = memory_file.tell()
                                    address[statement[1]] = position  # 记录下跳转的位置，最后进行修改
                                    command = '0' * 64  # 为地址留下位置
                                    memory_file.write(''.join([command, '\n']))
                                    PC = add_PC(PC, need_regids, need_valC)
                                    continue
                                elif statement[0] in ["irmovq","rmmovq","mrmovq"]:
                                    need_regids = 1
                                    need_valC = 1
                                    if statement[0] == "irmovq":
                                        imm = Bin(64) #立即数
                                        imm.from_decimal(int(statement[1].split(',')[0].lstrip('$')))
                                        command = "001100001111" + translate_reg(statement[1].split(',')[1]) +\
                                                  ''.join(map(str, imm.num))
                                    elif statement[0] == "rmmovq":
                                        bias = Bin(64)
                                        if statement[1].split(',')[1].split('(')[1]:
                                            bias.from_decimal(int(statement[1].split(',')[1].split('(')[0]))
                                        command = "01000000" + translate_reg(statement[1].split(',')[0]) +\
                                                  translate_reg(statement[1].split(',')[1].split('(')[1].rstrip(')')) +\
                                                  ''.join(map(str, bias.num))
                                        """这一段丑得令人发指"""
                                    elif statement[0] == "mrmovq":
                                        bias = Bin(64)
                                        if statement[1].split(',')[0].split('(')[1]:
                                            bias.from_decimal(int(statement[1].split(',')[0].split('(')[0]))
                                        command = "01010000" + translate_reg(statement[1].split(',')[1]) +\
                                                  translate_reg(statement[1].split(',')[0].split('(')[1].rstrip(')')) +\
                                                  ''.join(map(str, bias.num))
                                    else:
                                        invalid_error()
                                else:
                                    invalid_error()


                        write_in(PC,command,memory_file)
                        PC = add_PC(PC,need_regids,need_valC)
                    """处理函数以及跳转标识"""
                    if label and address: #label—— name:address  address—— name:position
                        if len(label) != len(address):
                            invalid_error()
                        else:
                            l_len = len(label)
                            address_keys = list(address.keys())
                            address_values = list(address.values())
                            for i in range(l_len):
                                memory_file.seek(address_values[i])
                                memory_file.write(label[address_keys[i]])
    return PC