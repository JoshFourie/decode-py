'''
Generic types for this module.

Semi-stable API for child modules.

These are generally things that the caller needs to implement, or have access to an implementation.
'''

from typing import TypeVar


VertexLabel = TypeVar('VertexLabel')

VertexData = TypeVar('VertexData')
