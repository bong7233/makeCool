# import requests
# from bs4 import BeautifulSoup
# from pymongo import MongoClient
# client = MongoClient(
#     'mongodb+srv://rlawlgh3894:Rkddkwl3894!@cluster0.ktjzj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
# db = client.makeCool
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(
#     'https://www.youtube.com/watch?v=pxe84igAXUk', headers=headers)
# soup = BeautifulSoup(data.text, 'html.parser')
# og_image = soup.select_one('meta[property="og:image"]')
# og_title = soup.select_one('meta[property="og:title"]')
# og_description = soup.select_one('meta[property="og:description"]')
# image = og_image['content']
# title = og_title['content']
# description = og_description['content']

# doc = {
#     'image': image,
#     'title': title,
#     'desc': description,
#     'video_id': "pxe84igAXUk",
# }
# db.waist.insert_one(doc)
