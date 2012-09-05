"""This file contains code used in "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import math

import matplotlib.pyplot as pyplot

import myplot
import Pmf


def NormalPdf(x):
    """Computes the PDF of x in the standard normal distribution."""
    return math.exp(-x**2/2) / math.sqrt(2 * math.pi)


def Linspace(start, stop, n):
    """Makes a list of n floats from start to stop.

    Similar to numpy.linspace()
    """
    return [start + (stop-start) * float(i)/(n-1) for i in range(n)]


def RenderPdf(mu, sigma, n=101):
    """Makes xs and ys for a normal PDF with (mu, sigma).

    n: number of places to evaluate the PDF
    """
    xs = Linspace(mu-4*sigma, mu+4*sigma, n)
    ys = [NormalPdf((x-mu) / sigma) for x in xs]
    return xs, ys


def main():
    xs, ys = RenderPdf(100, 15)

    n = 34
    pyplot.fill_between(xs[-n:], ys[-n:], y2=0.0001, color='blue', alpha=0.2)
    s = 'Congratulations!\nIf you got this far,\nyou must be here.'
    d = dict(shrink=0.05)
    pyplot.annotate(s, [127, 0.02], xytext=[80, 0.05], arrowprops=d)

    myplot.Plot(xs, ys,
                clf=False,
                show=True,
                title='Distribution of IQ',
                xlabel='IQ',
                ylabel='PDF',
                legend=False
                )

if __name__ == "__main__":
    main()
