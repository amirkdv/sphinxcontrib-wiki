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

    body = soup.find(id='master-title')
    num_occur = len(body.findAll(text='Why?'))
    assert num_occur == 1, 'Wiki sections should be removed from their ' + \
                           'original place of appearance'


    wikisecs = body.findAll('div', {'class': 'wikipage-section'})
    assert wikisecs, 'There should be wiki sections rendered on front page'

    for sec in wikisecs:
        wikisec_refs = sec.findAll('p', {'class': 'section-source'})
        assert wikisec_refs, 'Wiki sections must cite their origin'
        link = wikisec_refs[0].find('a', {'class': 'reference'})
        assert link and link['href'], 'Wiki sections must cite their origin'

    localref = body.find('a', {
        'href': 'some_pkg.other_mod.html#some_pkg.other_mod.wrap_mod_func'
    })
    assert localref, 'References within the same document should work.'

    extref = body.find('a', {
        'href': 'some_pkg.some_mod.html#some_pkg.some_mod.mod_func'
    })
    assert extref, 'References to other documents should work.'

    page_body = body.find('p', text='FAQ page body.')
    assert page_body, 'Wiki page bodies should not be lost'



@with_app(buildername='latex', srcdir=srcdir)
def test_build_latex(app, status, warning):
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'pkg.tex'))


# for print debugging:
if __name__ == '__main__':
    test_build_html()
    test_build_latex()
