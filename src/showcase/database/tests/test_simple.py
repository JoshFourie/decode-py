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
    
    graph_db.write_stateful_vertex(label = 0, data = None)

    assert list(graph_db._graph.nodes) == [0], 'expected <%s>.write_stateful_vertex(..) to add a vertex to the list of nodes.' % SimpleGraphDB.__name__ # type: ignore private usage and unknown field type

    graph_db.write_stateful_vertex(label = 9, data = None)

    assert list(graph_db._graph.nodes) == [0, 9], 'expected <%s>.write_stateful_vertex(..) to add a vertex to the list of nodes.' % SimpleGraphDB.__name__ # type: ignore private usage and unknown field type

    # all tests passed

    return None


def test_stateless_edge_writing_for_simple_graph_database() -> None:
    '''
    Tests that a `SimpleGraphDb` type can write an unlabelled edge between two maybe non-existent vertices.
    '''

    graph_db: SimpleGraphDB[MockVertexData] = SimpleGraphDB()

    # test adding an edge between existing vertices

    graph_db.write_stateless_directed_edge(source = 0, destination = 9)

    assert list(graph_db._graph.edges) == [(0, 9)], 'expected <%s>.write_stateless_directed_edge(..) to add an edge from nodes 0 -> 9 in the list of edges.' % SimpleGraphDB.__name__ # type: ignore unknown field type

    # all tests passed

    return None
