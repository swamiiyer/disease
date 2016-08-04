import igraph, networkx, pickle, operator, sys

def eigenvector_centrality(G):
    """
    Returns a map that maps a vertex id to the eigenvector centrality of 
    that vertex, calculated using igraph.
    """
    tempG = igraph.Graph()
    tempG.add_vertices([str(v) for v in G.nodes()])
    tempG.add_edges([(str(u), str(v)) for u, v in G.edges()])
    return {int(tempG.vs[i]["name"]): v for i, v in 
            enumerate(tempG.eigenvector_centrality())}

def main(args):
    """
    Reads in a network in GraphML format, computes the order in which the 
    vertices of the network must be removed using various (betweenness, 
    closeness, degree, and eigenvector) attack strategies and simultaneous 
    and sequential attack modes. The orderings are pickled in a file.
    """

    if len(args) != 1:
        sys.exit("Usage: python centralities.py <graphml file>")

    ifname = args[0]
    G = networkx.read_graphml(ifname)
    G = networkx.convert_node_labels_to_integers(G)
    Vcount = len(G)

    # Betweenness.
    print("Betweenness attack...")
    Gcopy = G.copy()
    V = sorted(networkx.betweenness_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    BET_SIM = [a for a, b in V]
    BET_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        BET_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(networkx.betweenness_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)
    
    # Closeness.
    print("Closeness attack...")
    Gcopy = G.copy()
    V = sorted(networkx.closeness_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    CLO_SIM = [a for a, b in V]
    CLO_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        CLO_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(networkx.closeness_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)

    # Degree.
    print("Degree attack...")
    Gcopy = G.copy()
    V = sorted(networkx.degree_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    DEG_SIM = [a for a, b in V]
    DEG_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        DEG_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(networkx.degree_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)

    # Eigenvector.
    print("Eigenvector attack...")
    Gcopy = G.copy()
    V = sorted(eigenvector_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    EIG_SIM = [a for a, b in V]
    EIG_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        EIG_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(eigenvector_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)
    
    # Pickle the centralities.
    ofname = ifname.replace(".graphml", ".centralities")
    outfile = open(ofname, "wb")
    centralities = {"BET_SIM" : BET_SIM,
                    "BET_SEQ" : BET_SEQ,
                    "CLO_SIM" : CLO_SIM,
                    "CLO_SEQ" : CLO_SEQ,
                    "DEG_SIM" : DEG_SIM,
                    "DEG_SEQ" : DEG_SEQ,
                    "EIG_SIM" : EIG_SIM,
                    "EIG_SEQ" : EIG_SEQ}
    pickle.dump(centralities, outfile)
    outfile.close()
        
if __name__ == "__main__":
    main(sys.argv[1:])
