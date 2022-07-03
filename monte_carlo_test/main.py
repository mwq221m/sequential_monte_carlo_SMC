import numpy as np
from system_test import Element_Simulation
import matplotlib.pyplot as plt
'''生成各个元件的时间序列'''
element_m1=Element_Simulation(lamb=0.2,r=3/8760,time_limit=1e4,name='元件m1')
element_m1.simulate()
#element_m1.show_result()

element_m2=Element_Simulation(lamb=0.3,r=3/8760,time_limit=1e4,name='元件m2')
element_m2.simulate()
#element_m2.show_result()

element_m3=Element_Simulation(lamb=0.1,r=3/8760,time_limit=1e4,name='元件m3')
element_m3.simulate()
#element_m3.show_result()

element_l1=Element_Simulation(lamb=0.75,r=1/8760,time_limit=1e4,name='元件l1')
element_l1.simulate()
#element_l1.show_result()
'''对需要修正的元件的时间序列进行修正'''
time_list1=element_m1.time_list.copy()
time_list2=element_m2.time_list.copy()
time_list3=element_m3.time_list.copy()
time_list4=element_l1.time_list.copy()
for i in range(int(len(time_list2)/2)):
    time_list2[2*i+1]=time_list2[2*i]+(time_list2[2*i+1]-time_list2[2*i])*(1/6)#故障修复时间的修正

for i in range(int(len(time_list3)/2)):
    time_list3[2*i+1]=time_list3[2*i]+(time_list3[2*i+1]-time_list3[2*i])*(1/6)#故障修复时间的修正

time_list=np.sort(time_list1+time_list2+time_list3+time_list4)
sum_temp=0
for i in range(int(len(time_list)/2)):
    sum_temp+=time_list[2*i+1]-time_list[2*i]
U_a=sum_temp/1e4
#U_a=(1e4*(element_m1.U+element_m2.U/6+element_m3.U/6+element_l1.U)/(1e4))#已经假定各元件的失效时间没有重叠 并非严格按照时间序列计算

print('元件a不可用率 单位小时/年为%s'%(U_a*8760))

lamb_a=((element_m1.m+element_m2.m+element_m3.m+element_l1.m)/(1e4*(1-U_a)))
print('元件a实验失效率为%s'%lamb_a)

r_a=(1e4*U_a/(element_m1.m+element_m2.m+element_m3.m+element_l1.m))
print('元件a实验修复时间 单位小时/年为%s'%(r_a*8760))

'''当元件本身失效率等参数服从一定概率分布时更有必要使用该方法'''
'''注意时间序列的修复时间可能需要的修正'''





#time_list=np.sort(element_l1.time_list)
#time_list=np.sort(element_m1.time_list+element_m2.time_list+element_m3.time_list+element_l1.time_list)#将时间序列合并 计算相关概率分布


#求解不可用率概率分布 结果的期望值与点估计不符合
U_list=[]
for i in range(int(len(time_list) / 2)):
    if i == 0:
        u = (time_list[2 * i + 1] - time_list[2 * i]) / time_list[2 * i]
    else:
        u = (time_list[2 * i + 1] - time_list[2 * i]) / (
                    time_list[2 * i + 1] - time_list[2 * i - 1])
    u *= 8760
    U_list.append(u)
#print(U_list)
#print(np.mean(U_list))
#print(np.max(U_list))
U_list=np.array(U_list)
#test_num=len(np.where(U_list<0.3)[0])/len(U_list)
#print(test_num)
temp_num=0.1
max_num=10#取得过大数值计算不稳定 可能刚好在较大数值处有一个点分布在那里
count0=0
U_distribution_list=[]
while temp_num<max_num:

    count=len(np.where(U_list<temp_num)[0])#例如小于0.1的统一认定为分布为0.1 因此期望可能偏大
    #print(count)
    U_distribution_list.append(count-count0)
    #print(count-count0)
    count0=count
    temp_num+=0.1
#print(U_distribution_list)
U_distribution_list=np.array(U_distribution_list)
U_distribution_list=U_distribution_list/len(U_list)
#print(U_distribution_list)
x_list=np.linspace(0.1,10,100)
sum_temp=np.sum(U_distribution_list*x_list)
print(sum_temp)
plt.figure()
plt.bar(x_list,U_distribution_list)
plt.show()

plt.figure()
plt.scatter(x_list,U_distribution_list,s=5)
plt.show()





