import urllib
from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
import json
import re

def image_load():
    url = 'https://www.ntf.or.jp/mouse/history/index.html'
    image_url = 'https://www.ntf.or.jp/mouse/history/'
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    img_soups = soup.find_all("img")
    img_paths = [img_soup["src"] for img_soup in img_soups if img_soup["src"].startswith("MazeImage")]

    
    for img_path in img_paths:
        with urllib.request.urlopen(image_url + img_path) as web_file:
            image: bytes = web_file.read()
            yield image, os.path.basename(img_path)
            
def get_wall_data(image: Image):
    horizontal_walls = [
        [1 if image.getpixel((12*x+6, 12*y)) == (255,0,0) else 0 for x in range(16)] for y in range(17)
    ]

    vertical_walls = [
        [1 if image.getpixel((12*x, 12*y+6)) == (255,0,0) else 0 for x in range(17)] for y in range(16)
    ]

    return horizontal_walls, vertical_walls

    
def load():
    for image, img_path in image_load():
        with open("fields/images/{}".format(img_path), mode="wb") as local_file:
            local_file.write(image)

def convert():
    for filename in os.listdir("fields/images"):
        if filename.endswith(".bmp"):
            img = Image.open(f"fields/images/{filename}")
            horizontal_walls, vertical_walls = get_wall_data(img)

            json_data = json.dumps({
                    "name": filename.split('.')[0],
                    "horizontal_walls": horizontal_walls,
                    "vertical_walls": vertical_walls
                }, indent=4, ensure_ascii=False)
            
            json_data = re.sub(r'\[[\s\S]+?\]', lambda s: s.group(0).replace('\n','').replace(' ',''), json_data)
            json_data = json_data.replace('[[', '[\n        [')

            with open("fields/data/{}.json".format(filename.split('.')[0]), mode="w") as local_file:
                local_file.write(json_data)
                

if __name__ == "__main__":
    #load()
    convert()
            




