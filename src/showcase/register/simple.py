'''
Simple register-like classes for in-memory storage.
'''

# built-in imports
from typing import Any, Generic
from collections import UserDict

# library imports
from .types import DisplayableSchema, NodeKey
from .abc import DisplayablesDatabase


class SimpleDisplayablesDatabase\
(
    Generic[NodeKey, DisplayableSchema], 
    DisplayablesDatabase[NodeKey, DisplayableSchema],
    UserDict
):
    '''
    Class that can look up a display schema with a node key stored in a dict-like structure.
    '''

    def lookup_node(self, node_key: NodeKey, *args: Any, **kwargs: Any) -> DisplayableSchema:
        '''
        Looks up the node key in a dict-like structure.

        Throws a `KeyError` if the key node key is not in the dict.
        '''
        return self.get(node_key)

