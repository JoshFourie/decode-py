'''
ABC classes for the register module.

See https://github.com/ZaliaFlow/decode-py/issues/1.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from .types import DisplayableSchema, Displayable, NodeDetails, NodeKey, NodeMemento


class GetMemento(Generic[NodeKey, NodeMemento], ABC):
    '''
    ABC for classes that can make a node memento from a node key.
    '''

    @abstractmethod
    def get_node_memento(self, node_key: NodeKey, *args: Any, **kwargs: Any) -> NodeMemento:
        '''
        Gets a node memento for this node key.
        '''
        raise NotImplementedError


class RegisterMediator(Generic[NodeKey, Displayable], ABC):
    '''
    ABC for classes that can mediate between `GetMemento` and `DisplayBuilder` to 
    get a `Displayable` from a `NodeKey`.
    '''

    @abstractmethod
    def get_displayable(self, node_key: NodeKey, *args: Any, **kwarg: Any) -> Displayable:
        '''
        Gets a displayable for this node key.
        '''
        raise NotImplementedError


class DisplayablesDatabase(Generic[NodeKey, DisplayableSchema], ABC):
    '''
    ABC for classes that can look up a `DisplayableSchema` from a `NodeKey`.
    '''

    @abstractmethod
    def lookup_node(self, node_key: NodeKey, *args: Any, **kwargs: Any) -> DisplayableSchema:
        '''
        Looks up a node key to find a displayable schema.
        '''
        raise NotImplementedError


class NodeDetailsFactory(Generic[NodeMemento, NodeDetails], ABC):
    '''
    ABC for classes that can make node details from a node memento.
    '''

    @abstractmethod
    def make_details(self, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> NodeDetails:
        '''
        Makes a node details instance from the node memento.
        '''
        raise NotImplementedError


class DisplayableBuilder(Generic[NodeKey, NodeMemento, Displayable]):
    '''
    ABC for classes that can make a displayable from a node key and a node memento.
    '''

    @abstractmethod
    def build_displayable(self, node_key: NodeKey, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> Displayable:
        '''
        Builds a displayable from this node key and node memento.
        '''
        raise NotImplementedError
        