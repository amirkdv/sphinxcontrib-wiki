# -*- coding: utf-8 -*-

from sphinx_testing import with_app


# FIXME we shouldn't rely on autodoc, commit the docs/*.rst files
# FIXME how to check for warnings
# FIXME how to make sure output is fine
@with_app(buildername='html', srcdir='tests/cases/docs-experiment/docs')
def test_build_html(app, status, warning):
    app.builder.build_all()
