html:
	rm -rf docs/_build
	sphinx-apidoc -f -e -o docs sphinxcontrib
	cd docs && sphinx-build -v -b html . _build
	@echo visit file://$(shell readlink -f docs)/_build/index.html

# FIXME
pdf:
	cd docs && sphinx-build -b latex . _build
	rm -f $@
	make -C docs/_build all-pdf

todo:
	find . -type f -regex '.*\(\.py\|\.c\|\.h\|Makefile\|\.mk\)' | xargs grep -C2 -nP --color 'FIXME|TODO|BUG'

loc:
	find sphinxcontrib -type f -regex '.*\(\.py\)' | xargs wc -l

.PHONY: html pdf todo loc
