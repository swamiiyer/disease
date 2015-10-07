# Disease Dynamics on Complex Networks

Python code for simulating the dynamics of infectious diseases on complex 
networks and studying the effects of different vaccination strategies on 
the spread of a disease.

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
`degree_vaccination`, and `eigenvector_vaccination`. For the allowed 
network parameters, consult [https://github.com/swamiiyer/network].

`sir_curves.py`: This script plots the s-i-r curves from the results produced 
by `disease_verbose.py` (fed via `STDIN`) and saves the plot in a file called 
`sir.pdf`.

`prevalence_curve.py`: This script plots the prevalence curve (prevalence 
versus fraction vaccinated) from the results produced by `disease.py` (names 
of the result files are fed via `STDIN`) and saves the plot in a file called 
`prevalence.pdf`. The script also calculates and prints the `P-index` value and 
the critical vaccination threshold value, `vstar`.

## Software Dependencies

* [Python](https://www.python.org/) (2.7.6)
* [NetworkX](https://networkx.github.io/) (1.8.1)
* [NumPy](http://www.numpy.org/) (1.8.2)
* [Pandas](http://pandas.pydata.org/) (0.13.1)
* [Matplotlib](http://matplotlib.org/) (1.3.1)

## Contact

If you have any questions about the software, please email swami.iyer@gmail.com.
