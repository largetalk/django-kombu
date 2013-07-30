from kombu.common import maybe_declare
from kombu.pools import producers


def emit(connection, exchange, routing_key, message):
    with producers[connection].acquire(block=True) as producer:
        maybe_declare(exchange, producer.channel)
        producer.publish(message,
                         serialize='json',
                         compression='bzip2',
                         exchange=exchange,
                         routing_key=routing_key)
