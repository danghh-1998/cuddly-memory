import os
import binascii
from django.conf import settings
from PIL import Image
import base64


def file_uploader(base64_image, _type):
    encypted_name = f"{binascii.hexlify(os.urandom(16)).decode()}.png"
    _dir = f"{settings.UPLOAD_FILE_DIR}/{_type}"
    os.makedirs(_dir, exist_ok=True)
    with open(f"{_dir}/{encypted_name}", 'wb+') as file:
        for chunk in base64_image.chunks():
            file.write(chunk)
    if _type == 'templates':
        image = Image.open(f"{_dir}/{encypted_name}")
        thumbnail_size = (200, 200)
        image.thumbnail(thumbnail_size, Image.ANTIALIAS)
        backgound = Image.new('RGBA', thumbnail_size, (255, 255, 255, 0))
        backgound.paste(image,
                        (int((thumbnail_size[0] - image.size[0]) / 2), int((thumbnail_size[1] - image.size[1]) / 2)))
        os.makedirs(f"{_dir}/thumbnails", exist_ok=True)
        backgound.save(f"{_dir}/thumbnails/{encypted_name}")
        return encypted_name


def file_downloader(file_name, _type, image_type=0):
    _dir = f"{settings.UPLOAD_FILE_DIR}/{_type}"
    if image_type:
        path = f"{_dir}/thumbnails/{file_name}"
    else:
        path = f"{_dir}/{file_name}"
    with open(path, 'rb+') as file:
        file_content = base64.b64encode(file.read())
        return file_content
