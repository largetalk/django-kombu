from kombu.common import maybe_declare
from kombu.pools import producers
from django_kombu.connection import default_connection, default_exchange

__all__ = ['publish']

def emit(connection, exchange, routing_key, message):
    with producers[connection].acquire(block=True) as producer:
        maybe_declare(exchange, producer.channel)
        producer.publish(message,
                         serialize='json',
                         compression='bzip2',
                         exchange=exchange,
                         routing_key=routing_key)

def publish(routing_key, message):
    emit(default_connection, default_exchange, routing_key, message)
