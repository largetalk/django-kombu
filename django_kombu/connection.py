from django_kombu.settings import kombu_settings
from kombu import Connection
from kombu import Exchange

default_connection = Connection(kombu_settings.TRANSPORT)
default_exchange = Exchange(name = kombu_settings.EXCHANGE['name'],
                            type = kombu_settings.EXCHANGE['type'],
                            durable = kombu_settings.EXCHANGE['durable'],
                            auto_delete = kombu_settings.EXCHANGE['auto_delete'])
