import disease, json, networkx, numpy, operator, random, sys

# Each individual in the population belongs to one of the following states.
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2
VACCINATED = 3

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
    return random.choice(neighbors(G, i))

def random_vaccination(G, population, fraction):
    """
    Try to vaccinate a specified fraction of the population at random and 
    return the number of vaccinations actually administered.
    """
    v = 0
    for i in range(int(fraction * len(population))):
        p = random_vertex(G)
        if population[p] != VACCINATED:
            population[p] = VACCINATED
            v += 1
    return v

def degree_vaccination(G, population, fraction):
    """
    Try to vaccinate a specified fraction of the population in reverse order 
    of degree and return the number of vaccinations actually administered.
    """
    v = 0
    L = sorted(networkx.degree_centrality(G).items(), 
               key = operator.itemgetter(1), reverse = True)
    for i in range(int(fraction * len(population))):
        population[L[i][0]] = VACCINATED
        v += 1
    return v

def referral_vaccination(G, population, fraction):
    """
    Try to vaccinate a specified fraction of the population by referral and 
    return the number of vaccinations actually administered.
    """
    v = 0
    for i in range(int(fraction * len(population))):
        p = random_vertex(G)
        q = random_neighbor(G, p)
        if population[q] != VACCINATED:
            population[q] = VACCINATED
            v += 1
    return v

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
        fraction = params["vaccination"]["fraction"]
        vaccination = getattr(disease, strategy)
        v = vaccination(G, population, fraction)

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
    if network_params["name"] == "read_graphml":
        network_params["args"]["node_type"] = int

    # Setup the network.
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
