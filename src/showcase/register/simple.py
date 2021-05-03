'''
Simple* Collection.
'''

# built-in imports
from typing import Any, Generic, Hashable

from typing_extensions import TypeAlias

# library imports
from ._types import Displayable

from ..database import StatefulVertexGraphLoaderInterface


'''
Types. 
'''

SimpleKey: TypeAlias = Hashable

'''
ABC extensions for defining the `Simple*` collection.
'''

class SimpleDisplayableMediator\
(
    Generic[Displayable]
):
    '''
    Class that can get a `Displayable` using a `SimpleKey`.
    '''

    __database: StatefulVertexGraphLoaderInterface[SimpleKey, Displayable]

    def __init__(self, database: StatefulVertexGraphLoaderInterface[SimpleKey, Displayable], *args: Any, **kwargs: Any) -> None:
        '''
        Calls the super classes and sets up a `SimpleDisplayableBuilder`
        '''
        self.__database = database

        return None

    def get_displayable(self, key: SimpleKey) -> Displayable:
        '''
        Gets a `Displayable` using a `SimpleKey`.
        '''
        return self.__database.load_stateful_vertex(label = key)
