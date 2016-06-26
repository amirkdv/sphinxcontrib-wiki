# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='sphinxcontrib-wiki',
    version='0.1',
    url='https://github.com/amirkdv/sphinxcontrib-wiki',
    license='MIT',
    author='Amir Kadivar',
    author_email='amir@amirkdv.ca',
    description='A simple wiki extension for Sphinx',
    long_description="""Allow wiki pages to be defined section by section in
        docstrings and assembled on demand in a sphinx documents.""",
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        #   TODO cf. https://pypi.python.org/pypi?%3Aaction=list_classifiers
        #
        #  'Development Status :: 5 - Production/Stable',
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
