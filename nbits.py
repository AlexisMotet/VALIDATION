from graph import TransitionRelation


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

            """
            if source >> i & 1 :
                child = source & ~(1<<i)
            else :
                child = source | (1<<i)
            """
        return neighbours