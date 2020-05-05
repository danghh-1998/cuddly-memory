from .models import Folder
from utils.custom_exceptions import *


def get_root_folder(user):
    return user.folders.first()


def create_folder(data, user, folder_type=0):
    parent_folder_id = data.get('parent_folder_id')
    parent_folder = get_root_folder(user=user) if list(user.folders.all()) else None
    if parent_folder_id:
        parent_folder = user.folders.filter(id=parent_folder_id).first()
        if not parent_folder:
            raise ObjectNotFound
    return Folder.objects.create(name=data.get('name'), parent_folder=parent_folder, user=user, folder_type=folder_type)


def update_folder(data, folder):
    if folder.folder_type == 1:
        return folder
    folder.name = data.get('name')
    folder.save(update_fields=['name'])
    return folder


def get_folder_or_root(user, folder_id):
    if folder_id == 0:
        return get_root_folder(user=user)
    else:
        return get_folders_by(id=folder_id).first()


def get_folders_by(raise_exception=True, only_deleted=False, **kwargs):
    if only_deleted:
        folders = Folder.objects.deleted_only().filter(**kwargs)
    else:
        folders = Folder.objects.filter(**kwargs)
    if not folders and raise_exception:
        raise ObjectNotFound
    return folders


def delete_folder(folder):
    if folder.folder_type == 1:
        return
    folder.delete()
