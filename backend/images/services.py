from images.models import Image
from utils.custom_exceptions import *


def create_image(**kwargs):
    return Image.objects.create(task=kwargs.get('task'), image=kwargs.get('image'), name=kwargs.get('name'))


def get_image_by(raise_exception=True, with_deleted=False, **kwargs):
    if with_deleted:
        image = Image.objects.all_with_deleted().filter(**kwargs).first()
    else:
        image = Image.objects.all().filter(**kwargs).first()
    if not image and raise_exception:
        raise ObjectNotFound
    return image
