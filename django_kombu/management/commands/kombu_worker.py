from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--daemon', '-d', dest='daemon',
            help="run as daemon"),
    )
    help = "kombu worker"

    def handle(self, *args, **options):
        print "This is kombu worker"
