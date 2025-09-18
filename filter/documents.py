# from django.contrib.auth.models import User
# from django_elasticsearch_dsl import Document, fields, Text, Date, Keyword, Nested
# from django_elasticsearch_dsl.registries import registry
# from .models import *
# from datetime import datetime 
from elasticsearch_dsl import Document, Text, Float, Integer, Date, Keyword, analyzer

text_analyzer = analyzer(
    'text_analyzer',
    tokenizer="standard",
    filter=["lowercase", "asciifolding"]
)

class ProductDocument(Document):
    id = Keyword() # name.created_at
    name = Text(analyzer=text_analyzer)
    description = Text(analyzer=text_analyzer)
    price = Float()
    category = Keyword()
    tags = Keyword(multi=True)
    created_at = Date()

    class Index:
        name = 'products'  
        settings = {
            "number_of_shards": 1,            
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "text_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding"]
                    }
                }
            }
        }

'''PUT /products
{
  "mappings": {
    "properties": {
      "id": {"type": "keyword"},
      "name": {"type": "text"},
      "description": {"type": "text"},
      "price": {"type": "float"},
      "category": {"type": "keyword"},
      "tags": {"type": "keyword"},
      "created_at": {"type": "date"}
    }
  }
}'''


class CategoryDocument(Document):
    name = Text(analyzer=text_analyzer, fields={'raw': Keyword()})
    description = Text(analyzer=text_analyzer)

    class Index:
        name = 'categories'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "text_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding"]
                    }
                }
            }
        }

class OrderedProductDocument(Document):
    id = Keyword()
    user_id = Keyword()
    product_id = Keyword()
    number = Integer()
    price = Float()
    ordered_at = Date()

    class Index:
        name = 'ordered_products'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "text_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding"]
                    }
                }
            }
        }

class CartDocument(Document):
    user_id = Keyword()
    product_ids = Keyword(multi=True)
    numbers = Integer(multi=True)
    total_price = Float()
    state = Keyword()
    updated_at = Date()

    class Index:
        name = 'carts'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "text_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding"]
                    }
                }
            }
        }

'''state:
open
close
'''