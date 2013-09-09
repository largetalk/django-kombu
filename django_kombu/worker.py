from __future__ import with_statement
import gevent
import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool

from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu.utils import kwdict, reprcall
from kombu.utils.encoding import safe_repr

from kombu import Exchange, Queue
from django_kombu.connection import default_connection, task_queues

from functools import partial
import collections, traceback

logger = get_logger(__name__)

class Worker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
        self.handlers = collections.defaultdict(list)
        self._loaded_handlers = False
        self._pool = Pool(5) #pool size

    def add_handler(self, queue, handler):
        self.handlers[queue].append(handler)

    def run(self):
        if not self._loaded_handlers:
            from django_kombu.settings import kombu_settings, perform_import
            for q in kombu_settings.QUEUES:
                for handler_cls in perform_import(q[2], 'QUEUE'):
                    self.add_handler(q[0], handler_cls())
            self._loaded_handlers = True

        super(Worker, self).run()

    def get_consumers(self, Consumer, channel):
        callbacks = [ partial(self.dispatch_message, q.name) for q in task_queues ]

        return [
            Consumer(queues=q, callbacks=[cb]) for q, cb in zip(task_queues, callbacks)
        ]

    def dispatch_message(self, queue, *args):
        for handler in self.handlers[queue]:
            if handler.match(*args):
                try:
                    self._pool.spawn(lambda : handler.handle(*args))
                    #handler.handle(*args)
                except:
                    logger.error(traceback.format_exc())
                else:
                    logger.info('SUCCESS: %(routing_key)s %(body)s' % dict(
                        body        = args[0],
                        routing_key = args[1].delivery_info['routing_key']
                    ))

    def on_connection_error(self, exc, interval):
        logger.error('Broker connection error: %r. Trying again in %s seconds.', exc, interval)

    def on_decode_error(self, message, exc):
        logger.error("Can't decode message body: %r (type:%r encoding:%r raw:%r')",
              exc, message.content_type, message.content_encoding,
              safe_repr(message.body)
        )

global_worker = Worker(default_connection)

if __name__ == '__main__':
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    setup_logging(loglevel='INFO')

    with Connection('amqp://guest:guest@localhost//') as conn:
        try:
            Worker(conn).run()
        except KeyboardInterrupt:
            print('bye bye')
