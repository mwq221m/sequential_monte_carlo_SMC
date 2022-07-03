import numpy as np
import matplotlib.pyplot as plt

class Element_Simulation():
    def __init__(self,lamb,r,time_limit,name):
        self.lamb=lamb
        self.r=r
        self.time=0
        self.time_limit=time_limit
        self.name=name
        self.time_list=[]
        self.U=0
        self.lamb_test=lamb
        self.m=0
        self.r_test=r
        self.U_list=[]

    def simulate(self):
        flag=1
        while self.time < self.time_limit:
            ran = np.random.random()
            if flag == 1:
                dt = -1 / self.lamb * np.log(ran)
                # print(dt)
                flag = 0
                self.time += dt
                self.time_list.append(self.time)

            if flag == 0:
                dt = -self.r * np.log(ran)
                flag = 1
                self.time += dt
                self.time_list.append(self.time)

        time_sum = 0
        for i in range(int(len(self.time_list) / 2)):
            start = self.time_list[2 * i]
            end = self.time_list[2 * i + 1]
            time_sum += end - start
        self.U = time_sum / self.time_limit

        self.m = len(self.time_list) / 2
        self.lamb_test = self.m / (self.time_limit * (1 - self.U))

        self.r_test = self.time_limit * self.U / self.m

    def show_result(self):
        print('元件名为%s'%self.name)
        #print('实验不可用率为%s'%self.U)
        print('实验不可用率 单位小时/年为%s'%(self.U*8760))
        print('实验失效率为%s'%self.lamb_test)
        print('实验修复时间（单位小时/年）为%s'%(self.r_test*8760))

    def U_series(self):#记录单个元件每一次运行循环的不可用率
        #U_list=[]
        for i in range(int(len(self.time_list) / 2)):
            if i==0:
                u=(self.time_list[2*i+1]-self.time_list[2*i])/self.time_list[2*i]
            else:
                u=(self.time_list[2*i+1]-self.time_list[2*i])/(self.time_list[2*i+1]-self.time_list[2*i-1])
            u*=8760
            self.U_list.append(u)



if __name__=='__main__':#保证测试代码不在别的文件中被调用
    element_a=Element_Simulation(lamb=0.2,r=3/8760,time_limit=1e4,name='元件a')
    element_a.simulate()
    element_a.show_result()
    element_a.U_series()
    print(element_a.U_list)



