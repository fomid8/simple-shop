from elasticsearch_dsl import connections

connections.create_connection(hosts=['http://localhost:9200'])
