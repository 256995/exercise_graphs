def build_adjacency_list(edges, directed=False):
    """
    Creates the adjacency list of directed or undirected graph
    :param edges: list of 2-tuples representing edges
    :param directed: boolean, True for directed graphs, False for undirected
    :return: adj_list, dict[str, list[str]]
    """
    vertex = []
    for edge in edges:
        vertex.append(edge[0])
        vertex.append(edge[1])
    vertex_unique = list(dict.fromkeys(vertex))
    adj_list = {i: [] for i in vertex_unique}
    for edge in edges:
        u = edge[0]
        v = edge[1]
        adj_list[u].append(v)
        if not directed:
            adj_list[v].append(u)
    return adj_list

def degrees(graph):
    """
    Computes the degree of every vertex of an undirected graph
    :param graph: adjacency list of an undirected graph
    :return: dictionary of vertices and their degrees
    """
    degree_dict = {}
    for vertex in graph:
        degree_dict[vertex] = len(graph[vertex])
    return degree_dict

def in_out_degree(graph):
    """
    Computes the in and out degrees of every vertex of a directed graph
    :param graph: adjacency list of a directed graph
    :return: (in_degree, out_degree), two dict[str, int], keyed by every vertex.
    """
    in_degree = {}
    out_degree = {}
    for vertex in graph:
        out_degree[vertex] = len(graph[vertex])
        in_degree[vertex] = 0
        for vtx in graph:
            in_degree[vertex] = in_degree[vertex] + graph[vtx].count(vertex)
    return in_degree, out_degree


if __name__ == "__main__":
    # TASK 1
    E = [('P1', 'P2'), ('P1', 'P3'), ('P2', 'P3'), ('P3', 'P4'), ('P4', 'P5')]
    undirected_graph = build_adjacency_list(E)
    print(undirected_graph)
    print(degrees(undirected_graph))
    directed_graph = build_adjacency_list(E, directed=True)
    print(directed_graph)
    print(in_out_degree(directed_graph))

