<<<<<<< HEAD
from transition_relation.model import TransitionRelation, Config

=======
from transition_relation.graph import TransitionRelation
from transition_relation.model import Config
>>>>>>> c256c9aab89cc5390e1a8d3d97f4743b5051f23f

class HanoiConfiguration(Config):
    def __init__(self, dict_ : dict):
        super().__init__()
        self.dict_ = dict_
        for l in dict_.values():
            assert all(l[i] > l[i + 1] for i in range(len(l) - 1))

    def __hash__(self):
        return hash(frozenset(self.dict_))

    def __str__(self):
        return str(self.dict_)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other_config):
        return self.dict_ == other_config.dict_

class Hanoi(TransitionRelation):
    def __init__(self, roots : list):
        super().__init__()
        self.roots = roots

    def get_roots(self):
        return self.roots

    def next(self, source : HanoiConfiguration):
        childs = []
        for old in source.dict_:
            if len(source.dict_[old]) == 0:
                continue
            for new in source.dict_:
                if new == old:
                    continue
                if len(source.dict_[new]) == 0 or source.dict_[new][-1] > source.dict_[old][-1]:
                    child = HanoiConfiguration({x: [y for y in source.dict_[x]] for x in source.dict_})
                    child.dict_[new].append(child.dict_[old].pop())
                    childs.append(child)
        return childs
