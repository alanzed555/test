import argparse, requests, json, sys
from urllib.parse import urlparse, urlencode, urlunparse
from os import path
import threading
import fileinput
import time
from datetime import datetime

URL = "https://api.nike.com/product_feed/threads/v2?count=1&anchor=0&filter=marketplace(CA)&filter=language(en-GB)&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&sort=lastFetchTimeDesc&filter=productInfo.availability.available(true)"

headers = {
    "Content-Type" : "application/json; charset=UTF-8",
    }

def send_gist(style_color, status, image_url, quantity_limit, label_name, link, current_price, currency, product_id, timestamp, final):
    url = "https://discordapp.com/api/webhooks/728977883745484800/E7hWeFIgWQLN5oW5vLXDO55C9ZLh9OGb6WbFGkwTsFEeN6uXmfN1U64XBHoYVNYQCzk_"   

    data = {
        "username" : "Nike Monitor"
    }

    if image_url:
        embeds =[{
                    "title": label_name,
                    "url": "https://www.nike.com/ca/t/" + link,
                    "color": 8754103,
                    "fields": [
                        {
                        "name": "Status",
                        "value": status,
                        "inline": True
                        },
                        {
                        "name": "Price",
                        "value": str(current_price) + " " +  currency,
                        "inline": True
                        },
                        {
                        "name": "Cart Limit",
                        "value": quantity_limit,
                        "inline": True
                        },
                        {
                        "name": "Style Code",
                        "value": style_color,
                        "inline": True
                        },
                        {
                        "name": "Add to Wishlist",
                        "value": "[Click Here](https://amcaatc.herokuapp.com/api/wishadd?productID=" + product_id + ")",
                        "inline": True
                        },
                        {
                        "name": "Sizes & Stock Levels",
                        "value": final
                        },
                        {
                        "name": "Useful Links",
                        "value": "[Cart](https://www.nike.com/ca/cart) | [Wishlist](https://www.nike.com/ca/favorites) | [Setup Add to Wishlist](https://amcaatc.herokuapp.com/api/tokensetup?)"
                        }
                    ],
                    "author": {
                        "name": "https://www.nike.com/ca/",
                        "url": "https://www.nike.com/ca/"
                    },
                    "footer": {
                        "text": "Nike Monitor v1.0 By @Mehdimoii • " + timestamp
                    },
                    "thumbnail": {
                        "url": image_url
                    }
                }]
    
        data["embeds"] = embeds

    result = requests.post(url, data=json.dumps(data), headers={"Content-Type" : "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        pass   

items = []

def initial_monitor():

    response = requests.get(URL, headers=headers)
    response_json = json.loads(response.text)["objects"]
    print(response.status_code, response.reason)

    for x in response_json:
        fetchTime = x["lastFetchTime"]
        items.append(fetchTime)

initial_monitor()

#sample_key_words = 
#sample_ley_words =
#sample_style_colors = {"CU1727-700","A09944-441","554725-069","554725-092","554275-173","CZ3572-104","555112-603","CV3018-001","CV5280-103","AV5174-600","554724-069","AQ0963-101","AV2187-160","CW1381-003","AH7860-100","AQ0963-002","555112-102","CK3022-107","CW7310-909","CW5490-001","CW5379-600","CZ6393-500","CQ8879-100","CU1110-010","BQ6931-102","CBQ6472-800","CW7309-090","AO9944-441","553560-611","CT8527-112","CJ1641-101","BQ6931-101","CD6393-051","CV9499-100","BQ6931-100","DB3621-600","CD6393-011","CU8126-063","CU8126-010","487471-006","554724-092","CW5550-001","CZ8915-100","CZ8659-100","555088-030","553558-611","DC0603-300","CK4348-007","CU0449-100","CU0450-100","BQ6931-104","CV3044-100","CZ1514-400","CI0919-106","BQ6817-800","553560-606","BQ6817-008","CW7577-100","553558-039","553558-606","CU3012-164","CD9664-001","554724-173","553558-034","852542-100","CZ4776-107","554723-106","555088-061","555088-030","861428-106","CQ9446-400","CI9925-400","CZ1514-400"}
sample_style_colors = {"CZ4272-100"}
def pinger():

    for sample_style_color in sample_style_colors:
        URL = "https://api.nike.com/product_feed/threads/v2?filter=marketplace(CA)&filter=language(en-GB)&filter=channelId(d9a5bc42-4b9c-4976-858a-f159cf99c647)&filter=productInfo.merchProduct.styleColor(" + sample_style_color + ")"
        response = requests.get(URL, headers=headers)
        response_json = json.loads(response.text)
        time.sleep(0.5)
        if response_json["pages"]["totalPages"] != 0 :
            try:
                print(response_json["objects"][0]["productInfo"][0]["merchProduct"]["styleColor"])
                image_url = response_json["objects"][0]["productInfo"][0]["imageUrls"]["productImageUrl"]
                style_color = response_json["objects"][0]["productInfo"][0]["merchProduct"]["styleColor"]
                status = response_json["objects"][0]["productInfo"][0]["merchProduct"]["status"]
                quantity_limit = response_json["objects"][0]["productInfo"][0]["merchProduct"]["quantityLimit"]
                label_name = response_json["objects"][0]["productInfo"][0]["merchProduct"]["labelName"]
                link = response_json["objects"][0]["productInfo"][0]["productContent"]["slug"]
                current_price = response_json["objects"][0]["productInfo"][0]["merchPrice"]["currentPrice"]
                currency = response_json["objects"][0]["productInfo"][0]["merchPrice"]["currency"]
                product_id = response_json["objects"][0]["productInfo"][0]["merchPrice"]["productId"]
                timestamp = datetime.now().strftime("%H:%M:%S")
                if 1 == 1:
                    try:
                        sizes = []
                        for x in response_json["objects"][0]["productInfo"][0]["skus"]:
                            sizes.append(x["nikeSize"])
                        stock_level = []
                        for x in response_json["objects"][0]["productInfo"][0]["availableSkus"]:
                            stock_level.append(x["level"])
                        final = ""
                        for i in range(len(sizes)):
                            if stock_level[i] == "OOS":
                                pass
                            else:
                                final = final + sizes[i] + f" - [{stock_level[i]}]" +"\n"
                        send_gist(style_color, status, image_url, quantity_limit, label_name, link, current_price, currency, product_id, timestamp, final)
                    except KeyError:
                        send_gist(style_color, status, image_url, quantity_limit, label_name, link, current_price, currency, product_id, timestamp, final="No stock loaded")

            except KeyError:
                print(sample_style_color + " not loaded")

        else:
            print(sample_style_color + " not loaded")

pinger()

def monitor():

    while True:

        response = requests.get(URL, headers=headers)
        response_json = json.loads(response.text)["objects"]
        print(response.status_code, response.reason)

        for x in response_json:
            fetchTime = x["lastFetchTime"]
            if fetchTime not in items:
                try:
                    found = False
                    for product_info in x["productInfo"]:
                        if product_info["merchProduct"]["styleColor"]  in sample_style_colors :  
                            found = True
                            break

                    if found:
                        print(product_info["merchProduct"]["styleColor"])
                        image_url = product_info["imageUrls"]["productImageUrl"]
                        style_color = product_info["merchProduct"]["styleColor"]
                        status = product_info["merchProduct"]["status"]
                        quantity_limit = product_info["merchProduct"]["quantityLimit"]
                        label_name = product_info["merchProduct"]["labelName"]
                        link = product_info["productContent"]["slug"]
                        current_price = product_info["merchPrice"]["currentPrice"]
                        currency = product_info["merchPrice"]["currency"]
                        product_id = product_info["merchPrice"]["productId"]
                        timestamp = datetime.now().strftime("%H:%M:%S")

                        try:
                            sizes = []
                            for x in product_info["skus"]:
                                sizes.append(x["nikeSize"])

                            stock_level = []
                            for x in product_info["availableSkus"]:
                                stock_level.append(x["level"])

                            final = ""
                            for i in range(len(sizes)):
                                if stock_level[i] == "OOS":
                                    pass
                                else:
                                    final = final + sizes[i] + f" - [{stock_level[i]}]" +"\n"
                            print(final)

                            send_gist(style_color, status, image_url, quantity_limit, label_name, link, current_price, currency, product_id, timestamp, final)
                            #print(style_color, status, image_url, quantity_limit, label_name, link, current_price, currency, product_id, timestamp, final)
                        except KeyError:

                            send_gist(style_color, status, image_url, quantity_limit, label_name, link, current_price, currency, product_id, timestamp, final="No stock loaded")
                            #print(style_color, status, image_url, quantity_limit, label_name, link, current_price, currency, product_id, timestamp, final="No stock loaded")

                        #print("New product : " + product_info["merchProduct"]["labelName"] + " : " + product_info["merchProduct"]["styleColor"])

                        items.append(fetchTime)
                    else:
                        pass
                except KeyError:
                    print("has failed")
                    print(product_info["merchProduct"]["styleColor"])
        time.sleep(2)

monitor()