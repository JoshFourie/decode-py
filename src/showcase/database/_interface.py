'''
ABC types for the maker module.

See https://github.com/ZaliaFlow/decode-py/issues/5.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic

# library imports
from ._types import VertexLabel, VertexData


class StatefulVertexGraphWriterInterface(Generic[VertexLabel, VertexData], ABC):
    '''
    ABC for objects that can write a `(label, data)` pair as a vertex in a graph-like structure.
    '''

    @abstractmethod
    def write_stateful_vertex_(self, label: VertexLabel, data: VertexData, *args: Any, **kwargs: Any) -> None:
        '''
        Writes a vertex with this `label` and associates it with this `data`. 
        '''
        raise NotImplementedError('%s requires a .write_stateful_vertex(..) abstract method.' % StatefulVertexGraphWriterInterface.__name__)


class StatefulVertexGraphLoaderInterface(Generic[VertexLabel, VertexData], ABC):
    '''
    ABC for objects that can load some `VertexData` from a graph-like structure using a `VertexLabel`.
    '''

    @abstractmethod
    def load_stateful_vertex(self, label: VertexLabel, *args: Any, **kwargs: Any) -> VertexData:
        '''
        Loads the `VertexData` associated with this `label` from a graph-like structure.
        '''
        raise NotImplementedError('%s requires a .load_stateful_vertex(..) abstract method.' % StatefulVertexGraphWriterInterface.__name__)


class StatelessDirectedEdgeGraphWriterInterface(Generic[VertexLabel], ABC):
    '''
    ABC for objects that can write an unlabelled directed edge between a pair of labelled vertices in a graph-like structure.
    '''

    @abstractmethod
    def write_stateless_directed_edge_(self, source: VertexLabel, destination: VertexLabel, *args: Any, **kwargs: Any) -> None:
        '''
        Writes an unlabelled directed edge from a vertex with this `source` label to a vertex with this `destination` label.
        '''
        raise NotImplementedError('%s requires a .write_directed_edge(..) abstract method.' % StatelessDirectedEdgeGraphWriterInterface.__name__)


class PartiallyStatefulDirectedGraphInterface\
(
    Generic[VertexLabel, VertexData],
    StatefulVertexGraphWriterInterface[VertexLabel, VertexData],
    StatelessDirectedEdgeGraphWriterInterface[VertexLabel]
):
    '''
    Interface for objects that are both `StatefulVertexWriteableGraphInterface` and `StatelessEdgeWriteableDirectedGraphInterface`.
    '''

    # @TODO: python does not support intersection typing, does this work around for all cases?

    # See: https://github.com/python/typing/issues/213

    pass
