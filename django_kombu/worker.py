from __future__ import with_statement

from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu.utils import kwdict, reprcall

from kombu import Exchange, Queue
from django_kombu.connection import default_exchange, task_queues

from functools import partial
import collections

logger = get_logger(__name__)

class Worker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
        self.handlers = collections.defaultdict(list)

    def add_handler(self, queue, handler):
        self.handlers[queue].append(handler)

    def get_consumers(self, Consumer, channel):
        callbacks = [ partial(self.dispatch_message, queue = q.name) for q in task_queues ]

        return [
            Consumer(queues=q, callbacks=[cb]) for q, cb in zip(task_queues, callbacks)
        ]

    def dispatch_message(self, queue, *args):
        for handler in self.handlers[queue]:
            if handler.match(*args):
                try:
                    handler.handle(*args)
                except:
                    _logger.error(traceback.format_exc())
                else:
                    _logger.info('SUCCESS: %(routing_key)s %(body)s' % dict(
                        body        = args[0],
                        routing_key = args[1].delivery_info['routing_key']
                    ))

    def on_connection_error(self, exc, interval):
        _logger.error('Broker connection error: %r. Trying again in %s seconds.', exc, interval)

    def on_decode_error(self, message, exc):
        _logger.error("Can't decode message body: %r (type:%r encoding:%r raw:%r')",
              exc, message.content_type, message.content_encoding,
              safe_repr(message.body)
        )

if __name__ == '__main__':
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    setup_logging(loglevel='INFO')

    with Connection('amqp://guest:guest@localhost//') as conn:
        try:
            Worker(conn).run()
        except KeyboardInterrupt:
            print('bye bye')
