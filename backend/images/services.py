from images.models import Image


def create_image(**kwargs):
    return Image.objects.create(task=kwargs.get('task'), image=kwargs.get('image'), name=kwargs.get('name'))
