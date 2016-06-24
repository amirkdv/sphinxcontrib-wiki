.. sphinxcontrib-wiki documentation master file.

===============
Wiki for Sphinx
===============

.. toctree::
  :hidden:

  wiki
  API Reference <modules>

``sphinxcontrib-wiki`` is a Sphinx_ extension which allows wiki pages to be
automatically generated from docstrings. Here is an example:

.. _Sphinx: www.sphinx-doc.org/

.. code-block:: rst

    .. wikisection:: example
        :title: Example wiki section title

        Wiki sections must have a body or they are ignored.


Wiki pages are generated like this:

.. code-block:: rst

    .. wikipage:: example
        :title: Example wiki section

        Body of a wiki page appears above all its sections.

By default, the structure of the wikisection tree within a wikipage is
determined by module hierarchy, namely:

- Sections within a module are treated as siblings in the order they
  appear regardless of the depth of the class or function they belong to.
- Sections within sibling modules are treated as siblings in the order
  they are processed as per ``autodoc_member_order``.
- Sections within a package are treated as the parent of those in modules
  immediately within it.

Alternatively, a section can force its parent to a be specific other section,
for instance:

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
