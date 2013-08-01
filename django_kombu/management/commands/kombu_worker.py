from sys import platform
from contextlib import contextmanager
from optparse import make_option
from django.core.management.base import BaseCommand

try:
    from daemon import DaemonContext as fork_process
except ImportError:
    @contextmanager
    def fork_process(): yield

class Command(BaseCommand):
    help = "Staring kombu worker"
    option_list = BaseCommand.option_list + (
        make_option('--daemon', '-d', dest='daemon',
            action='store_true', default=False,
            help="run as daemon"),
    )
    
    def handle(self, *args, **options):        
        try:
            from django_kombu.worker import global_worker

            quit_command = (platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C'
            print 'Starting worker...'
            print 'Connection is %s' % global_worker.connection.as_uri()
            print 'Quit the worker with %s' % quit_command

            if options.get('daemon'):
                with fork_process():
                    global_worker.run()
            else:
                global_worker.run()
        except KeyboardInterrupt:
            global_worker.connection.release()
        finally:
            print 'bye'
