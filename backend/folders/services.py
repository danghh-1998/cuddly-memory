from .models import Folder
from utils.custom_exceptions import *


def get_root_folder(user):
    return user.folders.first()


def list_sub_folder_name(folder):
    return list(map(lambda sub_folder: sub_folder.name, folder.sub_folders.all()))


def list_template_name(folder):
    return list(map(lambda template: template.display_name, folder.templates.all()))


def create_folder(data, user, folder_type=0):
    parent_folder_id = data.get('parent_folder_id')
    name = data.get('name')
    parent_folder = get_root_folder(user=user) if list(user.folders.all()) else None
    if parent_folder_id:
        parent_folder = user.folders.filter(id=parent_folder_id).first()
        if not parent_folder:
            raise ObjectNotFound
    sibling_names = list_sub_folder_name(parent_folder)
    if name in sibling_names:
        raise DuplicateEntry(entry=name, key='name')
    return Folder.objects.create(name=name, parent_folder=parent_folder, user=user, folder_type=folder_type)


def update_folder(data, folder):
    if folder.folder_type == 1:
        return folder
    name = data.get('name')
    sibling_names = list_sub_folder_name(folder.parent_folder)
    if name in sibling_names:
        raise DuplicateEntry(entry=name, key='name')
    folder.name = name
    folder.save(update_fields=['name'])
    return folder


def get_folder_or_root(user, folder_id):
    if not folder_id:
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
