'''
Simple register-like classes for in-memory storage.
'''

# built-in imports
from typing import Any, Dict, Generic, Hashable, Union
from collections import UserDict

from typing_extensions import TypeAlias

# library imports
from .types import DisplayableSchema, DisplayableTemplate
from .abc import DisplayableBuilder, DisplayableTemplateFactory, DisplayableTemplateVisitor, DisplayablesDatabase, GetMemento, NodeDetailsFactory, RegisterMediator


HashableNodeKey: TypeAlias = Hashable

SimpleMemento: TypeAlias = NotImplementedError

SimpleNodeDetails: TypeAlias = NotImplementedError

SimpleDisplayable: TypeAlias = NotImplementedError

SimpleDisplayableTemplate: TypeAlias = NotImplementedError

SimpleDisplayableSchema: TypeAlias = SimpleDisplayableTemplate

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


class SimpleNodeDetailsFactory\
(
    NodeDetailsFactory[SimpleMemento, SimpleNodeDetails]
):
    '''
    Class that can make a `SimpleNodeDetails` instance from a `SimpleMemento`.
    '''

    def make_details(self, node_memento: SimpleMemento, *args: Any, **kwargs: Any) -> SimpleNodeDetails:
        '''
        Makes a `SimpleNodeDetails` instance from the given `node_memento`.
        '''
        raise NotImplementedError('no way to build a `SimpleNodeDetails` instance from a `SimpleMemento`')


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
    __node_details_factory: SimpleNodeDetailsFactory
    __displayable_template_visitor: SimpleDisplayableTemplateVisitor

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
    def node_details_factory(self) -> SimpleNodeDetailsFactory:
        '''
        Getter for a `SimpleNodeDetailsFactory`.
        '''
        try: return self.__node_details_factory

        except AttributeError as error: raise AttributeError('no node details factory attached to this instance', error)

        except Exception as error: raise error 

    @node_details_factory.setter
    def node_details_factory(self, value: SimpleNodeDetailsFactory) -> None:
        '''
        Sets an attribute for a `SimpleNodeDetailsFactory`.
        '''
        self.__node_details_factory = value

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
        Setter for a `SimpleDisplayVisitor`.
        '''
        self.__displayable_template_visitor = value

        return None

    '''
    ABC extensions.
    '''

    def build_displayable(self, node_key: HashableNodeKey, node_memento: SimpleMemento, *args: Any, **kwargs: Any) -> SimpleDisplayable:
        '''
        Builds a `Displayable` from a `HashableNodeKey` and `SimpleMemento`
        '''
        displayable_template: SimpleDisplayableTemplate = self.displayable_template_factory.make_template(node_key = node_key)

        node_details: SimpleNodeDetails = self.node_details_factory.make_details(node_memento = node_memento)

        visited_displayable_template: SimpleDisplayableTemplate = self.displayable_template_visitor.visit_displayable_template(displayable_template = displayable_template, node_details = node_details)

        raise NotImplementedError('blocked until we can adapt a `SimpleDisplayableTemplate` into a `SimpleDisplayable` instance')


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

        displayable_builder: SimpleDisplayableBuilder = self.displayable_builder.build_displayable(node_key = node_key, node_memento = node_memento)

        raise NotImplementedError('still require a concrete `SimpleDisplayBuilder` class to map a `SimpleNodeMemento` to a `Displayable`')

        return displayable_builder
