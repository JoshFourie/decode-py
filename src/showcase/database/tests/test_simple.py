'''
Tests for the Simple* Collection in the database module.
'''

# built-in imports
from typing_extensions import TypeAlias

# library imports
from ..simple import SimpleGraphDB


'''
Concrete types.
'''

MockVertexData: TypeAlias = None

'''
Unit tests for writing to a simple graph database.
'''

def test_stateful_vertex_writing_for_simple_graph_database() -> None:
    '''
    Tests that a `SimpleGraphDb` type can write a `(label, data)` pair as a vertex.
    '''

    graph_db: SimpleGraphDB[MockVertexData] = SimpleGraphDB()

    # test adding a vertex
    
    graph_db.write_stateful_vertex_(label = 0, data = None)

    assert list(graph_db._graph.nodes) == [0], 'expected <%s>.write_stateful_vertex(..) to add a vertex to the list of nodes.' % SimpleGraphDB.__name__ # type: ignore private usage and unknown field type

    graph_db.write_stateful_vertex_(label = 9, data = None)

    assert list(graph_db._graph.nodes) == [0, 9], 'expected <%s>.write_stateful_vertex(..) to add a vertex to the list of nodes.' % SimpleGraphDB.__name__ # type: ignore private usage and unknown field type

    # all tests passed

    return None


def test_stateless_edge_writing_for_simple_graph_database() -> None:
    '''
    Tests that a `SimpleGraphDb` type can write an unlabelled edge between two maybe non-existent vertices.
    '''

    graph_db: SimpleGraphDB[MockVertexData] = SimpleGraphDB()

    # test adding an edge between existing vertices

    graph_db.write_stateful_vertex_(label = 0, data = None)

    graph_db.write_stateful_vertex_(label = 1, data = None)

    graph_db.write_stateless_directed_edge_(source = 0, destination = 1)

    assert list(graph_db._graph.edges) == [(0, 1)], 'expected <%s>.write_stateless_directed_edge(..) to add an edge.' % SimpleGraphDB.__name__ # type: ignore unknown field type

    # test adding an edge between non existing vertices

    graph_db.write_stateless_directed_edge_(source = 2, destination = 3)

    assert list(graph_db._graph.edges) == [(0, 1), (2, 3)], 'expected <%s>.write_stateless_directed_edge(..) to add an edge .' % SimpleGraphDB.__name__ # type: ignore unknown field type

    # all tests passed

    return None


'''
Unit tests for loading from a simple graph database.
'''

def test_stateful_vertex_loading_for_simple_graph_database() -> None:
    '''
    Tests that a `SimpleGraphDb` type can load some data from an existing vertex.
    '''
    graph_db: SimpleGraphDB[str] = SimpleGraphDB()

    # set up some test parameters

    expected: str = 'expected'

    label: int = 0

    # write some data for the graph

    graph_db.write_stateful_vertex_(label = label, data = expected)

    # test loading some data from an existing vertex

    assert graph_db.load_stateful_vertex(label = label) == expected, 'expected <%s>.load_stateful_vertex(..) to load the stored output for this label.' % SimpleGraphDB.__name__

    # test loading some data from a non-existent vertex throws an error

    try:
        graph_db.load_stateful_vertex(label = 9)

        raise AssertionError('expected <%s>.load_stateful_vertex(..) would raise an error on a bad label.' % SimpleGraphDB.__name__) # pragma: no cover

    except KeyError: pass
    
    # all tests passed

    return None
