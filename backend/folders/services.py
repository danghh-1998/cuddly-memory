from .models import Folder
from utils.custom_exceptions import *


def get_root_folder(user):
    return user.folders.first() if user.role == 1 else user.admin.folders.first()


def list_sub_folder_name(folder):
    return list(map(lambda sub_folder: sub_folder.name, folder.sub_folders.all()))


def list_template_name(folder):
    return list(map(lambda template: template.display_name, folder.templates.all()))


def has_sub_folder_or_template(folder):
    return list(folder.templates.all()) or list(folder.sub_folders.all())


def recursive_folder_ids(folder):
    ids = [folder.id]
    sub_folders = folder.sub_folders.all()
    for sub_folder in sub_folders:
        ids.extend(recursive_folder_ids(sub_folder))
    return ids


def create_folder(user, folder_type=0, **kwargs):
    parent_folder_id = kwargs.get('parent_folder_id')
    name = kwargs.get('name')
    parent_folder = get_root_folder(user=user) if list(user.folders.all()) else None
    if parent_folder_id:
        parent_folder = user.folders.filter(id=parent_folder_id).first()
        if not parent_folder:
            raise ObjectNotFound
    sibling_names = list_sub_folder_name(parent_folder) if folder_type == 0 else []
    if name in sibling_names:
        raise DuplicateEntry(entry=name, key='name')
    return Folder.objects.create(name=name, parent_folder=parent_folder, user=user, folder_type=folder_type)


def update_folder(folder, **kwargs):
    if not any(kwargs.values()):
        raise ValidationError
    if folder.folder_type == 1:
        return folder
    name = kwargs.get('name')
    folder_id = kwargs.get('folder_id')
    new_parent_folder = get_folders_by(id=folder_id).first() if folder_id else folder.parent_folder
    if new_parent_folder.user != folder.parent_folder.user:
        raise Unauthorized
    if name:
        sibling_names = list_sub_folder_name(new_parent_folder)
        if name in sibling_names:
            raise DuplicateEntry(entry=name, key='name')
        folder.name = name
        folder.save(update_fields=['name'])
    folder.parent_folder = new_parent_folder
    folder.save(update_fields=['parent_folder_id'])
    return folder


def duplicate_folder(folder, **kwargs):
    from templates.services import duplicate_template
    if folder.folder_type == 1:
        return folder
    name = kwargs.get('name')
    folder_id = kwargs.get('folder_id')
    new_parent_folder = get_folders_by(id=folder_id).first() if folder_id else folder.parent_folder
    if new_parent_folder.user != folder.parent_folder.user:
        raise Unauthorized
    sibling_names = list_sub_folder_name(new_parent_folder)
    if name in sibling_names:
        raise DuplicateEntry(entry=name, key='name')
    sub_folder_ids = recursive_folder_ids(folder)
    if folder_id in sub_folder_ids:
        raise ValidationError(message='target folder inside source folder')
    sub_folders = folder.sub_folders.all()
    templates = folder.templates.all()
    folder.id = None
    folder.name = name
    folder.parent_folder = new_parent_folder
    folder.save()
    for sub_folder in sub_folders:
        duplicate_folder(folder=sub_folder, folder_id=folder.id, name=sub_folder.name)
    for template in templates:
        duplicate_template(template=template, folder_id=folder.id, name=template.display_name)
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
    return folder
