from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django_kombu.worker import global_worker
import daemon

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--daemon', '-d', dest='daemon',
            help="run as daemon"),
    )
    help = "kombu worker"

    def handle(self, *args, **options):
        print "kombu worker is running"
        daemon = option_list.get('daemon')
        if daemon:
            with daemon.DaemonContext():
                global_worker.run()
        else:
            global_worker.run()
