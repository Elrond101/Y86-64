"""执行"""

from basic import *
def execute(decode,CC): #decode为decode函数的返回值，内容为(Stat,icode,ifun,valC,valA,valB,dstE,dstM)
    Stat = decode[0]
    icode = decode[1]
