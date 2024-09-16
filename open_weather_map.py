import os 
import requests

KEY = os.getenv("WEATHER")
CITY = "COURBEVOIE"

r = requests.get(
    url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
        CITY, KEY
    )
)

data = r.json()

clean_data = {i: data[i] for i in ["weather", "main"]}

clean_data["weather"] = clean_data["weather"][0]


### 

# from datetime import datetime

# current = datetime.now().strftime("%H:%M:%S")
# clean_data["time"] = current
# clean_data["city"] = city


# # 
# from pymongo import MongoClient

# client = MongoClient(host="localhost", port=27017, username="datascientest", password="dst123")

# sample = client["sample"]

# col = sample.create_collection(name="weather")

# col.insert_one(clean_data)

# def make_data(city):
#          r = requests.get(
#         url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
#             city, KEY
#         )
#     )
#     data = r.json()
#     clean_data = {i: data[i] for i in ["weather", "main"]}
#     clean_data["weather"] = clean_data["weather"][0]
#     return clean_data


# def add_key(data, city):
#     current = datetime.now().strftime("%H:%M:%S")
#     data["time"] = current
#     data["city"] = city

#     return data


# def add_data(client, cities):

#     col = client["sample"]["weather"]

#     for city in cities:
#         data = make_data(city)
#         data = add_key(data, city)
#         col.insert_one(data)


# add_data(client, ["courbevoie", "puteaux", "lourdes","bourg-la-reine"])