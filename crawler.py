import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

# main data table
table=pd.DataFrame(columns=['建案','地址','每坪房價(萬元)','屋齡(年)','主要車站通勤時間(分鐘)','醫院距離(公里)','學校距離(公里)','半徑1km內公共及商業場域(個)','預售屋'])

# set up driver
driver = webdriver.Chrome()
url='https://market.591.com.tw/list?regionId=1&sectionId=12&purpose=5&postType=2,8'
driver.get(url)

seen=set()
success,fail=0,0
while True:
    try:
        # scroll down to bottom
        driver.execute_script('window.scrollBy(0, 2000);')
        #driver.find_element_by_tag_name('body').send_keys(Keys.END)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for i in soup.find_all('div',class_='community-info'):
            name=i.select_one('h3').select_one('em').text
            if name in seen:
                continue
            seen.add(name)
            try:
                # 建案名稱
                name=i.select_one('h3').select_one('em').text
                # 地址
                address=None
                try:
                    address=i.select_one('p').select_one('em').find_next_sibling().text
                except:
                    address=i.select_one('p').select_one('em').text
                # 屋齡
                try:
                    age=int(i.select_one('.type-0').text[:-3])
                except:
                    try:
                        age=i.select_one('.type-0').text
                    except:
                        try:
                            age=i.select_one('.type-1').text
                        except:
                            age=i.select_one('.type-2').text
                # 每坪房價
                price=float(i.select_one('.price').select_one('span').text[:-3])
                
                info=pd.DataFrame({'建案':[name],'地址':[address],'屋齡(年)':[age],'每坪房價(萬元)':[price]})
                table=pd.concat([table,info])
                success+=1
                print("成功："+str(success),"失敗："+str(fail),name)
            except:
                fail+=1
                print('fail',name)
                continue
        '''
        if (driver.execute_script('return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;')):
            break
        '''
        sleep(0.5)
    except:
        break
print('total:',success+fail)
table.to_csv('Data/台北市/table.csv',encoding='utf_8_sig',index=False)

