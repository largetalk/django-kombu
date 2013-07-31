#django-kombu  

Celery is cool, but it couldn't use to switch messages between system, with different language

so django-kombu is a utility for product message, comsume message in django

install:

    pip install -e https://github.com/largetalk/django-kombu.git#egg=django_kombu

worker:

    python manage.py kombu_worker [-d]

publish

    from django_kombu.client import publish
    publish('test.abc', {'test':'for fun'})

