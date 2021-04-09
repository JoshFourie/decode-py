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

CONTEXT = SimpleDisplayableContext.Debug

MockDisplayOutput = str

class DisplaySomething\
(
    SimpleDisplayable[MockDisplayOutput]
):
    '''
    Class that returns a test value on calling `.display(..)`
    '''

    __value: str

    def __init__(self, value: str) -> None: 
        '''
        Stores this value to return in a display call.
        '''
        self.__value = value 

        return None

    @property
    def value(self) -> str: return self.__value

    def display(self, context: SimpleDisplayableContext, *args: Any, **kwargs: Any) -> MockDisplayOutput:
        '''
        Returns `Ok` on calling. Expects Debug context.
        ''' 
        assert context == SimpleDisplayableContext.Debug, 'expected Debug context, got %s' % context

        return self.__value


MockDisplayableTemplate: TypeAlias = DisplaySomething

MockDisplayableSchema: TypeAlias = MockDisplayableTemplate

MockNodeKey: TypeAlias = str

MockNodeDetails: TypeAlias = str

MockNodeMemento: TypeAlias = str


'''
Unit tests for SimpleDisplayableDatabase
'''

def test_simple_display_database_userdict_semantics() -> None:
    '''
    Tests that a SimpleDisplayableDatabase is dict-like.
    '''
    # test setup
    node_key: MockNodeKey = 'node_key'

    exp: str = 'Ok'

    displayable_schema: MockDisplayableSchema = MockDisplayableSchema(value = exp)

    # test instance    
    test_instance = SimpleDisplayablesDatabase[MockDisplayableSchema]()

    test_instance.update({ node_key : displayable_schema })

    test: MockDisplayableSchema = test_instance.lookup_node(node_key)

    assert test.display(CONTEXT) == exp, 'expected %s to equal %s' % (test, displayable_schema)

    return None


'''
Unit tests for `SimpleDisplayTemplateFactory`.
'''

def test_simple_display_template_factory() -> None:
    '''
    Tests that `SimpleDisplayTemplateFactory` can get a template.
    '''
    # test setup
    node_key: MockNodeKey = 'node_key'

    ## for a simple template factory, the schema is the template

    displayable_schema: MockDisplayableSchema = MockDisplayableSchema(value = 'displayable_template')

    displayable_template: MockDisplayableTemplate = MockDisplayableTemplate(value = 'displayable_template')

    # test database semantics

    database = SimpleDisplayableTemplateFactory[MockDisplayableSchema]()
    
    database.update({ node_key : displayable_schema })
    
    assert database.lookup_node(node_key) == displayable_schema

    assert database.make_template(node_key).value == displayable_template.value # otherwise python compares instance classes


def test_simple_display_template_factory_from_simple_display_database() -> None:
    '''
    Tests that a `SimpleDisplayTemplateFactory` can be instantiated from a `SimpleDisplayableDatabase`
    '''
    # test setup
    node_key: MockNodeKey = 'node_key'

    displayable_template: MockDisplayableTemplate = MockDisplayableTemplate(value = 'displayable_template')

    alt_displayable_template: MockDisplayableTemplate = MockDisplayableTemplate(value = 'alt_displayable_template')

    ## get a source database

    source_database = SimpleDisplayablesDatabase[MockDisplayableTemplate]()

    source_database.update({ node_key : displayable_template })

    # test instance 

    test_instance = SimpleDisplayableTemplateFactory[MockDisplayableTemplate]()
    
    test_instance.from_database(database = source_database)

    ## does a test instance copy the data?

    test = test_instance.lookup_node(node_key = node_key)


    assert test == displayable_template, 'expected to copy data from source database'

    ## does a test instance copy a reference to the source data?

    source_database.update({ node_key : alt_displayable_template })

    test = test_instance.lookup_node(node_key = node_key)

    assert test == alt_displayable_template, 'expected to copy a reference to data from a mutable source database'

    return None