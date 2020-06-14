from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .services import *
from .models import Bill
from .permissions import SuperAdminPermission
from utils.serializer_validator import validate_serializer


class BillListApi(APIView):
    permission_classes = (SuperAdminPermission,)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Bill
            exclude = ['deleted', 'order_id', 'signature', 'client']

    def get(self, request):
        self.check_permissions(request=request)
        bills = get_bills_by(client=request.user.client)
        response_serializer = self.ResponseSerializer(bills, many=True)
        return Response({
            'bills': response_serializer.data
        }, status=status.HTTP_200_OK)


class BillDetailApi(APIView):
    permission_classes = (SuperAdminPermission,)

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Bill
            exclude = ['deleted', 'order_id', 'signature', 'client']

    def get(self, request, bill_id):
        self.check_permissions(request=request)
        bill = get_bills_by(client=request.user.client, id=bill_id)
        self.check_object_permissions(request=request, obj=bill)
        response_serializer = self.ResponseSerializer(bill)
        return Response({
            'bill': response_serializer.data
        }, status=status.HTTP_200_OK)


class BillMakePaymentApi(APIView):
    permission_classes = (SuperAdminPermission,)

    def post(self, request, bill_id):
        self.check_permissions(request=request)
        bill = get_bills_by(client=request.user.client, id=bill_id).first()
        self.check_object_permissions(request=request, obj=bill)
        pay_url = make_payment(bill)
        return Response({
            'pay_url': pay_url
        }, status=status.HTTP_200_OK)


class BillNotifyApi(APIView):
    permission_classes = (AllowAny,)

    class RequestSerializer(serializers.Serializer):
        partnerCode = serializers.CharField(required=True)
        accessKey = serializers.CharField(required=True)
        requestId = serializers.CharField(required=True)
        orderId = serializers.CharField(required=True)
        errorCode = serializers.IntegerField(required=True)
        message = serializers.CharField(required=True)
        responseTime = serializers.CharField(required=True)
        extraData = serializers.CharField(required=True, allow_blank=True)
        signature = serializers.CharField(required=True)

    def post(self, request):
        request_serializer = self.RequestSerializer(data=request.data)
        validate_serializer(request_serializer)
        bill = get_bills_by(order_id=request_serializer.validated_data.get('orderId')).first()
        submit_payment(bill, **request_serializer.validated_data)
        return Response({

        }, status=status.HTTP_200_OK)
