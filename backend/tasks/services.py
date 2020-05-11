import os
from django.conf import settings

from utils.static_file_handler import extract_zip, file_uploader
from .models import Task
from templates.services import get_templates_by
from utils.custom_exceptions import *
from images.services import create_image


def create_task(user, **kwargs):
    raw_file = kwargs.get('file')
    _, ext = os.path.splitext(raw_file.name)
    if ext == '.zip':
        file = raw_file.file
        encrypted_names, image_names = extract_zip(file)
    elif ext not in settings.IMAGE_TYPES:
        raise ValidationError('Bad image type')
    else:
        encrypted_name, image_name = file_uploader(image=raw_file, _type='images')
        encrypted_names = [encrypted_name]
        image_names = [image_name]
    template = get_templates_by(id=kwargs.get('template_id')).first()
    if not template:
        raise ObjectNotFound
    task = Task.objects.create(user=user, template=template)
    for i in range(len(encrypted_names)):
        create_image(task=task, name=image_names[i], image=encrypted_names[i])
    return task


def update_task(task, **kwargs):
    status = kwargs.get('status')
    task.status = status
    task.save(update_fields=['status'])
    return task


def get_tasks_by(raise_exception=True, only_deleted=False, **kwargs):
    if only_deleted:
        tasks = Task.objects.deleted_only().filter(**kwargs)
    else:
        tasks = Task.objects.filter(**kwargs)
    if not tasks and raise_exception:
        raise ObjectNotFound
    return tasks
