<<<<<<< HEAD
from transition_relation.model import TransitionRelation
=======
from transition_relation.graph import TransitionRelation
>>>>>>> c256c9aab89cc5390e1a8d3d97f4743b5051f23f


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