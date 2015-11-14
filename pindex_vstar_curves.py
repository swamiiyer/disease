import numpy, pandas, sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

def main(args):
    """
    Given a network-related string (say <prefix>), plots the P-index
    and vaccination threshold curves for the seven vaccination strategies, 
    obtained from directories with names starting with <prefix>, and saves 
    the plots in files called <prefix>_pindex_curves.pdf and 
    <prefix>_vstar_curves.pdf
    """
    prefix = args[0]
    K = range(10, 32, 2)
    P_indices = {"BET" : [], "CLO" : [], "DEG" : [], "EIG" : [], "RAN" : [], 
                 "REF" : [], "RWK" : []}
    vstars = {"BET" : [], "CLO" : [], "DEG" : [], "EIG" : [], "RAN" : [], 
              "REF" : [], "RWK" : []}
    for k in K:
        for suffix in P_indices.keys():
            R = []
            lines = open("%s_%d_%s/FILES" %(prefix, k, suffix), 
                         "r").readlines()
            for line in lines:
                try:
                    data = pandas.read_table(line.strip(), header = None)
                    tail = data.tail(1).values[0]
                    R.append(round(tail[2], 3))
                except:
                    print("Error: %s" %(line))
                    R.append(0)
            auc = sum([0.01 * r for r in R])
            P_indices[suffix].append(round(auc, 3))
            epsilon = 1e-2
            vstar = 0.0
            for x in R:
                if x > epsilon:
                    vstar += 0.01
            vstars[suffix].append(round(vstar, 3))

    font_prop = font_manager.FontProperties(size = 8)

    plt.figure(1, figsize = (7, 4.5), dpi = 500)
    plt.xlabel(r"mean degree $k$", fontproperties = font_prop)
    plt.ylabel(r"prevalence index $\Pi$", fontproperties = font_prop)
    plt.plot(K, P_indices["BET"], "b.", linewidth = 2, alpha = 0.6)
    plt.plot(K, P_indices["BET"], "b-", linewidth = 1, alpha = 0.6, 
             label = "betweenness")
    plt.plot(K, P_indices["CLO"], "g.", linewidth = 2, alpha = 0.6)
    plt.plot(K, P_indices["CLO"], "g-", linewidth = 1, alpha = 0.6, 
             label = "closeness")
    plt.plot(K, P_indices["DEG"], "r.", linewidth = 2, alpha = 0.6)
    plt.plot(K, P_indices["DEG"], "r-", linewidth = 1, alpha = 0.6, 
             label = "degree")
    plt.plot(K, P_indices["EIG"], "c.", linewidth = 2, alpha = 0.6)
    plt.plot(K, P_indices["EIG"], "c-", linewidth = 1, alpha = 0.6, 
             label = "eigenvector")
    plt.plot(K, P_indices["RAN"], "m.", linewidth = 2, alpha = 0.6)
    plt.plot(K, P_indices["RAN"], "m-", linewidth = 1, alpha = 0.6, 
             label = "random")
    plt.plot(K, P_indices["REF"], "y.", linewidth = 2, alpha = 0.6)
    plt.plot(K, P_indices["REF"], "y-", linewidth = 1, alpha = 0.6, 
             label = "referral")
    plt.plot(K, P_indices["RWK"], "k.", linewidth = 2, alpha = 0.6)
    plt.plot(K, P_indices["RWK"], "k-", linewidth = 1, alpha = 0.6, 
             label = "random walk")
    plt.legend(loc = "best", prop = font_prop)
    plt.xlim(8, 32)
    plt.ylim(0, 1.0)
    plt.savefig("%s_pindex_curves.pdf" %(prefix), format = "pdf", 
                bbox_inches = "tight")
    plt.close(1)

    plt.figure(2, figsize = (7, 4.5), dpi = 500)
    plt.xlabel(r"mean degree $k$", fontproperties = font_prop)
    plt.ylabel(r"vaccination threshold $v^\star$", fontproperties = font_prop)
    plt.plot(K, vstars["BET"], "b.", linewidth = 2, alpha = 0.6)
    plt.plot(K, vstars["BET"], "b-", linewidth = 1, alpha = 0.6, 
             label = "betweenness")
    plt.plot(K, vstars["CLO"], "g.", linewidth = 2, alpha = 0.6)
    plt.plot(K, vstars["CLO"], "g-", linewidth = 1, alpha = 0.6, 
             label = "closeness")
    plt.plot(K, vstars["DEG"], "r.", linewidth = 2, alpha = 0.6)
    plt.plot(K, vstars["DEG"], "r-", linewidth = 1, alpha = 0.6, 
             label = "degree")
    plt.plot(K, vstars["EIG"], "c.", linewidth = 2, alpha = 0.6)
    plt.plot(K, vstars["EIG"], "c-", linewidth = 1, alpha = 0.6, 
             label = "eigenvector")
    plt.plot(K, vstars["RAN"], "m.", linewidth = 2, alpha = 0.6)
    plt.plot(K, vstars["RAN"], "m-", linewidth = 1, alpha = 0.6, 
             label = "random")
    plt.plot(K, vstars["REF"], "y.", linewidth = 2, alpha = 0.6)
    plt.plot(K, vstars["REF"], "y-", linewidth = 1, alpha = 0.6, 
             label = "referral")
    plt.plot(K, vstars["RWK"], "k.", linewidth = 2, alpha = 0.6)
    plt.plot(K, vstars["RWK"], "k-", linewidth = 1, alpha = 0.6, 
             label = "random walk")
    plt.legend(loc = "best", prop = font_prop)
    plt.xlim(8, 32)
    plt.ylim(0, 1.0)
    plt.savefig("%s_vstar_curves.pdf" %(prefix), format = "pdf", 
                bbox_inches = "tight")
    plt.close(2)

if __name__ == "__main__":
    main(sys.argv[1:])
