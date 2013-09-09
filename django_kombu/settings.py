"""
Settings for django-kombu are all namespaced in the DJ_KOMBU setting.
For example your project's `settings.py` file might look like this:

DJ_KOMBU = {
    'GEVENT': False,
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

This module provides the `kombu_setting` object, that is used to access
django-kombu settings, checking for user settings first, then falling
back to the defaults.
"""
from __future__ import unicode_literals

from django.conf import settings
from django.utils import importlib

# Try to import six from Django, fallback to included `six`.
try:
    from django.utils import six
except ImportError:
    from django_kombu import six


USER_SETTINGS = getattr(settings, 'DJ_KOMBU', None)

DEFAULTS = {
    'GEVENT': False,
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


# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'TRANSPORT',
)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if isinstance(val, six.string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class KombuSettings(object):
    """
    A settings object, that allows API settings to be accessed as properties.

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}
        self.import_strings = import_strings or ()

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError("Invalid Kombu setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        self.validate_setting(attr, val)

        # Cache the result
        setattr(self, attr, val)
        return val

    def validate_setting(self, attr, val):
        if attr == 'QUEUES':
            for q in val:
                perform_import(q[2], attr)


kombu_settings = KombuSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
