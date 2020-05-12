from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.db import models

from .managers import TasksManager
from users.models import User
from templates.models import Template


class Task(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    QUEUE = 0
    PROCESSING = 1
    DONE = 2
    FAILED = 3
    STATUS_CHOICES = (
        (QUEUE, 'QUEUE'),
        (PROCESSING, 'PROCESSING'),
        (DONE, 'DONE'),
        (FAILED, 'FAILED'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    user = models.ForeignKey(User, related_name='tasks', null=True, on_delete=models.CASCADE, unique=False)
    template = models.ForeignKey(Template, related_name='tasks', null=True, on_delete=models.CASCADE, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TasksManager()

    class Meta:
        db_table = 'task'
        app_label = 'tasks'

    def __str__(self):
        return str(self.status)
