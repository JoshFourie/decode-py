'''
ABC classes for the assembler module.

See https://github.com/ZaliaFlow/decode-py/issues/1.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from ._types import DisplayableComponentSchema, DisplayableComponent, DisplayableComponentSchemaKey, DisplayableComponentTemplate, DisplayableComponentDetails, NodeMemento


class DisplayableComponentTemplateFactory\
(
    Generic[DisplayableComponentSchema, DisplayableComponentTemplate], 
    ABC
):
    '''
    ABC for classes that can make a `DisplayableComponentTemplate` from a `DisplayableComponentSchema`.
    '''

    @abstractmethod
    def make_component_template(self, schema: DisplayableComponentSchema, *args: Any, **kwargs: Any) -> DisplayableComponentTemplate:
        '''
        Makes a `DisplayableComponentTemplate` from a `DisplayableComponentSchema`.
        '''
        raise NotImplementedError('%s requires .make_component_template(..) abstract method.' % DisplayableComponentTemplateFactory.__name__)


class DisplayableComponentDetailsFactory\
(
    Generic[NodeMemento, DisplayableComponentDetails], 
    ABC
):
    '''
    ABC for classes that can make a `DisplayableComponentDetails` type from a `NodeMemento`.
    '''

    @abstractmethod
    def make_component_details(self, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> DisplayableComponentDetails:
        '''
        Makes a node details instance from a `NodeMemento` %s.
        '''
        raise NotImplementedError('%s requires .adapt_to_details(..) abstract method.' % DisplayableComponentDetailsFactory.__name__)


class DisplayableComponentTemplateVisitor\
(
    Generic[DisplayableComponentDetails, DisplayableComponentTemplate], 
    ABC
):
    '''
    ABC for classes that can visit a `DisplayableComponentTemplate` instance and populate it with `DisplayableComponentDetails`.
    '''

    @abstractmethod
    def visit_component_template(self, component_template: DisplayableComponentTemplate, component_details: DisplayableComponentDetails, *args: Any, **kwargs: Any) -> DisplayableComponentTemplate:
        '''
        Visits a `DisplayableComponentTemplate` instance and populates it using the given `DisplayableComponentDetails`.
        '''
        raise NotImplementedError('%s requires .visit_component_template(..) abstract method.' % DisplayableComponentTemplateVisitor.__name__)


class DisplayableComponentTemplateAdapter\
(
    Generic[DisplayableComponentTemplate, DisplayableComponent], 
    ABC
):
    '''
    Adapts a `DisplayableComponentTemplate` into a `DisplayableComponent`.
    '''

    @abstractmethod
    def adapt_to_component(self, component_template: DisplayableComponentTemplate) -> DisplayableComponent:
        '''
        Copies data from a `DisplayableComponentTemplate` into a `DisplayableComponent` instance.
        '''
        raise NotImplementedError('%s requires .adapt_to_component(..) abstract method.' % DisplayableComponentTemplateAdapter.__name__)


class DisplayableComponentBuilder\
(
    Generic[DisplayableComponentSchemaKey, NodeMemento, DisplayableComponent]
):
    '''
    ABC for classes that can make a `DisplayableComponent` from a `NodeKey` and a `NodeMemento`.
    '''

    @abstractmethod
    def build_component(self, schema_key: DisplayableComponentSchemaKey, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> DisplayableComponent:
        '''
        Builds a component from this node key and node memento.
        '''
        raise NotImplementedError('%s requires .build_component(..) abstract method.' % DisplayableComponentBuilder.__name__)
        