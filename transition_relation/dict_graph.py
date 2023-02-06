from transition_relation.model import TransitionRelation

class DictGraph(TransitionRelation):
    def __init__(self, roots : list, dict_ : dict):
        self.roots = roots
        self.dict_ = dict_
    def get_roots(self):
        return self.roots

    def next(self, source):
        return self.dict_[source]
