from django.urls import path
from .apis import *

urlpatterns = [
    path('tasks', TaskListApi.as_view(), name='list_tasks'),
    path('tasks/create', TaskCreateApi.as_view(), name='create_task'),
    path('tasks/<task_id>/update', TaskUpdateApi.as_view(), name='update_task'),
]
