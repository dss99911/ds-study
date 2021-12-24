# from __future__ import division  # make normal integer to
import matplotlib.pyplot as plt
import numpy as np
from sympy import *
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()


def same_size(size):
    return {
        "xlim": (-size, size),
        "ylim": (-size, size)
    }


def plotFunction(f, xlim=(-10, 10), ylim=(-10, 10), is_dot=False, dot_count=1000):
    x = np.linspace(xlim[0], xlim[1], dot_count)
    call = lambda x: f.eval(x) if isinstance(f, type) and issubclass(f, Function) else f(x)

    y = np.array([call(ix) for ix in x])
    _show_graph(x, y, xlim, ylim, is_dot)


def _set_axes(ax, xlim, ylim):
    ax.spines.left.set_position('zero')  # move left line to zero axe. "center"
    ax.spines.bottom.set_position('zero')
    ax.spines.right.set_color('none')  # hide right border line
    ax.spines.top.set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.yaxis.set_ticks_position('left')


def _show_graph(x, y, xlim, ylim, is_dot=False):
    fig, ax = plt.subplots()
    if is_dot:
        ax.plot(x, y, "o", markersize=0.3)
    else:
        ax.plot(x, y)
    _set_axes(ax, xlim, ylim)
    plt.show()
