'''
ABC classes for the register module.

See https://github.com/ZaliaFlow/decode-py/issues/1.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from .types import DisplayableSchema, Displayable, DisplayableTemplate, NodeDetails, NodeKey, NodeMemento


class GetMemento(Generic[NodeKey, NodeMemento], ABC):
    '''
    ABC for classes that can make a `NodeMemento` from a `NodeKey`.
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


class DisplayableTemplateFactory(Generic[NodeKey, DisplayableTemplate], ABC):
    '''
    ABC for classes that can make a `DisplayableTemplate` from a `NodeKey`.
    '''

    @abstractmethod
    def make_template(self, node_key: NodeKey, *args: Any, **kwargs: Any) -> DisplayableTemplate:
        '''
        Makes a `DisplayableTemplate` from a `NodeKey`.
        '''
        raise NotImplementedError


class NodeDetailsAdapter(Generic[NodeMemento, NodeDetails], ABC):
    '''
    ABC for classes that can make `NodeDetails` from a `NodeMemento`.
    '''

    @abstractmethod
    def make_details(self, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> NodeDetails:
        '''
        Makes a node details instance from the node memento.
        '''
        raise NotImplementedError


class DisplayableTemplateVisitor(Generic[NodeDetails, DisplayableTemplate], ABC):
    '''
    ABC for classes that can visit a `DisplayableTemplate` instance and populate it with `NodeDetails`.
    '''

    @abstractmethod
    def visit_displayable_template(self, displayable_template: DisplayableTemplate, node_details: NodeDetails, *args: Any, **kwargs: Any) -> DisplayableTemplate:
        '''
        Visits a `DisplayableTemplate` instance and populates it using the given `NodeDetails`.
        '''
        raise NotImplementedError


class DisplayableAdapter(Generic[DisplayableTemplate, Displayable], ABC):
    '''
    Adapts a `DisplayableTemplate` into a `Displayable`.
    '''

    @abstractmethod
    def adapt_template(self, displayable_template: DisplayableTemplate) -> Displayable:
        '''
        Copies data from a `DisplayableTemplate` into a `Displayable` instance.
        '''
        raise NotImplementedError


class DisplayableBuilder(Generic[NodeKey, NodeMemento, Displayable]):
    '''
    ABC for classes that can make a `Displayable` from a `NodeKey` and a `NodeMemento`.
    '''

    @abstractmethod
    def build_displayable(self, node_key: NodeKey, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> Displayable:
        '''
        Builds a displayable from this node key and node memento.
        '''
        raise NotImplementedError
        