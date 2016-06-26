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

    soup = get_html_soup(app, 'index.html')

    toc = soup.find('a', text='Table Of Contents').parent.nextSibling
    assert toc, 'There must be a Table Of Contents'

    doc = find_sub(toc, 'Master Title')
    assert doc, 'The document master title must be in the ToC'

    page = find_sub(doc, 'Page Title')
    assert page, 'The wiki page must be directly underneath the master doc'

    A = find_sub(page, 'A')
    assert A, 'Section A must be at top level of wiki page'
    assert find_sub(page, 'B'), 'Section B must be at top level of wiki page'
    assert find_sub(A, 'A1'), 'Section A1 must be directly below section A'

    A2 = find_sub(A, 'A2')
    assert A2, 'Section A2 must be directly below section A'
    assert find_sub(A2, 'A3'), 'Section A3 must be directly below section A2'


@with_app(buildername='latex', srcdir=srcdir)
def test_build_latex(app, status, warning):
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'pkg.tex'))


# for print debugging:
if __name__ == '__main__':
    test_build_html()
    test_build_latex()
