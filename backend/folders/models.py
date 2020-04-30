from django.db import models

from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from users.models import User
from .managers import FolderManager


class Folder(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    COMMON_FOLDER = 0
    ROOT_FOLDER = 1
    FOLDER_TYPE_CHOICES = (
        (ROOT_FOLDER, 'ROOT_FOLDER'),
        (COMMON_FOLDER, 'COMMON_FOLDER')
    )
    name = models.CharField(max_length=255)
    folder_type = models.SmallIntegerField(choices=FOLDER_TYPE_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_folder = models.ForeignKey("self", related_name='sub_folders', on_delete=models.CASCADE, unique=False,
                                      null=True, default=None)
    user = models.ForeignKey(User, related_name='folders', on_delete=models.SET_NULL, unique=False, null=True)
    objects = FolderManager()

    class Meta:
        app_label = 'folders'
        db_table = 'folder'

    def __str__(self):
        return self.name
