# -*- coding: utf-8 -*-
"""
Allow wiki pages to be automatically generated from docstrings.

.. wikisection:: intro
    :title: Basic usage

    ``sphinxcontrib-wiki`` is a Sphinx_ extension which allows wiki pages to be
    automatically generated from docstrings. Here is an example:

    .. _Sphinx: http://www.sphinx-doc.org/

    .. code-block:: rst

      .. wikisection:: example
          :title: Example wiki section title

          Wiki sections must have a body or they are ignored.


    Wiki pages are generated like this:

    .. code-block:: rst

      .. wikipage:: example
          :title: Example wiki section

          Body of a wiki page appears above all its sections.

.. wikisection:: intro
    :title: Section Hierarchy

    By default, the structure of the ``wikisection`` tree within a ``wikipage``
    is determined by module hierarchy, namely:

    - Sections within a module are treated as siblings in the order they
      appear regardless of the depth of the class or function they belong to.
    - Sections within sibling modules are treated as siblings in the order
      they are processed as per ``autodoc_member_order``.
    - Sections within a package are treated as the parent of those in modules
      immediately within it.

    Alternatively, a section can force its parent to a be specific other
    section, for instance:

    .. code-block:: rst

      .. wikisection:: example
          :title: A section with forced parent
          :parent: Example wiki section title

          Mandatory section body.

.. wikisection:: faq
  :title: Section within Sections

  Title elements are not allowed in docstring by docutils or sphinx.
  Other extensions that require this functionality, e.g. numpy, implement
  their own preprocessing methods (cf. ``source-read`` event by sphinx).
  The possible ways nested sections can be achieved by ``sphinxcontrib-wiki``
  are:

  - Separate out the subsection into a ``wikisection`` of its own and assign
    its parent to the parent ``wikisection``, for instance:

    .. code-block:: rst

          .. wikisection:: example
              :title: Parent Section

              Body of parent.

          .. wikisection:: example
              :title: Child Section
              :parent: Parent Section

              Body of child.
  - Use the ``rubric`` directive which allows adding a title within a
    directive body but whose information is lost to the table of contents.

.. wikisection:: faq
  :title: Section Reuse

  It may be desirable to reuse the same section in different wiki pages. This
  is currently not possible as it requires rethinking the ``parent`` option.
  One possibility is to extend the syntax as follows:

  .. code-block:: rst

      .. wikisection:: first, second
          :title: Section belonging to many pages
          :parents: first[Parent in first page], second[_default_]

  Another possibility is to invert the control and let pages decide their
  hierarchy, requiring some preprocessing on raw sources:

  .. code-block:: rst

      .. wikipage:: example
          :tree:
              section1
                  section1.1
                  section1.2
              section2

.. wikisection:: todo
    :title: Tree documentation

    Document more clearly how the wiki page tree structure is determined by
    default: it's all in the dots in rst document name, i.e ideally for python
    packages and potentially confusing otherwise.

.. wikisection:: todo
    :title: Report

    Sphinx API documentation for developing extensions is not friendly to
    newcomers. Document the available sources (docutils, sphinx, and
    extensions in sphinxcontrib) and the basics of creating an extension.
"""

import sphinx
from sphinx import addnodes
from sphinx.util.compat import nodes
from sphinx.util.compat import Directive
from sphinx.environment import NoUri
from docutils.parsers.rst import directives


class wikisection(nodes.section):
    pass


class wikipage(nodes.General, nodes.Element):
    pass


def _name_to_anchor(name):
    return '-'.join(name.split()).lower()


class WikiSection(Directive):
    """
    Handler for the ``wikisection`` directive. Each section has one reqiured
    argument, the identifier of the wikipage to which it belongs, and one
    required option ``title`` which is used by other sections to reference it.
    Furthermore, each section must have a non-empty body.

    By default, the placement of each section, and thus the depth of its title
    heading, is automatically calculated based on the package hirerarchy.
    Optionally, the parent of the section in the page tree, which is another
    section, can be specified as an option, default is ``_default_``. Parent
    resolution is performed as follows:

    1. If parent is ``_default_``, the parent is the last observed section (as
       per sphinx-dictated order of ``traverse``) whose depth is one less than
       this section.
    2. If parent is the title of another section, that section will be forced
       to be the parent of this section.
    3. If parent is ``_none_``, this section is placed in the top level of the
       corresponding wiki page.

    """

    node_class = wikisection
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'title': directives.unchanged,
        'parent': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        if 'title' not in self.options or not self.options['title']:
            env.app.warn('Ignoring wikipage section with no title in %s.' %
                         env.docname)
            return []

        assert self.options['title'] not in ['_none_', '_default_']
        sec = wikisection()
        sec['options'] = {
            'page_name': self.arguments[0],
            'title': self.options['title'],
            'parent': self.options.get('parent', '_default_'),
        }

        self.assert_has_content()

        title_text = self.options['title']
        sec += nodes.title(title_text, title_text)
        self.state.nested_parse(self.content, self.content_offset, sec)

        sec['ids'] = [_name_to_anchor(title_text)]
        return [sec]


