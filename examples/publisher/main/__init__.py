from django_kombu.client import publish
print 'begin emit message'
publish('test.abc', {'a':1})
publish('test.bcd', {'b':2})
