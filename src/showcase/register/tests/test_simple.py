'''
Tests the Simple implementations of the register ABCs.
'''

# built-in imports
from typing_extensions import TypeAlias

# library imports
from ..simple import *


'''
Mockups for testing
'''

MockSimpleKey: TypeAlias = str

MockDisplayable: TypeAlias = str


'''
Unit tests for database-related activities.
'''

def test_simple_generic_database_integration() -> None:
    '''
    Tests that a SimpleGenericDatabase can write and load a mock `NodeKey` and `NodeMemento`.
    '''
    # set up
    database: SimpleGenericDatabase[MockDisplayable] = SimpleGenericDatabase()

    mock_key: MockSimpleKey = 'MockSimpleKey'; mock_memento: MockDisplayable = 'MockDisplayable'

    # write to database
    database.write(mock_key, mock_memento)

    assert database.data == {mock_key : mock_memento}, 'expected <%s>.write(..) to update a `UserDict`.' % SimpleGenericDatabase.__name__

    # try load with a good key

    value: str = database.load(mock_key)

    assert value == mock_memento, 'expected <%s>.load(..) to return a value on a valid key selection.' % SimpleGenericDatabase.__name__

    # try load with a bad key

    try: 
        database.load('BadNodeKey')
        
        raise AssertionError('expected <%s>.load(..) to throw a KeyError type on a bad key selection.' % SimpleGenericDatabase.__name__)

    except KeyError: pass # test passed

    # all tests passed

    return None   


def test_simple_generic_database_proxy_connector() -> None:
    '''
    Tests that a `SimpleGenericDatabaseProxyConnector` can set and get a `SimpleDatabaseConnection`.
    '''

    # set up

    database: SimpleGenericDatabase[MockDisplayable] = SimpleGenericDatabase()

    proxy: SimpleDatabaseProxyConnector[MockDisplayable] = SimpleDatabaseProxyConnector()

    # try get a bad property

    try: 
        proxy.database

        raise AssertionError('expected <%s>.database getter to throw an error on an empty database connection.' % SimpleDatabaseProxyConnector.__name__)

    except AttributeError: pass # test passed

    # try set a valid property

    try: proxy.database = database

    except Exception as error: raise AssertionError('<%s>.database setter threw an unexpected error.', error)

    # try get a valid property

    assert proxy.database == database, 'expected <%s>.database to return the connected database.' % SimpleDatabaseProxyConnector.__name__

    # pylance should protect against bad settings with a squiggly line of doom: the pythonic way is to ask for forgiveness...

    proxy.database = 'BadConnection'

    proxy._SimpleDatabaseProxyConnector__database = 'SomeoneToldMeToOverridePrivateProperties'

    bad_database: SimpleDatabaseConnection[MockDisplayable] = proxy.database

    assert not isinstance(bad_database, SimpleDatabaseConnection), 'expected <%s>.database to have returned a bad database connection on a bad connection setting.' % SimpleDatabaseProxyConnector.__name__
    
    # all tests passed

    return None


def test_simple_proxy_writer() -> None:
    '''
    Tests that a `SimpleNodeMementoCaretakerProxyWriter` can write to a database connection.
    ''' 
    # set up

    database: SimpleGenericDatabase[MockDisplayable] = SimpleGenericDatabase()

    proxy: SimpleGenericDatabaseProxyWriter[MockDisplayable] = SimpleGenericDatabaseProxyWriter()

    proxy.database = database

    node_key: MockSimpleKey = 'NodeKey'; node_memento: MockDisplayable = 'NodeMemento'

    # try write

    proxy.write_memento(node_key = node_key, node_memento = node_memento)

    assert database == { node_key : node_memento }, 'expected <%s>.write_memento(..) to write values to the connected database.' % SimpleGenericDatabaseProxyWriter.__name__

    # all tests passed

    return None


def test_simple_proxy_loader() -> None:
    '''
    Tests that a `SimpleNodeMementoCaretakerProxyloader` can load a `NodeMemento` from a database connection.
    ''' 
    # set up

    database: SimpleGenericDatabase[MockDisplayable] = SimpleGenericDatabase()

    node_key: MockSimpleKey = 'NodeKey'; node_memento: MockDisplayable = 'NodeMemento'

    database.write(key = node_key, value = node_memento)

    proxy: SimpleGenericDatabaseProxyLoader[MockDisplayable] = SimpleGenericDatabaseProxyLoader()

    proxy.database = database

    # try load

    test: MockDisplayable = proxy.load_memento(node_key = node_key)

    assert test == node_memento, 'expected <%s>.load_memento(..) to load %s from the connected database, but got %s instead.' % (SimpleGenericDatabaseProxyWriter.__name__, node_memento, test)

    # all tests passed

    return None


'''
Unit tests for building displayables.
'''

def test_simple_displayable_mediator() -> None:
    '''
    Tests that a `SimpleDisplayableMediator` can get a `Displayable`.
    '''

    # set up

    database: SimpleGenericDatabase[MockDisplayable] = SimpleGenericDatabase()

    simple_key: MockSimpleKey = 'SimpleKey'; displayable: MockDisplayable = 'Displayable'

    database.update({ simple_key : displayable })

    # get a mediator

    mediator: SimpleDisplayableMediator[MockDisplayable] = SimpleDisplayableMediator()

    mediator.database = database

    # try load a displayable.

    test: MockDisplayable = mediator.get_displayable(key = simple_key)

    assert test == displayable, 'expected that <%s>.get_displayable(..) would get %s, but got %s.' % (SimpleDisplayableMediator.__name__, displayable, test)

    # try load a bad key

    try: 
        test: MockDisplayable = mediator.get_displayable(key = 'BadKey')

        raise AssertionError('expected that <%s>.get_displayable(..) would throw a key error on a bad key.' % SimpleDisplayableMediator.__name__)

    except KeyError: pass # check passed

    # all tests passed

    return None
