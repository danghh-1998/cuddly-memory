"""
Create Template API
Update Template API
Detail Template API
Delete Template API
Duplicate template API
Template Download Image API
Created on 20/4/2020
"""

from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .services import *
from .permissions import *
from .models import Template
from utils.custom_fields import Base64ImageField
from bounding_boxes.models import BoundingBox
from auth_tokens.services import get_auth_token_by
from utils.static_file_handler import file_downloader
from utils.custom_renderer import PNGRenderer
from utils.serializer_validator import validate_serializer


class TemplateCreateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        image = serializers.ImageField(required=True)
        name = serializers.CharField(required=True, max_length=255)
        folder_id = serializers.IntegerField(required=False)
        bounding_boxes = serializers.CharField(required=True)

    class ResponseSerializer(serializers.ModelSerializer):
        class BoundingBoxSerializer(serializers.ModelSerializer):
            class Meta:
                model = BoundingBox
                exclude = ['deleted']

        bounding_boxes = BoundingBoxSerializer(many=True)

        class Meta:
            model = Template
            exclude = ['deleted']

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        self.check_permissions(request=request)
        template = create_template(user=request.user, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(template)
        return Response({
            'template': response_serializer.data
        }, status=status.HTTP_200_OK)


class TemplateDetailApi(APIView):
    permission_classes = [UserPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class BoundingBoxSerializer(serializers.ModelSerializer):
            class Meta:
                model = BoundingBox
                exclude = ['deleted', 'template']

        bounding_boxes = BoundingBoxSerializer(many=True)

        class Meta:
            model = Template
            exclude = ['deleted']

    def get(self, request, template_id):
        template = get_templates_by(id=template_id).first()
        self.check_object_permissions(request=request, obj=template)
        response_serializer = self.ResponseSerializer(template)
        return Response({
            'template': response_serializer.data
        }, status=status.HTTP_200_OK)


class TemplateDownloadImageApi(APIView):
    permission_classes = [UserPermission, ]
    renderer_classes = [PNGRenderer, ]

    def get(self, request, template_id, image_type):
        template = get_templates_by(id=template_id).first()
        auth_token = get_auth_token_by(key=request.query_params.get('token'))
        allow_dowload_image(auth_token.user, template=template)
        image = file_downloader(file_name=template.name, _type='templates',
                                image_type=image_type)
        return Response(image, status=status.HTTP_200_OK)


class TemplateUpdateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=False)
        image = Base64ImageField(required=False)
        folder_id = serializers.IntegerField(required=False)
        bounding_boxes = serializers.CharField(required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class BoundingBoxSerializer(serializers.ModelSerializer):
            class Meta:
                model = BoundingBox
                exclude = ['deleted']

        bounding_boxes = BoundingBoxSerializer(many=True)

        class Meta:
            model = Template
            exclude = ['deleted']

    def put(self, request, template_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        template = get_templates_by(id=template_id).first()
        self.check_object_permissions(request=request, obj=template)
        template = update_template(**request_serializer.validated_data, template=template)
        response_serializer = self.ResponseSerializer(template)
        return Response({
            'template': response_serializer.data
        }, status=status.HTTP_200_OK)


class TemplateDuplicateApi(APIView):
    permission_classes = [AdminPermission, ]

    class RequestSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255, required=True)
        folder_id = serializers.IntegerField(required=False)

    class ResponseSerializer(serializers.ModelSerializer):
        class BoundingBoxSerializer(serializers.ModelSerializer):
            class Meta:
                model = BoundingBox
                exclude = ['deleted']

        bounding_boxes = BoundingBoxSerializer(many=True)

        class Meta:
            model = Template
            exclude = ['deleted']

    def post(self, request, template_id):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        template = get_templates_by(id=template_id).first()
        self.check_object_permissions(request=request, obj=template)
        new_template = duplicate_template(template, **request_serializer.validated_data)
        response_serializer = self.ResponseSerializer(new_template)
        return Response({
            'template': response_serializer.data
        }, status=status.HTTP_200_OK)


class TemplateDeleteApi(APIView):
    permission_classes = [AdminPermission, ]

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Template
            exclude = ['deleted']

    def delete(self, request, template_id):
        template = get_templates_by(id=template_id).first()
        self.check_object_permissions(request=request, obj=template)
        template = delete_template(template)
        response_serializer = self.ResponseSerializer(template)
        return Response({
            'template': response_serializer.data
        }, status=status.HTTP_200_OK)
