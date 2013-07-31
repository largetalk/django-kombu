from django_kombu.settings import kombu_settings
from kombu import Connection
from kombu import Exchange, Queue
import itertools

default_connection = Connection(kombu_settings.TRANSPORT)
default_exchange = Exchange(name = kombu_settings.EXCHANGE['name'],
                            type = kombu_settings.EXCHANGE['type'],
                            durable = kombu_settings.EXCHANGE['durable'],
                            auto_delete = kombu_settings.EXCHANGE['auto_delete'])

task_queues = [ Queue(q[0], default_exchange, q[1]) for q in kombu_settings.QUEUES ]
queue_handle_pairs = list(itertools(task_queues, [ q[2] for q in kombu_settings.QUEUES ]))
