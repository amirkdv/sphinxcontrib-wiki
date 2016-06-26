# -*- coding: utf-8 -*-
from sphinx_testing import with_app
import sys
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

    docroot = find_sub(toc, 'Master Title')
    assert docroot, 'The document master title must be in the ToC'

    pageroot = find_sub(docroot, 'Page Title')
    assert pageroot, 'The wiki page must be directly underneath the master doc'

    secroot = find_sub(pageroot, 'Section Title')
    assert secroot, 'The wiki section must be directly underneath the wiki page'


@with_app(buildername='latex', srcdir=srcdir)
def test_build_latex(app, status, warning):
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'pkg.tex'))


# for print debugging:
if __name__ == '__main__':
    test_build_html()
    test_build_latex()
