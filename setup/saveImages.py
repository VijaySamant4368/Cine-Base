import requests
import json

LOW_QUALITY = False
if LOW_QUALITY:
    IMAGE_PATH = "../static/assets/lowQ/"
else:
    IMAGE_PATH = "../static/assets/highQ/"

with open("movieLinks.json", "r") as file:
    title_links = json.load(file)[340:]

errors = []

for title_link in title_links:
    title_id = title_link["title_id"]
    try:
        if LOW_QUALITY:
            image_url = title_link["img_src"]
        else:
            image_url = title_link["img_src_high"]
    except KeyError:
        errors.append(title_id)
        continue
    
    # img_data = requests.get(image_url).content
    # with open(IMAGE_PATH + str(title_id) + ".jpg", 'wb') as handler:
    #     handler.write(img_data)
    print(f"{title_id}/1000 completed")

print(errors)