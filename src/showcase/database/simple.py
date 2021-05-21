'''
Simple* Collection for the database module.
'''

# built-in imports
from typing import Any, Generic, Hashable, TypeVar

# library imports
from ._interface import PartiallyStatefulDirectedGraphInterface, StatefulVertexGraphLoaderInterface
from ._types import VertexData

# external imports
from networkx.classes.digraph import DiGraph

'''
Types.
'''

SimpleVertexLabel = TypeVar('SimpleVertexLabel', Hashable, int, str, float)


'''
Concrete classes and ABC extensions.
'''

class SimpleGraphDB\
(
    Generic[SimpleVertexLabel, VertexData], 
    PartiallyStatefulDirectedGraphInterface[SimpleVertexLabel, VertexData],
    StatefulVertexGraphLoaderInterface[SimpleVertexLabel, VertexData]
):
    '''
    Class that can write stateful vertices and stateless directed edges into a graph-like structure.
    '''

    __graph: DiGraph

    '''
    Property and dunder methods
    '''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a `networkx.DiGraph` structure for writing stateful vertices and stateless directed edges.
        '''
        self.__graph = DiGraph()

        return None

    @property
    def _graph(self) -> DiGraph: return self.__graph

    '''
    ABC extensions.
    '''

    def write_stateful_vertex_(self, label: SimpleVertexLabel, data: VertexData, *args: Any, **kwargs: Any) -> None:
        '''
        Writes a vertex with this `label` associated with this `data` into a `networkx.DiGraph` object.
        '''
        self.__graph.add_node(node_for_adding = label, data = data)

        return None

    def write_stateless_directed_edge_(self, source: SimpleVertexLabel, destination: SimpleVertexLabel, *args: Any, **kwargs: Any) -> None:
        '''
        Writes an unlabelled edge between a vertex with this `source` label and one with this `destination` label into a `networkx.DiGraph` object.
        '''
        self.__graph.add_edge(u_of_edge = source, v_of_edge = destination)

        return None

    def load_stateful_vertex(self, label: SimpleVertexLabel, *args: Any, **kwargs: Any) -> VertexData:
        '''
        Loads the `VertexData` associated with this `label` from a `networkx.DiGraph` object.
        '''
        return self.__graph.nodes[label].get('data')
