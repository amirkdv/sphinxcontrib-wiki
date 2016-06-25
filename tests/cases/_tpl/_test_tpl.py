# -*- coding: utf-8 -*-
from sphinx_testing import with_app
import os.path
import sys

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(this_dir))
from util import find_sub

@with_app(buildername='html', srcdir=os.path.join(this_dir, 'docs/'))
def test_build_html(app, status, warning):
    app.builder.build_all()
    assert not warning.getvalue()

# for print debugging:
if __name__ == '__main__':
    test_build_html()
