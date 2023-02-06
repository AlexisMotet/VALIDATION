from transition_relation.graph import TransitionRelation


class NBits(TransitionRelation):
    def __init__(self, roots, n):
        self.roots = roots
        self.n = n

    def get_roots(self):
        return self.roots

    def next(self, source):
        neighbours = []
        for i in range(self.n):
            neighbours.append(source ^ (1 << i))
        return neighbours