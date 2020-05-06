from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE
from templates.models import Template


class BoundingBox(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    ENG = 0
    VIE = 1
    ENG_MULTIPLE_LINE = 2
    VIE_MULTIPLE_LINE = 3
    DIGIT = 4
    CHECKBOX = 5
    RECOGNIZE_TYPE_CHOICES = (
        (ENG, 'ENG'),
        (VIE, 'VIE'),
        (ENG_MULTIPLE_LINE, 'ENG_MULTIPLE_LINE'),
        (VIE_MULTIPLE_LINE, 'VIE_MULTIPLE_LINE'),
        (DIGIT, 'DIGIT'),
        (CHECKBOX, 'CHECKBOX')
    )

    metadata = models.CharField(max_length=255)
    recognize_type = models.SmallIntegerField(choices=RECOGNIZE_TYPE_CHOICES, default=0)
    template = models.ForeignKey(Template, related_name='bounding_boxes', unique=False, null=True,
                                 on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'bounding_boxes'
        db_table = 'bounding_box'

    def __str__(self):
        return self.metadata
