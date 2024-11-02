import redis
import json
from elasticsearch import Elasticsearch
import threading
import time

# Redis ve Elasticsearch bağlantıları
r = redis.Redis(host='redis', port=6379, db=0, password='mypassword')
es = Elasticsearch(
            hosts=[{"host": "elasticsearch", "port": 9200}]
        )

def process_task(task):
    try:
        es.index(index="logs", body=task)
        print(f"Logged to Elasticsearch: {task}")
    except Exception as e:
        print(f"Error logging to Elasticsearch: {e}")

def worker():
    while True:
        _, message = r.blpop("task_queue")  # Kuyruktan mesaj al
        task = json.loads(message)
        thread = threading.Thread(target=process_task, args=(task,))
        thread.start()
        thread.join()

if __name__ == "__main__":
    print("Worker running with multithreading...")
    threading.Thread(target=worker).start()

