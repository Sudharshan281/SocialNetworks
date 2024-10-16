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


def initialize_points(G):
    points = [100 for i in range(G.number_of_nodes())]
    return points


def distribute_points(G, points):
    prev_points = points
    new_points = [0 for i in range(G.number_of_nodes())]

    for i in G.nodes():
        out = G.out_edges(i)
        if len(out) == 0:
            new_points[i] += prev_points[i]
        else:
            share = float(prev_points[i]) / len(out)
            for each in out:  # [i, neighbour]
                new_points[each[1]] += share
    return G, new_points


def keep_distributing_points(G, points):
    prev_points = points
    print("Enter 0 to stop")
    ch = '1'
    while ch != '0':
        G, new_points = distribute_points(G, prev_points)
        print(new_points)
        for i in range(len(points)):
            points[i] = 0.8*points[i]
        for i in range(len(points)):
            points[i] += 20    # 20% of total points distributed uniformly to all nodes (n*100*.02)/n
        ch = input()
        prev_points = new_points
    return G, prev_points


def sort_by_points(points):
    points_array = np.array(points)
    sorted_nodes = np.argsort(-points_array)  # to sort in dec order (we need nodes which has high points first)
    return sorted_nodes

def start():
    # create a directed graph with 'n' nodes
    G = nx.DiGraph()
    G.add_nodes_from([i for i in range(10)])
    G = add_edges(G, 0.3)

    # assign 100 points to each nodes
    points = initialize_points(G)
    print("INITIAL POINTS: ", points)

    # keep distributing points until convergence
    G, points = keep_distributing_points(G, points)

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
