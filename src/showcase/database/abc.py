'''
ABC types for the broadcast module.

See https://github.com/ZaliaFlow/decode-py/issues/5.
'''


# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from .types import VertexLabel, VertexData


class StatefulVertexWriteableGraphInterface(Generic[VertexLabel, VertexData], ABC):
    '''
    ABC for objects that can write a `(label, data)` pair as a vertex in a graph-like structure.
    '''

    @abstractmethod
    def write_stateful_vertex(self, label: VertexLabel, data: VertexData, *args: Any, **kwargs: Any) -> None:
        '''
        Writes a vertex with this `label` and associates it with this `data`. 
        '''
        raise NotImplementedError('%s requires a .write_vertex(..) abstract method.' % StatefulVertexWriteableGraphInterface.__name__)

class StatelessEdgeWriteableDirectedGraphInterface(Generic[VertexLabel], ABC):
    '''
    ABC for objects that can write an unlabelled directed edge between a pair of labelled vertices in a graph-like structure.
    '''

    @abstractmethod
    def write_stateless_directed_edge(self, source: VertexLabel, destination: VertexLabel, *args: Any, **kwargs: Any) -> None:
        '''
        Writes an unlabelled directed edge from a vertex with this `source` label to a vertex with this `destination` label.
        '''
        raise NotImplementedError('%s requires a .write_directed_edge(..) abstract method.' % StatelessEdgeWriteableDirectedGraphInterface.__name__)
