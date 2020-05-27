from django.urls import path
from .apis import *

urlpatterns = [
    path('tasks', TaskListApi.as_view(), name='list_tasks'),
    path('tasks/create', TaskCreateApi.as_view(), name='create_task'),
    path('tasks/<task_id>/update', TaskUpdateApi.as_view(), name='update_task'),
    path('tasks/<task_id>', TaskDetailApi.as_view(), name='task_detail'),
    path('tasks/<task_id>/images', TaskListImagesApi.as_view(), name='task_list_images'),
    path('tasks/<task_id>/images/<image_name>', TaskDownloadImageApi.as_view(), name='task_download_image'),
    path('tasks/<task_id>/metadata', TaskGetMetadataApi.as_view(), name='task_get_metadata'),
    path('tasks/<task_id>/result', TaskDownloadResult.as_view(), name='task_download_result'),
    path('tasks/<task_id>/delete', TaskDeleteApi.as_view(), name='delete_task')
]
