'''
Simple* Collection.
'''

# built-in imports
from typing import Any, Generic, Hashable, Type, Union, cast
from collections import UserDict

from typing_extensions import TypeAlias

# library imports
from .types import DatabaseLookupValue, Displayable
from .abc import DisplayableBuilder, DisplayablesSchemaDatabaseProxyLoader, DisplayablesSchemaDatabaseProxyWriter, GenericDatabase, GenericDatabaseConnector, NodeMementoCaretakerProxyLoader, NodeMementoCaretakerProxyWriter


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


SimpleDatabaseConnection: TypeAlias = SimpleGenericDatabase

class SimpleDatabaseProxyConnector\
(
    Generic[DatabaseLookupValue],
    GenericDatabaseConnector[SimpleDatabaseConnection[DatabaseLookupValue]]
):
    '''
    Class for managing a connection to a `SimpleGenericDatabase`.
    '''

    __database: SimpleDatabaseConnection[DatabaseLookupValue]

    @property
    def database(self) -> SimpleDatabaseConnection[DatabaseLookupValue]:
        '''
        Property method for getting a `SimpleDatabaseConnection` associated with this instance.
        '''
        try: return self.__database

        except AttributeError: raise AttributeError('<%s>.database does not have a connection to a database, try setting the `.database` property.' % self.__class__.__name__) 

    @database.setter
    def database(self, connection: SimpleDatabaseConnection[DatabaseLookupValue]) -> None:
        '''
        Property method for setting a `SimpleDatabaseConnection` to this instance.
        '''
        self.__database = connection

        return None


class SimpleGenericDatabaseProxyWriter\
(
    Generic[Displayable],
    SimpleDatabaseProxyConnector[Displayable],
    NodeMementoCaretakerProxyWriter[SimpleKey, Displayable],
    DisplayablesSchemaDatabaseProxyWriter[SimpleKey, Displayable]
):
    '''
    Class that can write a `NodeMemento` to a `SimpleDatabaseConnection` against a `NodeKey`.
    '''

    def write_memento(self, node_key: SimpleKey, node_memento: Displayable, *args: Any, **kwargs: Any) -> None:
        '''
        Writes a `NodeMemento` to a `SimpleDatabaseConnection` against a `NodeKey`.
        '''
        self.database.write(key = node_key, value = node_memento)

        return None

    def write_schema(self, schema_key: SimpleKey, schema: Displayable, *args: Any, **kwargs: Any) -> None:
        '''
        Writes this `Displayable` to a `SimpleDatabaseConnection` against a `SimpleKey` using `<SimpleGenericDatabaseProxyWriter>.write_memento(..)`.
        '''
        self.write_memento(node_key = schema_key, node_memento = schema)

        return None

class SimpleGenericDatabaseProxyLoader\
(
    Generic[Displayable],
    SimpleDatabaseProxyConnector[Displayable],
    NodeMementoCaretakerProxyLoader[SimpleKey, Displayable],
    DisplayablesSchemaDatabaseProxyLoader[SimpleKey, Displayable]
):
    '''
    Class that can write a `NodeMemento` to a `SimpleDatabaseConnection` against a `NodeKey`.
    '''

    def load_memento(self, node_key: SimpleKey, *args: Any, **kwargs: Any) -> Displayable:
        '''
        Loads a `Displayable` from a `SimpleDatabaseConnection` using a `SimpleKey`.
        '''
        return self.database.load(key = node_key)


    def load_schema(self, schema_key: SimpleKey, *args: Any, **kwargs: Any) -> Displayable:
        '''
        Loads a `Displayable` from a `SimpleDatabaseConnection` using a `SimpleKey` via `<SimpleGenericDatabaseProxyWriter>.load_memento(..)`.
        '''
        return self.load_memento(node_key = schema_key)


class SimpleDisplayableBuilder\
(
    Generic[Displayable],
    DisplayableBuilder[SimpleKey, None, Displayable],
    SimpleGenericDatabaseProxyLoader[Displayable]
):
    '''
    Class that can build a `Displayable` from a `SimpleKey` using a `SimpleGenericDatabaseConnection`
    '''

    def build_displayable(self, schema_key: SimpleKey, node_memento: None = None, *args: Any, **kwargs: Any) -> Displayable:
        '''
        Gets a `Displayable` from a `SimpleGenericDatabaseConnection` using this `SimpleKey`.
        '''
        return self.load_schema(schema_key = schema_key)


class SimpleDisplayableMediator\
(
    Generic[Displayable],
    SimpleDisplayableBuilder[Displayable]
):
    '''
    Class that can get a `Displayable` using a `SimpleKey`.
    '''

    def get_displayable(self, key: SimpleKey) -> Displayable:
        '''
        Gets a `Displayable` using a `SimpleKey`.
        '''
        return self.build_displayable(schema_key = key)
