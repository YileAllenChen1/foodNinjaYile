from foodNinja import foodNinja
from flask import render_template, request, Flask
import http.client
import json

processed_text = ""

@foodNinja.route('/')
@foodNinja.route('/index')
def index():
    return render_template('index.html')

@foodNinja.route('/', methods=['POST'])
@foodNinja.route('/index', methods=['POST'])
def index_post():
    text = request.form['input_text']
    food_name = text.upper()
    
    # get data information
    conn = http.client.HTTPSConnection("rapidapi.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "d0f3049c61mshf600ba97b74fb49p11b213jsn607180f06887",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
    conn.request("GET", f"/?q={food_name}", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    food_info_list = data["results"]
    food_thumbnail_list = []
    for i in food_info_list:
        if i['thumbnail']:
            food_thumbnail_list.append(i)
    for i in food_info_list:
        if not i['thumbnail']:
            food_thumbnail_list.append(i)
    print(food_name, food_thumbnail_list, food_info_list)
    return render_template('recipe.html', recipe_name = food_name, food_list = food_thumbnail_list)