import os
import binascii
from django.conf import settings
from PIL import Image
import base64
from io import BytesIO
import boto3
import datetime

from environment import DJANGO_ENV


def make_thumbnail(file):
    thumbnail_size = (200, 200)
    image = Image.open(file)
    backgound = Image.new('RGBA', thumbnail_size, (255, 255, 255, 0))
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
    backgound.paste(image,
                    (int((thumbnail_size[0] - image.size[0]) / 2), int((thumbnail_size[1] - image.size[1]) / 2)))
    buffered = BytesIO()
    backgound.save(buffered, format='PNG')
    return buffered


def upload_local(file, path):
    abs_dir = os.path.join(settings.UPLOAD_FILE_DIR, os.path.dirname(path))
    abs_path = os.path.join(settings.UPLOAD_FILE_DIR, path)
    os.makedirs(abs_dir, exist_ok=True)
    with open(abs_path, 'wb+') as write_file:
        write_file.write(file.getbuffer())


def download_local(path):
    abs_path = os.path.join(settings.UPLOAD_FILE_DIR, path)
    with open(abs_path, 'rb+') as file:
        return base64.b64encode(file.read())


def upload_s3(file, path):
    s3 = boto3.client(service_name='s3', aws_access_key_id=settings.AWS_ACCESS_KEY,
                      aws_secret_access_key=settings.AWS_ACCESS_TOKEN)
    bucket_name = settings.AWS_BUCKET_NAME
    file.seek(0)
    s3.put_object(Bucket=bucket_name, Key=path, Body=file)


def download_s3(path):
    s3 = boto3.client(service_name='s3', aws_access_key_id=settings.AWS_ACCESS_KEY,
                      aws_secret_access_key=settings.AWS_ACCESS_TOKEN)
    bucket_name = settings.AWS_BUCKET_NAME
    tmp_file = os.path.join('/tmp', f"{str(datetime.datetime.now())}.png")
    s3.download_file(bucket_name, path, tmp_file)
    with open(tmp_file, 'rb+') as file:
        return base64.b64encode(file.read())


def file_uploader(base64_image, _type):
    encypted_name = f"{binascii.hexlify(os.urandom(16)).decode()}.png"
    is_production = DJANGO_ENV == 'production'
    file = base64_image.file
    if is_production:
        upload_s3(file=file, path=os.path.join(_type, encypted_name))
        if _type == 'templates':
            thumbnail = make_thumbnail(file=file)
            upload_s3(file=thumbnail, path=os.path.join(_type, 'thumbnails', encypted_name))
    else:
        upload_local(file=file, path=os.path.join(_type, encypted_name))
        if _type == 'templates':
            thumbnail = make_thumbnail(file=file)
            upload_local(file=thumbnail, path=os.path.join(_type, 'thumbnails', encypted_name))
    return encypted_name


def file_downloader(file_name, _type, image_type=0):
    is_production = DJANGO_ENV == 'production'
    if is_production:
        if image_type:
            return download_s3(os.path.join(_type, file_name))
        else:
            return download_s3(os.path.join(_type, 'thumbnails', file_name))
    else:
        if image_type:
            return download_local(os.path.join(_type, file_name))
        else:
            return download_local(os.path.join(_type, 'thumbnails', file_name))
