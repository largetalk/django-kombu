#django-kombu  

Celery is cool, but it couldn't use to switch messages between system, with different language

so django-kombu is a utility for product message, comsume message in django

install:

    pip install -e https://github.com/largetalk/django-kombu.git#egg=django_kombu

settings:

add 'django_kombu' to settings.INSTALLED_APPS, and configs to settings.py

    DJ_KOMBU = {
        'TRANSPORT': 'amqp://guest:guest@localhost:5672//',
        'EXCHANGE': {
            'name': 'tasks',
            'type': 'topic',
            'durable': True,
            'auto_delete': False,
        },
        'QUEUES': (
            ('test_queue', 'test.*', ['django_kombu.tasks.PrintTestHandler',]),
        )
    }

worker:

    python manage.py kombu_worker [-d]

publish:

    from django_kombu.client import publish
    publish('test.abc', {'test':'for fun'})

