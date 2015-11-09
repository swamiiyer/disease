import numpy, pandas, sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

def main(args):
    """
    Given a network-related string (say <prefix>), plots the prevalence 
    curves for the seven vaccination strategies, obtained from directories 
    with names starting with <prefix>, and saves the plot in a file called 
    <prefix>_prevalence_curves.pdf.
    """
    prefix = args[0]
    V = numpy.arange(0, 1.0, 0.01)
    R = {"BET" : [], "CLO" : [], "DEG" : [], "EIG" : [], "RAN" : [], 
         "REF" : [], "RWK" : []}
    P_indices = {"BET" : 0.0, "CLO" : 0.0, "DEG" : 0.0, "EIG" : 0.0, 
                 "RAN" : 0.0, "REF" : 0.0, "RWK" : 0.0}
    vstars = {"BET" : 0.0, "CLO" : 0.0, "DEG" : 0.0, "EIG" : 0.0, 
              "RAN" : 0.0, "REF" : 0.0, "RWK" : 0.0}
    for suffix in R.keys():
        lines = open("%s_%s/FILES" %(prefix, suffix), "r").readlines()
        for line in lines:
            try:
                data = pandas.read_table(line.strip(), header = None)
                tail = data.tail(1).values[0]
                R[suffix].append(round(tail[2], 3))
            except:
                print("Error: %s" %(line))
                R[suffix].append(0)
        auc = sum([0.01 * r for r in R[suffix]])
        P_indices[suffix] = round(auc, 3)
        epsilon = 1e-2
        vstar = 0.0
        for x in R[suffix]:
            if x > epsilon:
                vstar += 0.01
        vstars[suffix] = round(vstar, 3)

    print("%s P-index: %s" %(prefix, P_indices))
    print("%s vstar: %s" %(prefix, vstars))

    font_prop = font_manager.FontProperties(size = 8)
    plt.figure(1, figsize = (7, 4.5), dpi = 500)
    plt.xlabel(r"fraction vaccinated $v$", fontproperties = font_prop)
    plt.ylabel(r"prevalence $\pi$", fontproperties = font_prop)
    plt.plot(V, R["BET"], "b-", linewidth = 1, alpha = 0.6, 
             label = "betweenness")
    plt.plot(V, R["CLO"], "g-", linewidth = 1, alpha = 0.6, 
             label = "closeness")
    plt.plot(V, R["DEG"], "r-", linewidth = 1, alpha = 0.6, 
             label = "degree")
    plt.plot(V, R["EIG"], "c-", linewidth = 1, alpha = 0.6, 
             label = "eigenvector")
    plt.plot(V, R["RAN"], "m-", linewidth = 1, alpha = 0.6, 
             label = "random")
    plt.plot(V, R["REF"], "y-", linewidth = 1, alpha = 0.6, 
             label = "referral")
    plt.plot(V, R["RWK"], "k-", linewidth = 1, alpha = 0.6, 
             label = "random walk")
    plt.legend(loc = "upper right", prop = font_prop)
    plt.xlim(0, 1.0)
    plt.ylim(0, 1.0)

    labels = ["BET", "CLO", "DEG", "EIG", "RAN", "REF", "RWK"]
    inset = plt.axes([0.735, 0.45, 0.15, 0.15])
    P = [P_indices[label] for label in labels]
    xlocations = numpy.array(range(len(labels))) + 0.2
    width = 0.2
    plt.bar(xlocations, P, color = ["b", "g", "r", "c", "m", "y", "k"], 
              alpha = 0.6, width = width)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.xlim(0, xlocations[-1] + width * 2)
    plt.ylim(0, 0.5)
    plt.yticks((0, 0.25, 0.5), fontproperties = font_prop)
    plt.xlabel(r"strategy", fontproperties = font_prop)
    plt.ylabel(r"$\Pi$", fontproperties = font_prop)

    inset = plt.axes([0.735, 0.25, 0.15, 0.15])
    V = [vstars[label] for label in labels]
    xlocations = numpy.array(range(len(labels))) + 0.2
    width = 0.2
    plt.bar(xlocations, V, color = ["b", "g", "r", "c", "m", "y", "k"], 
              alpha = 0.6, width = width)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.xlim(0, xlocations[-1] + width * 2)
    plt.ylim(0, 1)
    plt.yticks((0, 0.5, 1), fontproperties = font_prop)
    plt.xlabel(r"strategy", fontproperties = font_prop)
    plt.ylabel(r"$v^\star$", fontproperties = font_prop)

    plt.savefig("%s_prevalence_curves.pdf" %(prefix), format = "pdf", bbox_inches = "tight")
    plt.close(1)

if __name__ == "__main__":
    main(sys.argv[1:])
