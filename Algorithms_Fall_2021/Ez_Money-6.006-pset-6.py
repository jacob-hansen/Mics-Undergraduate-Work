import math

def ez_money(D):
    """
    Algorithm for finding negative weight loops in commodity exchange system. Hense: Ez Money

    Uses Johnson's Algorithm with overall runtime of O(V^3) where V is the number of commodities.


    Find a sequence of commodities to exchange to get more of that
    commodity.

    Args:
        D: A list of deals, each deal is of the form (A, x, B, y)
           which means someone will give you y of B for x of A.

    Returns:
        None if no such opputunity is found, otherwise a List of
        commodities to exchange.
    """
    graph, parents = make_graph(D)
    return find_path(graph, parents)

def make_graph(D):
    graph = {}
    parents = {}
    for trade in D:
        if trade[0] not in graph:
            graph[trade[0]] = {trade[2]: trade[3]/trade[1]}
            parents[trade[0]] = {trade[2]: [trade[0]]}
        else:
            graph[trade[0]][trade[2]] = trade[3]/trade[1]
            parents[trade[0]][trade[2]] = [trade[0]]
    return graph, parents


def find_path(Adj, parents):
    for i in range(len(Adj)): # relax all edges in (V - 1) rounds
        to_iter = Adj.keys()
        for u in to_iter: # loop over all edges (u, v)
            next_iter = list(Adj[u].keys())
            for v in next_iter: # relax edge from u to v
                test = relax(Adj, parents, u, v)
                if test:
                    return test
    return None

def relax(Adj, parents, u, v):
    if v in Adj:
        to_iter = Adj[v].keys()
        for next in to_iter:
            new_value = Adj[u][v]*Adj[v][next]
            if (next == u and new_value > 1):
                return parents[u][v]+parents[v][next]

            elif(next != u):
                Adj[u][next] = Adj[u][v]*Adj[v][next]
                parents[u][next] = parents[u][v]+parents[v][next]

        del Adj[u][v]
    return None


# a = ez_money([
#     ("laptop", 5, "TV", 3),
#     ("TV", 1, "shirt", 1),
#     ("shirt", 3, "laptop", 5),
#     ("phone", 5, "camera", 3),
#     ("camera", 1, "couch", 10),
#     ("couch", 3, "phone", 5),
# ])
# print(a)
