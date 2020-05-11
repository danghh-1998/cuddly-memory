from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .models import Task
from images.models import Image
from .permissions import *
from utils.serializer_validator import validate_serializer


class TaskCreateApi(APIView):
    permission_classes = (UserPermission,)

    class RequestSerializer(serializers.Serializer):
        template_id = serializers.IntegerField(required=True)
        file = serializers.FileField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class ImageSerializer(serializers.ModelSerializer):
            class Meta:
                model = Image
                exclude = ['deleted']

        images = ImageSerializer(many=True)

        class Meta:
            model = Task
            exclude = ['deleted']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        task = create_task(**request_serializer.validated_data, user=request.user)
        response_serializer = self.ResponseSerializer(task)
        return Response({
            'task': response_serializer.data
        }, status=status.HTTP_200_OK)


class TaskUpdateApi(APIView):
    permission_classes = (OwnerPermission,)

    class RequestSerializer(serializers.Serializer):
        status = serializers.IntegerField(max_value=3)

    class ResponseSerializer(serializers.ModelSerializer):
        class ImageSerializer(serializers.ModelSerializer):
            class Meta:
                model = Image
                exclude = ['deleted']

        images = ImageSerializer(many=True)

        class Meta:
            model = Task
            exclude = ['deleted']

    def put(self, request, task_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        task = update_task(task=task, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(task)
        return Response({
            'task': response_serializer.data
        }, status=status.HTTP_200_OK)


class TaskListApi(APIView):
    permission_classes = (UserPermission,)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            exclude = ['deleted']

    def get(self, request):
        self.check_permissions(request=request)
        tasks = get_tasks_by(user=request.user)
        response_serializer = self.ResponseSerializer(tasks, many=True)
        return Response({
            'tasks': response_serializer.data
        }, status=status.HTTP_200_OK)
