import os
import json
from django.conf import settings
import datetime

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
    if template and template.folder.user != user.admin:
        raise Unauthorized
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


def get_task_results(task):
    if task.status != 2:
        raise ValidationError(message='Task is not done')
    results = {}
    for image in task.images.all():
        image_result = {}
        bounding_box_id = 0
        for result in image.results.all():
            image_result[str(bounding_box_id)] = result.confirm_result if result.confirm_result else result.result
            bounding_box_id += 1
        results[image.name] = image_result
    now = datetime.datetime.now()
    results = json.dumps(results)
    tmp_file_path = os.path.join('/tmp', f"{now}.json")
    with open(tmp_file_path, 'wb') as tmp_file:
        tmp_file.write(results.encode('utf8'))
    with open(tmp_file_path, 'rb') as tmp_file:
        return tmp_file.read()


def delete_task(task):
    task.delete()
    return task
