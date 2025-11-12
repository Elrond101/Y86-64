from basic import *
from logic import *
def create_heap(PC,file):
    file.seek(0,2) #将光标移动到文件末尾
    for i in range(10):
        file.write("\n")
    mask = Bin(64)
    eight = Bin(64)
    empty_data = Bin(64)
    eight.from_decimal(8)
    for i in range(61):
        mask.num[i] = 1
    heap_PC = and_bin(mask,PC)[0]
    heap_PC = add(heap_PC,eight)[0] #将地址按8字节对齐
    for i in range(32):
        file.write(f"{''.join(map(str, heap_PC.num))}:{''.join(map(str, empty_data.num))}\n")
        heap_PC = add(heap_PC,eight)[0]
    return heap_PC
def create_stack(PC,file):
    stack_PC = PC
    for i in range(10):
        file.write("\n")
    eight = Bin(64)
    empty_data = Bin(64)
    eight.from_decimal(8)
    for i in range(31):
        file.write(f"{''.join(map(str, stack_PC.num))}:{''.join(map(str, empty_data.num))}\n")
        stack_PC = add(stack_PC, eight)[0]
    file.write(f"{''.join(map(str, stack_PC.num))}:{''.join(map(str, empty_data.num))}\n")
    return stack_PC