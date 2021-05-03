'''
Generic types for this module.

Semi-stable API for child modules.

These are generally things that the caller needs to implement, or have access to an implementation.
'''

from typing import TypeVar

# displayable-like types

Displayable = TypeVar('Displayable')

DisplayableTemplate = TypeVar('DisplayableTemplate')

DisplayableSchema = TypeVar('DisplayableSchema')

DisplayableSchemaKey = TypeVar('DisplayableSchemaKey')

DisplayableDetails = TypeVar('DisplayableDetails')

# node-like types

NodeKey = TypeVar('NodeKey')

NodeMemento = TypeVar('NodeMemento')
