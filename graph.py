from abc import abstractmethod, ABC
from collections import deque
"""
graphe = ["x", [["y", []], ["z", [["w", []], ["a", []]]]]]
def traversal_depth(graphe):
    valeur = graphe[0]
    print(valeur)
    n = len(graphe[1])
    if n == 0 :
        print("fin")
    else :
        for i in range(n):
            traversal_depth(graphe[1][i])

"""

class Node :
    def __init__(self, valeur):
        self.valeur = valeur
        self.children = []
    def addchild(self, child):
        self.children.append(child)

    def __str__(self) :
        return "Node %d" % self.valeur

    def __repr__(self):
        return self.__str__()

def traversal_depth(Node, marked=[], depth=0):
    n = len(Node.children)
    """
    for _ in range(depth) :
        print(" ", end="")
    print(Node.valeur)
    """
    if n > 0 :
        for child in Node.children:
            if child not in marked :
                marked.append(child)
                traversal_depth(child, marked, depth+1)
    return marked


def width_traversal(sommet, marked=[]):
    file = []
    file.insert(0, sommet)
    marked.append(sommet)
    while len(file) != 0 :
        Node = file.pop()
        for child in Node.children :
            if child not in marked :
                file.insert(0, child)
                marked.append(child)
    return marked

class TransitionRelation(ABC) :
    @abstractmethod
    def get_roots(self):
        pass
    @abstractmethod
    def next(self, source):
        pass

class DictGraph(TransitionRelation):
    def __init__(self, roots, d):
        self.roots = roots
        self.d = d
    def get_roots(self):
        return self.roots

    def next(self, source):
        return self.d[source]


def bfs(graph, o, on_discovery = lambda source, n, o : None ,
                  on_known = lambda source, n, o : None,
                  on_all_discovered = lambda source, o : None):
    knowns = set()
    border = deque()
    at_start = True
    while border or at_start :
        source = None
        if at_start :
            neighbours = graph.get_roots()
            at_start = False
        else :
            source = border.popleft()
            neighbours = graph.next(source)
        for n in neighbours :
            if n in knowns :
                if on_known(source, n, o) :
                    return knowns, o
                continue
            if on_discovery(source, n, o) : # on decouvre un voisin
                return knowns, o
            knowns.add(n)
            border.append(n)
        if on_all_discovered(source, o) :
            return knowns, o
    return knowns, o

if __name__ == "__main__" :

    def basic1(source, n, o):
        if n is o :
            print("target trouvée : %s" % n)
    def basic2(source, o):
        o[0] += 1

    def nothing1(source, n, o):
        pass

    def nothing2(source, o):
        pass

    """
    a
    |
    b c d
    | |
    | r  t ----- a
    e f --- f
    
    """

    dad = Node(3)
    child_dad1 = Node(1)
    child_child_dad11 = Node(10)
    child_child_dad12 = Node(9)
    child_dad1.addchild(child_child_dad11)
    child_dad1.addchild(child_child_dad12)
    child_dad2 = Node(4)
    child_child_dad21 = Node(4)
    child_child_dad22 = Node(14)
    child_dad2.addchild(child_child_dad21)
    child_dad2.addchild(child_child_dad22)
    dad.addchild(child_dad1)
    dad.addchild(child_dad2)

    child_child_dad21.addchild(child_child_dad22)
    """
    Arbre :
        3 _________
        |          |
        1 ___      4
        |    |   |    |
        10   9   4  - 14
    """
    # traversal_depth(dad)
    Nodes = width_traversal(dad)
    print(Nodes)