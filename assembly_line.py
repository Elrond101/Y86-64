from main_parts.Fetch import *
from main_parts.Decode import decode
from main_parts.Execute import execute
from main_parts.Memory import *
from main_parts.Write_back import write_back
class Lines:
    def __init__(self,data): #data = [D_data, E_data, M_data, W_data, F_data, PC, CC, Cnd, reg]
        self.D_data = data[0]
        self.E_data = data[1]
        self.M_data = data[2]
        self.W_data = data[3]
        self.F_data = data[4]
        self.PC = data[5]
        self.CC = data[6]
        self.Cnd = data[7]
        self.reg = data[8]
        self.begin_stat = [0, 0]
        self.begin_code = Bin(4)
        self.begin_code.num = [0, 0, 0, 1]
        self.begin_num64 = Bin(64)
        self.begin_reg = [1,1,1,1]
        self.empty_D_data = (self.begin_stat, self.begin_code, self.begin_code,
                             self.begin_reg, self.begin_reg, self.begin_num64, self.begin_num64)
    def insert_bubble(self):
        self.D_data, self.E_data, self.M_data, self.W_data, self.F_data = \
        self.empty_D_data, decode(self.D_data, self.reg), execute(self.E_data, self.CC), memory(self.M_data), write_back(self.W_data, self.reg)
    def one_step(self):
        rsp_need = [[1,0,0,0],[1,0,0,1],[1,0,1,0],[1,0,1,1]]
        if (self.D_data[3] != [1, 1, 1, 1] and self.D_data[3] in [self.E_data[6], self.E_data[7], self.M_data[5], self.M_data[6], self.W_data[4],self.W_data[5]]) \
        or (self.D_data[4] != [1, 1, 1, 1] and self.D_data[4] in [self.E_data[6], self.E_data[7], self.M_data[5], self.M_data[6], self.W_data[4],self.W_data[5]])\
        or (self.D_data[1].num in rsp_need and (self.E_data[1].num in rsp_need or self.M_data[1].num in rsp_need or self.W_data[1].num in rsp_need)):
                self.E_data, self.M_data, self.W_data, self.F_data = \
                (self.begin_stat,self.begin_code,self.begin_code,self.begin_num64,self.begin_num64,self.begin_num64,self.begin_reg,self.begin_reg),\
                 execute(self.E_data, self.CC), memory(self.M_data), write_back(self.W_data, self.reg)
        elif self.D_data[1].num == [1, 0, 0, 1] or self.E_data[1].num == [1, 0, 0, 1] or self.M_data[1].num == [1, 0, 0, 1]:
            self.insert_bubble()
        else:
            self.D_data, self.E_data, self.M_data, self.W_data, self.F_data =\
            fetch(self.PC), decode(self.D_data, self.reg), execute(self.E_data, self.CC), memory(self.M_data), write_back(self.W_data, self.reg)
        self.CC = self.M_data[7]
        if self.W_data[0] == [0, 1]:
            return [0,[self.D_data, self.E_data, self.M_data, self.W_data, self.F_data, self.PC, self.CC, self.Cnd, self.reg]]
        if self.M_data[1].num in [[0, 1, 1, 1], [0, 0, 1, 0]]:
            self.Cnd = self.M_data[2]
        if (self.M_data[1].num == [0, 1, 1, 1]) and (not self.Cnd):
            M_valA = self.M_data[4]  # 读出下一条指令的地址
            self.PC.modify(M_valA)
            self.D_data = fetch(self.PC)
            self.D_data, self.E_data = fetch(self.PC), decode(self.D_data, self.reg)  # 重新写入正确指令
        elif self.W_data[1].num == [1, 0, 0, 1]:
            W_valM = self.W_data[3]
            self.PC.modify(W_valM)
        return [1,[self.D_data, self.E_data, self.M_data, self.W_data, self.F_data, self.PC, self.CC, self.Cnd, self.reg]]