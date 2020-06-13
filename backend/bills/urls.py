from django.urls import path
from .apis import *

urlpatterns = [
    path('bills', BillListApi.as_view(), name='list_bills'),
    path('bills/<int:bill_id>', BillDetailApi.as_view(), name='bill_detail'),
    path('bills/<int:bill_id>/make_payment', BillMakePaymentApi.as_view(), name='bill_make_payment'),
    path('bills/notify', BillNotifyApi.as_view(), name='bill_notify'),
]
