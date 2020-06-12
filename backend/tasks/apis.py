from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .models import Task
from templates.models import Template
from images.models import Image
from results.models import Result
from .permissions import *
from utils.serializer_validator import validate_serializer
from utils.custom_renderer import PNGRenderer
from utils.static_file_handler import file_downloader
from auth_tokens.services import get_auth_token_by


class TaskCreateApi(APIView):
    permission_classes = (UserPermission,)

    class RequestSerializer(serializers.Serializer):
        template_id = serializers.IntegerField(required=True)
        file = serializers.FileField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class TemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = Template
                fields = ['id', 'display_name']

        template = TemplateSerializer()

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
        class TemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = Template
                fields = ['id', 'display_name']

        template = TemplateSerializer()

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
        class ResultSerializer(serializers.ModelSerializer):
            class Meta:
                model = Result
                fields = ['id', 'result', 'confirm_result']

        results = ResultSerializer(many=True)

        class Meta:
            model = Image
            fields = ['id', 'image', 'name', 'results']

    def get(self, request, task_id):
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        check_task_done(task)
        images = task.images.all()
        response_serializer = self.ResponseSerializer(images, many=True)
        return Response({
            'images': response_serializer.data
        }, status=status.HTTP_200_OK)


class TaskConfirmResultApi(APIView):
    permission_classes = (OwnerPermission,)

    class RequestSerializer(serializers.Serializer):
        image_id = serializers.IntegerField(required=True)
        result_id = serializers.IntegerField(required=True)
        confirm_result = serializers.CharField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class ImageSerializer(serializers.ModelSerializer):
            class Meta:
                model = Image
                fields = ['id']

        image = ImageSerializer()

        class Meta:
            model = Result
            fields = ['id', 'result', 'confirm_result', 'image']

    def put(self, request, task_id):
        task = get_tasks_by(id=task_id).first()
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(serializer=request_serializer)
        self.check_object_permissions(request=request, obj=task)
        result = confirm_task_result(**request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(result)
        return Response({
            'result': response_serializer.data
        }, status=status.HTTP_200_OK)


class TaskDownloadImageApi(APIView):
    permission_classes = (OwnerPermission,)
    renderer_classes = (PNGRenderer,)

    def get(self, request, task_id, image_name):
        task = get_tasks_by(id=task_id).first()
        auth_token = get_auth_token_by(key=request.query_params.get('token'))
        allow_dowload_image(user=auth_token.user, task=task)
        image = file_downloader(file_name=image_name, _type='images')
        return Response(image, status=status.HTTP_200_OK)


class TaskDeleteApi(APIView):
    permission_classes = (OwnerPermission,)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = '__all__'

    def delete(self, request, task_id):
        task = get_tasks_by(id=task_id).first()
        self.check_object_permissions(request=request, obj=task)
        task = delete_task(task)
        response_serializer = self.ResponseSerializer(task)
        return Response({
            'task': response_serializer.data
        }, status=status.HTTP_200_OK)
