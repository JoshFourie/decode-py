'''
Tests the Simple* implementation of a maker module.
'''

# built-in imports
from typing import Any, Generic, TypeVar

# library imports
from ..simple import SimpleMakerFacade, SimpleBufferedGraphColouringContext, SimpleBufferedGraphColouringStrategy, PartiallyStatefulDirectedGraphInterface, SimpleGraphKey, SimpleGraphMemento

# external imports
from networkx.classes.digraph import DiGraph

'''
Mock-ups for testing.
'''

MockVertexData = TypeVar('MockVertexData')


class MockDisplayableComponent:
    '''
    Type for testing the maker facade.
    '''

    @classmethod
    def display(cls) -> str: return 'MockDisplayableComponent'


class MockSimpleGraphDB\
(
    Generic[MockVertexData],
    PartiallyStatefulDirectedGraphInterface[SimpleGraphKey, MockVertexData]
):
    '''
    Type for mocking a simple database.
    '''

    data: DiGraph

    def __init__(self) -> None: self.data = DiGraph()

    def write_stateful_vertex_(self, label: SimpleGraphKey, data: MockVertexData, *args: Any, **kwargs: Any) -> None: self.data.add_node(node_for_adding = label, memento = data)  # type: ignore unkonwn
    
    def write_stateless_directed_edge_(self, source: SimpleGraphKey, destination: SimpleGraphKey, *args: Any, **kwargs: Any) -> None: self.data.add_edge(u_of_edge = source, v_of_edge = destination)  # type: ignore unkonwn member


'''
Unit tests for buffered graph colouring.
'''

def test_simple_buffered_graph_colouring_context() -> None:
    '''
    Tests the behaviour of the `SimpleBufferedGraphColouringContext` object.
    ''' 

    graph: MockSimpleGraphDB[None] = MockSimpleGraphDB()

    context: SimpleBufferedGraphColouringContext[SimpleGraphKey, None] = SimpleBufferedGraphColouringContext(writer = graph)

    # test adding a vertex

    context.add_vertex_with_data_(label = 0, data = None)

    assert list(context.writer.data.nodes) == [0], 'expected <%s>.add_vertex(..) to add a vertex to the list of nodes.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore unknown field type

    context.add_vertex_with_data_(label = 9, data = None)

    assert list(context.writer.data.nodes) == [0, 9], 'expected <%s>.add_vertex(..) to add a vertex to the list of nodes.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore unknown field type

    # test adding an edge between existing vertices

    context.add_edge_between_(source = 0, destination = 9)

    assert list(context.writer.data.edges) == [(0, 9)], 'expected <%s>.add_edge(..) to add an edge from nodes 0 -> 9 in the list of edges.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore unknown field type

    # test pushing an existing node to the path

    context.push_to_path_(label = 0)

    assert context._path == [0], 'expected <%s>.push_to_path(..) to add the label to the list of nodes on the current path.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore private usage

    context.push_to_path_(label = 9)

    assert context._path == [0, 9], 'expected <%s>.push_to_path(..) to add the label to the list of nodes on the current path.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore private usage

    # test popping a label from the current path

    assert context.pop_from_path_() == 9, 'expected <%s>.pop_from_path(..) to pop the most recent label from the current path.' % SimpleBufferedGraphColouringContext.__name__

    assert context.pop_from_path_() == 0, 'expected <%s>.pop_from_path(..) to pop the most recent label from the current path.' % SimpleBufferedGraphColouringContext.__name__
    
    
