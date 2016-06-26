# -*- coding: utf-8 -*-
"""
.. wikisection:: todo
    :title: Fix output format

    Currently :func:`.wrap_mod_func` is responsible for it, but could be
    delegated to :func:`.some_mod.mod_func`.
"""

from .some_mod import mod_func

def wrap_mod_func():
    """

    .. wikisection:: faq
        :title: From func?

        Yes.
    """
    mod_func()
    pass
