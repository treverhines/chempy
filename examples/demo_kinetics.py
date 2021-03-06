#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from chempy.kinetics.integrated import (
    pseudo_irrev, pseudo_rev, binary_irrev, binary_rev
)

import sympy

funcs = (pseudo_irrev, pseudo_rev, binary_irrev, binary_rev)


def main():
    t, kf, P0, t0, excess_C, limiting_C, eps_l, beta = sympy.symbols(
        't k_f P0 t0 Y Z epsilon beta', negative=False)
    for f in funcs:
        args = t, kf, P0, t0, excess_C, limiting_C, eps_l
        kwargs = {'exp': sympy.exp}
        if f in (pseudo_rev, binary_rev):
            args += (beta,)
        if f is binary_rev:
            kwargs['one'] = sympy.S(1)
        expr = f(*args, **kwargs)
        with open(f.__name__ + '.png', 'wb') as ofh:
            sympy.printing.preview(expr, output='png', filename='out.png',
                                   viewer='BytesIO', outputbuffer=ofh)
        with open(f.__name__ + '_diff.png', 'wb') as ofh:
            sympy.printing.preview(expr.diff(t).subs({t0: 0}).simplify(),
                                   output='png', filename='out.png',
                                   viewer='BytesIO', outputbuffer=ofh)


if __name__ == '__main__':
    try:
        import argh
    except ImportError:
        main()
    else:
        argh.dispatch_command(main)
