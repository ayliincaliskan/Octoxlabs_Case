import json
import redis

from elasticsearch import Elasticsearch
from django.conf import settings


def redis_connection():
    r = redis.Redis(host=f'{settings.REDIS_HOST}', port=settings.REDIS_PORT, db=0, password=f'{settings.REDIS_PASSWORD}')
    return r

def elasticsearch_connection():
    es = Elasticsearch(hosts=[{"host": f'{settings.ELASTICSEARCH_HOST}', "port": settings.ELASTICSEARCH_PORT}])
    return es

def create_task(message, title, value):
    r = redis_connection()
    task = {
        "action": f"{message}",
        f"{title}": f"{value}"
    }
    r.rpush("task_queue", json.dumps(task))
