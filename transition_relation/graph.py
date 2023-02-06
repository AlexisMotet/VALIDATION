from transition_relation.model import TransitionRelation

class DictGraph(TransitionRelation):
    def __init__(self, roots, d):
        self.roots = roots
        self.d = d
    def get_roots(self):
        return self.roots

    def next(self, source):
        return self.d[source]
