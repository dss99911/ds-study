# from __future__ import division  # make normal integer to
import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from sympy.plotting.plot import MatplotlibBackend, Plot

x, y, z, t = symbols('x y z t')
a, b, c = symbols('a b c')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)
init_printing()


def get_sympy_subplots(plot: Plot):
    backend = MatplotlibBackend(plot)

    backend.process_series()
    backend.fig.tight_layout()
    return backend.fig, backend.ax[0]


def points(tuple_list:list[tuple]):
    return [
        [t[0] for t in tuple_list],
        [t[1] for t in tuple_list]
    ]


def lim(x, y=None):
    if y is None:
        y = x
    return {
        "xlim": (-x, x),
        "ylim": (-y, y)
    }


def inverse_function(f, x=x, y=y, i=-1):
    """
    x,y: x,y에 특정 제약이 주어져야 하는 경우, 직접 입력
    i: 해가 여러개라서, 그 중 하나를 선택해야 함"""
    return solve(Eq(f, y), x)[i].subs(y, x)


def is_bijective_function(f, x=x, y=y, i=-1):
    """전단사 함수 체크."""
    g = inverse_function(f, x, y, i)
    return g.subs(x, f).equals(x) == True


def plot_function(f, xlim=(-10, 10), ylim=(-10, 10), is_dot=False, dot_count=1000):
    x = np.linspace(xlim[0], xlim[1], dot_count)
    call = lambda x: f.eval(x) if isinstance(f, type) and issubclass(f, Function) else f(x)

    y = np.array([call(ix) for ix in x])
    _show_graph(x, y, xlim, ylim, is_dot)


#%%

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