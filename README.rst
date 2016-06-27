===========================
A Wiki extension for Sphinx
===========================

|teststatus| |docstatus| |pypistatus|

An extension for sphinx_ that allows wiki pages to be defined section by section
and assembled on demand using two custom directives: ``wikisection``, and
``wikipage``, respectively. This is particularly useful for code documentation
(although arbitrary sphinx documents can use the directives) by allowing
external documentation files to be broken down to sections and placed in
docstrings for corresponding portions of code.

To get started, install the package via PyPI_, follow the docs_ and
sample usage in the tests_ directory.

.. _PyPi: https://pypi.python.org/pypi/sphinxcontrib-wiki/
.. _sphinx: https://www.sphinx-doc.org/
.. _tests: https://github.com/amirkdv/sphinxcontrib-wiki/blob/master/tests/
.. _docs: http://sphinxcontrib-wiki.readthedocs.io/en/latest/wiki.html

.. |docstatus| image:: https://readthedocs.org/projects/sphinxcontrib-wiki/badge/?version=latest
    :target: http://sphinxcontrib-wiki.readthedocs.org/en/latest

.. |teststatus| image:: https://circleci.com/gh/amirkdv/sphinxcontrib-wiki.svg?style=shield
    :target: https://circleci.com/gh/amirkdv/sphinxcontrib-wiki

.. |pypistatus| image:: https://img.shields.io/pypi/v/sphinxcontrib-wiki.svg
    :target: https://pypi.python.org/pypi/sphinxcontrib-wiki/
