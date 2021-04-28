'''
Simple* Collection.
'''

# built-in imports
from abc import ABC, abstractmethod
from typing import Any, Generic, List, Type
from typing_extensions import TypeAlias

# library imports
from .types import VertexData
from .abc import SimpleGraphStrategy

# external imports
from networkx.classes.digraph import DiGraph


'''
Types.
'''

SimpleVertexLabel: TypeAlias = int

SimpleVertexPath: TypeAlias = List[int]

SimpleBroadcastData: TypeAlias = type

'''
ABC things.
'''

class BufferedGraphColouringContext\
(
    Generic[VertexData], ABC   
):
    '''
    ABC for objects that can manage a context for a `BufferedGraphColouring` strategy.
    '''

    @abstractmethod
    def add_edge(self, source: SimpleVertexLabel, destination: SimpleVertexLabel, *args: Any, **kwargs: Any) -> None:
        '''
        Adds an edge from this `source` to this `destination` label on a graph-like structure.
        '''
        raise NotImplementedError('%s requires an .add_edge(..) abstract method.' % BufferedGraphColouringContext.__name__)

    @abstractmethod
    def add_vertex(self, label: SimpleVertexLabel, data: VertexData, *args: Any, **kwargs: Any) -> None:
        '''
        Adds a disjointed vertex with this `label` and associated `data` to a graph-like structure.
        '''
        raise NotImplementedError('%s requires an .add_vertex(..) abstract method.' % BufferedGraphColouringContext.__name__)
    
    @abstractmethod
    def push_to_path(self, label: SimpleVertexLabel, *arg: Any, **kwargs: Any) -> None:
        '''
        Pushes a vertex with this `label` to the current path on a graph-like structure.
        '''
        raise NotImplementedError('%s requires an .add_to_path(..) abstract method.' % BufferedGraphColouringContext.__name__)

    @abstractmethod
    def pop_from_path(self, *args: Any, **kwargs: Any) -> SimpleVertexLabel:
        '''
        Pops a vertex from the current path and returns the associated `SimpleVertexLabel`. 
        '''
        raise NotImplementedError('%s requires a .pop_from_path(..) abstract method.' % BufferedGraphColouringContext.__name__)


'''
Concrete classes and ABC extensions.
'''

class SimpleBufferedGraphColouringContext\
(
    Generic[VertexData], BufferedGraphColouringContext[VertexData]
):
    '''
    Class that can manage the context for a `BufferedGraphColouring` strategy.
    '''

    __graph: DiGraph
    __path: SimpleVertexPath

    '''
    Property and dunder methods.
    '''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a `DiGraph` and `Path` instance. 
        '''
        self.__graph = DiGraph()
        
        self.__path = list()

        return None

    @property
    def _graph(self) -> DiGraph: return self.__graph

    @property
    def _path(self) -> SimpleVertexPath: return self.__path

    '''
    ABC extensions.
    '''

    def add_edge(self, source: SimpleVertexLabel, destination: SimpleVertexLabel, *args: Any, **kwargs: Any) -> None:
        '''
        Adds an edge from this `source` to this `destination` on a `networkx` `DiGraph` instance.
        '''
        self.__graph.add_edge(u_of_edge = source, v_of_edge = destination)

        return None

    def add_vertex(self, label: SimpleVertexLabel, data: VertexData, *args: Any, **kwargs: Any) -> None:
        '''
        Adds a disjoint vertex with this `label` and `data` attribute to a `networkx` `DiGraph` instance.

        The `data` argument is stored in the vertex as a `data` attribute.
        '''
        self.__graph.add_node(node_for_adding = label, data = data)

        return None

    def push_to_path(self, label: SimpleVertexLabel, *arg: Any, **kwargs: Any) -> None:
        '''
        Appends this `label` to a `SimpleVertexPath` type.
        '''
        self.__path.append(label)

        return None

    def pop_from_path(self, *args: Any, **kwargs: Any) -> SimpleVertexLabel:
        '''
        Pops the most recent `SimpleVertexLabel` from a `SimpleVertexPath` type.
        '''
        return self.__path.pop()


class SimpleBufferedGraphColouringStrategy\
(
    Generic[VertexData], SimpleGraphStrategy[VertexData]
):
    '''
    Class that can extend to new nodes and move backwards on a graph-like structure.
    '''

    __nodes: SimpleVertexLabel
    __frontier: SimpleVertexLabel

    __context: SimpleBufferedGraphColouringContext[VertexData]

    '''
    Dunder and property methods.
    '''
    
    def __init__(self, context: SimpleBufferedGraphColouringContext[VertexData], *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a `SimpleBufferedGraphColouringStrategy` in this `context`.
        '''
        self.__nodes = 0
        
        self.__frontier = 0

        self.__context = context

        return None

    @property
    def _nodes(self) -> SimpleVertexLabel: return self.__nodes

    @property
    def _frontier(self) -> SimpleVertexLabel: return self.__frontier

    @property
    def _context(self) -> SimpleBufferedGraphColouringContext[VertexData]: return self.__context

    '''
    ABC extensions.
    '''

    def extend(self, data: VertexData, *args: Any, **kwargs: Any) -> None:
        '''
        Extends the graph-like context frontier to a new node with this data.

        See https://github.com/ZaliaFlow/decode-py/issues/2 for details.
        '''
        self.__nodes += 1

        self.__context.add_vertex(label = self.__nodes, data = data)

        self.__context.add_edge(source = self.__frontier, destination = self.__nodes)

        self.__context.push_to_path(label = self.__frontier)

        self.__frontier = self.__nodes

        return None

    def retreat(self, *args: Any, **kwargs: Any) -> None:
        '''
        Retreats the current frontier of the graph-like context to the previous vertex on the current path.

        See https://github.com/ZaliaFlow/decode-py/issues/2 for details.
        '''
        self.__frontier = self.__context.pop_from_path()

        return None


class SimpleBroadcastFacade:
    '''
    Class that can start and stop a trace on an object, storing only type data.
    '''

    __strategy: SimpleBufferedGraphColouringStrategy[SimpleBroadcastData]

    '''
    Dunder and property methods.
    '''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a strategy and context for this instance.
        '''
        context: SimpleBufferedGraphColouringContext[SimpleBroadcastData] = SimpleBufferedGraphColouringContext()

        self.__strategy = SimpleBufferedGraphColouringStrategy(context = context)

        return None

    @property
    def _strategy(self) -> SimpleBufferedGraphColouringStrategy[SimpleBroadcastData]: return self.__strategy

    '''
    Facade logic.
    '''

    def trace(self, data: SimpleBroadcastData, *args: Any, **kwargs: Any) -> None:
        '''
        Starts a trace on this `data` in a given context.
        '''
        self.__strategy.extend(data = data)

        return None

    def untrace(self, *args: Any, **kwargs: Any) -> None:
        '''
        Stops the last trace in this context.
        '''
        self.__strategy.retreat()

        return None
