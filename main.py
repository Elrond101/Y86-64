from basic import *
"""创建寄存器并定义其编号"""
rax = Register((0,0,0,0))
rcx = Register((0,0,0,1))
rdx = Register((0,0,1,0))
rbx = Register((0,0,1,1))
rsp = Register((0,1,0,0))
rbp = Register((0,1,0,1))
rsi = Register((0,1,1,0))
rdi = Register((0,1,1,1))
r8 = Register((1,0,0,0))
r9 = Register((1,0,0,1))
r10 = Register((1,0,1,0))
r11 = Register((1,0,1,1))
r12 = Register((1,1,0,0))
r13 = Register((1,1,0,1))
r14 = Register((1,1,1,0))
ZF = 0
SF = 0
OF = 0
Stat = [0,0]#状态码
rax.num[63] = 1
print(rax.num,rcx.num)
rcx.modify(rax)
print(rax.num,rcx.num)