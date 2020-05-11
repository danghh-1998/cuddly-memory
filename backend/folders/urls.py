from django.urls import path
from .apis import *

urlpatterns = [
    path('folders/create', FolderCreateApi.as_view(), name='create_folder'),
    path('folders/<int:folder_id>', FolderDetailApi.as_view(), name='folder_detail'),
    path('folders/<int:folder_id>/update', FolderUpdateApi.as_view(), name='update_folder'),
    path('folders/<int:folder_id>/delete', FolderDeleteApi.as_view(), name='delete_folder'),
    path('folders/<int:folder_id>/duplicate', FolderDuplicateApi.as_view(), name='duplicate_folder')
]
