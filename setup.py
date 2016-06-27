# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

try:
    from io import open
except ImportError:
    pass

with open('README.rst', encoding='utf-8') as f:
    README = f.read()

setup(
    name='sphinxcontrib-wiki',
    version='0.2.3',
    url='https://github.com/amirkdv/sphinxcontrib-wiki',
    license='MIT',
    author='Amir Kadivar',
    author_email='amir@amirkdv.ca',
    description='Assemble sections into wiki pages in sphinx documents',
    long_description=README,
    zip_safe=True,
    classifiers=[ # cf. https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        #  'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #  'Programming Language :: Python :: 3.2',
        #  'Programming Language :: Python :: 3.3',
        #  'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=['sphinx>=0.6'],
    extras_require={
        'tests': [
            'flake8',
            'sphinx_testing',
            'bs4',
            'nose',
            'tox',
        ],
        'docs': ['sphinx_rtd_theme'],
    },
    namespace_packages=['sphinxcontrib'],
)
