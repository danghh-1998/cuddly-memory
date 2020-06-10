from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from folders.models import Folder


class Template(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, related_name='templates', on_delete=models.CASCADE, unique=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'templates'
        db_table = 'template'

    def __str__(self):
        return self.display_name
