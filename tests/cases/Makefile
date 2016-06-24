html:
	rm -rf docs/_build
	sphinx-apidoc -f -e -o docs biseqt
	cd docs && sphinx-build -v -b html . _build
	@echo visit file://$(shell readlink -f docs)/_build/index.html

pdf:
	cd docs && sphinx-build -b latex . _build
	rm -f $@
	make -C docs/_build all-pdf

.PHONY: html pdf todo loc
