import pandas as pd
import os

total=0

def cnt(city,htype):
    global total
    path = 'Data/{}/{}/'.format(city,htype)
    files = os.listdir(path)
    
    for file in files:
        num=len(pd.read_csv(path+file))
        total+=num
        print('{}：{}筆'.format(file[:-4],num))
    print()

cities=['台北市','新北市','基隆市','桃園市']
htypes=['公寓','住宅大樓','透天厝','華夏']

for city in cities:
    print('--------------------{}--------------------'.format(city))
    
    for htype in htypes:
        print('*****{}*****'.format(htype))
        cnt(city,htype)

print('---------------------------------------------')
print('總共：{}筆'.format(total))