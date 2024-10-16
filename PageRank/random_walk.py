import networkx as nx
import random
import numpy as np


def add_edges(G, p):
    # add edges with probability 'p/
    for i in G.nodes():
        for j in G.nodes():
            if i == j:
                continue
            r = random.random()
            if r <= p:
                G.add_edge(i, j)
    return G


def random_walk(G):
    nodes = G.nodes()
    nodes = np.array(nodes)
    points = [0 for _ in range(G.number_of_nodes())]

    # Start from a random node
    random_node = nodes[random.randint(0, len(nodes) - 1)]
    points[random_node] += 1
    out = G.out_edges(random_node)

    c = 0
    while c != 100000:  # We'll have this many iterations of the random walk
        if len(out) == 0:
            # Teleport to a random node if the current node is a sink
            next_node = random.choice(nodes)
        else:
            # Extract target nodes from the out_edges
            target_nodes = [t for _, t in out]
            next_node = random.choice(target_nodes)

        points[next_node] += 1
        out = G.out_edges(next_node)
        c += 1

    return points

def sort_by_points(points):
    points_array = np.array(points)
    sorted_nodes = np.argsort(-points_array)  # to sort in dec order (we need nodes which has high points first)
    return sorted_nodes

def start():
    # create a directed graph with 'n' nodes
    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(10)])
    G = add_edges(G, 0.3)

    # Preform a random walk
    points = random_walk(G)

    # get nodes ranking as per the points accumulated
    print("FINAL ARRAY OF POINTS: ", points)
    sorted_nodes = sort_by_points(points)
    print("NODES RANKING: ", sorted_nodes)

    # compare the ranks obtained with the ranks from the inbuilt
    page_rank = nx.pagerank(G)
    page_rank_array = [value for key, value in page_rank.items()]
    page_rank_array = np.array(page_rank_array)
    sorted_page_rank = np.argsort(-page_rank_array)
    print("PAGE RANK: ", sorted_page_rank)


if __name__ == '__main__':
    start()
