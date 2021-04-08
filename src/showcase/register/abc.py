'''
ABC classes for the register module.

See https://github.com/ZaliaFlow/decode-py/issues/1.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from .types import DatabaseConnection, DatabaseLookupKey, DatabaseLookupValue, DisplayableSchema, Displayable, DisplayableSchemaKey, DisplayableTemplate, DisplayableDetails, NodeKey, NodeMemento



class GenericDatabase(Generic[DatabaseLookupKey, DatabaseLookupValue], ABC):
    '''
    ABC for classes that can look up a `DatabaseLookupValue` from a `DatabaseLookupKey`.
    '''

    @abstractmethod
    def write(self, key: DatabaseLookupKey, value: DatabaseLookupValue, *args: Any, **kwargs: Any) -> None:
        '''
        Writes this `DatabaseLookupValue` to this instance against this `DatabaseLookupKey`.
        '''
        raise NotImplementedError('%s requires .write(..) abstract method.' % GenericDatabase.__name__)

    @abstractmethod
    def load(self, key: DatabaseLookupKey, *args: Any, **kwargs: Any) -> DatabaseLookupValue:
        '''
        Loads a `DatabaseLookupValue` from somewhere using a `DatabaseLookupKey`.
        '''
        raise NotImplementedError('%s requires .load(..) abstract method.' % GenericDatabase.__name__)


class GenericDatabaseConnector(Generic[DatabaseConnection], ABC):
    '''
    ABC for classes that can open or return a connection to `GenericDatabase` type from a `.database` property.
    '''

    @property
    @abstractmethod
    def database(self) -> DatabaseConnection:
        '''
        Property method for getting a `DatabaseConnection` associated with this instance.
        '''
        raise NotImplementedError('%s requires a `.database` property getter method.' % GenericDatabaseConnector.__name__)

    @database.setter
    @abstractmethod
    def database(self, connection: DatabaseConnection) -> None:
        '''
        Property method for setting a `DatabaseConnection` to this instance.
        '''
        raise NotImplementedError('%s requires a `.database` property setter method.' % GenericDatabaseConnector.__name__)


class NodeMementoCaretakerProxyWriter(Generic[NodeKey, NodeMemento], ABC):
    '''
    ABC for classes that can write a `NodeMemento` to a `GenericDatabase` against a `NodeKey`.
    '''

    @abstractmethod
    def write_memento(self, node_key: NodeKey, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Writes this `NodeMemento` to a connected `DisplayableDatabase` with this `NodeKey`.
        '''
        raise NotImplementedError('%s requires .write_memento(..) abstract method' % NodeMementoCaretakerProxyWriter.__name__)


class NodeMementoCaretakerProxyLoader(Generic[NodeKey, NodeMemento], ABC):
    '''
    ABC for classes that can load a `NodeMemento` from a connected `GenericDatabase` using this `NodeKey`.
    '''

    @abstractmethod
    def load_memento(self, node_key: NodeKey, *args: Any, **kwargs: Any) -> NodeMemento:
        '''
        Loads a `NodeMemento` from a connected `DisplayableDatabase` using this `NodeKey`.
        '''
        raise NotImplementedError('%s requires .load_memento(..) abstract method' % NodeMementoCaretakerProxyLoader.__name__)


class DisplayablesSchemaDatabaseProxyWriter(Generic[DisplayableSchemaKey, DisplayableSchema], ABC):
    '''
    ABC for classes that can write a `DisplayableSchema` to a `GenericDatabase` against a `DisplayableSchemaKey`.
    '''

    @abstractmethod
    def write_schema(self, schema_key: DisplayableSchemaKey, schema: DisplayableSchema, *args: Any, **kwargs: Any) -> None:
        '''
        Writes this `DisplayableSchema` to a connected `GenericDatabase` with this `DisplayableSchemaKey`.
        '''
        raise NotImplementedError('%s requires .write_schema(..) abstract method' % DisplayablesSchemaDatabaseProxyWriter.__name__)


class DisplayablesSchemaDatabaseProxyLoader(Generic[DisplayableSchemaKey, DisplayableSchema], ABC):
    '''
    ABC for classes that can load a `DisplayableSchema` from a `GenericDatabase` using a `DisplayableSchemaKey`.
    '''

    @abstractmethod
    def load_schema(self, schema_key: DisplayableSchemaKey, *args: Any, **kwargs: Any) -> DisplayableSchema:
        '''
        Loads a `DisplayableSchema` from a connected `GenericDatabase` using this `DisplayableSchemaKey`.
        '''
        raise NotImplementedError('%s requires .load_schema(..) abstract method' % DisplayablesSchemaDatabaseProxyLoader.__name__)


class DisplayableTemplateFactory(Generic[DisplayableSchema, DisplayableTemplate], ABC):
    '''
    ABC for classes that can make a `DisplayableTemplate` from a `DisplayableSchema`.
    '''

    @abstractmethod
    def make_displayable_template(self, schema: DisplayableSchema, *args: Any, **kwargs: Any) -> DisplayableTemplate:
        '''
        Makes a `DisplayableTemplate` from a `DisplayableSchema`.
        '''
        raise NotImplementedError('%s requires .make_displayable_template(..) abstract method.' % DisplayableTemplateFactory.__name__)


class DisplayableDetailsFactory(Generic[NodeMemento, DisplayableDetails], ABC):
    '''
    ABC for classes that can make a `DisplayableDetails` type from a `NodeMemento`.
    '''

    @abstractmethod
    def make_displayable_details(self, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> DisplayableDetails:
        '''
        Makes a node details instance from a `NodeMemento` %s.
        '''
        raise NotImplementedError('%s requires .adapt_to_details(..) abstract method.' % DisplayableDetailsFactory.__name__)


class DisplayableTemplateVisitor(Generic[DisplayableDetails, DisplayableTemplate], ABC):
    '''
    ABC for classes that can visit a `DisplayableTemplate` instance and populate it with `DisplayableDetails`.
    '''

    @abstractmethod
    def visit_displayable_template(self, displayable_template: DisplayableTemplate, displayable_details: DisplayableDetails, *args: Any, **kwargs: Any) -> DisplayableTemplate:
        '''
        Visits a `DisplayableTemplate` instance and populates it using the given `DisplayableDetails`.
        '''
        raise NotImplementedError('%s requires .visit_displayable_template(..) abstract method.' % DisplayableTemplateVisitor.__name__)


class DisplayableTemplateAdapter(Generic[DisplayableTemplate, Displayable], ABC):
    '''
    Adapts a `DisplayableTemplate` into a `Displayable`.
    '''

    @abstractmethod
    def adapt_to_displayable(self, displayable_template: DisplayableTemplate) -> Displayable:
        '''
        Copies data from a `DisplayableTemplate` into a `Displayable` instance.
        '''
        raise NotImplementedError('%s requires .adapt_to_displayable(..) abstract method.' % DisplayableTemplateAdapter.__name__)


class DisplayableBuilder(Generic[DisplayableSchemaKey, NodeMemento, Displayable]):
    '''
    ABC for classes that can make a `Displayable` from a `NodeKey` and a `NodeMemento`.
    '''

    @abstractmethod
    def build_displayable(self, schema_key: DisplayableSchemaKey, node_memento: NodeMemento, *args: Any, **kwargs: Any) -> Displayable:
        '''
        Builds a displayable from this node key and node memento.
        '''
        raise NotImplementedError('%s requires .build_displayable(..) abstract method.' % DisplayableBuilder.__name__)
        