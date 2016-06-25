# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

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
