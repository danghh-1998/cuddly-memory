from .models import Bill
from utils.custom_exceptions import *
from utils.momo_wallet import make_request


def get_bills_by(raise_exception=True, with_deleted=False, **kwargs):
    bills = Bill.objects.all_with_deleted().filter(**kwargs) if with_deleted else Bill.objects.filter(**kwargs)
    if raise_exception:
        raise ObjectNotFound
    return bills


def make_payment(bill):
    if bill.status == 1:
        raise PaidBill
    pay_url, signature = make_request(bill=bill)
    bill.signature = signature
    bill.save(update_fields=['signature'])
    return pay_url


def submit_payment(bill, **kwargs):
    if bill.signature != kwargs.get('signature'):
        raise SignatureError
    if kwargs.get('errorCode') != 0:
        raise PaymentFailed
    bill.status = 1
    bill.save(update_fields=['status'])
    return bill
