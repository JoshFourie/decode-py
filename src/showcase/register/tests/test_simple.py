'''
Tests the Simple implementations of the register ABCs.
'''

# built-in imports
from typing_extensions import TypeAlias

# library imports
from ..simple import SimpleDisplayableTemplateFactory, SimpleDisplayablesDatabase


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

    # test instance    
    test_instance = SimpleDisplayablesDatabase[displayableSchema]()

    test_instance.update({ node_key : displayable_schema })

    test: displayableSchema = test_instance.lookup_node(node_key)

    assert test == displayable_schema, 'expected %s to equal %s' % (test, displayable_schema)

    return None


'''
Unit tests for SimpleDisplayTemplateFactory.
'''

def test_simple_display_template_factory() -> None:
    '''
    Tests that SimpleDisplayTemplateFactory can get a template.
    '''
    # test setup
    node_key: nodeKey = 'node_key'

    ## for a simple template factory, the schema is the template

    displayable_schema: displayableSchema = 'displayable_template'

    displayable_template: displayableTemplate = 'displayable_template'

    # test database semantics

    database = SimpleDisplayableTemplateFactory[displayableSchema]()
    
    database.update({ node_key : displayable_schema })
    
    assert database.lookup_node(node_key) == displayable_schema

    assert database.make_template(node_key) == displayable_template

