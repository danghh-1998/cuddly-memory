from django.urls import path
from .apis import *

urlpatterns = [
    path('bills', BillListApi.as_view(), 'list_bills'),
    path('bills/<int:bill_id>', BillDetailApi.as_view(), 'bill_detail'),
    path('bills/<int:bill_id>', BillMakePaymentApi.as_view(), 'bill_make_payment'),
    path('bills/notify', BillNotifyApi.as_view(), 'bill_notify'),
]
