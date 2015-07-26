import pandas, pylab, sys
import matplotlib.font_manager as font_manager

def main(args):
    """
    Plots the s-i-r curves from the results produced by disease.py (fed 
    via STDIN) and saves the plot in a file called sir.pdf.
    """
    data = pandas.read_table(sys.stdin, header = None)
    font_prop = font_manager.FontProperties(size = 12)
    pylab.figure(1, figsize = (7, 4.5), dpi = 500)
    pylab.xlabel(r"time $t$", fontproperties = font_prop)
    pylab.ylabel(r"susceptible $s$, infected $i$, recovered $r$", 
                 fontproperties = font_prop)
    t = range(len(data))
    s, i, r = list(data[0]), list(data[1]), list(data[2])
    pylab.plot(t, s, "b-", linewidth = 2, alpha = 0.6, label = r"$s$")
    pylab.plot(t, i, "g-", linewidth = 2, alpha = 0.6, label = r"$i$")
    pylab.plot(t, r, "r-", linewidth = 2, alpha = 0.6, label = r"$r$")
    pylab.xlim(0, max(t))
    pylab.ylim(0, 1.0)
    pylab.legend(loc = 'upper right', prop = font_prop)
    pylab.figtext(0.72, 0.85, r"$\pi = %.3f$" %(r[-1]), 
                        ha = 'center', va = 'center', 
                        bbox = dict(facecolor = 'white', edgecolor = 'black'))
    pylab.savefig("sir.pdf", format = "pdf", bbox_inches = "tight")
    pylab.close(1)
    
if __name__ == "__main__":
    main(sys.argv[1:])
