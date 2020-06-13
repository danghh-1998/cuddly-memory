from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from templates.models import Template


class BoundingBox(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    ENG = 0
    VIE = 1
    DIGIT = 2
    CHECKBOX = 3
    EMAIL = 4
    RECOGNIZE_TYPE_CHOICES = (
        (ENG, 'ENG'),
        (VIE, 'VIE'),
        (DIGIT, 'DIGIT'),
        (CHECKBOX, 'CHECKBOX'),
        (EMAIL, 'EMAIL')
    )

    metadata = models.CharField(max_length=255)
    recognize_type = models.SmallIntegerField(choices=RECOGNIZE_TYPE_CHOICES, default=0)
    context = models.CharField(max_length=255)
    template = models.ForeignKey(Template, related_name='bounding_boxes', unique=False, null=True,
                                 on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'bounding_boxes'
        db_table = 'bounding_box'

    def __str__(self):
        return self.metadata
