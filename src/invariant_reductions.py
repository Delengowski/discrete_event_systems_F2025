from .objects import Activity
from itertools import islice
from collections import deque


def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def rule1(T: list[Activity]) -> list[list[Activity]]:
    """Combines dependent sequential activities where activites have input or output consumable resources.

    Given a set of 2 or more activities if given one of the activities in the sequence,
    there exists an activity in the set that is a pre-activity of the current, with no activities requiring
    resources then the activities can be combined.
    """
    T = list(set(T))
    T.sort()
    applied = []
    combined = set()
    for a in T:
        combinable = []
        if (
            a.rss != frozenset()
            or a.srs != frozenset()
            or a.pa == frozenset()
            or sum(x.pa == frozenset([a.idx]) for x in T) > 1
            or len(a.pa) > 1
        ):
            continue
        cur_idx = T.index(a)
        remaining = iter(T[cur_idx + 1 :])
        b = next(remaining, None)
        if b is None:
            break  # there is nothing to iterate
        if a in combined or b in combined:
            continue  # we already reduced these out
        if (
            b.rss == frozenset()
            and b.pa == frozenset([a.idx])
            and b.srs == frozenset()
            and not sum(x.pa == frozenset([b.idx]) for x in T) > 1
        ):
            combinable.append(a)
            combinable.append(b)
            combined.update((a, b))
        else:
            continue
        prev = b
        for b in remaining:  # keep adding activities that meet the rules
            if (
                b.rss == frozenset()
                and b.pa == frozenset([prev.idx])
                and b.srs == frozenset()
                and not sum(x.pa == frozenset([b.idx]) for x in T) > 1
            ):
                combinable.append(b)
                prev = b
                combined.update((b,))
        if combinable:
            applied.append(tuple(combinable))
    return applied


def rule1_1(T: list[Activity]) -> list[tuple[Activity, ...]]:
    """Combines dependent sequential activities where the first activity of the sequence requires input consumable resources.

    Given a set of 2 or more activities if given one of the activities in the sequence,
    there exists an activity in the set that is a pre-activity of the current, with the first activity
    requiring consumable resources then the activites can be combined.
    """
    T = list(set(T))
    T.sort()
    applied = []
    combined = set()
    for a in T:
        combinable = []
        if (
            a.rss == frozenset()
            or not all(x.prop == "Consumable" for x in a.rss)
            or a.srs != frozenset()
            or a.pa == frozenset()
            or sum(x.pa == frozenset([a.idx]) for x in T) > 1
            or len(a.pa) > 1
        ):
            continue
        cur_idx = T.index(a)
        remaining = iter(T[cur_idx + 1 :])
        b = next(remaining, None)
        if b is None:
            break  # there is nothing to iterate
        if a in combined or b in combined:
            continue  # we already reduced these out
        if (
            b.rss == frozenset()
            and b.pa == frozenset([a.idx])
            and b.srs == frozenset()
            and not sum(x.pa == frozenset([a.idx]) for x in T) > 1
            and not sum(x.pa == frozenset([b.idx]) for x in T) > 1
        ):
            combinable.append(a)
            combinable.append(b)
            combined.update((a, b))
        else:
            continue
        prev = b
        for b in remaining:  # keep adding activities that meet the rules
            if (
                b.rss == frozenset()
                and b.pa == frozenset([prev.idx])
                and not sum(x.pa == frozenset([a.idx]) for x in T) > 1
                and not sum(x.pa == frozenset([b.idx]) for x in T) > 1
            ):
                combinable.append(b)
                prev = b
                combined.update((b,))

        if combinable:
            applied.append(tuple(combinable))
    return applied


def rule1_2(T: list[Activity]) -> list[list[Activity]]:
    """Combines dependent sequential activities where the last activity of the sequence requires output consumable resources.

    Given a set of 2 or more activities if given one of the activities in the sequence,
    there exists an activity in the set that is a pre-activity of the current, with the last activity
    requiring output consumable resources then the activites can be combined.
    """
    T = list(set(T))
    T.sort()
    applied = []
    combined = set()
    for a in T:
        combinable = []
        if (
            a.rss != frozenset()
            or a.srs != frozenset()
            or a.pa == frozenset()
            or sum(x.pa == frozenset([a.idx]) for x in T) > 1
            or len(a.pa) > 1
        ):
            continue
        cur_idx = T.index(a)
        remaining = iter(T[cur_idx + 1 :])
        b = next(remaining, None)
        if b is None:
            break  # there is nothing to iterate
        if a in combined or b in combined:
            continue  # we already reduced these out
        if (
            b.rss == frozenset()
            and b.pa == frozenset([a.idx])
            and not sum(x.pa == frozenset([b.idx]) for x in T) > 1
        ):
            if b.srs == frozenset():
                combinable.append(a)
                combinable.append(b)
            elif all(x.prop == "Consumable" for x in b.rss):
                combinable.append(a)
                combinable.append(b)
                combined.update((a, b))
                applied.append(tuple(combinable))
                continue
        else:
            continue
        prev = b
        break_out = False
        for b in remaining:
            if break_out:
                break  # keep adding activities that meet the rules
            if (
                b.rss == frozenset()
                and b.pa == frozenset([prev.idx])
                and not sum(x.pa == frozenset([b.idx]) for x in T) > 1
            ):
                if b.srs == frozenset():
                    combinable.append(b)
                elif all(x.prop == "Consumable" for x in b.rss):
                    combinable.append(b)
                    break_out = True
            else:
                break
        if break_out:
            combined.update(combinable)
            applied.append(tuple(combinable))
    return applied

