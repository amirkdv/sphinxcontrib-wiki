html:
	rm -rf docs/_build
	cd docs && sphinx-build -v -b html . _build
	@echo visit file://$(shell readlink -f docs)/_build/index.html

docs/modules.rst:
	sphinx-apidoc -f -e -o docs some_pkg

pdf:
	cd docs && sphinx-build -b latex . _build
	rm -f $@
	make -C docs/_build all-pdf

.PHONY: html pdf todo loc docs/modules.rst
