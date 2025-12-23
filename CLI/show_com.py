from basic import *
def show_com(icode,ifun):
    def bits_to_int(bits):
        result = 0
        for bit in bits:
            result = (result << 1) | bit
        return result

    icode_num = bits_to_int(icode.num)
    ifun_num = bits_to_int(ifun.num)

    # 指令映射表
    instruction_map = {
        (0, 0): "halt",
        (1, 0): "nop",
        (1, 1): "nop",
        (2, 0): "rrmovq",
        (2, 1): "cmovle",
        (2, 2): "cmovl",
        (2, 3): "cmove",
        (2, 4): "cmovne",
        (2, 5): "cmovge",
        (2, 6): "cmovg",
        (3, 0): "irmovq",
        (4, 0): "rmmovq",
        (5, 0): "mrmovq",
        (6, 0): "addq",
        (6, 1): "subq",
        (6, 2): "andq",
        (6, 3): "xorq",
        (7, 0): "jmp",
        (7, 1): "jle",
        (7, 2): "jl",
        (7, 3): "je",
        (7, 4): "jne",
        (7, 5): "jge",
        (7, 6): "jg",
        (8, 0): "call",
        (9, 0): "ret",
        (10, 0): "pushq",
        (11, 0): "popq",
    }

    key = (icode_num, ifun_num)
    print(instruction_map[key])