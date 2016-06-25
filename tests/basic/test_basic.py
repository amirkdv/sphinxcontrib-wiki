# -*- coding: utf-8 -*-
from sphinx_testing import with_app
import os.path
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(this_dir))
from util import find_sub, BeautifulSoup

srcdir = os.path.join(this_dir, 'docs/')

@with_app(buildername='html', srcdir=srcdir)
def test_build_html(app, status, warning):
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'index.html'))

    with open(os.path.join(app.outdir, 'index.html')) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    toc = soup.select('.sphinxsidebarwrapper > ul')[0]
    assert toc, 'There must be a ToC in the sidebar'

    docroot = find_sub(toc, 'Master Title')
    assert docroot, 'The document master title must be in the ToC'

    pageroot = find_sub(docroot, 'Page Title')
    assert pageroot, 'The wiki page must be directly underneath the master doc'

    secroot = find_sub(pageroot, 'Section Title')
    assert secroot, 'The wiki section must be directly underneath the wiki page'

# for print debugging:
if __name__ == '__main__':
    test_build_html()
