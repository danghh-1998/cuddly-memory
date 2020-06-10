from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from images.models import Image
from bounding_boxes.models import BoundingBox
from .managers import ResultsManager

'''
Entity Result
'''


class Result(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    result = models.CharField(max_length=255, blank=True, null=True)
    confirm_result = models.CharField(max_length=255, blank=True, null=True)
    image = models.ForeignKey(Image, related_name='results', on_delete=models.CASCADE)
    bounding_box = models.ForeignKey(BoundingBox, related_name='results', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ResultsManager()

    class Meta:
        db_table = 'result'
        app_label = 'results'

    def __str__(self):
        return self.result
