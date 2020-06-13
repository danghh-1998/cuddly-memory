import os
import binascii
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import boto3
import datetime
import zipfile
from datetime import datetime
from django.conf import settings
import shutil

from environment import DJANGO_ENV
from utils.custom_exceptions import ValidationError


def make_thumbnail(file):
    thumbnail_size = (200, 200)
    image = Image.open(file)
    backgound = Image.new('RGBA', thumbnail_size, (255, 255, 255, 0))
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)
    backgound.paste(image, (int((thumbnail_size[0] - image.size[0]) / 2), int((thumbnail_size[1] - image.size[1]) / 2)))
    buffered = BytesIO()
    backgound.save(buffered, format='PNG')
    return buffered


def extract_zip(file, template):
    zip_file = zipfile.ZipFile(file)
    now = str(datetime.now())
    tmp_dir = f"/tmp/{now}"
    zip_file.extractall(tmp_dir)
    namelist = zip_file.namelist()
    encypted_names = []
    for tmp_filepath in [os.path.join(tmp_dir, name) for name in namelist]:
        with open(tmp_filepath, 'rb') as tmp_file:
            _, ext = os.path.splitext(tmp_filepath)
            if ext not in settings.IMAGE_TYPES:
                raise ValidationError("Bad zipfile")
            encypted_name, _ = file_uploader(image=BytesIO(tmp_file.read()), _type='images', template=template)
            encypted_names.append(encypted_name)
    shutil.rmtree(tmp_dir)
    return encypted_names, namelist


def upload_local(file, path):
    abs_dir = os.path.join(settings.UPLOAD_FILE_DIR, os.path.dirname(path))
    abs_path = os.path.join(settings.UPLOAD_FILE_DIR, path)
    os.makedirs(abs_dir, exist_ok=True)
    with open(abs_path, 'wb+') as write_file:
        write_file.write(file.getbuffer())


def download_local(path):
    abs_path = os.path.join(settings.UPLOAD_FILE_DIR, path)
    with open(abs_path, 'rb+') as file:
        return file.read()


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
    tmp_file = os.path.join('/tmp', f"{str(datetime.now())}.png")
    s3.download_file(bucket_name, path, tmp_file)
    with open(tmp_file, 'rb+') as file:
        return file.read()


def file_uploader(image, _type, template=None):
    image_name = None
    if not isinstance(image, BytesIO):
        image_name = image.name
        image = image.file
    if _type == 'images':
        reverse_template_image_shape = cv2.imdecode(
            np.frombuffer(file_downloader(file_name=template.name, _type='templates'), np.uint8), 0).shape[::-1]
        resized_image = cv2.resize(cv2.imdecode(np.frombuffer(image.read(), np.uint8), -1),
                                   reverse_template_image_shape,
                                   interpolation=cv2.INTER_AREA)
        _, buffer = cv2.imencode('.png', resized_image)
        image = BytesIO(buffer)

    encypted_name = f"{binascii.hexlify(os.urandom(16)).decode()}.png"
    is_production = DJANGO_ENV == 'production'
    image.seek(0)
    if is_production:
        upload_s3(file=image, path=os.path.join(_type, encypted_name))
        if _type == 'templates':
            thumbnail = make_thumbnail(file=image)
            upload_s3(file=thumbnail, path=os.path.join(_type, 'thumbnails', encypted_name))
    else:
        upload_local(file=image, path=os.path.join(_type, encypted_name))
        if _type == 'templates':
            thumbnail = make_thumbnail(file=image)
            upload_local(file=thumbnail, path=os.path.join(_type, 'thumbnails', encypted_name))
    return encypted_name, image_name


def file_downloader(file_name, _type, image_type=1):
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
