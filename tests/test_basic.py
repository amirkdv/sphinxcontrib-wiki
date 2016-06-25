# -*- coding: utf-8 -*-

from sphinx_testing import with_app
from bs4 import BeautifulSoup
import os.path

def _find_sub(parent, text):
    """
    Given an a ToC entry find an entry directly underneath it with the given
    text. Here is the structure of a rendered table of contents with two levels
    of depth:

        .. code-block:: html

            <div class="toctree-wrapper compound">
             <ul>
              <li>
               <a href="foo">Grandparent</a>
               <ul>
                <li>
                 <a href="bar">Parent</a>
                 <ul>
                  <li>
                    <a href="baz">Child</a>
                  </li>
                 </ul>
                </li>
               </ul>
              </li>
            </div>

    For convenience, the provided parent can be either the <a> tag of the parent
    entry or the <ul> tag containing all its ToC descendents.
    """
    assert parent.name in ['a', 'ul']
    ul = parent.nextSibling if parent.name == 'a' else parent
    for child in ul.findChildren(recursive=False):
        sub = child.find('a', href=True, text=text, recursive=False)
        if sub:
            return sub
    return None

@with_app(buildername='html', srcdir='tests/cases/docs-experiment/docs')
def test_build_html(app, status, warning):
    app.builder.build_all()
    assert not warning.getvalue()

    with open(os.path.join(app.srcdir, '_build', 'index.html')) as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    toc = soup.find('div', {'class': 'toctree-wrapper'})
    toc = toc.findChildren()[0]
    assert toc

    docroot = _find_sub(toc, 'Wiki')
    assert docroot

    pageroot = _find_sub(docroot, 'Wiki Root')
    assert pageroot

    pkg_sec = _find_sub(pageroot, 'Section from pkg')
    assert pkg_sec

    assert _find_sub(pkg_sec, 'Section from pkg.mod_a')
    assert _find_sub(pkg_sec, 'Section from pkg.mod_a.SomeClass')

# for print debugging:
if __name__ == '__main__':
    test_build_html()
