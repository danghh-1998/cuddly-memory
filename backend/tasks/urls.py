from django.urls import path
from .apis import *

urlpatterns = [
    path('tasks', TaskListApi.as_view(), name='list_tasks'),
    path('tasks/create', TaskCreateApi.as_view(), name='create_task'),
    path('tasks/<int:task_id>/update', TaskUpdateApi.as_view(), name='update_task'),
    path('tasks/<int:task_id>', TaskDetailApi.as_view(), name='task_detail'),
    path('tasks/<int:task_id>/images', TaskListImagesApi.as_view(), name='task_list_images'),
    path('tasks/<int:task_id>/images/<image_name>', TaskDownloadImageApi.as_view(), name='task_download_image'),
    path('tasks/<int:task_id>/confirm_result', TaskConfirmResultApi.as_view(), name='task_confirm_result'),
    path('tasks/<int:task_id>/delete', TaskDeleteApi.as_view(), name='delete_task')
]
