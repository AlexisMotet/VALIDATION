from graph import TransitionRelation, bfs

class HanoiConfiguration():
    def __init__(self, d):
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
        print(self.roots)
        return self.roots

    def next(self, source):
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

if __name__ == '__main__':

    hanoiConfiguration = HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})

    hanoi = Hanoi([hanoiConfiguration])

    def look_for_config(source, n, o):

        if n is not None and \
                n == HanoiConfiguration(
            {1: [], 2: [], 3: [3, 2, 1]}):
            print("Node Found : ", n)
            return True
        else:
            print("Node Discovered : ", n)
        return False


    def basic1(source, n, o):
        return False


    def basic2(source, o):
        return False


    k, o = bfs(hanoi, None, look_for_config, basic1, basic2)
