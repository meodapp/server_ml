from controller.algorithm import Algorithm
from celery import Celery

from controller.storage_handler import StorageHandler
from utils.elbow_method import Elbow

broker_url = 'amqp://guest:guest@localhost:5672/'

# broker_url = 'redis://localhost:6379/0'
app = Celery('tasks', broker=broker_url)
@app.task
def update_all(k: int, distance_function: int):
    storage_handler = StorageHandler()
    algo = Algorithm(storage_handler=storage_handler, num_clusters=k, distance_function=distance_function)
    algo.create_model()

@app.task
def run_elbow_method():
    e = Elbow()
    e.elbow_check()
