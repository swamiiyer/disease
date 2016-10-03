import igraph, networkx, pickle, operator, random, sys

def random_vertex(G):
    """ 
    Return a random vertex from G.
    """
    return random.choice(G.nodes())

def neighbors(G, i):
    """
    Return the neighbors of vertex i in G.
    """
    return G.neighbors(i)

def random_neighbor(G, i):
    """
    Return a random neighbor of vertex i in G.
    """
    l = neighbors(G, i)
    return random.choice(l) if len(l) > 0 else None

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
    vertices of the network must be removed using various (random walk, 
    referral, betweenness, closeness, degree, and eigenvector) attack 
    strategies and simultaneous and sequential attack modes. The orderings 
    are pickled in a file.
    """
    if len(args) != 1:
        sys.exit("Usage: python attack_sequence.py <graphml file>")

    ifname = args[0]
    G = networkx.read_graphml(ifname)
    G = networkx.convert_node_labels_to_integers(G)
    Vcount = len(G)

    # Random walk.
    print("Random walk (simultaneous) attack...")
    Gcopy = G.copy()
    RWK_SIM = []
    count = 0
    p = random_vertex(Gcopy)
    while count < Vcount:
        q = random_neighbor(Gcopy, p)
        if q == None:
            if p in RWK_SIM:
                continue
            else:
                RWK_SIM.append(p)
                count += 1
                p = random_vertex(Gcopy)
                continue
        else:
            p = q
            if q in RWK_SIM:
                continue
        RWK_SIM.append(p)
        count += 1
    print("Random walk (sequential) attack...")
    RWK_SEQ = []
    count = 0
    p = random_vertex(Gcopy)
    while count < Vcount:
        q = random_neighbor(Gcopy, p) if p in Gcopy else random_vertex(Gcopy)
        if q == None:
            if p in RWK_SEQ:
                continue
            else:
                RWK_SEQ.append(p)
                Gcopy.remove_node(p)                
                count += 1
                p = random_vertex(Gcopy)
                continue
        else:
            p = q
            if q in RWK_SEQ:
                continue
        RWK_SEQ.append(p)
        Gcopy.remove_node(p)                
        count += 1
    
    # Referral.
    print("Referral (simultaneous) attack...")
    Gcopy = G.copy()
    REF_SIM = []
    count = 0
    while count < Vcount:
        p = random_vertex(G)
        q = random_neighbor(G, p)
        if q == None:
            if not p in REF_SIM:
                REF_SIM.append(p)
                count += 1
        else:
            if not q in REF_SIM:
                REF_SIM.append(q)
                count += 1    
    print("Referral (sequential) attack...")
    REF_SEQ = []
    count = 0
    while count < Vcount:
        p = random_vertex(G)
        q = random_neighbor(G, p)
        if q == None:
            if not p in REF_SEQ:
                REF_SEQ.append(p)
                Gcopy.remove_node(p)
                count += 1
        else:
            if not q in REF_SEQ:
                REF_SEQ.append(q)
                Gcopy.remove_node(q)
                count += 1    

    # Betweenness.
    print("Betweenness (simultaneous) attack...")
    Gcopy = G.copy()
    V = sorted(networkx.betweenness_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    BET_SIM = [a for a, b in V]
    print("Betweenness (sequential) attack...")
    BET_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        BET_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(networkx.betweenness_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)
    
    # Closeness.
    print("Closeness (simultaneous) attack...")
    Gcopy = G.copy()
    V = sorted(networkx.closeness_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    CLO_SIM = [a for a, b in V]
    print("Closeness (sequential) attack...")
    CLO_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        CLO_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(networkx.closeness_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)

    # Degree.
    print("Degree (simultaneous) attack...")
    Gcopy = G.copy()
    V = sorted(networkx.degree_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    DEG_SIM = [a for a, b in V]
    print("Degree (sequential) attack...")
    DEG_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        DEG_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(networkx.degree_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)

    # Eigenvector.
    print("Eigenvector (simultaneous) attack...")
    Gcopy = G.copy()
    V = sorted(eigenvector_centrality(Gcopy).items(), 
               key = operator.itemgetter(1), reverse = True)
    EIG_SIM = [a for a, b in V]
    print("Eigenvector (sequential) attack...")
    EIG_SEQ = []
    for i in range(1, Vcount - 1):
        v = V.pop(0)[0]
        EIG_SEQ.append(v)
        Gcopy.remove_node(v)
        V = sorted(eigenvector_centrality(Gcopy).items(), 
                   key = operator.itemgetter(1), reverse = True)
    
    # Pickle the centralities.
    ofname = ifname.replace(".graphml", ".pkl")
    outfile = open(ofname, "wb")
    attack_sequences = {"RWK_SIM" : RWK_SIM,
                        "RWK_SEQ" : RWK_SEQ,
                        "REF_SIM" : REF_SIM,
                        "REF_SEQ" : REF_SEQ,
                        "BET_SIM" : BET_SIM,
                        "BET_SEQ" : BET_SEQ,
                        "CLO_SIM" : CLO_SIM,
                        "CLO_SEQ" : CLO_SEQ,
                        "DEG_SIM" : DEG_SIM,
                        "DEG_SEQ" : DEG_SEQ,
                        "EIG_SIM" : EIG_SIM,
                        "EIG_SEQ" : EIG_SEQ}
    pickle.dump(attack_sequences, outfile)
    outfile.close()
        
if __name__ == "__main__":
    main(sys.argv[1:])
