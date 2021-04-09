'''
Simple register-like classes for in-memory storage.
'''

# built-in imports
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Hashable, Union
from collections import UserDict
from enum import Enum

from typing_extensions import TypeAlias

# library imports
from .types import DisplayableSchema, DisplayableTemplate
from .abc import DisplayableAdapter, DisplayableBuilder, DisplayableTemplateFactory, DisplayableTemplateVisitor, DisplayablesDatabase, GetMemento, NodeDetailsAdapter, RegisterMediator


HashableNodeKey: TypeAlias = Hashable

SimpleMemento: TypeAlias = NotImplementedError

SimpleNodeDetails: TypeAlias = NotImplementedError


'''
ABC things for interfacing with the `Simple*` collection.
'''

class SimpleDisplayableContext(Enum):
    '''
    Enum for defining the context of a `SimpleDisplayable`.
    '''
    Debug = 0
    Streamlit = 1

class SimpleDisplayable(ABC):
    '''
    ABC for displayables in a Streamlit showcase.
    '''
    
    @abstractmethod
    def display(self, context: SimpleDisplayableContext, *args: Any, **kwargs: Any) -> Any:
        '''
        Displays this displayable in the context.
        '''
        raise NotImplementedError


# `Simple*` collection relies on aliasing for simplification of concrete implementations.

SimpleDisplayableTemplate: TypeAlias = SimpleDisplayable

SimpleDisplayableSchema: TypeAlias = SimpleDisplayableTemplate

'''
ABC extensions for defining the `Simple*` collection.
'''

