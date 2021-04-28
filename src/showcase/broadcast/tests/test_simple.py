'''
Tests the Simple* implementation of a broadcast module.
'''

# built-in imports
from typing import List, Tuple
from typing_extensions import TypeAlias

# library imports
from ..simple import SimpleBroadcastFacade, SimpleBufferedGraphColouringContext, SimpleBufferedGraphColouringStrategy


'''
Mock-ups for testing.
'''

MockVertexData: TypeAlias = None


class MockDisplayable:
    '''
    Type for testing the broadcast facade.
    '''

    @classmethod
    def display(cls) -> str: return 'MockDisplayable'



'''
Unit tests for buffered graph colouring.
'''

def test_simple_buffered_graph_colouring_context() -> None:
    '''
    Tests the behaviour of the `SimpleBufferedGraphColouringContext` object.
    ''' 

    context: SimpleBufferedGraphColouringContext[MockVertexData] = SimpleBufferedGraphColouringContext()

    # test adding a vertex
    
    context.add_vertex(label = 0, data = None)

    assert list(context._graph.nodes) == [0], 'expeced <%s>.add_vertex(..) to add a vertex to the list of nodes.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore private usage and unknown field type

    context.add_vertex(label = 9, data = None)

    assert list(context._graph.nodes) == [0, 9], 'expeced <%s>.add_vertex(..) to add a vertex to the list of nodes.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore private usage and unknown field type

    # test adding an edge between existing vertices

    context.add_edge(source = 0, destination = 9)

    assert list(context._graph.edges) == [(0, 9)], 'expeced <%s>.add_edge(..) to add an edge from nodes 0 -> 9 in the list of edges.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore private usage and unknown field type

    # test pushing an existing node to the path

    context.push_to_path(label = 0)

    assert context._path == [0], 'expeced <%s>.push_to_path(..) to add the label to the list of nodes on the current path.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore private usage

    context.push_to_path(label = 9)

    assert context._path == [0, 9], 'expeced <%s>.push_to_path(..) to add the label to the list of nodes on the current path.' % SimpleBufferedGraphColouringContext.__name__ # type: ignore private usage

    # test popping a label from the current path

    assert context.pop_from_path() == 9, 'expected <%s>.pop_from_path(..) to pop the most recent label from the current path.' % SimpleBufferedGraphColouringContext.__name__

    assert context.pop_from_path() == 0, 'expected <%s>.pop_from_path(..) to pop the most recent label from the current path.' % SimpleBufferedGraphColouringContext.__name__
    
    
def test_buffered_graph_colouring_strategy() -> None:
    '''
    Tests the behaviour of the `SimpleBufferedGraphColouringStrategy`.
    '''

    context: SimpleBufferedGraphColouringContext[MockVertexData] = SimpleBufferedGraphColouringContext()

    strategy: SimpleBufferedGraphColouringStrategy[MockVertexData] = SimpleBufferedGraphColouringStrategy(context = context)

    # test that strategy can extend to a new node

    strategy.extend(data = None)

    assert strategy._nodes == 1 and strategy._frontier == 1, 'expected <%s>.extend(..) to increment the ._nodes and ._frontier properties.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert list(strategy._context._graph.edges) == [(0, 1)], 'expected <%s>.extend(..) to add an edge from nodes 0 to 1.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage and unknown member type

    assert strategy._context._path == [0], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    # test that strategy can walk backwards from a frontier

    strategy.retreat()

    assert strategy._nodes == 1 and strategy._frontier == 0, 'expected <%s>.retreat(..) to decrement the ._frontier property.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy._context._path == [ ], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    # tests that strategy can grow three branches from a root node

    strategy.extend(data = None)

    assert strategy._nodes == 2 and strategy._frontier == 2, 'expected <%s>.extend(..) to increment the ._nodes and ._frontier properties.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy._context._path == [0], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    strategy.retreat()

    assert strategy._nodes == 2 and strategy._frontier == 0, 'expected <%s>.retreat(..) to go back to the last ._frontier on the current path.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy._context._path == [ ], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    strategy.extend(data = None)

    assert strategy._nodes == 3 and strategy._frontier == 3, 'expected <%s>.extend(..) to increment the ._nodes and ._frontier properties.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy._context._path == [0], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    strategy.retreat()

    assert strategy._nodes == 3 and strategy._frontier == 0, 'expected <%s>.retreat(..) to go back to the last ._frontier on the current path.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    assert strategy._context._path == [ ], 'expected <%s>.extend(..) to update the current path of the context.' % SimpleBufferedGraphColouringStrategy.__name__  # type: ignore private usage

    # all tests passed

    return None

def test_nested_buffered_graph_colouring_strategy() -> None:
    '''
    Tests that `SimpleBufferedGraphColouringStrategy` can grow nested trees.
    '''
    context: SimpleBufferedGraphColouringContext[MockVertexData] = SimpleBufferedGraphColouringContext()

    strategy: SimpleBufferedGraphColouringStrategy[MockVertexData] = SimpleBufferedGraphColouringStrategy(context = context)

    for i in range(0, 3): 
        strategy.extend(data = None)
        for _ in range(i + 1, 3): 
            strategy.extend(data = None)
            strategy.retreat()
        strategy.retreat()

    test = set(strategy._context._graph.edges)  # type: ignore private usage and unknown member type
    expected = set([(0, 1), (0, 4), (0, 6), (1, 2), (1, 3), (4, 5)])

    assert test == expected, 'expected <%s>.extend(..) and <%s>.retreat(..) to grow the expected tree' % (SimpleBufferedGraphColouringStrategy.__name__, SimpleBufferedGraphColouringStrategy.__name__)


'''
Unit tests for the simple broadcast facade.
'''

def test_simple_broadcast_facade() -> None:
    '''
    Tests the behaviour of the `SimpleBroadcastFacade` object.
    '''
    facade: SimpleBroadcastFacade = SimpleBroadcastFacade()

    # test that the facade can start a trace

    facade.trace(data = MockDisplayable)

    assert list(facade._strategy._context._graph.edges) == [(0, 1)], 'expected that <%s>.trace(..) would add an edge to the context.' % SimpleBroadcastFacade.__name__  # type: ignore private usage

    assert facade._strategy._context._path == [0], 'expected that <%s>.trace(..) would add an entrypoint to the current path.' % SimpleBroadcastFacade.__name__  # type: ignore private usage

    assert facade._strategy._nodes == 1 and facade._strategy._frontier == 1, 'expected that <%s>.trace(..) would update the strategy.' % SimpleBroadcastFacade.__name__  # type: ignore private usage

    # test that a facade can stop a trace

    facade.untrace()

    assert facade._strategy._context._path == [ ], 'expected that <%s>.trace(..) would pop everything from the current path.' % SimpleBroadcastFacade.__name__  # type: ignore private usage

    assert facade._strategy._nodes == 1 and facade._strategy._frontier == 0, 'expected that <%s>.trace(..) would update the strategy to the last frontier.' % SimpleBroadcastFacade.__name__  # type: ignore private usage 

    assert facade._strategy._context._graph.nodes[1].get('data').display() == 'MockDisplayable', 'expected that <%s> would update the context with a callable MockDisplayable type' % SimpleBroadcastFacade.__name__  # type: ignore private usage

    return None
