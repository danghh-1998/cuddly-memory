from .models import Client
from users.services import create_user, deactivate_user, get_user_by
from utils.custom_exceptions import *


def get_super_admin(client):
    return list(filter(lambda user: user.is_super_admin, client.users))[0]


def create_client(data):
    validated_data = data.copy()
    user = get_user_by(email=data.get('email'))
    if user:
        raise DuplicateEntry(entry=user.email, key='email')
    client = Client.objects.create(client_name=validated_data.get('client_name'),
                                   address=validated_data.get('address'))
    validated_data.pop('client_name')
    validated_data.pop('address')
    validated_data['client_id'] = client.id
    create_user(data=validated_data, role=2)
    return client


def get_client_by(**kwargs):
    client = Client.objects.get(**kwargs)
    if not client:
        raise ObjectNotFound
    return client


def get_deleted_client_by(**kwargs):
    client = Client.objects.deleted_only().get(**kwargs)
    if not client:
        raise ObjectNotFound
    return client


def update_client(client, data):
    if not any(data.values()):
        raise ValidationError
    client.client_name = data.get('client_name')
    client.save(update_fields=['client_name'])
    return client


def deactivate_client(client):
    for user in client.users.all():
        deactivate_user(user=user)
    client.is_active = False
    client.save(update_fields=['is_active'])
    client.delete()
    return client


def activate_client(client):
    client.is_active = True
    client.save(update_fields=['is_active'])
    return client
