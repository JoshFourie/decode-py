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

    mediator: SimpleDisplayableMediator[MockDisplayable] = SimpleDisplayableMediator(database = database)

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
