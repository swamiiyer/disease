# Disease Dynamics on Complex Networks

Python code for simulating the dynamics of infectious diseases on complex 
networks and studying the effects of different vaccination strategies on 
the spread of a disease.

`attack_sequence.py`: This script reads in a network in GraphML format,
computes the order in which the vertices of the network must be removed using
various (random walk, referral, betweenness, closeness, degree, and
eigenvector) attack strategies and simultaneous and sequential attack modes.
The orderings are pickled in a file.

`disease.py`: This script simulates disease dynamics on complex networks 
using the parameters specified in `<params file>`, and prints the final 
fractions (`s`, `i`, and `r`) of the susceptible, intected, and recovered 
individuals, along with the standard deviation of `r`.

```bash
> python disease.py <params file>
```

`disease_verbose.py`: This script behaves similarly to `disease.py`, but for 
output, prints the time-evolution of the `s`, `i`, `r` values.

```bash
> python disease_verbose.py <params file>
```

`params.json.sample`: Sample parameter file. The allowed vaccination 
strategies are: `random_vaccination`, `random_walk_vaccination`, 
`referral_vaccination`, `betweenness_vaccination`, `closeness_vaccination`,
`degree_vaccination`, and `eigenvector_vaccination`. 

`sir_curves.py`: This script plots the s-i-r curves from the results produced 
by `disease_verbose.py` (fed via `STDIN`) and saves the plot in a file called 
`sir.pdf`.

`prevalence_curve.py`: This script plots the prevalence curve (prevalence 
versus fraction vaccinated) from the results produced by `disease.py` (names 
of the result files are fed via `STDIN`) and saves the plot in a file called 
`prevalence.pdf`. The script also calculates and prints the `P-index` value and 
the critical vaccination threshold value, `vstar`.

`prevalence_curves.py`: Given a network-related string (say `<prefix>`), plots
the prevalence curves for the seven vaccination strategies, obtained from
directories  with names starting with `<prefix>`, and saves the plot in a file
called `<prefix>_prevalence_curves.pdf`.

`pindex_vstar_curves.py`: Given a network-related string (say `<prefix>`),
plots the P-index and vaccination threshold curves for the seven vaccination
strategies, obtained from directories with names starting with `<prefix>`, and
saves the plots in files called `<prefix>_pindex_curves.pdf` and
`<prefix>_vstar_curves.pdf`.

`gr_network.py`: This script generates an exponential (growing random) 
network with `n` vertices and mean degree `k`, and saves it in graphml format.

```bash
> python gr_network.py <n> <k>
```

## Software Dependencies

* [Python](https://www.python.org/)
* [igraph](http://igraph.org/)
* [NetworkX](https://networkx.github.io/)
* [NumPy](http://www.numpy.org/)
* [Pandas](http://pandas.pydata.org/)
* [Matplotlib](http://matplotlib.org/)

## Contact

If you have any questions about the software, please email swami.iyer@gmail.com.
