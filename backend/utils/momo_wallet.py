import hmac
import hashlib
import requests
from django.conf import settings
import uuid

from utils.custom_exceptions import *

endpoint = 'https://test-payment.momo.vn/gw_payment/transactionProcessor'
partner_code = settings.PARTNER_CODE
access_key = settings.MOMO_ACCESS_KEY
secret_key = settings.MOMO_SECRET_KEY.encode('utf-8')

order_info = str(uuid.uuid4())


def make_request(bill):
    return_url = f"{settings.VUE_HOST}/bills"
    notify_url = f"{settings.DJANGO_HOST}/api/bills/notify"
    amount = str(bill.amount)
    order_id = bill.order_id
    request_id = str(uuid.uuid4())
    request_type = 'captureMoMoWallet'
    extra_data = ''
    raw_signature = f"partnerCode={partner_code}&accessKey={access_key}&requestId={request_id}&amount={amount}" \
                    f"&orderId={order_id}&orderInfo={order_info}&returnUrl={return_url}&notifyUrl={notify_url}" \
                    f"&extraData={extra_data}"
    signature = hmac.new(secret_key, raw_signature.encode('utf-8'), hashlib.sha256).hexdigest()

    data = {
        'partnerCode': partner_code,
        'accessKey': access_key,
        'requestId': request_id,
        'amount': amount,
        'orderId': order_id,
        'orderInfo': order_info,
        'returnUrl': return_url,
        'notifyUrl': notify_url,
        'extraData': extra_data,
        'requestType': request_type,
        'signature': signature
    }

    response = requests.post(endpoint, json=data).json()
    if response.get('errorCode') != 0:
        bill.order_id = str(uuid.uuid4())
        bill.save(update_fields=['order_id'])
        raise PaymentFailed
    return response.get('payUrl'), response.get('signature')
