import redis
import json
import threading
from config import (
    ELASTICSEARCH_HOST,
    ELASTICSEARCH_PORT,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT)

from elasticsearch import Elasticsearch

r = redis.Redis(
        host=f'{REDIS_HOST}',
        port=REDIS_PORT,
        db=0,
        password=f'{REDIS_PASSWORD}'
    )

es = Elasticsearch(
        hosts=[{"host": f'{ELASTICSEARCH_HOST}', 
                "port": ELASTICSEARCH_PORT}]
    )


def process_task(task):
    try:
        es.index(index="logs", body=task)
        print(f"Logged to Elasticsearch: {task}")
    except Exception as e:
        print(f"Error logging to Elasticsearch: {e}")

def worker():
    while True:
        _, message = r.blpop("task_queue")
        task = json.loads(message)
        thread = threading.Thread(target=process_task, args=(task,))
        thread.start()
        thread.join()

if __name__ == "__main__":
    print("Worker running with multithreading...")
    threading.Thread(target=worker).start()