class SimpleDisplayablesDatabase\
(
    Generic[DisplayableSchema], 
    DisplayablesDatabase[HashableNodeKey, DisplayableSchema],
    UserDict # type checks sometimes think this needs type arguments but that is a syntax error
):
    '''
    Class that can look up a `SimpleDisplayableSchema` with a `HashableNodeKey` stored in a dict-like structure.
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

    def from_database(self, database: SimpleDisplayablesDatabase[DisplayableTemplate]) -> None:
        '''
        Stores a reference to the data in a `SimpleDisplayablesDatabase` to this instance.
        '''
        data: Dict[HashableNodeKey, DisplayableTemplate] = database.data

        self.data = data

        return None


class SimpleNodeDetailsAdapter\
(
    NodeDetailsAdapter[SimpleMemento, SimpleNodeDetails]
):
    '''
    Class that can make a `SimpleNodeDetails` instance from a `SimpleMemento`.
    '''

    def make_details(self, node_memento: SimpleMemento, *args: Any, **kwargs: Any) -> SimpleNodeDetails:
        '''
        Makes a `SimpleNodeDetails` instance from the given `node_memento`.
        '''
        raise NotImplementedError('no way to build a `SimpleNodeDetails` instance from a `SimpleMemento`')



class SimpleDisplayableAdapter(DisplayableAdapter[SimpleDisplayableTemplate, SimpleDisplayable]):
    '''
    Class for adapting a `SimpleDisplayableTemplate` into a `SimpleDisplayable`.
    '''

    def adapt_template(self, displayable_template: SimpleDisplayableTemplate) -> SimpleDisplayable:
        '''
        Adapts a `SimpleDisplayableTemplate` into a `SimpleDisplayable`.
        '''
        return displayable_template


class SimpleDisplayableTemplateVisitor\
(
    DisplayableTemplateVisitor[SimpleNodeDetails, SimpleDisplayableTemplate]
):
    '''
    Class that can visit a `SimpleDisplayableTemplate` and populate it with a `SimpleNodeDetails` instance.
    '''

    def visit_displayable_template(self, displayable_template: SimpleDisplayableTemplate, node_details: SimpleNodeDetails, *args: Any, **kwargs: Any) -> SimpleDisplayableTemplate:
        '''
        Visits a `SimpleDisplayableTemplate` instance using the given `SimpleNodeDetails`.
        '''
        raise NotImplementedError('blocked until `SimpleDisplayableTemplate` and `SimpleNodeDetails` are implemented')


class SimpleDisplayableBuilder\
(
    DisplayableBuilder[HashableNodeKey, SimpleMemento, SimpleDisplayable]
):
    '''
    Class that can build a `Displayable` from a `HashableNodeKey` and `SimpleMemento`
    '''

    __displayable_template_factory: SimpleDisplayableTemplateFactory[SimpleDisplayableTemplate]
    __node_details_adapter: SimpleNodeDetailsAdapter
    __displayable_template_visitor: SimpleDisplayableTemplateVisitor
    __displayable_adapter: SimpleDisplayableAdapter

    '''
    Property methods.
    '''

    @property
    def displayable_template_factory(self) -> SimpleDisplayableTemplateFactory[SimpleDisplayableTemplate]:
        '''
        Getter for a `SimpleDisplayableTemplateFactory`.
        '''
        try: return self.__displayable_template_factory

        except AttributeError as error: raise AttributeError('no displayable template factory attached to this instance', error)

        except Exception as error: raise error 

    @displayable_template_factory.setter
    def displayable_template_factory(self, value: SimpleDisplayableTemplateFactory[SimpleDisplayableTemplate]) -> None:
        '''
        Sets an attribute for a `SimpleDisplayableTemplateFactory`.
        '''
        self.__displayable_template_factory = value

        return None

    @property
    def node_details_adapter(self) -> SimpleNodeDetailsAdapter:
        '''
        Getter for a `SimpleNodeDetailsFactory`.
        '''
        try: return self.__node_details_adapter

        except AttributeError as error: raise AttributeError('no node details factory attached to this instance', error)

        except Exception as error: raise error 

    @node_details_adapter.setter
    def node_details_adapter(self, value: SimpleNodeDetailsAdapter) -> None:
        '''
        Sets an attribute for a `SimpleNodeDetailsFactory`.
        '''
        self.__node_details_adapter = value

        return None

    @property
    def displayable_template_visitor(self) -> SimpleDisplayableTemplateVisitor:
        '''
        Getter for a `SimpleDisplayableVisitor`.
        '''
        try: return self.__displayable_template_visitor

        except AttributeError as error: raise AttributeError('no simple displayable visitor attached to this instance', error)

        except Exception as error: raise error

    @displayable_template_visitor.setter
    def displayable_template_visitor(self, value: SimpleDisplayableTemplateVisitor) -> None:
        '''
        Setter for a `SimpleDisplayableTemplateVisitor`.
        '''
        self.__displayable_template_visitor = value

        return None

    @property
    def displayable_adapter(self) -> SimpleDisplayableAdapter:
        '''
        Getter for a `SimpleDisplayableAdapter`.
        '''
        try: return self.__displayable_adapter

        except AttributeError as error: raise AttributeError('no displayable adapter attached to this instance', error)

        except Exception as error: raise error

    @displayable_adapter.setter
    def displayable_adapter(self, value: SimpleDisplayableAdapter) -> None:
        '''
        Setter for a `SimpleDisplayableAdapter`.
        ''' 
        self.__displayable_adapter = value

        return None

    '''
    ABC extensions.
    '''

    def build_displayable(self, node_key: HashableNodeKey, node_memento: SimpleMemento, *args: Any, **kwargs: Any) -> SimpleDisplayable:
        '''
        Builds a `Displayable` from a `HashableNodeKey` and `SimpleMemento`
        '''
        displayable_template: SimpleDisplayableTemplate = self.displayable_template_factory.make_template(node_key = node_key)

        node_details: SimpleNodeDetails = self.node_details_adapter.make_details(node_memento = node_memento)

        visited_displayable_template: SimpleDisplayableTemplate = self.displayable_template_visitor.visit_displayable_template(displayable_template = displayable_template, node_details = node_details)

        displayable: SimpleDisplayable = self.displayable_adapter.adapt_template(visited_displayable_template)

        return displayable

class SimpleRegisterMediator\
(
    RegisterMediator[HashableNodeKey, SimpleDisplayable]
):
    '''
    Class that can mediate between a `GetMemento[HashableNodeKey, SimpleMemento]` instance
    and a `SimpleDisplayBuilder` to get a `SimpleDisplayable` from a `HashableNodeKey`.
    '''

    __mementos: GetMemento[HashableNodeKey, SimpleMemento]
    __builder: SimpleDisplayableBuilder

    '''
    Property methods.
    '''

    @property
    def mementos(self) -> GetMemento[HashableNodeKey, SimpleMemento]:
        '''
        Getter for a `GetMemento` instance that can return a `SimpleMemento` from a `HashableNodeKey`.
        '''
        try: return self.__mementos

        except AttributeError as error: raise AttributeError('no computation graph holding simple mementos attached to this instance', error)

        except Exception as error: raise error 

    @mementos.setter
    def mementos(self, value: GetMemento[HashableNodeKey, SimpleMemento]) -> None:
        '''
        Sets an attribute for a `GetMemento` instance that can return a `SimpleMemento` from a `HashableNodeKey`.
        '''
        self.__mementos = value

        return None

    @property
    def displayable_builder(self) -> SimpleDisplayableBuilder:
        '''
        Get a `DisplayableBuilder` for this mediator instance.
        '''
        try: return self.__builder

        except AttributeError as error: raise AttributeError('no display builder attached to this instance', error)

        except Exception as error: raise error

    @displayable_builder.setter
    def displayable_builder(self, value: SimpleDisplayableBuilder) -> None:
        '''
        Sets an attribute for a `GetMemento` instance that can return a `SimpleMemento` from a `HashableNodeKey`.
        '''
        self.__builder = value

        return None

    '''
    ABC extensions.
    '''

    def get_displayable(self, node_key: HashableNodeKey, *args: Any, **kwarg: Any) -> SimpleDisplayable:
        '''
        Gets a `Displayable` from a `HashableNodeKey` using a `GetMemento` class.
        '''
        node_memento: SimpleMemento = self.mementos.get_node_memento(node_key = node_key)

        displayable: SimpleDisplayable = self.displayable_builder.build_displayable(node_key = node_key, node_memento = node_memento)

        return displayable
