from basic import *
def create_heap(PC,file):
    file.seek(0,2) #将光标移动到文件末尾
    for i in range(10):
        file.write("\n")
    mask = Bin(64)
    num_128 = Bin(64)
    eight = Bin(64)
    eight.from_decimal(8)
    empty_data = Bin(64)
    num_128.from_decimal(128)
    for i in range(61):
        mask.num[i] = 1
    heap_PC = and_bin(mask,PC)[0]
    heap_PC.num = add(heap_PC,num_128)[0].num #将地址按8字节对齐
    for i in range(32):
        file.write(f"{''.join(map(str, heap_PC.num))}:{''.join(map(str, empty_data.num))}\n")
        heap_PC.num = add(heap_PC,eight)[0].num
    return heap_PC
def create_stack(PC,file):
    stack_PC = Bin(64)
    stack_PC.num = PC.num
    for i in range(10):
        file.write("\n")
    num_128 = Bin(64)
    eight = Bin(64)
    eight.from_decimal(8)
    empty_data = Bin(64)
    num_128.from_decimal(128)
    for i in range(31):
        file.write(f"{''.join(map(str, stack_PC.num))}:{''.join(map(str, empty_data.num))}\n")
        stack_PC.num = add(stack_PC, eight)[0].num
    file.write(f"{''.join(map(str, stack_PC.num))}:{''.join(map(str, empty_data.num))}\n")
    return stack_PC