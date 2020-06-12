import uuid
from datetime import datetime

from clients.models import Client
from bills.models import Bill

clients = Client.objects.all()
today = datetime.today()

for client in clients:
    Bill.objects.create(
        order_id=str(uuid.uuid4()),
        month=today.month,
        year=today.year,
        client=client,
        amount=100000
    )
