from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .services import *
from .models import Task
from images.models import Image
from .permissions import *
from utils.serializer_validator import validate_serializer
from utils.custom_renderer import PNGRenderer
from utils.static_file_handler import file_downloader
from bounding_boxes.models import BoundingBox


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
            exclude = ['images', 'deleted']

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


class TaskDetailApi(APIView):
    permission_classes = (OwnerPermission,)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            exclude = ['deleted']

    def get(self, request, task_id):
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        response_serializer = self.ResponseSerializer(task)
        return Response({
            'task': response_serializer.data
        }, status=status.HTTP_200_OK)


class TaskListImagesApi(APIView):
    permission_classes = (OwnerPermission,)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Image
            fields = ['image', 'name']

    def get(self, request, task_id):
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        images = task.images.all()
        response_serializer = self.ResponseSerializer(images, many=True)
        return Response({
            'images': response_serializer.data
        }, status=status.HTTP_200_OK)


class TaskDownloadImageApi(APIView):
    permission_classes = (OwnerPermission,)
    renderer_classes = (PNGRenderer,)

    def get(self, request, task_id, image_name):
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        image = file_downloader(file_name=image_name, _type='images')
        return Response(image, status=status.HTTP_200_OK)


class TaskGetMetadataApi(APIView):
    permission_classes = (OwnerPermission,)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = BoundingBox
            fields = ['metadata', 'recognize_type']

    def get(self, request, task_id):
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        bounding_boxes = task.template.bounding_boxes.all()
        response_serializer = self.ResponseSerializer(bounding_boxes, many=True)
        return Response({
            'bounding_boxes': response_serializer.data
        }, status=status.HTTP_200_OK)


class TaskDownloadResult(APIView):
    permission_classes = (OwnerPermission,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, task_id):
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        json_result = get_task_results(task=task)
        return Response(json_result, status=status.HTTP_200_OK)
