import pandas as pd
import requests
from geopy.distance import geodesic
from functions import *
import googlemaps
import os
from tqdm import tqdm

data=pd.DataFrame(columns=['建案','地址','每坪房價(萬元)','屋齡(年)','主要車站通勤時間(分鐘)','醫院距離(公里)','學校距離(公里)','半徑1km內公共及商業場域(個)'])

def run(city,htype,file):
    global data
    table=pd.read_csv('Data/{}/{}/{}'.format(city,htype,file))
    data=pd.concat([data,table])
    #table['預售屋']=[0]*len(table)
    #table['新成屋']=[0]*len(table)
    
    # 清除多餘index欄位
    columns_to_keep = ['建案','地址','每坪房價(萬元)','屋齡(年)','主要車站通勤時間(分鐘)','醫院距離(公里)','學校距離(公里)','半徑1km內公共及商業場域(個)','建案','地址','每坪房價(萬元)','屋齡(年)','主要車站通勤時間(分鐘)','醫院距離(公里)','學校距離(公里)','半徑1km內公共及商業場域(個)','預售屋']
    table=table.drop(columns=[col for col in table.columns if col not in columns_to_keep])

    # 檢查空值
    has_missing_values = table.isnull().values.any()
    if(has_missing_values):
        print('{}/{}/{}'.format(city,htype,file[:-4]))

    # 資料處理(逐列)
    l=len(table)
    success,fail=0,0
    
    for i in range(l):
        if table.loc[i,'屋齡(年)']==0 or table.loc[i,'屋齡(年)']=='0':
            table=table.drop(index=i)
        
        address=city+table.loc[i,'地址']
        try:
            table.loc[i,'地址']=address
            table.loc[i,'到主要火車站通勤時間']=get_station_commute(address)
            table.loc[i,'到醫院距離']=get_hospital_dis(address)
            table.loc[i,'到學校距離']=get_school_dis(address)
            table.loc[i,'直徑1km內商業設施數量']=get_establishment(address)
            table.loc[i,'到主要火車站通勤時間']=convert_to_minutes(table.loc[i,'到主要火車站通勤時間'])
            success+=1
        except Exception as e:
            fail+=1
            #print(f'失敗：{address} 錯誤信息：{e}')
            continue;
        
    #print("成功：{} 失敗：{}".format(success,fail))
    #table.to_csv('Data/{}/{}/{}'.format(city,htype,file),encoding='utf_8_sig',index=False)

    
cities=['台北市','新北市','基隆市','桃園市'] #'台北市','新北市','基隆市','桃園市'
htypes=['公寓','住宅大樓','透天厝','華夏'] #'公寓','住宅大樓','透天厝','華夏'

total_pre=0

for city in cities:
    print('--------------------{}--------------------'.format(city))
    
    for htype in htypes:
        print('*****{}*****'.format(htype))
        files=os.listdir('Data/{}/{}'.format(city,htype))
        l=len(files)
        cnt=0
        
        for file in files:
            cnt+=1
            print(file[:-4],'{}/{}'.format(cnt,l))
            '''
            table=pd.read_csv('Data/{}/{}/{}'.format(city,htype,file))
            pre=list(table['屋齡(年)']).count('0')+list(table['屋齡(年)']).count(0)
            print(pre)
            total_pre+=pre
            '''
            run(city,htype,file)

#print('Total:',total_pre)
data.to_csv('Data/總表.csv',encoding='utf_8_sig',index=False)
print(len(data))

