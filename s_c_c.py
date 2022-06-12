import networkx as nx


def filter_big_scc(g, edges_to_be_removed):
    # Given a graph g and edges to be removed
    # Return a list of big scc subgraphs (# of nodes >= 2)
    g.remove_edges_from(edges_to_be_removed)
    sub_graphs = filter(lambda scc: scc.number_of_nodes() >= 2,
                        [g.subgraph(c) for c in nx.strongly_connected_components(g)])
    return sub_graphs


def get_big_sccs(g):
    self_loop_edges = nx.selfloop_edges(g)
    g.remove_edges_from(nx.selfloop_edges(g))
    num_big_sccs = 0
    edges_to_be_removed = []
    big_sccs = []
    # strongly_connected_component_subgraphs = [g.subgraph(c) for c in nx.strongly_connected_components(g)]

    # for sub in strongly_connected_component_subgraphs:
    for c in nx.strongly_connected_components(g):
        sub = g.subgraph(c)
        if sub.number_of_nodes() >= 2:
            # strongly connected components
            big_sccs.append(nx.DiGraph(sub))
    return big_sccs


def nodes_in_scc(sccs):
    scc_nodes = []
    scc_edges = []
    for scc in sccs:
        scc_nodes += list(scc.nodes())
        scc_edges += list(scc.edges())

    # print("# nodes in big sccs: %d" % len(scc_nodes))
    # print("# edges in big sccs: %d" % len(scc_edges))
    return scc_nodes


def scc_nodes_edges(g):
    scc_nodes = set()
    scc_edges = set()
    num_big_sccs = 0
    num_nodes_biggest_scc = 0
    biggest_scc = None
    for c in nx.strongly_connected_components(g):
        sub = g.subgraph(c)
        number_nodes = sub.number_of_nodes()
        if sub.number_of_nodes() >= 2:
            scc_nodes.update(sub.nodes())
            scc_edges.update(sub.edges())
            num_big_sccs += 1
            if num_nodes_biggest_scc < number_nodes:
                num_nodes_biggest_scc = number_nodes
                biggest_scc = sub
    nonscc_nodes = set(g.nodes()) - scc_nodes
    nonscc_edges = set(g.edges()) - scc_edges
    print(num_nodes_biggest_scc)
    print(f"num of big sccs: {int(num_big_sccs)}")
    if biggest_scc is None:
        return scc_nodes, scc_nodes, nonscc_nodes, nonscc_edges
    print(f"# nodes in biggest scc: {biggest_scc.number_of_nodes()}, # edges in biggest scc: {biggest_scc.number_of_edges()}")
    print(f"# nodes, edges in scc: ({len(scc_nodes)}, {len(scc_edges)}), # nodes, edges in non-scc: ({len(nonscc_nodes)}, {len(nonscc_edges)})")
    num_of_nodes = g.number_of_nodes()
    num_of_edges = g.number_of_edges()
    print(
        f"# nodes in graph: {num_of_nodes}, # of edges in graph: {num_of_edges}, "
        f"percentage nodes, edges in scc: ({len(scc_nodes) * 1.0 / num_of_nodes:0.4f}, {len(scc_edges) * 1.0 / num_of_edges: 0.4f}), "
        f"percentage nodes, edges in non-scc: ({len(nonscc_nodes) * 1.0 / num_of_nodes:0.4f}, {len(nonscc_edges) * 1.0 / num_of_edges:0.4f})")
    return scc_nodes, scc_edges, nonscc_nodes, nonscc_edges


def c_c(graph_file):
    g = nx.read_edgelist(graph_file, create_using=nx.Graph(), nodetype=int)
    graphs = nx.connected_component_subgraphs(g)
    for graph in graphs:
        print(graph.number_of_nodes(), graph.number_of_edges())
    print(len(graphs))
