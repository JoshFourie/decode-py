'''
Simple* Collection.
'''

# built-in imports
from abc import abstractmethod, ABC
from typing import Any, Generic, List
from typing_extensions import TypeAlias

# library imports
from ._types import NodeKey, NodeMemento

from ..database import PartiallyStatefulDirectedGraphInterface


'''
Types.
'''

SimpleGraphKey: TypeAlias = int

SimpleConnectedGraphKeyCollection: TypeAlias = List[NodeKey]

SimpleGraphMemento: TypeAlias = type


'''
ABC definitions for this module.
'''

class BufferedGraphColouringStrategy\
(
    Generic[NodeMemento], 
    ABC
):
    '''
    ABC for objects that can extend to new nodes and move backwards on a graph-like structure.
    '''

    @abstractmethod
    def extend_(self, data: NodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Extend the graph-like structure from the current frontier to a new node associated with this data.
        '''
        raise NotImplementedError('%s requires an .extend(..) abstract method.' % BufferedGraphColouringStrategy.__name__)

    @abstractmethod
    def retreat_(self, *args: Any, **kwargs: Any) -> None:
        '''
        Retreat fron the current frontier to the previous node.
        '''
        raise NotImplementedError('%s requires a .retreat(..) abstract method.' % BufferedGraphColouringStrategy.__name__)



'''
Concrete classes and ABC extensions.
'''

class SimpleBufferedGraphColouringContext\
(
    Generic[NodeKey, NodeMemento]
):
    '''
    Class that can manage the context for a `SimpleBufferedGraphColouringStrategy` type.
    '''

    __writer: PartiallyStatefulDirectedGraphInterface[NodeKey, NodeMemento]
    __path: SimpleConnectedGraphKeyCollection[NodeKey]

    '''
    Property and dunder methods.
    '''

    def __init__(self, writer: PartiallyStatefulDirectedGraphInterface[NodeKey, NodeMemento], *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a path and graph for this context. 
        '''

        self.__path = list()

        self.__writer = writer

        return None

    @property
    def _path(self) -> SimpleConnectedGraphKeyCollection[NodeKey]: return self.__path

    @property
    def writer(self) -> PartiallyStatefulDirectedGraphInterface[NodeKey, NodeMemento]: return self.__writer

    '''
    ABC extensions.
    '''

    def add_edge_between_(self, source: NodeKey, destination: NodeKey, *args: Any, **kwargs: Any) -> None:
        '''
        Adds an edge from this `source` to this `destination` on a `networkx` `DiGraph` instance.
        '''
        self.__writer.write_stateless_directed_edge_(source = source, destination = destination)

        return None

    def add_vertex_with_data_(self, label: NodeKey, data: NodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Adds a disjoint vertex with this `label` and `data` attribute to a `networkx` `DiGraph` instance.

        The `data` argument is stored in the vertex as a `data` attribute.
        '''
        self.__writer.write_stateful_vertex_(label = label, data = data)

        return None

    def push_to_path_(self, label: NodeKey, *arg: Any, **kwargs: Any) -> None:
        '''
        Appends this `label` to a `SimpleVertexPath` type.
        '''
        self.__path.append(label)

        return None

    def pop_from_path_(self, *args: Any, **kwargs: Any) -> NodeKey:
        '''
        Pops the most recent `SimpleVertexLabel` from a `SimpleVertexPath` type.
        '''
        return self.__path.pop()


class SimpleBufferedGraphColouringStrategy\
(
    Generic[NodeMemento],
    BufferedGraphColouringStrategy[NodeMemento]
):
    '''
    Class that can extend to new nodes and move backwards on a graph-like structure.
    '''

    __nodes: SimpleGraphKey
    __frontier: SimpleGraphKey

    __context: SimpleBufferedGraphColouringContext[SimpleGraphKey, NodeMemento]

    '''
    Dunder and property methods.
    '''
    
    def __init__(self, context: SimpleBufferedGraphColouringContext[SimpleGraphKey, NodeMemento], *args: Any, **kwargs: Any) -> None:
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
    def context(self) -> SimpleBufferedGraphColouringContext[SimpleGraphKey, NodeMemento]: return self.__context

    '''
    ABC extensions.
    '''

    def extend_(self, data: NodeMemento, *args: Any, **kwargs: Any) -> None:
        '''
        Extends the graph-like context frontier to a new node with this data.

        See https://github.com/ZaliaFlow/decode-py/issues/2 for details.
        '''
        self.__nodes += 1

        self.__context.add_vertex_with_data_(label = self.__nodes, data = data)

        self.__context.add_edge_between_(source = self.__frontier, destination = self.__nodes)

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


class SimpleMakerFacade\
(
    Generic[NodeMemento]
):
    '''
    Class that can start and stop a trace on an object, storing only type data.
    '''

    __strategy: SimpleBufferedGraphColouringStrategy[NodeMemento]

    '''
    Dunder and property methods.
    '''

    def __init__(self, graph: PartiallyStatefulDirectedGraphInterface[SimpleGraphKey, NodeMemento], *args: Any, **kwargs: Any) -> None:
        '''
        Sets up a strategy and context for this instance.
        '''
        context: SimpleBufferedGraphColouringContext[SimpleGraphKey, NodeMemento] = SimpleBufferedGraphColouringContext(writer = graph)

        self.__strategy = SimpleBufferedGraphColouringStrategy(context = context)

        return None

    @property
    def _strategy(self) -> SimpleBufferedGraphColouringStrategy[NodeMemento]: return self.__strategy

    @property
    def context(self) -> SimpleBufferedGraphColouringContext[SimpleGraphKey, NodeMemento]: return self.__strategy.context

    @property
    def graph(self) -> PartiallyStatefulDirectedGraphInterface[SimpleGraphKey, NodeMemento]: return self.context.writer

    '''
    Facade logic.
    '''

    def trace_(self, data: NodeMemento, *args: Any, **kwargs: Any) -> None:
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
