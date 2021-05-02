'''
Simple* Collection.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic, List
from typing_extensions import TypeAlias

# library imports
from .types import GraphNodeMemento
from .abc import SimpleGraphStrategy

# external imports
from networkx.classes.digraph import DiGraph


'''
Types.
'''

SimpleGraphKey: TypeAlias = int

SimpleConnectedGraphKeyCollection: TypeAlias = List[SimpleGraphKey]

SimpleGraphMemento: TypeAlias = type

'''
ABC things.
'''

class BufferedGraphColouringContext\
(
    Generic[GraphNodeMemento], ABC   
):
    '''
    ABC for objects that can manage a context for a `SimpleBufferedGraphColouringStrategy` type.
    '''

    @abstractmethod
    def add_edge_(self, source: SimpleGraphKey, destination: SimpleGraphKey, *args: Any, **kwargs: Any) -> None:
        '''
        Adds an edge from this `source` to this `destination` label on a graph-like structure.
        '''
        raise NotImplementedError('%s requires an .add_edge(..) abstract method.' % BufferedGraphColouringContext.__name__)

    @abstractmethod
    def add_vertex_(self, label: SimpleGraphKey, data: GraphNodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Adds a disjointed vertex with this `label` and associated `data` to a graph-like structure.
        '''
        raise NotImplementedError('%s requires an .add_vertex(..) abstract method.' % BufferedGraphColouringContext.__name__)
    
    @abstractmethod
    def push_to_path_(self, label: SimpleGraphKey, *arg: Any, **kwargs: Any) -> None:
        '''
        Pushes a vertex with this `label` to the current path on a graph-like structure.
        '''
        raise NotImplementedError('%s requires an .add_to_path(..) abstract method.' % BufferedGraphColouringContext.__name__)

    @abstractmethod
    def pop_from_path_(self, *args: Any, **kwargs: Any) -> SimpleGraphKey:
        '''
        Pops a vertex from the current path and returns the associated `SimpleVertexLabel`. 
        '''
        raise NotImplementedError('%s requires a .pop_from_path(..) abstract method.' % BufferedGraphColouringContext.__name__)


'''
Concrete classes and ABC extensions.
'''

class SimpleBufferedGraphColouringContext\
(
    Generic[GraphNodeMemento], BufferedGraphColouringContext[GraphNodeMemento]
):
    '''
    Class that can manage the context for a `SimpleBufferedGraphColouringStrategy` type.
    '''

    __graph: DiGraph
    __path: SimpleConnectedGraphKeyCollection

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
    def _path(self) -> SimpleConnectedGraphKeyCollection: return self.__path

    @property
    def graph(self) -> DiGraph: return self.__graph

    '''
    ABC extensions.
    '''

    def add_edge_(self, source: SimpleGraphKey, destination: SimpleGraphKey, *args: Any, **kwargs: Any) -> None:
        '''
        Adds an edge from this `source` to this `destination` on a `networkx` `DiGraph` instance.
        '''
        self.__graph.add_edge(u_of_edge = source, v_of_edge = destination)

        return None

    def add_vertex_(self, label: SimpleGraphKey, data: GraphNodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Adds a disjoint vertex with this `label` and `data` attribute to a `networkx` `DiGraph` instance.

        The `data` argument is stored in the vertex as a `data` attribute.
        '''
        self.__graph.add_node(node_for_adding = label, data = data)

        return None

    def push_to_path_(self, label: SimpleGraphKey, *arg: Any, **kwargs: Any) -> None:
        '''
        Appends this `label` to a `SimpleVertexPath` type.
        '''
        self.__path.append(label)

        return None

    def pop_from_path_(self, *args: Any, **kwargs: Any) -> SimpleGraphKey:
        '''
        Pops the most recent `SimpleVertexLabel` from a `SimpleVertexPath` type.
        '''
        return self.__path.pop()


class SimpleBufferedGraphColouringStrategy\
(
    Generic[GraphNodeMemento], SimpleGraphStrategy[GraphNodeMemento]
):
    '''
    Class that can extend to new nodes and move backwards on a graph-like structure.
    '''

    __nodes: SimpleGraphKey
    __frontier: SimpleGraphKey

    __context: SimpleBufferedGraphColouringContext[GraphNodeMemento]

    '''
    Dunder and property methods.
    '''
    
    def __init__(self, context: SimpleBufferedGraphColouringContext[GraphNodeMemento], *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a `SimpleBufferedGraphColouringStrategy` in this `context`.
        '''
        self.__nodes = 0
        
        self.__frontier = 0

        self.__context = context

        return None

    @property
    def _nodes(self) -> SimpleGraphKey: return self.__nodes

    @property
    def _frontier(self) -> SimpleGraphKey: return self.__frontier

    @property
    def context(self) -> SimpleBufferedGraphColouringContext[GraphNodeMemento]: return self.__context

    '''
    ABC extensions.
    '''

    def extend_(self, data: GraphNodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Extends the graph-like context frontier to a new node with this data.

        See https://github.com/ZaliaFlow/decode-py/issues/2 for details.
        '''
        self.__nodes += 1

        self.__context.add_vertex_(label = self.__nodes, data = data)

        self.__context.add_edge_(source = self.__frontier, destination = self.__nodes)

        self.__context.push_to_path_(label = self.__frontier)

        self.__frontier = self.__nodes

        return None

    def retreat_(self, *args: Any, **kwargs: Any) -> None:
        '''
        Retreats the current frontier of the graph-like context to the previous vertex on the current path.

        See https://github.com/ZaliaFlow/decode-py/issues/2 for details.
        '''
        self.__frontier = self.__context.pop_from_path_()

        return None


class SimpleBroadcastFacade:
    '''
    Class that can start and stop a trace on an object, storing only type data.
    '''

    __strategy: SimpleBufferedGraphColouringStrategy[SimpleGraphMemento]

    '''
    Dunder and property methods.
    '''

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a strategy and context for this instance.
        '''
        context: SimpleBufferedGraphColouringContext[SimpleGraphMemento] = SimpleBufferedGraphColouringContext()

        self.__strategy = SimpleBufferedGraphColouringStrategy(context = context)

        return None

    @property
    def _strategy(self) -> SimpleBufferedGraphColouringStrategy[SimpleGraphMemento]: return self.__strategy

    @property
    def context(self) -> SimpleBufferedGraphColouringContext[SimpleGraphMemento]: return self.__strategy.context

    '''
    Facade logic.
    '''

    def trace_(self, data: SimpleGraphMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Starts a trace on this `data` in a given context.
        '''
        self.__strategy.extend_(data = data)

        return None

    def untrace_(self, *args: Any, **kwargs: Any) -> None:
        '''
        Stops the last trace in this context.
        '''
        self.__strategy.retreat_()

        return None