class WikiPage(Directive):
    """
    Handler for the ``wikipage`` directive. Each page has one required
    argument, its identifier and a required option, its ``title``. Optionally,
    a page can have a body which will be rendered above all its child sections.
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'title': directives.unchanged,
    }

    def run(self):
        page_node = wikipage()
        env = self.state.document.settings.env
        if 'title' not in self.options or not self.options['title']:
            title = '[' + self.arguments[0] + ']'
            env.app.warn(env.docname,
                         'Using name "%s" for wikipage with no title' % title)
        else:
            title = self.options['title']

        page_node['options'] = {
            'name': self.arguments[0],
            'title': title,
        }

        # The wikipage directive can have its own content, parse it now. For
        # the page sections belonging to it we have to wait until doctree-read
        # for all page sections to be collected.
        self.state.nested_parse(self.content, self.content_offset, page_node)

        return [page_node]


def doctree_read(app, doctree):
    """Handler for sphinx's ``doctree-read`` event. This is where we remove all
    ``wikisection`` nodes from the doctree and store them in the build
    environment.

    .. wikisection:: faq
        :title: Resolving References
        :parent: _none_

        The current implementation stores all sections in the build
        environment after ``doctree-read`` and uses them to populate all pages
        upon ``doctree-resolved``. This is needed to allow all sections to be
        collected before any page is assembled.
    """
    env = app.builder.env

    if not hasattr(env, 'wikisections'):
        env.wikisections = {}

    for node in doctree.traverse(wikisection):
        page_name = node['options']['page_name']
        if page_name not in env.wikisections:
            env.wikisections[page_name] = []

        if app.config['wiki_enabled']:
            env.wikisections[page_name].append({
                'docname': env.docname,
                'depth': env.docname.count('.') + 1,
                'node': node.deepcopy(),
            })
            # Remove the section from its original place.
            node.parent.remove(node)

    # At this point, a document containing wikisections has spurious entries
    # in its ToC; rebuild it.
    env.build_toc_from(env.docname, doctree)


def doctree_resolved(app, doctree, docname):
    """Handler for sphinx's ``doctree-resolved`` event. This is where we replace
    all ``wikipage`` nodes based on the stored sections from the build
    environment and resolve all references.
    """
    env = app.builder.env
    for node in doctree.traverse(wikipage):
        newnode = wikipage_tree(app, env, docname, page_node=node)
        node.replace_self(newnode)

    # At this point, a document containing pages has missing entries in its
    # ToC; rebuild it.
    env.build_toc_from(docname, doctree)

    # Now all pending_xref nodes can be properly resolved.
    # NOTE this is taken, and slightly modified, from
    # sphinx.environment.resolve_references().
    for node in doctree.traverse(addnodes.pending_xref):
        contnode = node[0].deepcopy()
        newnode = None

        typ = node['reftype']
        target = node['reftarget']
        domain = None

        try:
            if 'refdomain' in node and node['refdomain']:
                # let the domain try to resolve the reference
                try:
                    domain = env.domains[node['refdomain']]
                except KeyError:
                    raise NoUri
                # We don't care where the node is actually coming from, i.e
                # its attributes['refdoc']. It now belongs to this document,
                # resolve links as if it belongs to us.
                newnode = domain.resolve_xref(env, docname, app.builder,
                                              typ, target, node, contnode)

        except NoUri:
            newnode = contnode
        node.replace_self(newnode or contnode)


def wikisection_container(app, env, sec_info):
    """Builds a sphinx section corresponding to a given ``wikisection``.

    :param app: The "application", instance of
        :class:`sphinx.application.Sphinx`.
    :param env: The build environment (i.e an instance of
        :class:`sphinx.environment.BuildEnvironment`).
    :param sec_info: A dictionary containing stored info about one section,
        cf. :func:`doctree_read()`.

    :returns: The sphinx section containing the given wiki section.
    :rtype: :class:`sphinx.util.compat.nodes.section`
    """
    sec_node, docname = sec_info['node'], sec_info['docname']

    # Create source citation "[source: :mod:`module.name`]".
    src = nodes.subscript()

    docref = nodes.reference('', '', internal=True)
    docref_inner = nodes.literal(docname, docname,
                                 classes=['xref', 'py', 'py-mod'])
    try:
        docref['refuri'] = app.builder.get_target_uri(docname)
    except NoUri:
        # Don't crash in LaTeX output
        pass
    docref += docref_inner

    parts = ['[' + sphinx.locale._('source') + ': ', ']']
    src += [
        nodes.inline(parts[0], parts[0]),
        docref,
        nodes.inline(parts[1], parts[1]),
    ]

    src_cont = nodes.paragraph(classes=['section-source'])
    src_cont += src

    cont = nodes.section(classes=['wikipage-section'])
    cont += sec_node.children               # section contents
    cont.append(src_cont)                   # source citation
    cont['ids'] = sec_info['node']['ids']   # permalink

    return cont


def wikipage_container(env, sec_tree, page_node):
    """Builds a sphinx section corresponding to a ``wikipage`` provided the
    ``wikisection`` tree for it is given.

    :param env: The build environment (i.e an instance of
        :class:`sphinx.environment.BuildEnvironment`).
    :param sec_tree: A list of sphinx sections at the top level of the tree.
    :param page_node: The :class:`wikipage` node as observed in some document.

    :returns: A sphinx section containing the wiki page.
    :rtype: :class:`sphinx.util.compat.nodes.section`
    """
    # NOTE If we wrap our wikisection section in a separate container,
    # env.build_toc_from() breaks: it only parses the section tree as long
    # as they are nested directly under each other (e.g. section -> wrapper ->
    # section does not work).
    cont = nodes.section(classes=['wikipage'])
    title = page_node['options']['title']
    cont += nodes.title(title, title)
    # wiki pages may have contents of their own:
    cont += page_node.children
    cont += sec_tree
    cont['ids'] = [_name_to_anchor(page_node['options']['name'])]
    return cont


def wikipage_tree(app, env, docname, page_node=None):
    """Builds a section tree for a given ``wikipage`` node by collecting all
    wikisections from the environment and placing them in the right place.

    :param app: The "application", instance of
        :class:`sphinx.application.Sphinx`.
    :param env: The build environment (i.e an instance of
        :class:`sphinx.environment.BuildEnvironment`).
    :param docname: The document name where this :class:`wikipage` was found.
    :param page_node: The :class:`wikipage` node as observed in some document.

    :returns: A list of top level sections.
    :rtype: :class:`list[sphinx.util.compat.nodes.section]`

    .. wikisection:: faq
        :title: Arbitrary Order of Processing
        :parent: _none_

        As long as the order in which sections are encountered is consistent
        with a DFS of the module hierarchy, i.e up to reorderings of siblings
        but not violating depth order, there are no problems. The DFS order is
        what sphinx follows and the only possible chance of variation is in
        sibling order caused by ``autodoc_member_order`` (and our output
        respects this sibling order by default). But if for some reason, this
        assumption is violated, i.e a section appearing deeper in the module
        hierarchy is encountered before another section appearing shallower in
        the module hierarchy, our logic for placing sections in the right place
        breaks.

    .. wikisection:: faq
        :title: Cycles in parent relationships
        :parent: _none_

        If there are any cycles in the parent relationships the entire set of
        sections within that cycle are swallowed by docutils. Since there is no
        error raised or warning issued, this extension cannot inform the user
        either. Checking for cycles requires a quadratic effort to scan
        the entire parent-child graph which currently seems unnecessary.
    """
    assert isinstance(page_node, wikipage)
    page_name = page_node['options']['name']
    try:
        sections = env.wikisections[page_name]
    except KeyError:
        app.warn('Ignoring wikipage "%s" with no page sections.' % page_name)
        return []

    # Make sure there are no duplicate wikisection titles:
    titles = []
    for sec_info in env.wikisections[page_name]:
        title = sec_info['node']['options']['title']
        if title in titles:
            app.warn(docname,
                     'Ignoring wikipage containing sections with ' +
                     'duplicate titles "%s"' % title)
            return []
        titles.append(title)

    # section name (str) => idx in sections list (int)
    secidx_by_name = {
        info['node']['options']['title']: idx
        for idx, info in enumerate(sections)
    }
    # wikisection index (int) => wikisection index of parent (int)
    forced_parent = {}
    containers = [wikisection_container(app, env, info) for info in sections]
    sec_tree = []

    # Firt, we place only those wikisections in the tree that have _default_
    # parent. Then, we place wikisections that force their parents (to _none_
    # or another wikisection).
    #
    # wikisection depth (int) => wikisection container object
    last_of_depth = {}

    # Place the all sections as docutils nodes in sec_tree.
    for idx, sec_info in enumerate(sections):
        sec_node = sec_info['node']
        parent = sec_node['options']['parent']
        if parent != '_default_':
            if parent == '_none_':
                forced_parent[idx] = None
                continue
            if parent in secidx_by_name:
                forced_parent[idx] = secidx_by_name[parent]
                continue
            # Unresolved reference; treat it as if it didn't have :parent:
            app.warn('wikisection "%s" references unknown parent "%s"' %
                     (sec_node['options']['title'], parent))

        depth = sec_info['depth']
        last_of_depth[depth] = idx
        if depth == 1:
            sec_tree.append(containers[idx])
        else:
            parent_depth = depth - 1
            while parent_depth not in last_of_depth and parent_depth > 0:
                parent_depth -= 1

            if parent_depth == 0:
                # Add to top level:
                sec_tree.append(containers[idx])
            else:
                parent = last_of_depth[parent_depth]
                containers[parent].append(containers[idx])

    for child, parent in forced_parent.items():
        if parent is None:
            sec_tree.append(containers[child])

    for child, parent in forced_parent.items():
        if parent is not None:
            containers[parent].append(containers[child])

    cont = wikipage_container(env, sec_tree, page_node)
    return cont


def env_purge_doc(app, env, docname):
    """Standard handler for sphinx's ``env-purge-doc`` event. We need to
    implement this because we store data in the build environment, cf.
    ``sphinx.ext.todo``.
    """
    if not hasattr(env, 'wikisections'):
        return
    for name in env.wikisections:
        env.wikisections[name] = [sec for sec in env.wikisections[name]
                                  if sec['docname'] != docname]


def env_merge_info(app, env, docnames, other):
    """Standard handler for sphinx's ``env-murge-info`` event. We need to
    implement this because we store data in the build environment, cf.
    ``sphinx.ext.todo``."""
    if not hasattr(other, 'wikisections'):
        return
    if not hasattr(env, 'wikisections'):
        env.wikisections = []
    env.sections += other.sections


def _visit_wikisection(self, node): pass


def _depart_wikisection(self, node): pass


def setup(app):
    """
    Entry point to sphinx. We define:

    1. The configuration parameter ``wiki_enabled``, defaulting to ``False``
       which turns our behavior on and off.
    2. Two node types: :class:`wikisection`, and :class:`wikipage`.
    3. Two directives: ``wikisection``, and ``wikipage`` with handlers
       :class:`WikiSection` and :class:`WikiPage`.
    4. Four hooks, two of which -- :func:`doctree_read` and
       :func:`doctree_resolved` -- are involved in moving sections from their
       original place to where the corresponding page is included. The other
       two -- :func:`env_purge_doc` and :func:`env_merge_info` -- are
       implemented to make our usage of the build environment
       parallel-friendly.

    """
    app.add_config_value('wiki_enabled', False, 'html')

    app.add_node(wikipage)
    app.add_node(wikisection,
                 html=(_visit_wikisection, _depart_wikisection),
                 latex=(_visit_wikisection, _depart_wikisection),
                 text=(_visit_wikisection, _depart_wikisection),
                 man=(_visit_wikisection, _depart_wikisection),
                 texinfo=(_visit_wikisection, _depart_wikisection))

    app.add_directive('wikisection', WikiSection)
    app.add_directive('wikipage', WikiPage)

    app.connect('doctree-read', doctree_read)
    app.connect('doctree-resolved', doctree_resolved)

    app.connect('env-purge-doc', env_purge_doc)
    app.connect('env-merge-info', env_merge_info)

    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
