# -*- coding: utf-8 -*-
import os.path
from bs4 import BeautifulSoup

try:
    from io import open
except ImportError:
    pass

def find_sub(parent, text):
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

def get_html_soup(app, path):
    with open(os.path.join(app.outdir, path), encoding='utf-8') as f:
        html = f.read()

    # get rid of whitespace; otherwise tests break cf.
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#next-sibling-and-previous-sibling
    html = ''.join(line.strip() for line in html.split('\n'))

    return BeautifulSoup(html, 'html.parser')
