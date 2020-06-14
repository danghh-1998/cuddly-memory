from datetime import datetime
import uuid

from .models import Bill
from utils.custom_exceptions import *
from utils.momo_wallet import make_request


def get_bills_by(raise_exception=True, with_deleted=False, **kwargs):
    bills = Bill.objects.all_with_deleted().filter(**kwargs) if with_deleted else Bill.objects.filter(**kwargs)
    if not bills and raise_exception:
        raise ObjectNotFound
    return bills


def make_payment(bill):
    if bill.status == 1:
        raise PaidBill
    if bill.status == 0 and bill.signature != '':
        bill.order_id = str(uuid.uuid4())
        bill.save(update_fields=['order_id'])
    pay_url, signature = make_request(bill=bill)
    bill.signature = signature
    bill.save(update_fields=['signature'])
    return pay_url


def submit_payment(bill, **kwargs):
    if kwargs.get('errorCode') != 0:
        raise PaymentFailed
    bill.status = 1
    bill.payment_at = datetime.now()
    bill.save(update_fields=['status', 'payment_at'])
    return bill
