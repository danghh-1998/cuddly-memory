from django.urls import path

from .apis import *

urlpatterns = [
    path('templates/create', TemplateCreateApi.as_view(), name='create_template'),
    path('templates/<int:template_id>', TemplateDetailApi.as_view(), name='template_detail'),
    path('templates/<int:template_id>/image/<int:image_type>', TemplateDownloadImageApi.as_view(),
         name='download_template_image'),
    path('templates/<int:template_id>/update', TemplateUpdateApi.as_view(), name='update_template'),
    path('templates/<int:template_id>/duplicate', TemplateDuplicateApi.as_view(), name='duplicate_template'),
    path('templates/<int:template_id>/delete', TemplateDeleteApi.as_view(), name='delete_template')
]
