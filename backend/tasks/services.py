import os
from django.conf import settings

from utils.static_file_handler import extract_zip, file_uploader
from .models import Task
from templates.services import get_templates_by
from utils.custom_exceptions import *
from images.services import create_image
from results.services import get_result_by
from images.services import get_image_by


def create_task(user, **kwargs):
    raw_file = kwargs.get('file')
    _, ext = os.path.splitext(raw_file.name)
    template = get_templates_by(id=kwargs.get('template_id')).first()
    if ext == '.zip':
        file = raw_file.file
        encrypted_names, image_names = extract_zip(file, template)
    elif ext not in settings.IMAGE_TYPES:
        raise ValidationError('Bad image type')
    else:
        encrypted_name, image_name = file_uploader(image=raw_file, _type='images', template=template)
        encrypted_names = [encrypted_name]
        image_names = [image_name]
    if template and template.folder.user != user.admin:
        raise Unauthorized
    task = Task.objects.create(user=user, template=template)
    for i in range(len(encrypted_names)):
        create_image(task=task, name=image_names[i], image=encrypted_names[i])
    return task


def check_task_done(task):
    if task.status != 2:
        raise ValidationError('Task is not done')
    return True


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


def delete_task(task):
    task.delete()
    return task


def confirm_task_result(**kwargs):
    image = get_image_by(id=kwargs.get('image_id'))
    result = get_result_by(image=image, id=kwargs.get('result_id'))
    result.result = kwargs.get('confirm_result')
    result.confirm_result = kwargs.get('confirm_result')
    result.save(update_fields=['result', 'confirm_result'])
    return result


def allow_dowload_image(user, task):
    if user != task.user:
        raise Unauthorized
    return True
