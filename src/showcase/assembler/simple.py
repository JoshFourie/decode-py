'''
Simple* Collection.
'''

# built-in imports
from typing import Any, Generic, Hashable

from typing_extensions import TypeAlias

# library imports
from ._types import DisplayableComponent

from ..database import StatefulVertexGraphLoaderInterface


'''
Types. 
'''

SimpleKey: TypeAlias = Hashable

'''
ABC extensions for defining the `Simple*` collection.
'''

class SimpleAssembler\
(
    Generic[DisplayableComponent]
):
    '''
    Class that can get a `DisplayableComponent` using a `SimpleKey`.
    '''

    __database: StatefulVertexGraphLoaderInterface[SimpleKey, DisplayableComponent]

    def __init__(self, database: StatefulVertexGraphLoaderInterface[SimpleKey, DisplayableComponent], *args: Any, **kwargs: Any) -> None:
        '''
        Calls the super classes and sets up a `SimpleDisplayableComponentBuilder`
        '''
        self.__database = database

        return None

    def get_component(self, key: SimpleKey) -> DisplayableComponent:
        '''
        Gets a `DisplayableComponent` using a `SimpleKey`.
        '''
        return self.__database.load_stateful_vertex(label = key)
