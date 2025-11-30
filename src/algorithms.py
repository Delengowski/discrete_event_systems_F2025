"""Implementation of algorithms from the appendix of main paper.


Notes:
   The paper utilizes black dot infront or behind a variable to represent
   input conditions to fire (left of variable) and produced outcomes
   (right of variable). These are sets, an element for each input condition
   and outcome.
"""

from typing import Callable
from itertools import permutations


def ds(P, T, F, a, b, W, m0):
    """Algorithm 1, Detection Resource Dependency.

    If two transitions share input conditions and those
    input conditions are a subset of Pr the resource place set.

    Pr = Pir | Per

    Pir - internal resource place set
    Per - external resource place set

    Per = Perr | Pecr

    Perr - external resuable resource place set
    Pecr - external consumable place set

    Args:

    Returns:
        DependencySet (ds).

    """
    ds = set()
    for ti, tj in permutations(T):
        if True:
            ds.add((ti, tj))
    return ds


def cs(P, T, F, a, b, W, m0, ds):
    """Algorithm 2, Checking Resouce Conflicts.

    Provides the potential conflict set. Two transitions
    are in conflict if they're part of the depedency set (ds),
    and there is an intersection between their start and end
    times.

    i.e.

    [Tstart(ti), Tend(ti)] & [Tstart(tj), Tend(tj)] != {}

    There's only a true conflict if there are not enough resources.

    Args:

    Returns:
        ConflictSet (cs).

    """
    ...


def vmec(P, T, F, a, b, W, m0):
    """Algorithm 3, Minimum External Consumable Resource Vector.

    Args:

    Returns:
        Vmec, Minimum External Consumable Resource Vector.

    """
    ...


def vmer(P, T, F, a, b, W, m0):
    """Algorithm 4, Minimum Resuable Resource Vector.

    Args:

    Returns:
        Vmer, Minimum Resuable Resource Vector.

    """
    ...


def vrer(P, T, F, a, b, W, m0, ds, vmr):
    """Algorithm 5, Reliable Resuable Resource Vector.

    Args:

    Returns:
        Vrer, Reliable Resuable Resource Vector.

    """
    ...


def kas(P, T, F, a, b, W, m0):
    """Algorithm 6, Key Activities.

    Args:

    Returns:
        kas, Key Activities.

    """


def pas(P, T, F, a, b, W, m0, cs):
    """Algorithm 7, Priority Activity Set.

    Args:

    Returns:
        pas, Priority Activity Set.

    """
