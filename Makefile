DOCS_EXCLUDE = tests
DOCS_OUT = docs
DOCS_BUILD = _build
html:
	rm -rf $(DOCS_OUT)/$(DOCS_BUILD)
	sphinx-apidoc -f -e -o $(DOCS_OUT) sphinxcontrib
	rm -f $(DOCS_OUT)/modules.rst $(DOCS_OUT)/sphinxcontrib.rst
	cd $(DOCS_OUT) && sphinx-build -v -b html . $(DOCS_BUILD)
	@echo visit file://$(shell readlink -f $(DOCS_OUT))/$(DOCS_BUILD)/index.html

pdf:
	cd docs && sphinx-build -b latex . _build
	rm -f $@
	make -C docs/_build all-pdf

todo:
	find . -type f -regex '.*\(\.py\|\.c\|\.h\|Makefile\|\.mk\)' | xargs grep -C2 -nP --color 'FIXME|TODO|BUG'

loc:
	find sphinxcontrib -type f -regex '.*\(\.py\)' | xargs wc -l

env:
	virtualenv env
	. env/bin/activate && \
		pip install -e . && \
		pip install -e .[tests] && \
		pip install -e .[docs]

env3:
	pyvenv env3
	. env3/bin/activate && \
		pip install -e . && \
		pip install -e .[tests] && \
		pip install -e .[docs]

DOCKER_IMG = amirkdv/python3
docker_image:
	cat Dockerfile | docker build -t $(DOCKER_IMG) -

docker_run:
	docker run -it -v $(PWD):/var/build $(DOCKER_IMG) bash

publish:
	python setup.py register
	python setup.py sdist upload
	rm -f ~/.pypirc

.PHONY: README.rst html pdf todo loc tests docker_image docker_run
