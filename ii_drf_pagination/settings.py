"""
Settings for ideallical drf pagination are all namespaced in the
II_DRF_PAGINATION setting.
For example your project's `settings.py` file might look like this:

II_DRF_PAGINATION = {
    'PAGE_SIZE_QUERY_PARAM': None,
}

This module provides the `pagination_setting` object, that is used to access
ideallical DRF pagination settings, checking for user settings first, then
falling back to the defaults.
"""
from __future__ import unicode_literals
from importlib import import_module

from django.conf import settings
from django.test.signals import setting_changed
from django.utils import six


DEFAULTS = {
    'PAGE_SIZE_QUERY_PARAM': None,


    'INCLUDE_COUNT': True,
    'LABEL_COUNT': 'count',

    'INCLUDE_NEXT': True,
    'LABEL_NEXT': 'next',

    'INCLUDE_PREVIOUS': True,
    'LABEL_PREVIOUS': 'previous',

    'INCLUDE_NEXT_PAGE_NUMBER': True,
    'LABEL_NEXT_PAGE_NUMBER': 'next_page_number',

    'INCLUDE_PREVIOUS_PAGE_NUMBER': True,
    'LABEL_PREVIOUS_PAGE_NUMBER': 'previous_page_number',

    'INCLUDE_PAGE_SIZE': True,
    'LABEL_PAGE_SIZE': 'page_size',

    'INCLUDE_RESULTS': True,
    'LABEL_RESULTS': 'results',

    'INCLUDE_PAGE_LINKS': True,
    'LABEL_PAGE_LINKS': 'page_links',

    'INCLUDE_CURRENT_PAGE_NUMBER': True,
    'LABEL_CURRENT_PAGE_NUMBER': 'current_page_number'
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = ()


# List of settings that have been removed
REMOVED_SETTINGS = ()


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, six.string_types):
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
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '{}' for API setting '{}'. {}: {}.".format(
            val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class PaginationSettings(object):
    """
    A settings object, that allows Pagination settings to be accessed as
    properties.
    For example:

        from ii_drf_pagination.settings import pagination_settings
        print(pagination_settings.VERSION)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'II_DRF_PAGINATION', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid Pagination setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "https://github.com/ideallical/ii_drf_pagination/"
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '{}' setting has been removed. Please refer to '{}' "
                    "for available settings.".format(setting, SETTINGS_DOC))
        return user_settings


pagination_settings = PaginationSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_pagination_settings(*args, **kwargs):
    global pagination_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'II_DRF_PAGINATION':
        pagination_settings = PaginationSettings(
            value, DEFAULTS, IMPORT_STRINGS)


setting_changed.connect(reload_pagination_settings)
