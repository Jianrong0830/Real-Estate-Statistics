import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score
from functions import *

# 讀取資料集到 DataFrame
data = pd.read_csv("Data/新北市/住宅大樓/三重區.csv")

# 提取特徵和目標變數
features = data[['屋齡(年)', '主要車站通勤時間(分鐘)', '醫院距離(公里)', '學校距離(公里)', '半徑1km內公共及商業場域(個)']]
target = data['每坪房價(萬元)']

# 分割資料集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.4, random_state=42)

# 建立線性迴歸模型
model = LinearRegression()
model.fit(X_train, y_train)

# 使用測試集進行預測
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
evs = explained_variance_score(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print('--------------------------------')
print("均方誤差：", mse)
print("平均絕對誤差：", mae)
print("解釋方差分數：", evs)
print("R平方：", r2)
print("係數：", model.coef_)
print("截距：", model.intercept_)
print('--------------------------------')
'''
address=input('Address:')
age=input('Age:')

# 假設有新資料，以 DataFrame 格式表示
new_data = pd.DataFrame({
    '屋齡(年)': [age],
    '主要車站通勤時間(分鐘)': [convert_to_minutes(get_station_commute(address))],
    '醫院距離(公里)': [get_hospital_dis(address)],
    '學校距離(公里)': [get_school_dis(address)],
    '半徑1km內公共及商業場域(個)': [get_establishment(address)]
})

predicted_prices = model.predict(new_data)
print("預測的每坪房價：", predicted_prices)
'''