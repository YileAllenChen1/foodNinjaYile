from app import app
from flask import render_template, request, Flask
import http.client
import json

processed_text = ""

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/', methods=['POST'])
@app.route('/index', methods=['POST'])
def index_post():
    text = ""
    if(request.form.get("chicken")):#=="Chicken"):
        text = "chicken"
    elif(request.form.get("hamburger")):
        text = "hamburger"
    elif(request.form.get("fried chicken")):
        text = "fried chicken"
    elif(request.form.get("pie")):
        text = "pie"
    elif(request.form.get("turkey")):
        text = "turkey"
    elif(request.form.get("cookies")):
        text = "cookies"
    elif(request.form.get("cheesecake")):
        text = "cheesecake"
    elif(request.form.get("pasta")):
        text = "pasta"
    elif(request.form.get("tenders")):
        text = "tenders"
    elif(request.form.get("salmon")):
        text = "salmon"
    elif(request.form.get("seafood")):
        text = "seafood"
    elif(request.form.get("beef")):
        text = "beef"
    elif(request.form.get("shrimp")):
        text = "shrimp"
    else:
        text = request.form['input_text']
    food_name = text.upper()
    title_name = food_name
    food_name = food_name.replace(" ", "%20")
    #get data information
    conn = http.client.HTTPSConnection("edamam-recipe-search.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "2865cb0646mshc0373c2ed63cb65p15a6e1jsne7e9349bde3d",
        'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com"
        }

    conn.request("GET", f"/search?q={food_name}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    data = json.loads(data)
    food_info_list=data["hits"][:min(8, len(data["hits"]))]
    
    conn1 = http.client.HTTPSConnection("tasty.p.rapidapi.com")

    headers1 = {
        'x-rapidapi-key': "95bac783aamsh1ddce04a70d8a97p1789afjsn6c076132223c",
        'x-rapidapi-host': "tasty.p.rapidapi.com"
        }

    conn1.request("GET", "/recipes/list?from=0&size=50&q=" + food_name, headers=headers1)

    res1 = conn1.getresponse()
    data1 = json.loads(res1.read().decode("utf-8"))
    #print(data1)

    food_result_list = data1['results']
    food_name_list = []
    food_r_list = []
    food_ingredient_list = []
    thumbnail_list = []
    video_list = []
    recipe_list = []
    tasty_ratings = []
    tasty_score = []
    tasty_cook_time = []
    tasty_serving_size = []
    renditions = []

    num_recipe = 0
    for i in food_result_list:
        #get name, image, video url, and all other ingredients
        if num_recipe == 9:
            break
        if (i['thumbnail_url'] and i['video_url'] and i['name'] and 'sections' in i.keys()) and i['user_ratings'] and i['cook_time_minutes'] and i['yields'] and i['renditions']:
            food_name_list.append(i['name'])
            thumbnail_list.append(i['thumbnail_url'])
            food_r_list.append(i['sections'])
            tasty_ratings.append(i['user_ratings'])
            tasty_cook_time.append(i['cook_time_minutes'])
            tasty_serving_size.append(i['yields'])
            renditions.append(i['renditions'])
            num_recipe = num_recipe + 1    
            
    for i in range(len(renditions)):
        video_list.append(renditions[i][0]['url'])

    for i in tasty_ratings:
        percentage = i['score']
        if percentage is None:
            percentage = "no ratings"
        else:
            percentage = round(float(percentage) * 100)
            percentage = str(percentage) + "% positive"
        tasty_score.append(percentage)

    for i in range(len(food_r_list)):
        for j in range(len(food_r_list[i])):
            ing_list = []
            for k in range(len(food_r_list[i][j]['components'])):
                ing_list.append(food_r_list[i][j]['components'][k]['ingredient']['name'])
        food_ingredient_list.append(ing_list)    

    for i in range(len(food_name_list)):
        s = ''
        for j in range(len(food_ingredient_list[i])):
            s = s + food_ingredient_list[i][j] + ", "
        recipe_list.append({'name': food_name_list[i], 'thumbnail': thumbnail_list[i], 'ingredients': s, 'href':video_list[i], 'ratings': tasty_score[i], 'cook_time': tasty_cook_time[i], 'serving_size': tasty_serving_size[i]})

    
    conn2 = http.client.HTTPSConnection("yummly2.p.rapidapi.com")

    headers2 = {
        'x-rapidapi-key': "d0f3049c61mshf600ba97b74fb49p11b213jsn607180f06887",
        'x-rapidapi-host': "yummly2.p.rapidapi.com"
        }

    conn2.request("GET", "/feeds/search?start=0&maxResult=10&q=" + food_name, headers=headers2)

    res2 = conn2.getresponse()
    data2 = json.loads(res2.read().decode("utf-8"))
    
    food_results_list2 = data2["feed"] #all the food, under key "content"
    food_name_list2 = []
    ingredient_list2=[]
    url_list2=[]
    image_list2=[]
    ratings_list2=[]
    totalTime_list2=[]
    recipe_list2 = []
    for i in food_results_list2:
        food_name_list2.append(i["content"]["details"]["name"])
        url_list2.append(i["content"]["details"]["attribution"]["url"])
        image_list2.append(i["content"]["details"]["images"][0]["resizableImageUrl"])
        ratings_list2.append(i["content"]["details"]["rating"])
        totalTime_list2.append(i["content"]["details"]["totalTime"])

        ingredient_list2_temp=[]
        for j in i["content"]["ingredientLines"]:
            ingredient_list2_temp.append(j["ingredient"])
        ingredient_list2.append(ingredient_list2_temp)

    for i in range(len(food_name_list2)):
        s = ''
        for j in range(len(ingredient_list2[i])):
            s = s + ingredient_list2[i][j] + ", "
        recipe_list2.append({'name': food_name_list2[i], 'image': image_list2[i], 'ingredients': s, 'href':url_list2[i], 'time': totalTime_list2[i], 'ratings': ratings_list2[i]})
   

    return render_template('recipe.html', recipe_name = title_name, food_list = food_info_list, tasty_food_list = recipe_list, yummly_food_list = recipe_list2)