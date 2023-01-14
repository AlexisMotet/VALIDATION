from abc import abstractmethod, ABC
from collections import deque

class TransitionRelation(ABC) :
    @abstractmethod
    def get_roots(self):
        pass
    @abstractmethod
    def next(self, source):
        pass

    def bfs(self, o, on_discovery = lambda source, n, o : False,
                  on_known = lambda source, n, o : False,
                  on_all_discovered = lambda source, o : False):
        knowns = set()
        border = deque()
        at_start = True
        while border or at_start :
            source = None
            if at_start :
                neighbours = self.get_roots()
                at_start = False
            else :
                source = border.popleft()
                neighbours = self.next(source)
            for n in neighbours :
                if n in knowns :
                    if on_known(source, n, o) :
                        return knowns, o
                    continue
                knowns.add(n)
                if on_discovery(source, n, o) : # on decouvre un voisin
                    return knowns, o
                border.append(n)
            if on_all_discovered(source, o) :
                return knowns, o
        return knowns, o

