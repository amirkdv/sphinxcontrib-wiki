DOCS_EXCLUDE = tests
DOCS_OUT = docs
DOCS_BUILD = _build
html:
	rm -rf $(DOCS_OUT)/$(DOCS_BUILD)
	sphinx-apidoc -f -e -o $(DOCS_OUT) sphinxcontrib
	rm -f $(DOCS_OUT)/modules.rst $(DOCS_OUT)/sphinxcontrib.rst
	cd $(DOCS_OUT) && sphinx-build -v -b html . $(DOCS_BUILD)
	@echo visit file://$(shell readlink -f $(DOCS_OUT))/$(DOCS_BUILD)/index.html

# FIXME
pdf:
	cd docs && sphinx-build -b latex . _build
	rm -f $@
	make -C docs/_build all-pdf

todo:
	find . -type f -regex '.*\(\.py\|\.c\|\.h\|Makefile\|\.mk\)' | xargs grep -C2 -nP --color 'FIXME|TODO|BUG'

loc:
	find sphinxcontrib -type f -regex '.*\(\.py\)' | xargs wc -l

tests:
	tox

env:
	virtualenv env
	. env/bin/activate && pip install flake8 sphinx sphinx_rtd_theme sphinx_testing bs4 pytest

env3:
	pyvenv env3
	. env3/bin/activate && pip install flake8 sphinx sphinx_rtd_theme sphinx_testing bs4 pytest

.PHONY: html pdf todo loc tests
