'''
Simple* Collection.
'''

# built-in imports
from typing import Any, Generic, Hashable, Type, Union, cast
from collections import UserDict

from typing_extensions import TypeAlias

# library imports
from .types import DatabaseLookupValue, Displayable
from .abc import GenericDatabase


'''
Types. 
'''

SimpleKey: TypeAlias = Hashable

'''
ABC extensions for defining the `Simple*` collection.
'''

class SimpleGenericDatabase\
(
    Generic[DatabaseLookupValue], 
    GenericDatabase[SimpleKey, DatabaseLookupValue],
    UserDict # type checks sometimes think this needs type arguments but that is a syntax error
):
    '''
    Class that extends `UserDict` to store `DatabaseLookupValue` types against a `DatabaseLookupKey`.
    '''

    def write(self, key: SimpleKey, value: DatabaseLookupValue, *args: Any, **kwargs: Any) -> None:
        '''
        Writes this `DatabaseLookupValue` against this `DatabaseLookupKey` in the `UserDict`.
        '''
        self.update({ key : value })

        return None


    def load(self, key: SimpleKey, *args: Any, **kwargs: Any) -> DatabaseLookupValue:
        '''
        Loads the `DatabaseLookupValue` associated with this `DatabaseLookupKey`.
        '''
        lookup: Union[DatabaseLookupValue, Type[KeyError]] = self.get(key = key, default = KeyError)

        if lookup is KeyError: raise KeyError('failed to find %s in this <SimpleGenericDatabase> instance.' % key)

        return cast(DatabaseLookupValue, lookup)

class SimpleDisplayableMediator\
(
    Generic[Displayable]
):
    '''
    Class that can get a `Displayable` using a `SimpleKey`.
    '''

    __database: SimpleGenericDatabase[Displayable]

    def __init__(self, database: SimpleGenericDatabase[Displayable], *args: Any, **kwargs: Any) -> None:
        '''
        Calls the super classes and sets up a `SimpleDisplayableBuilder`
        '''
        self.__database = database

        return None

    def get_displayable(self, key: SimpleKey) -> Displayable:
        '''
        Gets a `Displayable` using a `SimpleKey`.
        '''
        return self.__database.load(key = key)
