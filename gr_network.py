import igraph, networkx, sys

# This script generates an exponential (growing random) network with n
# vertices and mean degree k, and saves it in graphml format.

def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: python gr_network.py <n> <k>')
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    m = k / 2
    g = igraph.Graph.Growing_Random(n, m, citation = True)
    g.write_graphml('gr%d.graphml' %(k))
    g = networkx.Graph(networkx.read_graphml('gr%d.graphml' %(k)))
    g = networkx.convert_node_labels_to_integers(g)
    networkx.write_graphml(g, 'gr%d.graphml' %(k))

if __name__ == '__main__':
    main()
