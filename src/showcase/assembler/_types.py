'''
Generic types for this module.

Semi-stable API for child modules.

These are generally things that the caller needs to implement, or have access to an implementation.
'''

from typing import TypeVar

# component-like types

DisplayableComponent = TypeVar('DisplayableComponent')

DisplayableComponentTemplate = TypeVar('DisplayableComponentTemplate')

DisplayableComponentSchema = TypeVar('DisplayableComponentSchema')

DisplayableComponentSchemaKey = TypeVar('DisplayableComponentSchemaKey')

DisplayableComponentDetails = TypeVar('DisplayableComponentDetails')

# node-like types

NodeKey = TypeVar('NodeKey')

NodeMemento = TypeVar('NodeMemento')