def test_buffered_graph_colouring_strategy() -> None:
    '''
    Tests the behaviour of the `SimpleBufferedGraphColouringStrategy`.
    '''

    graph: MockSimpleGraphDB[None] = MockSimpleGraphDB()

    context: SimpleBufferedGraphColouringContext[SimpleGraphKey, None] = SimpleBufferedGraphColouringContext(writer = graph)

    strategy: SimpleBufferedGraphColouringStrategy[None] = SimpleBufferedGraphColouringStrategy(context = context)

    # test that strategy can extend to a new node

    strategy.extend_(data = None)

    assert strategy._nodes == 1 and strategy._frontier == 1, 'expected <%s>.extend(..) to increment the ._nodes and update the ._frontier properties.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert list(strategy.context.writer.data.edges) == [(0, 1)], 'expected <%s>.extend(..) to add an edge from nodes 0 to 1.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore unknown member type

    assert strategy.context._path == [0], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    # test that strategy can walk backwards from a frontier

    strategy.retreat_()

    assert strategy._nodes == 1 and strategy._frontier == 0, 'expected <%s>.retreat(..) to decrement the ._frontier property.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy.context._path == [ ], 'expected <%s>.retreat(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    # tests that strategy can grow three branches from a root node

    strategy.extend_(data = None)

    assert strategy._nodes == 2 and strategy._frontier == 2, 'expected <%s>.extend(..) to increment the ._nodes and update the ._frontier properties.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy.context._path == [0], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert list(strategy.context.writer.data.edges) == [(0, 1), (0, 2)], 'expected <%s>.extend(..) to add an edge from nodes 0 to 2.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore unknown member type

    strategy.retreat_()

    assert strategy._nodes == 2 and strategy._frontier == 0, 'expected <%s>.retreat(..) to go back to the last ._frontier on the current path.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy.context._path == [ ], 'expected <%s>.retreat(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    strategy.extend_(data = None)

    assert strategy._nodes == 3 and strategy._frontier == 3, 'expected <%s>.extend(..) to increment the ._nodes and update the ._frontier properties.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy.context._path == [0], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert list(strategy.context.writer.data.edges) == [(0, 1), (0, 2), (0, 3)], 'expected <%s>.extend(..) to add an edge from nodes 0 to 3.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore unknown member type

    strategy.retreat_()

    assert strategy._nodes == 3 and strategy._frontier == 0, 'expected <%s>.retreat(..) to go back to the last ._frontier on the current path.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy.context._path == [ ], 'expected <%s>.retreat(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    # all tests passed

    return None

def test_nested_buffered_graph_colouring_strategy() -> None:
    '''
    Tests that `SimpleBufferedGraphColouringStrategy` can grow nested trees.
    '''
    graph: MockSimpleGraphDB[None] = MockSimpleGraphDB()

    context: SimpleBufferedGraphColouringContext[SimpleGraphKey, None] = SimpleBufferedGraphColouringContext(writer = graph)

    strategy: SimpleBufferedGraphColouringStrategy[None] = SimpleBufferedGraphColouringStrategy(context = context)

    for i in range(0, 3): 
        strategy.extend_(data = None)
        for _ in range(i + 1, 3): 
            strategy.extend_(data = None)
            strategy.retreat_()
        strategy.retreat_()

    test = set(strategy.context.writer.data.edges)  # type: ignore unknown member type
    expected = set([(0, 1), (0, 4), (0, 6), (1, 2), (1, 3), (4, 5)])

    assert test == expected, 'expected <%s>.extend(..) and <%s>.retreat(..) to grow the expected tree' % (SimpleBufferedGraphColouringStrategy.__name__, SimpleBufferedGraphColouringStrategy.__name__)


'''
Unit tests for the simple maker facade.
'''

def test_simple_maker_facade() -> None:
    '''
    Tests the behaviour of the `SimpleMakerFacade` object.
    '''
    graph: MockSimpleGraphDB[SimpleGraphMemento] = MockSimpleGraphDB()

    facade: SimpleMakerFacade[SimpleGraphMemento] = SimpleMakerFacade(graph = graph)

    # test that the facade can start a trace

    facade.trace_(data = MockDisplayableComponent)

    assert list(facade.context.writer.data.edges) == [(0, 1)], 'expected that <%s>.trace(..) would add an edge to the context.' % SimpleMakerFacade.__name__  # type: ignore unknown members  

    assert facade.context._path == [0], 'expected that <%s>.trace(..) would add an entrypoint to the current path.' % SimpleMakerFacade.__name__  # type: ignore private usage

    assert facade._strategy._nodes == 1 and facade._strategy._frontier == 1, 'expected that <%s>.trace(..) would update the strategy.' % SimpleMakerFacade.__name__  # type: ignore private usage

    # test that a facade can stop a trace

    facade.untrace_()

    assert facade.context._path == [ ], 'expected that <%s>.untrace(..) would pop everything from the current path.' % SimpleMakerFacade.__name__  # type: ignore private usage

    assert facade._strategy._nodes == 1 and facade._strategy._frontier == 0, 'expected that <%s>.untrace(..) would update the strategy to the last frontier.' % SimpleMakerFacade.__name__  # type: ignore private usage 

    # test that a facade can store type data

    assert facade.context.writer.data.nodes[1].get('memento').display() == 'MockDisplayableComponent', 'expected that <%s> would update the context with a callable MockDisplayableComponent type' % SimpleMakerFacade.__name__ # type: ignore unknown members

    # all tests passed

    return None
