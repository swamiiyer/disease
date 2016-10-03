"""
Usage: python %(script_name)s <params file>

This script simulates disease dynamics on complex networks using the 
parameters specified in <params file>, and prints the time evolution of the 
final fractions (s, i, and r) of the susceptible, intected, and recovered 
individuals.
"""

import disease, json, networkx, numpy, operator, pickle, random, sys

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
    l = neighbors(G, i)
    return random.choice(l) if len(l) > 0 else None

def random_vaccination(population, v, attack_sequences, is_sequential):
    """
    Vaccinate v individuals from the population, at random.
    """
    for p in random.sample(range(len(G)), v):
        population[p] = VACCINATED

def random_walk_vaccination(population, v, attack_sequences, is_sequential):
    """
    Vaccinate v individuals from the population, by random walk.
    """
    RWK = attack_sequences["RWK_SEQ"] if is_sequential \
          else attack_sequences["RWK_SIM"]
    for i in range(v):
        population[RWK[i]] = VACCINATED

def referral_vaccination(population, v, attack_sequences, is_sequential):
    """
    Vaccinate v individuals from the population, by referral.
    """
    REF = attack_sequences["REF_SEQ"] if is_sequential \
          else attack_sequences["REF_SIM"]
    for i in range(v):
        population[REF[i]] = VACCINATED

def betweenness_vaccination(population, v, attack_sequences, is_sequential):
    """
    Vaccinate v individuals from the population, in reverse order 
    of betweenness centrality.
    """
    BET = attack_sequences["BET_SEQ"] if is_sequential \
          else attack_sequences["BET_SIM"]
    for i in range(v):
        population[BET[i]] = VACCINATED

def closeness_vaccination(population, v, attack_sequences, is_sequential):
    """
    Vaccinate v individuals from the population, in reverse order 
    of closeness centrality.
    """
    CLO = attack_sequences["CLO_SEQ"] if is_sequential \
          else attack_sequences["CLO_SIM"]
    for i in range(v):
        population[CLO[i]] = VACCINATED

def degree_vaccination(population, v, attack_sequences, is_sequential):
    """
    Vaccinate v individuals from the population, in reverse order 
    of degree centrality.
    """
    DEG = attack_sequences["DEG_SEQ"] if is_sequential \
          else attack_sequences["DEG_SIM"]
    for i in range(v):
        population[DEG[i]] = VACCINATED

def eigenvector_vaccination(population, v, attack_sequences, is_sequential):
    """
    Vaccinate v individuals from the population, in reverse order 
    of eigenvector centrality.
    """
    EIG = attack_sequences["EIG_SEQ"] if is_sequential \
          else attack_sequences["EIG_SIM"]
    for i in range(v):
        population[EIG[i]] = VACCINATED

def infection_probability(G, population, i, beta):
    """
    Return the probability that the specified individual i will be infected 
    by one of its infected neighbors.
    """
    infected_neighbors = numpy.in1d(population[neighbors(G, i)],
                                    INFECTED).sum()
    return 1 - (1 - beta) ** infected_neighbors

def extend(a, b):
    """
    Extend the smaller list to the size of the larger, using the last 
    element of the smaller list.
    """
    a_size = len(a)
    b_size = len(b)
    if a_size < b_size:
        a = numpy.append(a, [a[-1]] * (b_size - a_size))
    elif a_size > b_size:
        b = numpy.append(b, [b[-1]] * (a_size - b_size))
    return a, b

def single_trial(G, params, attack_sequences):
    """
    Carry out a single trial of the disease dynamics and return three lists 
    containing the fraction of susceptible, infected, and recovered 
    individuals at each time step.
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
        is_sequential = params["vaccination"]["is_sequential"]
        vaccination(population, v, attack_sequences, is_sequential)

    # Infect one susceptible individual at random. 
    while True:
        p = random.randint(0, n - 1)
        if population[p] == SUSCEPTIBLE:
            population[p] = INFECTED
            break

    S = numpy.array([n - v - 1], dtype = float)
    I = numpy.array([1], dtype = float)
    R = numpy.array([0], dtype = float)
    while True:
        s, i, r = S[-1], I[-1], R[-1]
        if i == 0:
            break
        for count in range(1, n + 1):
            idx = random.randint(0, n - 1)
            if population[idx] == SUSCEPTIBLE:
                p = infection_probability(G, population, idx, beta)
                if random.random() < p:
                    population[idx] = INFECTED
                    s -= 1
                    i += 1
            elif population[idx] == INFECTED:
                if random.random() < gamma:
                    population[idx] = RECOVERED
                    i -= 1
                    r += 1
            elif population[idx] == RECOVERED:
                pass
            elif population[idx] == VACCINATED:
                pass
        S = numpy.append(S, s)
        I = numpy.append(I, i)
        R = numpy.append(R, r)
    return S / n, I / n, R / n

def main(args):
    """
    Entry point.
    """
    if len(args) != 2:
        sys.exit(__doc__ %{"script_name" : args[0].split("/")[-1]})

    # Load the simulation parameters.
    params = json.load((open(args[1], "r")))
    network_params = params["network_params"]

    # Setup the network.
    G = networkx.read_graphml(network_params["args"]["path"])
    G = networkx.convert_node_labels_to_integers(G)

    # Load the attack sequences.
    fname = network_params["args"]["path"].replace(".graphml", ".pkl")
    attack_sequences = pickle.load(open(fname, "rb"))

    # Carry out the requested number of trials of the disease dynamics and 
    # compute basic statistics of the results.
    Sm, Im, Rm = numpy.array([0.0]), numpy.array([0.0]), numpy.array([0.0])
    for t in range(1, params["trials"] + 1):
        S, I, R = single_trial(G, params, attack_sequences)
        Sm, S = extend(Sm, S)
        Im, I = extend(Im, I)
        Rm, R = extend(Rm, R)
        Sm += (S - Sm) / t
        Im += (I - Im) / t
        Rm += (R - Rm) / t

    # Print the averaged results to STDOUT.
    for i in range(len(Sm)):
        print "%.3f\t%.3f\t%.3f" %(Sm[i], Im[i], Rm[i])

if __name__ == "__main__":
    main(sys.argv)
