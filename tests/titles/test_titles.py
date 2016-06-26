# -*- coding: utf-8 -*-
from sphinx_testing import with_app
import os.path

from ..util import find_sub, get_html_soup

this_dir = os.path.abspath(os.path.dirname(__file__))
srcdir = os.path.join(this_dir, 'docs/')

@with_app(buildername='html', srcdir=srcdir)
def test_build_html(app, status, warning):
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'index.html'))


@with_app(buildername='latex', srcdir=srcdir)
def test_build_latex(app, status, warning):
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'pkg.tex'))

    assert 'Duplicate Section Title' in warning.getvalue()

    assert 'Using name "[wiki]"' in warning.getvalue()


# for print debugging:
if __name__ == '__main__':
    test_build_html()
    test_build_latex()
