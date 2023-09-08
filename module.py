import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import time
import os

url = "http://127.0.0.1:7861"
api_url = f'{url}/sdapi/v1/txt2img'


def get_image_link(prompt):
    payload = {
        "prompt": prompt,
        "steps": 5
    }

    response = requests.post(url=api_url, json=payload)


    r = response.json()
    file_name = f'{prompt}_{str(time.time())}.png'
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        image.save(file_name, pnginfo=pnginfo)

    download_link = f"http://{os.environ.get('VPS_IP', 'localhost')}:{os.environ.get('VPS_PORT', '8000')}/{file_name}"
    return download_link
print(get_image_link('cat'))


