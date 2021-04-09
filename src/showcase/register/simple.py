'''
Simple register-like classes for in-memory storage.
'''

# built-in imports
from typing import Any, Generic, Hashable, Union
from collections import UserDict

from typing_extensions import TypeAlias

# library imports
from .types import DisplayableSchema, DisplayableTemplate
from .abc import DisplayableTemplateFactory, DisplayablesDatabase


HashableNodeKey: TypeAlias = Hashable

class SimpleDisplayablesDatabase\
(
    Generic[DisplayableSchema], 
    DisplayablesDatabase[HashableNodeKey, DisplayableSchema],
    UserDict # type checks sometimes think this needs type arguments but that is a syntax error
):
    '''
    Class that can look up a display schema with a node key stored in a dict-like structure.
    '''

    def lookup_node(self, node_key: HashableNodeKey, *args: Any, **kwargs: Any) -> DisplayableSchema:
        '''
        Looks up the node key in a dict-like structure.

        Throws a `KeyError` if the key node key is not in the dict.
        '''
        lookup: Union[DisplayableSchema, None] = self.get(key = node_key, default = None)

        if lookup is None: raise KeyError('looking up %s returned a None' % (node_key, lookup))

        return lookup


class SimpleDisplayableTemplateFactory\
(
    Generic[DisplayableTemplate],
    DisplayableTemplateFactory[HashableNodeKey, DisplayableTemplate],
    SimpleDisplayablesDatabase[DisplayableTemplate]
):
    '''
    Class that can make a `DisplayableTemplate` using 
    a stored `Dict` of `NodeKeys` that map to a `DisplayableSchema`.
    '''
    
    def make_template(self, node_key: HashableNodeKey, *args: Any, **kwargs: Any) -> DisplayableTemplate:
        '''
        Makes a `DisplayableTemplate` by adapting a `DisplayableSchema` associated with 
        the given `NodeKey`.
        '''
        return self.lookup_node(node_key)
