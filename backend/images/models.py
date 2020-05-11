from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

from tasks.models import Task
from .managers import ImageManager


class Image(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    image = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    task = models.ForeignKey(Task, related_name='images', on_delete=models.CASCADE, unique=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ImageManager()

    class Meta:
        db_table = 'image'
        app_label = 'images'

    def __str__(self):
        return self.image
