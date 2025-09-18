from ...documents import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Initialize Elasticsearch index for products'

    def handle(self, *args, **options):
        self.stdout.write("Initializing Elasticsearch index...")
        #ProductDocument.init()
        #CategoryDocument.init()
        OrderedProductDocument.init()
        CartDocument.init()
        self.stdout.write(self.style.SUCCESS("Index initialized successfully"))
