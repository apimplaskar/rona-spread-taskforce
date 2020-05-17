def generic_bfs_edges(G, source, neighbors=None, depth_limit=None, prob = 0.5):
    visited = {source}
    if depth_limit is None:
        depth_limit = len(G)
    queue = deque([(source, depth_limit, neighbors(source))])
    while queue:
        parent, depth_now, children = queue[0]
        try:
            child = next(children)
            p = np.random.uniform(0,1)
            if child not in visited and p < prob:
                yield parent, child
                visited.add(child)
                if depth_now > 1:
                    queue.append((child, depth_now - 1, neighbors(child)))
        except StopIteration:
            queue.popleft()


# Modifying networkx source code to add probability of edge traversal 
def bfs_edges(G, source, reverse=False, depth_limit=None, prob=0.2):
    if reverse and G.is_directed():
        for i in G.predecessors:
            p = np.random.uniform(0,1)
            if p < prob: 
                successors.append(i)
    else:
        successors = G.neighbors
    # TODO In Python 3.3+, this should be `yield from ...`
    for e in generic_bfs_edges(G, source, successors, depth_limit):
        yield e

def getInfected(edges):
    edges = list(edges)
    nodes = []
    for i in edges:
        nodes.append(i[1])
    return nodes
