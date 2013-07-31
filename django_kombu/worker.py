from __future__ import with_statement

from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu.utils import kwdict, reprcall

from kombu import Exchange, Queue
from django_kombu.connection import default_exchange, task_queues
from django_kombu.connection import queue_handle_pairs


logger = get_logger(__name__)


class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [ Consumer(queues=q_h[0], callbacks=q_h[1]) for q_h in queue_handle_pairs ]

    #def process_task(self, body, message):
    #    fun = body['fun']
    #    args = body['args']
    #    kwargs = body['kwargs']
    #    logger.info('Got task: %s', reprcall(fun.__name__, args, kwargs))
    #    try:
    #        fun(*args, **kwdict(kwargs))
    #    except Exception, exc:
    #        logger.error('task raised exception: %r', exc)
    #    message.ack()

if __name__ == '__main__':
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    setup_logging(loglevel='INFO')

    with Connection('amqp://guest:guest@localhost//') as conn:
        try:
            Worker(conn).run()
        except KeyboardInterrupt:
            print('bye bye')
