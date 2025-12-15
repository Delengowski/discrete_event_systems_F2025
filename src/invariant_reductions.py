from .objects import Activity
from typing import Literal
from itertools import pairwise, product, combinations, chain
from dataclasses import asdict


def rule1(T: list[Activity]) -> list[tuple[Activity, ...]]:
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


def rule1_2(T: list[Activity]) -> list[tuple[Activity, ...]]:
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
                    prev = b
                elif all(x.prop == "Consumable" for x in b.rss):
                    combinable.append(b)
                    break_out = True
            else:
                break
        if break_out:
            combined.update(combinable)
            applied.append(tuple(combinable))
    return applied


def rule2(T: list[Activity]) -> list[tuple[Activity, ...]]:
    """Combines parallel activities that fan-out from the same activity and fan-in to the same activity.

    Given 2 or activities that fan-out from the same activitiy X and fan-in to the same activity Y, if all
    activities do not have consumable resources then they can be combined per rule 2.
    """
    T = list(set(T))
    T.sort()
    applied = []
    combined = set()
    for a in T:
        if (
            len(a.pa) < 2
            or not all(
                (y - x) == 1 for x, y in pairwise(a.pa)
            )  # have to be consecutively increasing
        ):
            continue
        pre_acts = [x for x in T if x.idx in a.pa]
        pre_acts_i = iter(pre_acts)
        prev = next(pre_acts_i, None)
        if prev is None:
            continue
        if prev.rss != frozenset() or prev.srs != frozenset() or len(prev.pa) > 1:
            continue
        else:
            fanout = prev.pa
        breakout = False
        for prev in pre_acts_i:
            if (
                prev.rss != frozenset()
                or prev.srs != frozenset()
                or len(prev.pa) > 1
                or prev.pa != fanout
            ):
                breakout = True
                break
        # if we made it here they all fan from same thing so we can combine, assuming we didn't break earlier
        if breakout:
            continue
        combined.update(pre_acts)
        applied.append(tuple(pre_acts))
    return applied


def rule1_tie_breaker(results: list) -> list[tuple[Activity, int]]:
    winners = []
    for prod in product(*results):
        if sum(x == frozenset((tuple(),)) for x in prod) == 2:
            overall_winner = max(prod, key=len)
            winners.append((overall_winner, next(idx for idx, x in enumerate(results) if overall_winner in x)))
        else:
            ties = []
            for combo in combinations(prod, 2):
                if combo[0].intersection(combo[1]):
                    overall_winner = max(combo, key=len)
                    ties.append(overall_winner)
            if ties:
                overall_winner = max(ties, key=len)
                winners.append((overall_winner, next(idx for idx, x in enumerate(results) if overall_winner in x)))
    return list(set(winners))


def consolidate_rule(
    results: list[frozenset[Activity]], cur_list: list[Activity], ruleset: Literal[1, 2]
) -> list[Activity]:
    cur_list_opt = cur_list.copy()
    for result in results:
        match ruleset:
            case 1:
                for act in result[0]:
                    cur_list_opt.pop(cur_list_opt.index(act))
                result, rule_idx = result
                idx = frozenset(x for x in chain(*((act.idx,) if isinstance(act.idx, int) else act.idx for act in result)))
                t_min = sum(act.t_min for act in result)
                t_max = sum(act.t_max for act in result)
                pa = min(result).pa
                match rule_idx:
                    case 0:
                        rule_kwargs = {}
                    case 1:
                        rule_kwargs = {"rss": min(result).rss}
                    case 2:
                        rule_kwargs = {"rss": min(result).srs}
                cur_list_opt.append(Activity(idx=idx, t_min=t_min, t_max=t_max, pa=pa, **rule_kwargs))
            case 2:
                for act in result:
                    cur_list_opt.pop(cur_list_opt.index(act))
                idx = frozenset(act.idx for act in result)
                t_min = min(act.t_min for act in result)
                t_max = max(act.t_max for act in result)
                pa = result[0].pa  # all same pre-activities
                new_act = Activity(idx=idx, t_min=t_min, t_max=t_max, pa=pa)
                cur_list_opt.append(new_act)
                # update the downstream pre-activity
                upd_act = next(x for x in cur_list_opt if x.pa == idx)
                upd_idx = cur_list_opt.index(upd_act)
                cur_settings = asdict(upd_act)
                cur_settings["pa"] = frozenset((new_act.idx,))
                cur_list_opt[upd_idx] = Activity(**cur_settings)
            case _:
                raise ValueError("Unknown ruleset.")
    return cur_list_opt


def apply_rules(T: list[Activity]) -> list[Activity]:
    rule1_checks = (rule1, rule1_1, rule1_2)
    has_reductions = True
    T_opt = T.copy()
    while has_reductions:
        rule1_results = [
            [frozenset(y) for y in x] if (x := rule(T_opt)) else [frozenset((tuple(),))]
            for rule in rule1_checks
        ]
        winners = rule1_tie_breaker(rule1_results)
        if winners != [(frozenset((tuple(),)),0)]:
            T_opt = consolidate_rule(winners, T_opt, 1)
        rule2_results = rule2(T_opt)
        if rule2_results:
            T_opt = consolidate_rule(rule2_results, T_opt, 2)
        if winners == [(frozenset((tuple(),)),0)] and not rule2_results:
            has_reductions = False
    return T_opt
