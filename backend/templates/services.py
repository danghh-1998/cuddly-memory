from utils.static_file_handler import file_uploader
from .models import Template
from folders.services import get_folder_or_root
from bounding_boxes.services import create_bounding_boxes
from utils.custom_exceptions import *
from folders.services import get_folders_by, list_template_name


def create_template(user, **kwargs):
    base64_image = kwargs.get('image')
    display_name = kwargs.get('name')
    folder_id = kwargs.get('folder_id')
    folder = get_folder_or_root(user=user, folder_id=folder_id)
    if folder.user != user:
        raise Unauthorized
    sibling_names = list_template_name(folder=folder)
    if display_name in sibling_names:
        raise DuplicateEntry(entry=display_name, key='name')
    encypted_name = file_uploader(base64_image=base64_image, _type='templates')
    template = Template.objects.create(name=encypted_name, display_name=display_name, folder=folder)
    create_bounding_boxes(kwargs.get('bounding_boxes'), template=template)
    return template


def get_templates_by(raise_exception=True, only_deleted=False, **kwargs):
    if only_deleted:
        templates = Template.objects.deleted_only().filter(**kwargs)
    else:
        templates = Template.objects.filter(**kwargs)
    if not templates and raise_exception:
        raise ObjectNotFound
    return templates


def update_template(template, **kwargs):
    if not any(kwargs.values()):
        raise ValidationError
    new_bounding_boxes = kwargs.get('bounding_boxes')
    base64_image = kwargs.get('image')
    display_name = kwargs.get('name')
    folder_id = kwargs.get('folder_id')
    folder = get_folders_by(id=folder_id).first() if folder_id else template.folder
    if folder.user != template.folder.user:
        raise Unauthorized
    if display_name and display_name in list_template_name(folder):
        raise DuplicateEntry(entry=display_name, key='name')
    if new_bounding_boxes:
        bounding_boxes = template.bounding_boxes.all()
        for bounding_box in bounding_boxes:
            bounding_box.delete()
        create_bounding_boxes(new_bounding_boxes, template=template)
    if base64_image:
        encypted_name = file_uploader(base64_image=base64_image, _type='templates')
        template.name = encypted_name
        template.save(update_fields=['name'])
    if display_name:
        template.display_name = display_name
        template.save(update_fields=['display_name'])
    if folder_id:
        template.folder = folder
        template.save(update_fields=['folder_id'])
    return template


def duplicate_template(template, **kwargs):
    folder_id = kwargs.get('folder_id')
    name = kwargs.get('name')
    folder = get_folders_by(id=folder_id).first() if folder_id else template.folder
    if folder.user != template.folder.user:
        raise Unauthorized
    sibling_name = list_template_name(folder=folder)
    if name in sibling_name:
        raise DuplicateEntry(entry=name, key='name')
    bounding_boxes = template.bounding_boxes.all()
    template.pk = None
    template.display_name = name
    template.folder = folder
    template.save()
    for bounding_box in bounding_boxes:
        bounding_box.id = None
        bounding_box.template = template
        bounding_box.save()
    return template


def delete_template(template):
    template.delete()
