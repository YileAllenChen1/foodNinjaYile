food_name = "burger"

import http.client
import json

conn = http.client.HTTPSConnection("edamam-recipe-search.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2865cb0646mshc0373c2ed63cb65p15a6e1jsne7e9349bde3d",
    'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com"
    }

conn.request("GET", f"/search?q={food_name}", headers=headers)

res = conn.getresponse()
data = res.read().decode("utf-8")
data = json.loads(data)
food_info_list=data["hits"]
print(food_info_list[0])
print(food_info_list[0].keys())
