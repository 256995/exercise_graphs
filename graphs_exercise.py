import copy

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


def dfs(graph, start):
    """
    Finds all vertices reachable from the start
    :param graph: adjacency list od a graph (undirected or directed)
    :param start: the starting vertex
    :return: list[str], the vertices reachable from start, in the order you first visit them.
    """
    actual_node = start
    visited = [start] # a set of all visited vertices
    walk = [start] # saving every step I take, so that I can determine, where to get back, when stuck
    while True:
        unvisited_neighbours = [neighbour for neighbour in graph[actual_node] if neighbour not in visited]
        if not unvisited_neighbours: # the case, when I'm stuck
            if actual_node == start: # end the search
                break
            else: # return to the node I initially came here from (using walk)
                idx = walk.index(actual_node) # return the index of the first occurrence of actual_node in the walk
                actual_node = walk[idx-1]
                walk.append(actual_node)
        else:
            unvisited_neighbours.sort()
            actual_node = unvisited_neighbours[0] # move to the alphabetically first unvisited neighbour
            walk.append(actual_node)
            visited.append(actual_node)
    return visited


def connected_components(graph):
    connected_comp =[]
    remaining_vertices = set(graph.keys()) # the vertices, that are not yet in any connected component
    while remaining_vertices:
        start = remaining_vertices.pop()
        component = set(dfs(graph, start))
        connected_comp.append(component) # add the connected component to the list of all connected components
        remaining_vertices = remaining_vertices - component
    return connected_comp


def is_weakly_connected(graph):
    shadow_graph = copy.deepcopy(graph)
    for vertex in graph:
        for destination in graph[vertex]:
            shadow_graph[destination].append(vertex)
    components = connected_components(shadow_graph)
    if len(components) == 1:
        return True
    else:
        return False


def eulerian_type(graph, directed=False):
    result = 'none'
    if directed: # directed
        if is_weakly_connected(graph):
            in_deg, out_deg = in_out_degree(graph)
            deg_plus = 0
            deg_minus = 0
            for node in in_deg:
                if in_deg[node] == out_deg[node]:
                    continue
                elif in_deg[node] == out_deg[node] + 1:
                    deg_plus += 1
                    continue
                elif in_deg[node] == out_deg[node] - 1:
                    deg_minus += 1
                    continue
                else:
                    return result
            if (deg_minus == 0) and (deg_plus == 0):
                result = 'circuit'
            elif (deg_plus == 1) and (deg_minus == 1):
                result = 'path'
            print(in_deg, out_deg)
    else: # undirected
        if len(connected_components(graph)) == 1:
            degrees_dict = degrees(graph)
            odd_deg = 0
            for node in degrees_dict:
                if (degrees_dict[node] % 2) == 1:
                    odd_deg += 1
            if odd_deg == 0:
                result = 'circuit'
            elif odd_deg == 2:
                result = 'path'
            print(degrees_dict, odd_deg)
    return result


if __name__ == "__main__":



    # TASK 1
    print("--- Task 1 ---")
    E = [('P1', 'P2'), ('P1', 'P3'), ('P2', 'P3'), ('P3', 'P4'), ('P4', 'P5')]
    undirected_graph = build_adjacency_list(E)
    print(undirected_graph)
    print(degrees(undirected_graph))
    directed_graph = build_adjacency_list(E, directed=True)
    print(directed_graph)
    print(in_out_degree(directed_graph))

    # TASK 3
    print("--- Task 3 ---")
    E1 = [('A', 'D'), ('A', 'I'), ('B', 'D'), ('B', 'F'), ('B', 'G'), ('B', 'I'), ('C', 'E'), ('C', 'H'), ('C', 'J'), ('C', 'K'), ('D', 'F'), ('D', 'G'), ('E', 'J'), ('H', 'J'), ('J', 'K')]
    G1 = build_adjacency_list(E1)
    print('G1 from A: ', dfs(G1, 'A'))
    print('G1 from C: ', dfs(G1, 'C'))
    E2 = [('P', 'Q'), ('Q', 'R'), ('R', 'P'), ('R', 'S'), ('T', 'S')]
    G2 = build_adjacency_list(E2, directed=True)
    print('G2 from P: ', dfs(G2, 'P'))
    print('G2 from S: ', dfs(G2, 'S'))
    print('G2 from T: ', dfs(G2, 'T'))
    print('Connected components of G1: ', connected_components(G1))
    print('Is the G2 weakly connected? ', is_weakly_connected(G2))

    ## TASK 4
    print(G2)
    G22 = build_adjacency_list(E2, directed=False)
    print('G2 Eulerian type:', eulerian_type(G2, directed=True))
    print('G2 Eulerian type:', eulerian_type(G22, directed=False))
    print('G1 Eulerian type:', eulerian_type(G1, directed=True))



