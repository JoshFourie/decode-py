'''
ABC classes for the broadcast module.

See https://github.com/ZaliaFlow/decode-py/issues/2.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from .types import GraphNodeMemento


class SimpleGraphStrategy(Generic[GraphNodeMemento], ABC):
    '''
    ABC for objects that can extend to new nodes and move backwards on a graph-like structure.
    '''

    @abstractmethod
    def extend_(self, data: GraphNodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Extend the graph-like structure from the current frontier to a new node associated with this data.
        '''
        raise NotImplementedError('%s requires an .extend(..) abstract method.' % SimpleGraphStrategy.__name__)

    @abstractmethod
    def retreat_(self, *args: Any, **kwargs: Any) -> None:
        '''
        Retreat fron the current frontier to the previous node.
        '''
        raise NotImplementedError('%s requires a .retreat(..) abstract method.' % SimpleGraphStrategy.__name__)
