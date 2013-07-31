from django_kombu.client import publish
publish('test.abc', {'a':1})
