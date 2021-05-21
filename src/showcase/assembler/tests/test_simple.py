'''
Tests the Simple implementations of the assembler ABCs.
'''

# built-in imports
from typing import Any
from typing_extensions import TypeAlias
from collections import UserDict

# library imports
from ..simple import SimpleAssembler, StatefulVertexGraphLoaderInterface


'''
Mockups for testing
'''

MockSimpleKey: TypeAlias = str

MockDisplayableComponent: TypeAlias = str


class MockDisplayableComponentDatabase\
(
    StatefulVertexGraphLoaderInterface[MockSimpleKey, MockDisplayableComponent],
    UserDict # type: ignore expected type arguments
):
    '''
    Mock-up for a component database.
    '''

    def load_stateful_vertex(self, label: MockSimpleKey, *args: Any, **kwargs: Any) -> MockDisplayableComponent:
        '''
        Loads a stateful vertex from the dictionary.
        '''
        return self[label] # type: ignore partially unknown


'''
Unit tests for building components.
'''

def test_simple_component_mediator() -> None:
    '''
    Tests that a `SimpleDisplayableComponentMediator` can get a `DisplayableComponent`.
    '''

    # set up

    database: MockDisplayableComponentDatabase = MockDisplayableComponentDatabase()

    simple_key: MockSimpleKey = 'SimpleKey'; component: MockDisplayableComponent = 'DisplayableComponent'

    database.update({ simple_key : component })  # type: ignore type of .update(..) is partially unknown

    # get a mediator

    mediator: SimpleAssembler[MockDisplayableComponent] = SimpleAssembler(database = database)

    # try load a component.

    test: MockDisplayableComponent = mediator.get_component(key = simple_key)

    assert test == component, 'expected that <%s>.get_component(..) would get %s, but got %s.' % (SimpleAssembler.__name__, component, test)

    # try load a bad key

    try: 
        test: MockDisplayableComponent = mediator.get_component(key = 'BadKey')

        raise AssertionError('expected that <%s>.get_component(..) would throw a key error on a bad key.' % SimpleAssembler.__name__) # pragma: no cover 

    except KeyError: pass # check passed

    # all tests passed

    return None
