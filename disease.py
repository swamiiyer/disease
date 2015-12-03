import disease, json, networkx, numpy, operator, random, sys

# Each individual in the population belongs to one of the following states.
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
VACCINATED = 3

# Memoize betweenness, closeness, degree, and eigenvector centrality
# calculations
BET, CLO, DEG, EIG = None, None, None, None

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

def random_vaccination(G, population, v):
    """
    Vaccinate v individuals from the population, at random.
    """
    for p in random.sample(range(len(G)), v):
        population[p] = VACCINATED

def random_walk_vaccination(G, population, v):
    """
    Vaccinate min(n, v) individuals from the population, by performing a 
    random walk on the largest component (size n) of the graph G, starting 
    at a random vertex.
    """
    Gsub = networkx.connected_component_subgraphs(G).next()
    v = min(len(Gsub), v)
    count = 0
    p = random_vertex(Gsub)
    while count < v:
        if population[p] != VACCINATED:
            population[p] = VACCINATED
            count += 1
        else:
            p = random_neighbor(Gsub, p)

def page_rank_vaccination(G, population, v, r = 0.9):
    """
    Vaccinate v individuals from the population, by performing a 
    random walk on G, starting at a random vertex as the current individual, 
    and using the 90-10 rule: with probability r vaccinate a random neighbor 
    of the current individual, and with probability 1 - r vaccinate a random 
    individual from the population and continue the random walk from the 
    corresponding vertex.
    """
    count = 0
    p = random_vertex(G)
    while count < v:
        if population[p] != VACCINATED:
            population[p] = VACCINATED
            count += 1
        else:
            if random.random() < r:
                p = random_neighbor(G, p)
            else:
                p = random_vertex(G)

def referral_vaccination(G, population, v):
    """
    Vaccinate v individuals from the population, by referral.
    """
    count = 0
    while count < v:
        p = random_vertex(G)
        q = random_neighbor(G, p)
        if q == None:
            continue
        if population[q] != VACCINATED:
            population[q] = VACCINATED
            count += 1

def betweenness_vaccination(G, population, v):
    """
    Vaccinate v individuals from the population, in reverse order 
    of betweenness centrality.
    """
    global BET
    if BET == None:
        BET = sorted(networkx.betweenness_centrality(G).items(), 
                     key = operator.itemgetter(1), reverse = True)
    for i in range(v):
        population[BET[i][0]] = VACCINATED

def closeness_vaccination(G, population, v):
    """
    Vaccinate v individuals from the population, in reverse order 
    of closeness centrality.
    """
    global CLO
    if CLO == None:
        CLO = sorted(networkx.closeness_centrality(G).items(), 
                     key = operator.itemgetter(1), reverse = True)
    for i in range(v):
        population[CLO[i][0]] = VACCINATED

def degree_vaccination(G, population, v):
    """
    Vaccinate v individuals from the population, in reverse order 
    of degree centrality.
    """
    global DEG
    if DEG == None:
        DEG = sorted(networkx.degree_centrality(G).items(), 
                     key = operator.itemgetter(1), reverse = True)
    for i in range(v):
        population[DEG[i][0]] = VACCINATED

def eigenvector_vaccination(G, population, v):
    """
    Vaccinate v individuals from the population, in reverse order 
    of eigenvector centrality.
    """
    global EIG
    if EIG == None:
        EIG = sorted(networkx.eigenvector_centrality(G).items(), 
                     key = operator.itemgetter(1), reverse = True)
    for i in range(v):
        population[EIG[i][0]] = VACCINATED

def infection_probability(G, population, i, beta):
    """
    Return the probability that the specified individual i will be infected 
    by one of its infected neighbors.
    """
    infected_neighbors = numpy.in1d(population[neighbors(G, i)], INFECTED).sum()
    return 1 - (1 - beta) ** infected_neighbors

def single_trial(G, params):
    """
    Carry out a single trial of the disease dynamics and return the fraction 
    of susceptible, infected, and recovered individuals at the last time step.
    """

    # Pick a random value from (0, 1) for beta and gamma if they are None.
    beta = random.random() if params["beta"] == None else params["beta"]
    gamma = random.random() if params["gamma"] == None else params["gamma"]
    
    # Create a population of n susceptible individuals.
    n = len(G)
    population = numpy.repeat([SUSCEPTIBLE], [n])

    # Carry out vaccinations if requested.
    v = 0
    if params["vaccination"] != None:
        strategy = params["vaccination"]["strategy"]
        v = int(params["vaccination"]["fraction"] * n)
        vaccination = getattr(disease, strategy)
        if strategy == "page_rank_vaccination" and "r" in params["vaccination"]:
            r = float(params["vaccination"]["r"])
            vaccination(G, population, v, r)
        else:
            vaccination(G, population, v)

    # Infect one susceptible individual at random. 
    while True:
        p = random.randint(0, n - 1)
        if population[p] == SUSCEPTIBLE:
            population[p] = INFECTED
            break

    S, I, R = n - v - 1, 1, 0
    while True:
        if I == 0:
            break
        for count in range(1, n + 1):
            idx = random.randint(0, n - 1)
            if population[idx] == SUSCEPTIBLE:
                p = infection_probability(G, population, idx, beta)
                if random.random() < p:
                    population[idx] = INFECTED
                    S -= 1
                    I += 1
            elif population[idx] == INFECTED:
                if random.random() < gamma:
                    population[idx] = RECOVERED
                    I -= 1
                    R += 1
            elif population[idx] == RECOVERED:
                pass
            elif population[idx] == VACCINATED:
                pass
    return 1.0 * S / n, 1.0 * I / n, 1.0 * R / n

def main(args):
    """
    Entry point.
    """
    if len(args) == 0:
        print "Usage: python disease.py <params file>"
        sys.exit(1)

    # Load the simulation parameters.
    params = json.load((open(args[0], "r")))
    network_params = params["network_params"]

    # Setup the network.
    if network_params["name"] == "read_graphml":
        G = networkx.read_graphml(network_params["args"]["path"])
        G = networkx.convert_node_labels_to_integers(G)
    else:
        G = getattr(networkx, network_params["name"])(**network_params["args"])

    # Carry out the requested number of trials of the disease dynamics and 
    # average the results.
    Sm, Im, Rm, Rv = 0.0, 0.0, 0.0, 0.0
    for t in range(1, params["trials"] + 1):
        S, I, R = single_trial(G, params)
        Rm_prev = Rm
        Sm += (S - Sm) / t
        Im += (I - Im) / t
        Rm += (R - Rm) / t
        Rv += (R - Rm) * (R - Rm_prev)

    # Print the average
    print("%.3f\t%.3f\t%.3f\t%.3f" \
          %(Sm, Im, Rm, (Rv / params["trials"]) ** 0.5))

if __name__ == "__main__":
    main(sys.argv[1:])
