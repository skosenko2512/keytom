import asyncio
from django.core.management.base import BaseCommand
from corebank.accounts.messaging import start_consumers
class Command(BaseCommand):
    help = "Run NATS JetStream subscribers."
    def handle(self, *args, **options):
        asyncio.run(start_consumers())
