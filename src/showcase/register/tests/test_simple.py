'''
Tests the Simple implementations of the register ABCs.
'''

# built-in imports
from typing import Any
from typing_extensions import TypeAlias
from collections import UserDict

# library imports
from ..simple import SimpleDisplayableMediator, StatefulVertexGraphLoaderInterface


'''
Mockups for testing
'''

MockSimpleKey: TypeAlias = str

MockDisplayable: TypeAlias = str


class MockDisplayableDatabase\
(
    StatefulVertexGraphLoaderInterface[MockSimpleKey, MockDisplayable],
    UserDict # type: ignore expected type arguments
):
    '''
    Mock-up for a displayable database.
    '''

    def load_stateful_vertex(self, label: MockSimpleKey, *args: Any, **kwargs: Any) -> MockDisplayable:
        '''
        Loads a stateful vertex from the dictionary.
        '''
        return self[label] # type: ignore partially unknown


'''
Unit tests for building displayables.
'''

def test_simple_displayable_mediator() -> None:
    '''
    Tests that a `SimpleDisplayableMediator` can get a `Displayable`.
    '''

    # set up

    database: MockDisplayableDatabase = MockDisplayableDatabase()

    simple_key: MockSimpleKey = 'SimpleKey'; displayable: MockDisplayable = 'Displayable'

    database.update({ simple_key : displayable })  # type: ignore type of .update(..) is partially unknown

    # get a mediator

    mediator: SimpleDisplayableMediator[MockDisplayable] = SimpleDisplayableMediator(database = database)

    # try load a displayable.

    test: MockDisplayable = mediator.get_displayable(key = simple_key)

    assert test == displayable, 'expected that <%s>.get_displayable(..) would get %s, but got %s.' % (SimpleDisplayableMediator.__name__, displayable, test)

    # try load a bad key

    try: 
        test: MockDisplayable = mediator.get_displayable(key = 'BadKey')

        raise AssertionError('expected that <%s>.get_displayable(..) would throw a key error on a bad key.' % SimpleDisplayableMediator.__name__) # pragma: no cover 

    except KeyError: pass # check passed

    # all tests passed

    return None
