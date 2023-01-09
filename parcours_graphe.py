from abc import abstractmethod, ABC
from collections import deque
"""
graphe = ["x", [["y", []], ["z", [["w", []], ["a", []]]]]]
def parcours_profondeur(graphe):
    valeur = graphe[0]
    print(valeur)
    n = len(graphe[1])
    if n == 0 :
        print("fin")
    else :
        for i in range(n):
            parcours_profondeur(graphe[1][i])

"""

class Noeud :
    def __init__(self, valeur):
        self.valeur = valeur
        self.enfants = []
    def ajouterEnfant(self, enfant):
        self.enfants.append(enfant)

    def __str__(self) :
        return "Noeud %d" % self.valeur

    def __repr__(self):
        return self.__str__()

def parcours_profondeur(noeud, marques=[], profondeur=0):
    n = len(noeud.enfants)
    """
    for _ in range(profondeur) :
        print(" ", end="")
    print(noeud.valeur)
    """
    if n > 0 :
        for enfant in noeud.enfants:
            if enfant not in marques :
                marques.append(enfant)
                parcours_profondeur(enfant, marques, profondeur+1)
    return marques
            

def parcours_largeur(sommet, marques=[]):
    file = []
    file.insert(0, sommet)
    marques.append(sommet)
    while len(file) != 0 :
        noeud = file.pop()
        # print(noeud.valeur)
        for enfant in noeud.enfants :
            if enfant not in marques :
                file.insert(0, enfant)
                marques.append(enfant)
    return marques


class Graph(dict):
    def __init__(self) :
        self.initial = None

    def add(self, a, neighbours, initial=False) :
        self[a] = neighbours
        if initial :
            assert self.initial == None
            self.initial = self[a]
    
    def get(self, a) :
        return self[a]

    def get_initial(self) :
        return self.initial
    
    
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
    
    
class HanoiConfiguration():
    def __init__(self, d) :
        self.d = d
        for l in d.values() :
            assert all(l[i] > l[i+1] for i in range(len(l) - 1))

    def __hash__(self):
        return hash(frozenset(self.d))
    
    def __str__(self):
        return str(self.d)
    
    def __repr__(self) :
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
        for old in source.d :
            if len(source.d[old]) == 0:
                continue
            for new in source.d :
                if new == old :
                    continue
                if len(source.d[new]) == 0 or source.d[new][-1] > source.d[old][-1] : 
                    child = HanoiConfiguration({x : [y  for y in source.d[x]] for x in source.d})
                    child.d[new].append(child.d[old].pop())
                    childs.append(child)
        return childs
    
    
    
def bfs(graph, o, on_discovery = lambda source, n, o : None , 
                  on_known = lambda source, n, o : None, 
                  on_all_discovered = lambda source, o : None):
    knowns = set()
    frontier = deque()
    at_start = True
    while frontier or at_start :
        source = None
        if at_start :
            neighbours = graph.get_roots()
            print("neighbours", neighbours)
            at_start = False
        else :
            source = frontier.popleft()
            neighbours = graph.next(source)
        for n in neighbours :
            if n in knowns :
                if on_known(source, n, o) :
                    return knowns, o
                continue
            if on_discovery(source, n, o) : # on decouvre un voisin
                return knowns, o
            knowns.add(n)
            frontier.append(n)
        if on_all_discovered(source, o) :
            return knowns, o
    print("fini")
    return knowns, o

if __name__ == "__main__" :
    
    hanoiConfiguration = HanoiConfiguration({1:[3, 2, 1], 2 : [], 3 : []})
    
    hanoi = Hanoi([hanoiConfiguration])
    

    def look_for_config(source, n, o):
        if n is not None and \
            n == HanoiConfiguration(
                {1:[], 2 : [], 3 : [3, 2, 1]}):
            return True
        return False
    
    def basic1(source, n, o):
        return False
    def basic2(source, o):
        return False

    
    k, o = bfs(hanoi, None, look_for_config, basic1, basic2)  
    """
    for c in k :
        print(c)
     
    
    n = 10
    nBits = NBits([0], n)
    print("limit %d" % (2**n - 1))
    
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
    
    """
    
    # dictGraph = DictGraph()
    """
    graph = Graph()
    pere = "a"
    enfants = ["b", "c", "d"] 
    enfants_b =["e", "f"]
    enfants_c = ["r", "t"]

    graph.add("a", enfants, initial=True)
    graph.add("b", enfants_b)
    graph.add("c", enfants_c)
    graph.add("d", [])
    graph.add("e", [])
    graph.add("f", ["f"])
    graph.add("r", [])
    graph.add("t", ["a"])

    def basic1(source, n, o):
        if n is o :
            print("target trouvée : %s" % n)
    def basic2(source, o):
        o[0] += 1

    def nothing1(source, n, o):
        pass

    def nothing2(source, o):
        pass

    o = "f"
    bfs(graph, o, basic1, basic1, nothing2)
    """
    """
    a
    |
    b c d
    | |
    | r  t ----- a
    e f --- f
    
    """

    """
    pere = Noeud(3)
    enfant_pere1 = Noeud(1)
    enfant_enfant_pere11 = Noeud(10)
    enfant_enfant_pere12 = Noeud(9)
    enfant_pere1.ajouterEnfant(enfant_enfant_pere11)
    enfant_pere1.ajouterEnfant(enfant_enfant_pere12)
    enfant_pere2 = Noeud(4)
    enfant_enfant_pere21 = Noeud(4)
    enfant_enfant_pere22 = Noeud(14)
    enfant_pere2.ajouterEnfant(enfant_enfant_pere21)
    enfant_pere2.ajouterEnfant(enfant_enfant_pere22)
    pere.ajouterEnfant(enfant_pere1)
    pere.ajouterEnfant(enfant_pere2)

    enfant_enfant_pere21.ajouterEnfant(enfant_enfant_pere22)

    Arbre :
        3 _________
        |          |
        1 ___      4
        |    |   |    |
        10   9   4  - 14

    # parcours_profondeur(pere)
    noeuds = parcours_largeur(pere)
    print(noeuds)
    """