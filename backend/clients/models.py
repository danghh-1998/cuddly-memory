from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from .managers import ClientManager
from utils.custom_exceptions import *


class Client(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    client_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ClientManager()

    class Meta:
        app_label = 'clients'
        db_table = 'client'

    def clean(self):
        client = Client.objects.filter(client_name=self.client_name).first()
        if client:
            raise DuplicateEntry(entry=client.client_name, key='client_name')

    def save(self, keep_deleted=False, **kwargs):
        self.clean()
        super().save(keep_deleted=False, **kwargs)

    def __str__(self):
        return self.client_name

    @property
    def user_num(self):
        return len(self.users.all())
