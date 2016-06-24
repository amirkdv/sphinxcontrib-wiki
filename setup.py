# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


requires = ['Sphinx>=0.6']  # TODO check

setup(
    name='sphinxcontrib-wiki',
    version='0.1',
    url='https://github.com/amirkdv/sphinxcontrib-wiki',
    license='BSD',
    author='Amir Kadivar',
    author_email='amir@amirkdv.ca',
    description='A simple wiki extension for Sphinx',
    long_description="""Allow wiki pages to be defined section by section in
        docstrings and assembled on demand in a sphinx documents.""",
    zip_safe=False,
    classifiers=[
        #   TODO cf. https://pypi.python.org/pypi?%3Aaction=list_classifiers
        #
        #  'Development Status :: 5 - Production/Stable',
        #  'Environment :: Console',
        #  'Environment :: Web Environment',
        #  'Framework :: Sphinx :: Extension',
        #  'Intended Audience :: Developers',
        #  'License :: OSI Approved :: BSD License',
        #  'Operating System :: OS Independent',
        #  'Programming Language :: Python',
        #  'Programming Language :: Python :: 2.6',
        #  'Programming Language :: Python :: 2.7',
        #  'Programming Language :: Python :: 3.2',
        #  'Programming Language :: Python :: 3.3',
        #  'Programming Language :: Python :: 3.4',
        #  'Programming Language :: Python :: 3.5',
        #  'Topic :: Documentation',
        #  'Topic :: Documentation :: Sphinx',
        #  'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
