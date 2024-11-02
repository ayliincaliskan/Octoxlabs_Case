from elasticsearch import Elasticsearch
import redis


def redis_connection():
    r = redis.Redis(host='redis', port=6379, db=0, password='mypassword')
    return r

def elasticsearch_connection():
    es = Elasticsearch(hosts=[{"host": "elasticsearch", "port": 9200}])
    return es