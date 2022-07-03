import numpy as np
import matplotlib.pyplot as plt

lamb=0.2;r=3/8760
time_limit=100*100#提高精度最直接方法就是提高采样年数
time=0
temp_list=[]
flag=1
num=1e6#作图时采样精度 不要影响到故障修复时间显示就行
ran=np.random.random()
#print(ran)
while time<time_limit:
    ran=np.random.random()
    if flag==1:
        dt=-1/lamb*np.log(ran)
        #print(dt)
        flag=0
        time += dt
        temp_list.append(time)

    if flag==0:
        dt=-r*np.log(ran)
        flag=1
        time += dt
        temp_list.append(time)

#print(temp_list)
'''#使用画图采样的方式逻辑简单 但运行时间过久
def f(x):
    length=len(temp_list)
    for i in range(int(length/2)):
        start=temp_list[2*i]
        #print('start',start)
        end=temp_list[2*i+1]
        #print('end',end)
        #print('start<x<end',start<x<end)
        #print('start<x and x<end',start<x and x<end)
        #print('start<x',start<x)
        #print(len(start<x))
        if start<x<end:
            return 0
    return 1

x=np.linspace(0,time_limit,int(num))

y=np.vectorize(f)(x)
plt.figure()
plt.plot(x,y)
plt.show()
zero_num=len(np.where(y==0)[0])
U=zero_num/num
print('不可用率',U)
m=len(temp_list)/2

lamb_test=m/(time_limit*(1-U))
print('实验得到的失效率',lamb_test)

r_test=time_limit*U/m
print('实验得到修复时间 单位小时',r_test*8760)

'''
time_sum=0
for i in range(int(len(temp_list)/2)):
    start=temp_list[2*i]
    end=temp_list[2*i+1]
    time_sum+=end-start
U=time_sum/time_limit
print('实验可用率',U)

m=len(temp_list)/2
lamb_test=m/(time_limit*(1-U))
print('实验失效率',lamb_test)

r_test=time_limit*U/m
print('实验得到修复时间 单位小时',r_test*8760)








