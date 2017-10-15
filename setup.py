import os
import re
from io import open

from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])

    return {package: filepaths}


version = get_version('ii_drf_pagination')

setup(
    name='ii_drf_pagination',
    version=version,
    description='ideallical django-restframework pagination',
    url='https://github.com/ideallical/ii-drf-pagination',
    download_url=('https://github.com/ideallical/ii-drf-pagination/archive/'
                  '{}.tar.gz'.format(version)),
    author='ideallical',
    author_email='info@ideallical.com',
    keywords=['drf', 'pagination'],
    license='BSD',
    install_requires=[
        'ii-django-package-settings>=0.1',
    ],
    packages=['ii_drf_pagination'],
    zip_safe=False
)
