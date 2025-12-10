def help_all():
    content = """
    有关某个指令的帮助，请输入help 命令名。如help assemble
    assemble                        汇编（默认同时运行）代码
    list                            显示所有可用的汇编代码
    operate                         直接运行Memory.txt中的二进制代码
    """
    print(content)
def help_list():
    print("显示所有可用的汇编代码")
def help_assemble():
    content = """
    汇编（默认同时运行）Assembly Language.txt中的汇编代码
    用法：assemble [-no] [-h] [-i|-t xxx [-pc] [-r] [-c]] [-all]
    
        没有参数                     按默认方式汇编并运行程序
        -no                        不运行程序，只编译输出二进制程序
        -h                         生成十六进制代码，输出到Memory_Hex.txt
        -i                         时钟将以用户输入enter为标志进入下一个周期，也就是enter进入下一步。q键退出
        -t xxx                     将时钟周期的间隙设为xxx秒，也就是每隔xxx秒执行下一步
        -pc                        每一步显示当前取指阶段的指令的地址，以十六进制显示
        -r                         每一步显示被修改过的所有寄存器的值，以十进制显示
        -c                         每一步显示当前指令的内容
        -all                       运行结束后显示所有寄存器的值，默认显示修改过的所有寄存器的值
    """
    print(content)
def help_operate():
    content = """
    运行Memory.txt中的二进制代码并忽略汇编代码 
    用法：operate [-h] [-i|-t xxx [-pc] [-r] [-c]] [-all]
    
        没有参数                     按默认方式运行程序
        -h                         生成十六进制代码，输出到Memory_Hex.txt
        -i                         时钟将以用户输入enter为标志进入下一个周期，也就是enter进入下一步。q键退出
        -t xxx                     将时钟周期的间隙设为xxx秒，也就是每隔xxx秒执行下一步
        -pc                        每一步显示当前取指阶段的指令的地址，以十六进制显示
        -r                         每一步显示被修改过的所有寄存器的值，以十进制显示
        -c                         每一步显示当前指令的内容
        -all                       运行结束后显示所有寄存器的值，默认显示修改过的所有寄存器的值
    """
    print(content)