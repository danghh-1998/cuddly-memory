from datetime import datetime

from clients.models import Client
from clients.services import deactivate_client

clients = Client.objects.all()
today = datetime.today()

for client in clients:
    for bill in clients.bills.all():
        if bill.month < today.month - 1 and bill.status == 0:
            deactivate_client(client)
            break
