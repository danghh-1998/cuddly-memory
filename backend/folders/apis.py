from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .models import Folder
from .permissions import *
from templates.models import Template


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
            fields = ['id', 'name', 'created_at', 'updated_at', 'sub_folders', 'templates']

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
        class Meta:
            model = Folder
            fields = ['id', 'name', 'created_at', 'updated_at']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        self.check_permissions(request=request)
        folder = create_folder(data=request_serializer.validated_data, user=request.user)
        response_serializer = self.ResponseSerializer(folder)
        return Response({
            'folder': response_serializer.data
        }, status=status.HTTP_200_OK)


class FolderUpdateApi(APIView):
    permission_classes = [OwnerPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Folder
            fields = ['id', 'name', 'created_at', 'updated_at']

    def put(self, request, folder_id):
        request_serializer = self.RequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        folder = get_folders_by(id=folder_id).first()
        self.check_object_permissions(request=request, obj=folder)
        folder = update_folder(data=request_serializer.validated_data, folder=folder)
        response_serializer = self.ResponseSerializer(folder)
        return Response({
            'folder': response_serializer.data
        }, status=status.HTTP_200_OK)


class FolderDeleteApi(APIView):
    permission_classes = [OwnerPermission, ]

    def delete(self, request, folder_id):
        folder = get_folders_by(id=folder_id).first()
        self.check_object_permissions(request=request, obj=folder)
        delete_folder(folder=folder)
        return Response({
        }, status=status.HTTP_200_OK)
