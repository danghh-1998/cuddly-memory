from .models import BoundingBox
from utils.custom_exceptions import *


def create_bounding_box(**kwargs):
    return BoundingBox.objects.create(**kwargs)


def get_bounding_boxes_by(raise_exception=True, only_deleted=False, **kwargs):
    if only_deleted:
        bounding_boxes = BoundingBox.objects.deleted_only().filter(**kwargs)
    else:
        bounding_boxes = BoundingBox.objects.filter(**kwargs)
    if not bounding_boxes and raise_exception:
        raise ObjectNotFound
    return bounding_boxes
