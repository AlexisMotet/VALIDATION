from transition_relation.graph import TransitionRelation
from transition_relation.model import Config

class HanoiConfiguration(Config):
    def __init__(self, d : dict):
        self.d = d
        for l in d.values():
            assert all(l[i] > l[i + 1] for i in range(len(l) - 1))

    def __hash__(self):
        return hash(frozenset(self.d))

    def __str__(self):
        return str(self.d)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other_config):
        return self.d == other_config.d

class Hanoi(TransitionRelation):
    def __init__(self, roots):
        self.roots = roots

    def get_roots(self):
        return self.roots

    def next(self, source : HanoiConfiguration):
        childs = []
        for old in source.d:
            if len(source.d[old]) == 0:
                continue
            for new in source.d:
                if new == old:
                    continue
                if len(source.d[new]) == 0 or source.d[new][-1] > source.d[old][-1]:
                    child = HanoiConfiguration({x: [y for y in source.d[x]] for x in source.d})
                    child.d[new].append(child.d[old].pop())
                    childs.append(child)
        return childs
