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


def plot_function(f, xlim=(-10, 10), ylim=(-10, 10), is_dot=False, dot_count=1000, ax=None, show=True):
    if isinstance(f, Expr):
        f = lambdify(x, f) # support only 'x' variable

    x_value = np.linspace(xlim[0], xlim[1], dot_count)

    call = lambda x_value: f.eval(x_value) if isinstance(f, type) and issubclass(f, Function) else f(x_value)

    y = np.array([call(ix) for ix in x_value])
    _show_graph(x_value, y, xlim, ylim, is_dot, ax, show)


def diff_line(f, x_symbol, x_value):
    """
    함수의 특정 점에서의 접선을 리턴한다
    :param x_value: 접선과 함수의 접점
    :return: 점선
    :rtype: Expr
    """
    d = diff(f)
    a = d.subs(x_symbol, x_value)
    return a*(x - x_value) + f.subs(x_symbol, x_value)


def idiff_line(f, y, x, point):
    """
    implicit 함수의 특정 점에서의 접선을 리턴한다
    :return: 점선
    :rtype: Expr
    """
    d = idiff(f, y, x)
    a = d.subs(x, point[0]).subs(y, point[1])
    return a*(x - point[0]) + point[1]

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


def _show_graph(x, y, xlim, ylim, is_dot=False, ax=None, show=True):
    if ax is None:
        fig, ax = plt.subplots()
        _set_axes(ax, xlim, ylim)

    if is_dot:
        ax.plot(x, y, "o", markersize=0.3)
    else:
        ax.plot(x, y)

    if show:
        plt.show()