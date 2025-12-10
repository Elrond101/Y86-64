def list():
    content = """
    halt                             停止处理器执行
    nop                              无操作
    rrmovq rA, rB                    寄存器到寄存器移动
    cmovle rA, rB                    条件移动当小于或等于时
    cmovl rA, rB                     条件移动当小于时
    cmove rA, rB                     条件移动当等于时
    cmovne rA, rB                    条件移动当不等于时
    cmovge rA, rB                    条件移动当大于或等于时
    cmovg rA, rB                     条件移动当大于时
    irmovq V, rB                     立即数到寄存器移动
    rmmovq rA, D(rB)                 寄存器到内存移动
    mrmovq D(rB), rA                 内存到寄存器移动
    addq rA, rB                      加法操作
    subq rA, rB                      减法操作
    andq rA, rB                      按位与操作
    xorq rA, rB                      按位异或操作
    jmp dest                         无条件跳转
    jle dest                         当小于或等于时跳转
    jl dest                          当小于时跳转
    je dest                          当等于时跳转
    jne dest                         当不等于时跳转
    jge dest                         当大于或等于时跳转
    jg dest                          当大于时跳转
    call dest                        调用函数
    ret                              从函数返回
    pushq rA                         压栈操作
    popq rA                          出栈操作
    
    寄存器列表：%rax,%rcx,%rdx,%rbx,%rsp,%rbp,%rsi,%rdi,%r8,%r9,%r10,%r11,%r12,%r13,%r14
    请确保访问内存时地址是8的倍数
    """
    print(content)