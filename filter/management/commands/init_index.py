from ...documents import ProductDocument
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Initialize Elasticsearch index for products'

    def handle(self, *args, **options):
        self.stdout.write("Initializing Elasticsearch index...")
        ProductDocument.init()
        self.stdout.write(self.style.SUCCESS("Index initialized successfully"))
