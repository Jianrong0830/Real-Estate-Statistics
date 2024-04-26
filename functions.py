import requests
import pandas as pd
import googlemaps
import time
import overpy
from geopy.distance import geodesic

api_key='AIzaSyCVKUHDOnUU0dg9QHcCd1FNPDIoG9T0mWg'

# 取得座標
def get_house(address):
    gmaps = googlemaps.Client(key=api_key)
    result = gmaps.geocode(address)
    
    try:
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']
        return str((lat, lng))[1:-1]
    
    except:
        return None

# 取得最近主要火車站座標
def get_station(coord):
    
    stations = {"基隆": (25.133177274218074, 121.73925753974794),
                "七堵": (25.093175849469397, 121.71400770427414),
                "汐止": (25.068075447428853, 121.66118646058075),
                "南港": (25.05323036378529, 121.60697558827616),
                "松山": (25.049864927527956, 121.57819761570367),
                "台北": (25.047749334216256, 121.51738474453973),
                "板橋": (25.014161806927294, 121.4638161750611),
                "樹林": (24.99153329643622, 121.42441887344117),
                "桃園": (24.989139080637564, 121.31445369430583),
                "中壢": (24.954132647049082, 121.22567907771331),}
    
    nearest_station = None
    nearest_station_coordinates = None
    min_distance = None
    
    for station, station_coord in stations.items():
        distance = geodesic(coord, station_coord).km

        if min_distance is None or distance < min_distance:
            nearest_station = station
            nearest_station_coordinates = station_coord
            min_distance = distance

    #print(nearest_station)
    return str(nearest_station_coordinates)[1:-1]

# 取得最近醫院座標
def get_hospital(coord):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{coord}",
        "rankby": "distance",
        "type": "hospital",
        "keyword": "大醫院",
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        # 取得最近醫院的座標
        nearest_hospital = data["results"][0]["geometry"]["location"]
        nearest_hospital_coordinates = (nearest_hospital["lat"], nearest_hospital["lng"])
        # 回傳最近醫院的座標
        return str(nearest_hospital_coordinates)[1:-1]
    
    except:
        return None

# 取得最近學校座標
def get_school(coord):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    # 國小
    params1 = {
        "location": f"{coord}",
        "rankby": "distance",
        "type": "school",
        "keyword": "國小學",
        "key": api_key
    }
    response1 = requests.get(url, params=params1)
    data1 = response1.json()
    # 國中
    params2 = {
        "location": f"{coord}",
        "rankby": "distance",
        "type": "school",
        "keyword": "國中學",
        "key": api_key
    }
    response2 = requests.get(url, params=params2)
    data2 = response2.json()
    # 高中
    params3 = {
        "location": f"{coord}",
        "rankby": "distance",
        "type": "school",
        "keyword": "高中學",
        "key": api_key
    }
    response3 = requests.get(url, params=params3)
    data3 = response3.json()
    # 大學
    params4 = {
        "location": f"{coord}",
        "rankby": "distance",
        "type": "school",
        "keyword": "大學",
        "key": api_key
    }
    response4 = requests.get(url, params=params4)
    data4 = response4.json()
    # 專科
    params5 = {
        "location": f"{coord}",
        "rankby": "distance",
        "type": "school",
        "keyword": "專科學校",
        "key": api_key
    }
    response5 = requests.get(url, params=params5)
    data5 = response5.json()
    
    try:
        # 取得最近學校的座標
        
        school1 = data1["results"][0]["geometry"]["location"]
        school2 = data2["results"][0]["geometry"]["location"]
        school3 = data3["results"][0]["geometry"]["location"]
        school4 = data4["results"][0]["geometry"]["location"]
        school5 = data5["results"][0]["geometry"]["location"]
        
        schools = { "school1": {"coord": (school1["lat"], school1["lng"]), "dis": geodesic(coord, (school1["lat"], school1["lng"])).km},
                    "school2": {"coord": (school2["lat"], school2["lng"]), "dis": geodesic(coord, (school2["lat"], school2["lng"])).km},
                    "school3": {"coord": (school3["lat"], school3["lng"]), "dis": geodesic(coord, (school3["lat"], school3["lng"])).km},
                    "school4": {"coord": (school4["lat"], school4["lng"]), "dis": geodesic(coord, (school4["lat"], school4["lng"])).km},
                    "school5": {"coord": (school5["lat"], school5["lng"]), "dis": geodesic(coord, (school5["lat"], school5["lng"])).km}, }
        
        nearest_school = min(schools, key=lambda x: schools[x]["dis"])
        nearest_school_coordinates = schools[nearest_school]["coord"]
        
        # 回傳最近學校的座標
        return str(nearest_school_coordinates)[1:-1]
    
    except:
        return None

# 取得最近主要火車站通勤時間
def get_station_commute(address):
    gmaps = googlemaps.Client(key=api_key)
    house=get_house(address)
    station=get_station(house)
    directions=gmaps.directions(house,station,mode="driving")
    
    return directions[0]['legs'][0]['duration']['text']

# 取得最近醫院距離
def get_hospital_dis(address):
    house=get_house(address)
    hospital=get_hospital(house)
    #print(hospital)
    
    return float(geodesic(house,hospital).km)

# 取得最近學校距離
def get_school_dis(address):
    house=get_house(address)
    school=get_school(house)
    #print(school)
    
    return float(geodesic(house,school).km)

# 取得直徑1公里內的商業設施數量
def get_establishment(address):
    api = overpy.Overpass()
    house=get_house(address)
    radius = 1000
    query = f"""
    [out:json];
    (
      node["shop"](around:{radius},{house});
      node["amenity"](around:{radius},{house});
    );
    out;
    """
    
    try:
        result = api.query(query)
        count = len(result.nodes)
        return count
    
    except:
        return None

# 轉換成分鐘數
def convert_to_minutes(time_string):
    time_units = time_string.split()
    minutes = 0
    for i in range(0, len(time_units), 2):
        if time_units[i+1] == "hour" or time_units[i+1] == "hours":
            minutes += int(time_units[i]) * 60
        elif time_units[i+1] == "min" or time_units[i+1] == "mins":
            minutes += int(time_units[i])
    return minutes

# 測試
'''
address='新北市新莊區中央路282號'
print(get_station_commute(address))
print(get_hospital_dis(address))
print(get_school_dis(address))
print(get_establishment(address))
'''
