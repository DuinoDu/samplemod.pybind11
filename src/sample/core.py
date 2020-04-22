# -*- coding: utf-8 -*-
""" Short description
Long description
"""

import sample.sample_cpp2py_export as _C


__all__ = ['hello']


def hello():
    s = _C.submodule
    print(s.__doc__)
