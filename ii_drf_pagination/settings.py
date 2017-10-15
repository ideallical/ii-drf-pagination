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
from ii_django_package_settings.settings import PackageSettings


class PaginationSettings(PackageSettings):
    NAME = 'II_DRF_PAGINATION'
    DOC = 'https://github.com/ideallical/ii-drf-pagination/'
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


pagination_settings = PaginationSettings(None)
