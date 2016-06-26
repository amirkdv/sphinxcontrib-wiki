# -*- coding: utf-8 -*-
from sphinx_testing import with_app
import os.path

from ..util import find_sub, get_html_soup

this_dir = os.path.abspath(os.path.dirname(__file__))
srcdir = os.path.join(this_dir, 'docs/')

@with_app(buildername='html', srcdir=srcdir)
def test_build_html(app, status, warning):
    # NOTE we cannot use ``assert not warning.getvalue()`` since ``with_app``
    # always causes warnings upon its second usage for the way extensions are
    # loaded. The reason is that each extension's ``setup()`` gets called a
    # second time (i.e no memory of the extension is kept) but the visitor
    # methods are already added to docutils.nodes.GenericNodeVisitor.
    # cf.
    #   sphinx_testing.TestApp.__init__()
    #   sphinx.application.Sphinx.__init__()
    #   sphinx.application.Sphinx.setup_extension()
    #   docutils.nodes._add_node_class_names()
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'index.html'))


@with_app(buildername='latex', srcdir=srcdir)
def test_build_latex(app, status, warning):
    app.builder.build_all()
    assert os.path.exists(os.path.join(app.outdir, 'pkg.tex'))


# for print debugging:
if __name__ == '__main__':
    test_build_html()
    test_build_latex()
