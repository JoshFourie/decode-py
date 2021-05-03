'''
ABC classes for the broadcast module.

See https://github.com/ZaliaFlow/decode-py/issues/2.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from .types import NodeKey, NodeMemento


class NodeMementoProxyWriter(Generic[NodeKey, NodeMemento], ABC):
    '''
    ABC for objects that can act as a proxy for writing to a database-like type.
    '''

    @abstractmethod
    def write_memento(self, key: NodeKey, memento: NodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Writes this `memento` into a database-like type against this `key`.
        '''
        raise NotImplementedError('%s requires a .write_memento(..) abstract method.' % NodeMementoProxyWriter.__name__)


class StatelessDirectedNodeMementoConnectionProxyWriter(Generic[NodeKey], ABC):
    '''
    ABC for objects that can act as a proxy for writing a stateless directed connection between two node keys to a database-like type.
    '''

    @abstractmethod
    def write_memento_connection(self, source: NodeKey, destination: NodeKey, *args: Any, **kwargs: Any) -> None:
        '''
        Writes a connection from this `source` key to this `destination` one in a database-like type.
        '''
        raise NotImplementedError('%s requires a .write_memento_connection(..) abstract method.' % StatelessDirectedNodeMementoConnectionProxyWriter.__name__)

