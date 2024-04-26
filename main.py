'''
using data from a free recipe api to load data into the database in kul
example api:https://www.themealdb.com/api/json/v1/1/lookup.php?i=52764

apis that used for uploading data to the database:
1.insert meal_info, 5 parameters,'id', `idReal`, `strName`, `strCategory`, `strArea`
https://studev.groept.be/api/a23PT214/insert_meal_info/

2.insert meal_img 3 paramters,`idMeal`, `idReal`, `imgMeal`
https://studev.groept.be/api/a23PT214/insert_meal_img/

3.insert meal_instrutions, 4 parameters, `idMeal`, `idReal`, `numStep`, `strInst`
https://studev.groept.be/api/a23PT214/insert_meal_inst/


'''

import requests
import time
def get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        #print(url)
        #print("successfully make a get request")
    except Exception as e:
        print("fail to get request from this url" + url, e)


def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except Exception as e:
        print("fail to get json data from this url"+url, e)
        return None


def get_id_name_area(json_data):
    meal_id = json_data["meals"][0]["idMeal"]
    meal_name = json_data["meals"][0]["strMeal"]
    meal_category = json_data["meals"][0]["strCategory"]
    meal_area = json_data["meals"][0]["strArea"]
    meal_name = meal_name.replace(" ", "+")
    return '/' + str(meal_id) +'/' +str(meal_name) + '/' + str(meal_category) + '/' + str(meal_area)


def get_inst(json_data):
    meal_id = json_data["meals"][0]["idMeal"]
    meal_inst = json_data["meals"][0]["strInstructions"]
    meal_inst = meal_inst.replace(" ", "+")
    segments = meal_inst.split('\r\n')
    segments = [segment for segment in segments if segment.strip()]
    return segments, meal_id


def get_img(json_data):
    meal_id = json_data["meals"][0]["idMeal"]
    meal_img = json_data["meals"][0]["strMealThumb"]
    meal_img = meal_img.replace("/", "|")
    return "/"+ str(meal_id) + "/" + str(meal_img)


def get_video(json_data):
    meal_video = json_data["meals"][0]["strYoutube"]
    return meal_video


def getinfo_interator():
    j = 0
    for i in range(52764,53100):
        url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i="+str(i)
        json_data = get_content(url)
        if json_data.get("meals") is None:
            print(f"API {url} return a null")
            continue
        else:
            j = j + 1
            print(get_id_name_area(json_data))
    print("final available data number"+str(j))



def upload_meal_info(upload_url):
    j = 1
    for i in range(52764, 53100):
        url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + str(i)
        json_data = get_content(url)
        url_head = upload_url

        if json_data.get("meals") is None:
            print(f"API {url} return a null")
            continue
        else:
            param = str(j) + get_id_name_area(json_data)
            realurl = url_head + param
            get_request(realurl)
            time.sleep(.1)
            #print(realurl)
            j = j + 1
    print("final available data number" + str(j))

def upload_iterator(upload_url,callback):
    "this callback should return a string start with / , and paramters after"
    j = 1
    for i in range(52764, 53100):
        url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + str(i)
        json_data = get_content(url)
        url_head = upload_url
        if json_data.get("meals") is None:
            print(f"API {url} return a null")
            continue
        else:
            param = str(j) + callback(json_data)
            realurl = url_head + param
            get_request(realurl)
            time.sleep(.1)
            print("upload to this url: "+str(realurl))
            j = j + 1
    print("final available data number" + str(j))


def upload_iterator_withsegment(upload_url,callback):
    "this callback should return a segment, which contains the elemnts for iteration"
    j = 1
    for i in range(52764, 53100):
        url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + str(i)
        json_data = get_content(url)
        url_head = upload_url
        if json_data.get("meals") is None:
            print(f"API {url} return a null")
            continue
        else:
            segment, idReal = callback(json_data)
            for n in range(0, len(segment)-1):
                param = str(j) + "/" + idReal + "/" + str(n+1) + "/" + segment[n]
                realurl = url_head + param
                get_request(realurl)
                time.sleep(.1)
                print("upload to this url: " + str(realurl))

            j = j + 1
    print("final available data number" + str(j))


def upload_inst():
    upload_url = "https://studev.groept.be/api/a23PT214/insert_meal_inst/"
    upload_iterator_withsegment(upload_url, get_inst)


def upload_meal_info_table():
    upload_meal_info_url = 'https://studev.groept.be/api/a23PT214/insert_meal_info/'
    upload_meal_info(upload_meal_info_url)


def upload_img():
    img_url = "https://studev.groept.be/api/a23PT214/insert_meal_img/"
    upload_iterator(img_url,get_img)


if __name__ == "__main__":
    upload_inst()
    #upload_img()
    # dburl = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=52764"
    # json_data = get_content(dburl)
    # get_inst(json_data)
    # print(get_json_data(json_data))

