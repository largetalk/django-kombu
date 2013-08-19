from django_kombu.settings import kombu_settings
from kombu import Connection
from kombu import Exchange, Queue
import itertools

def get_queue_arguments(setting):
    return len(setting) >3 and setting[3] or {}

default_connection = Connection(kombu_settings.TRANSPORT)
default_exchange = Exchange(name = kombu_settings.EXCHANGE['name'],
                            type = kombu_settings.EXCHANGE['type'],
                            durable = kombu_settings.EXCHANGE['durable'],
                            auto_delete = kombu_settings.EXCHANGE['auto_delete'])

task_queues = [ Queue(q[0], default_exchange, q[1], queue_arguments=get_queue_arguments(q)) for q in kombu_settings.QUEUES ]
