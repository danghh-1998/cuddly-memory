from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from .managers import BillManager
from clients.models import Client


class Bill(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    UNPAID = 0
    PAID = 1
    BILL_STATUSES = (
        (PAID, 'PAID'),
        (UNPAID, 'UNPAID')
    )

    order_id = models.CharField(max_length=255)
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.IntegerField()
    signature = models.CharField(max_length=255)
    status = models.IntegerField(choices=BILL_STATUSES, default=0)
    client = models.ForeignKey(Client, related_name='bills', on_delete=models.SET_NULL, unique=False, null=True)
    payment_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BillManager()

    class Meta:
        app_label = 'bills'
        db_table = 'bill'

    def __str__(self):
        return self.order_id
