from transition_relation.model import TransitionRelation


class NBits(TransitionRelation):
    def __init__(self, roots, n):
        super().__init__()
        self.roots = roots
        self.n = n

    def get_roots(self):
        return self.roots

    def next(self, source):
        neighbours = []
        for i in range(self.n):
            neighbours.append(source ^ (1 << i))
        return neighbours