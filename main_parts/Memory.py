from basic import *
def memory(execute): #execute为execute函数的返回值，内容为(Stat, icode, Cnd, valE, valA, dstE, dstM, CC)
    Stat = execute[0]
    icode = execute[1]
    valE = execute[3]
    valA = execute[4]
    dstE = execute[5]
    dstM = execute[6]
    """设置读写信号"""
    mem_read = (icode.num in [[0,1,0,1],[1,0,0,1],[1,0,1,1]])
    mem_write = (icode.num in [[0,1,0,0],[1,0,1,0],[1,0,0,0]])
    """设置内存地址"""
    if icode.num in [[0,1,0,0],[0,1,0,1],[1,0,0,0],[1,0,1,0]]:
        mem_addr = valE
    elif icode.num in [[1,0,0,1],[1,0,1,1]]:
        mem_addr = valA
    else:
        mem_addr = Bin(64)
    """设置内存内容"""
    mem_data = valA
    """更新Stat"""
    if icode.num == [0,0,0,0]:
        Stat = [0,1] #HLT
    elif mem_addr.num[0] == 1:
        Stat = [1,0] #ADR

    valM = Bin(64)
    # 将内存地址转换为二进制字符串
    addr_str = ''.join(map(str, mem_addr.num))
    if mem_read:
        with open('Memory.txt', 'r') as file:
            for line in file:
                """这里存在一个很大的问题，就是如果访问地址是在两个地址之间，无法读取，未来需要修复"""
                if line[:64] == ''.join(map(str,mem_addr.num)):  #寻找内存地址对应的指令
                    data = list(map(int,list(line)[65:129]))
                    valM.num = data
    elif mem_write:
        with open('Memory.txt', 'r+b') as file:
            # 移动到文件开头
            file.seek(0)

            found = False
            data_str = ''.join(map(str, mem_data.num))
            new_line = f"{addr_str}:{data_str}\n".encode('utf-8')

            while True:
                # 记录当前行开始位置
                line_start = file.tell()

                # 读取一行
                line_bytes = file.readline()
                if not line_bytes:  # 到达文件末尾
                    break

                # 解码为字符串
                try:
                    line = line_bytes.decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue

                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue

                # 检查是否是有效的地址:数据行
                if ':' in line:
                    parts = line.split(':', 1)
                    file_addr = parts[0].strip()

                    # 如果找到匹配的地址
                    if file_addr == addr_str:
                        found = True
                        # 移动到行开始位置
                        file.seek(line_start)
                        # 写入新行（确保长度相同）
                        if len(new_line) > len(line_bytes):
                            # 新行更长，需要截断
                            file.write(new_line[:len(line_bytes)])
                        else:
                            # 新行更短或等长，填充空格
                            file.write(new_line.ljust(len(line_bytes)))
                        break

    return Stat, icode, valE, valM, dstE, dstM