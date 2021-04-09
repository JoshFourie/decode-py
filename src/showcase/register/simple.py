'''
Simple register-like classes for in-memory storage.
'''

# built-in imports
from typing import Any, Dict, Generic, Hashable, Union
from collections import UserDict

from typing_extensions import TypeAlias

# library imports
from .types import Displayable, DisplayableSchema, DisplayableTemplate, NodeMemento
from .abc import DisplayableBuilder, DisplayableTemplateFactory, DisplayablesDatabase, GetMemento, RegisterMediator


HashableNodeKey: TypeAlias = Hashable

SimpleMemento: TypeAlias = NotImplementedError

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


class SimpleDisplayableBuilder\
(
    DisplayableBuilder[HashableNodeKey, SimpleMemento, SimpleDisplayable]
):
    '''
    Class that can build a `Displayable` from a `HashableNodeKey` and `SimpleMemento`
    '''
    
    '''
    ABC extensions.
    '''

    def build_displayable(self, node_key: HashableNodeKey, node_memento: SimpleMemento, *args: Any, **kwargs: Any) -> SimpleDisplayable:
        '''
        Builds a `Displayable` from a `HashableNodeKey` and `SimpleMemento`
        '''
        # display_template: SimpleDisplayableTemplate 
        raise NotImplementedError('require property methods to get the underlying components.')




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
