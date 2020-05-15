from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .models import Folder
from .permissions import *
from templates.models import Template
from utils.serializer_validator import validate_serializer


class FolderDetailApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class FolderSerializer(serializers.ModelSerializer):
            class Meta:
                model = Folder
                fields = ['id', 'name', 'created_at', 'updated_at']

        class TemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = Template
                exclude = ['deleted', 'folder']

        sub_folders = FolderSerializer(many=True)
        templates = TemplateSerializer(many=True)

        class Meta:
            model = Folder
            fields = ['id', 'name', 'parent_folder', 'created_at', 'updated_at', 'sub_folders', 'templates']

    def get(self, request, folder_id):
        folder = get_folder_or_root(user=request.user, folder_id=folder_id)
        self.check_object_permissions(request=request, obj=folder)
        response_serializer = self.ResponseSerializer(folder)
        return Response({
            'folder': response_serializer.data
        }, status=status.HTTP_200_OK)


class FolderCreateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=True)
        parent_folder_id = serializers.IntegerField(default=None)

    class ResponseSerializer(serializers.ModelSerializer):
        class FolderSerializer(serializers.ModelSerializer):
            class Meta:
                model = Folder
                fields = ['id', 'name', 'created_at', 'updated_at']

        class TemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = Template
                exclude = ['deleted']

        sub_folders = FolderSerializer(many=True)
        templates = TemplateSerializer(many=True)

        class Meta:
            model = Folder
            fields = ['id', 'name', 'parent_folder', 'created_at', 'updated_at', 'sub_folders', 'templates']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        folder = create_folder(user=request.user, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(folder)
        return Response({
            'folder': response_serializer.data
        }, status=status.HTTP_200_OK)


class FolderUpdateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        folder_id = serializers.IntegerField(required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class FolderSerializer(serializers.ModelSerializer):
            class Meta:
                model = Folder
                fields = ['id', 'name', 'created_at', 'updated_at']

        class TemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = Template
                exclude = ['deleted', 'folder']

        sub_folders = FolderSerializer(many=True)
        templates = TemplateSerializer(many=True)

        class Meta:
            model = Folder
            fields = ['id', 'name', 'parent_folder', 'created_at', 'updated_at', 'sub_folders', 'templates']

    def put(self, request, folder_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        folder = get_folders_by(id=folder_id).first()
        self.check_object_permissions(request=request, obj=folder)
        folder = update_folder(folder=folder, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(folder)
        return Response({
            'folder': response_serializer.data
        }, status=status.HTTP_200_OK)


class FolderDuplicateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(required=True)
        folder_id = serializers.IntegerField(required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class FolderSerializer(serializers.ModelSerializer):
            class Meta:
                model = Folder
                fields = ['id', 'name', 'created_at', 'updated_at']

        class TemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = Template
                exclude = ['deleted', 'folder']

        sub_folders = FolderSerializer(many=True)
        templates = TemplateSerializer(many=True)

        class Meta:
            model = Folder
            fields = ['id', 'name', 'parent_folder', 'created_at', 'updated_at', 'sub_folders', 'templates']

    def post(self, request, folder_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        folder = get_folders_by(id=folder_id).first()
        self.check_object_permissions(request=request, obj=folder)
        folder = duplicate_folder(folder=folder, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(folder)
        return Response({
            'folder': response_serializer.data
        }, status=status.HTTP_200_OK)


class FolderDeleteApi(APIView):
    permission_classes = [AdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Folder
            fields = ['id', 'name', 'parent_folder', 'created_at', 'updated_at']

    def delete(self, request, folder_id):
        folder = get_folders_by(id=folder_id).first()
        self.check_object_permissions(request=request, obj=folder)
        folder = delete_folder(folder=folder)
        response_serializer = self.ResponseSerializer(folder)
        return Response({
            'folder': response_serializer.data
        }, status=status.HTTP_200_OK)
