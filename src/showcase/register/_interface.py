'''
ABC classes for the register module.

See https://github.com/ZaliaFlow/decode-py/issues/1.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from ._types import DisplayableSchema, Displayable, DisplayableSchemaKey, DisplayableTemplate, DisplayableDetails, NodeMemento


class DisplayableTemplateFactory\
(
    Generic[DisplayableSchema, DisplayableTemplate], 
    ABC
):
    '''
    ABC for classes that can make a `DisplayableTemplate` from a `DisplayableSchema`.
    '''

    @abstractmethod
    def make_displayable_template(self, schema: DisplayableSchema, *args: Any, **kwargs: Any) -> DisplayableTemplate:
        '''
        Makes a `DisplayableTemplate` from a `DisplayableSchema`.
        '''
        raise NotImplementedError('%s requires .make_displayable_template(..) abstract method.' % DisplayableTemplateFactory.__name__)


class DisplayableDetailsFactory\
(
    Generic[NodeMemento, DisplayableDetails], 
    ABC
):
    '''
    ABC for classes that can make a `DisplayableDetails` type from a `NodeMemento`.
    '''

    @abstractmethod
    def make_displayable_details(self, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> DisplayableDetails:
        '''
        Makes a node details instance from a `NodeMemento` %s.
        '''
        raise NotImplementedError('%s requires .adapt_to_details(..) abstract method.' % DisplayableDetailsFactory.__name__)


class DisplayableTemplateVisitor\
(
    Generic[DisplayableDetails, DisplayableTemplate], 
    ABC
):
    '''
    ABC for classes that can visit a `DisplayableTemplate` instance and populate it with `DisplayableDetails`.
    '''

    @abstractmethod
    def visit_displayable_template(self, displayable_template: DisplayableTemplate, displayable_details: DisplayableDetails, *args: Any, **kwargs: Any) -> DisplayableTemplate:
        '''
        Visits a `DisplayableTemplate` instance and populates it using the given `DisplayableDetails`.
        '''
        raise NotImplementedError('%s requires .visit_displayable_template(..) abstract method.' % DisplayableTemplateVisitor.__name__)


class DisplayableTemplateAdapter\
(
    Generic[DisplayableTemplate, Displayable], 
    ABC
):
    '''
    Adapts a `DisplayableTemplate` into a `Displayable`.
    '''

    @abstractmethod
    def adapt_to_displayable(self, displayable_template: DisplayableTemplate) -> Displayable:
        '''
        Copies data from a `DisplayableTemplate` into a `Displayable` instance.
        '''
        raise NotImplementedError('%s requires .adapt_to_displayable(..) abstract method.' % DisplayableTemplateAdapter.__name__)


class DisplayableBuilder\
(
    Generic[DisplayableSchemaKey, NodeMemento, Displayable]
):
    '''
    ABC for classes that can make a `Displayable` from a `NodeKey` and a `NodeMemento`.
    '''

    @abstractmethod
    def build_displayable(self, schema_key: DisplayableSchemaKey, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> Displayable:
        '''
        Builds a displayable from this node key and node memento.
        '''
        raise NotImplementedError('%s requires .build_displayable(..) abstract method.' % DisplayableBuilder.__name__)
        