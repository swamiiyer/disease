import pandas, pylab, sys
import matplotlib.font_manager as font_manager

def main(args):
    """
    Plots the prevalence curve (prevalence versus fraction vaccinated) from 
    the results produced by disease.py (names of the result files are 
    fed via STDIN) and saves the plot in a file called prevalence.pdf.
    """
    V = pylab.arange(0, 1.0, 0.01)
    R = []
    Rerr = []
    lines = sys.stdin.readlines()
    for line in lines:
        data = pandas.read_table(line.strip(), header = None)
        tail = data.tail(1).values[0]
        R.append(round(tail[2], 3))
        Rerr.append(round(tail[3], 3))
    auc = sum([0.01 * r for r in R])
    print("%.3f" %(auc))
    font_prop = font_manager.FontProperties(size = 12)
    pylab.figure(1, figsize = (7, 4.5), dpi = 500)
    pylab.xlabel(r"fraction vaccinated $v$", fontproperties = font_prop)
    pylab.ylabel(r"prevalence $\pi$", fontproperties = font_prop)
    pylab.errorbar(V, R, Rerr, color = "k", fmt = ".")
    pylab.plot(V, R, "k-", linewidth = 2, alpha = 0.6)
    pylab.xlim(0, 1.0)
    pylab.ylim(0, 1.0)
    pylab.figtext(0.82, 0.85, r"$\Pi = %.3f$" \
                  %(auc), ha = 'center', va = 'center', 
                  bbox = dict(facecolor = 'white', edgecolor = 'black'))
    pylab.savefig("prevalence.pdf", format = "pdf", bbox_inches = "tight")
    pylab.close(1)

if __name__ == "__main__":
    main(sys.argv[1:])
