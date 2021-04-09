'''
Tests the Simple implementations of the register ABCs.
'''

# built-in imports
from src.showcase.register.types import DisplayableSchema
from typing import Callable, Dict
from typing_extensions import TypeAlias

# library imports
from ..simple import SimpleDisplayablesDatabase


# mock types for testing

displayable: TypeAlias = str

displayableTemplate: TypeAlias = str

displayableSchema: TypeAlias = str

nodeKey: TypeAlias = str

nodeDetails: TypeAlias = str

nodeMemento: TypeAlias = str


'''
Unit tests for SimpleDisplayableDatabase
'''

def test_simple_display_database_userdict_semantics() -> None:
    '''
    Tests that a SimpleDisplayableDatabase is dict-like.
    '''
    # test setup
    node_key: nodeKey = 'node_key'
    displayable_schema: displayableSchema = 'displayable_schema'

    get_key: Callable[..., nodeKey] = lambda tag: node_key + tag
    get_value: Callable[..., displayableSchema] = lambda tag: displayable_schema + tag

    get_dict: Callable[..., Dict[nodeKey, displayableSchema]] = lambda tag: { get_key(tag) : get_value(tag) }

    # test instance    
    test_instance = SimpleDisplayablesDatabase[nodeKey, displayableSchema]()

    for i in range(3): 
        tag: str = str(i)
        update: Dict[nodeKey, nodeMemento] = get_dict(tag)
        test_instance.update(update)

    # test assertions
    for i in range(3):
        tag: str = str(i)
        key: nodeKey = get_key(tag)
        exp: displayableSchema = get_value(tag)

        test: displayableSchema = test_instance.lookup_node(key)

        assert test is not None, 'expected test value to not be a None'
        assert test == exp, 'expected %s to equal %s' % (test, exp)

    return None
