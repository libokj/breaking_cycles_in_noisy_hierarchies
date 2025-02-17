import argparse
import random
from time import time

import networkx as nx
from trueskill import Rating, rate_1vs1

from measures import measure_pairs_agreement
from s_c_c import scc_nodes_edges


def compute_trueskill(pairs, players):
    if not players:
        for u, v in pairs:
            if u not in players:
                players[u] = Rating()
            if v not in players:
                players[v] = Rating()

    start = time()
    random.shuffle(pairs)
    for u, v in pairs:
        players[v], players[u] = rate_1vs1(players[v], players[u])

    end = time()
    print(f"time used in computing true skill (per iteration): {(end - start):0.4f} s")
    return players


def get_players_score(players, n_sigma):
    relative_score = {}
    for k, v in players.items():
        relative_score[k] = players[k].mu - n_sigma * players[k].sigma
    return relative_score


def trueskill_ratings(pairs, iter_times=15, n_sigma=3, threshold=0.85):
    start = time()
    players = {}
    for i in range(iter_times):
        # print("========= Trueskill iteration times: %d =========" % (i + 1))
        players = compute_trueskill(pairs, players)
        relative_scores = get_players_score(players, n_sigma=n_sigma)
        accu = measure_pairs_agreement(pairs, relative_scores)
        # print("agreement of pairs: %0.4f" % accu)
        if accu >= threshold:
            return relative_scores
    end = time()
    time_used = end - start
    print(f"time used in computing true skill: {time_used:0.4f} s, iteration time is: {i + 1}")
    return relative_scores


def graphbased_trueskill(g, iter_times=15, n_sigma=3, threshold=0.95):
    relative_scores = trueskill_ratings(list(g.edges()), iter_times=iter_times, n_sigma=n_sigma, threshold=threshold)
    scc_nodes, scc_edges, nonscc_nodes, nonscc_edges = scc_nodes_edges(g)
    print("----scc-------")
    scc_accu = measure_pairs_agreement(scc_edges, relative_scores)
    print("----non-scc---")
    nonscc_accu = measure_pairs_agreement(nonscc_edges, relative_scores)
    print(f"scc accu: {scc_accu:0.4f}, nonscc accu: {nonscc_accu:0.4f}")
    return relative_scores


def main(edges_file_name="/home/sunjiank/Dropbox/Data/cit-Patents/cit-Patents.txt"):
    g = nx.read_edgelist(edges_file_name, create_using=nx.DiGraph(), nodetype=int)
    graphbased_trueskill(g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--graph", type=str, default=" ", help="graph edges list file")
    args = parser.parse_args()
    edges_file_name = args.graph
    # main(edges_file_name = "/home/sunjiank/Dropbox/Data/cit-Patents/cit-Patents.txt")
    # main(edges_file_name = "/home/sunjiank/Dropbox/Codes/question_difficulty_estimation/dataset/Java/competition_graph.edges")
    main(edges_file_name)
