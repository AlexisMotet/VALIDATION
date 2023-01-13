from graph import TransitionRelation, bfs


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

if __name__ == '__main__':

    n = 10
    nBits = NBits([0], n)
    print("limit %d" % (2 ** n - 1))


    def basic1(source, n, o):
        return False


    def look_for_int(source, n, o):
        if (source == 511):
            print("trouvé")
            return True
        return False


    def basic2(source, o):
        return False

    o = None
    k, o = bfs(nBits, o, look_for_int, basic1, basic2)