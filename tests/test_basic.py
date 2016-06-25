# -*- coding: utf-8 -*-

from sphinx_testing import with_app
from bs4 import BeautifulSoup
import os.path

"""
<div class="toctree-wrapper compound">
 <ul>
  <li>
   <a href="a_wiki.html"> Wiki </a>
   <ul>
    <li>
     <a href="a_wiki.html#wiki"> Wiki Root </a>
     <ul>
      <li>
        <a href="a_wiki.html#section-from-pkg"> Section from pkg </a>
      </li>
     </ul>
    </li>
   </ul>
  </li>
</div>
"""


def _find_sub(ul, text):
    for child in ul.findChildren(recursive=False):
        sub = child.find('a', href=True, text=text)
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
    toc_ul = toc.findChildren()[0]
    assert toc_ul

    root = _find_sub(toc_ul, 'Wiki Root')
    assert root

    pkg_sec = _find_sub(root.nextSibling, 'Section from pkg')
    assert pkg_sec

    assert _find_sub(pkg_sec.nextSibling, 'Section from pkg.mod_a')
    assert _find_sub(pkg_sec.nextSibling, 'Section from pkg.mod_a.SomeClass')

# for print debugging:
if __name__ == '__main__':
    test_build_html()
