from model import TransitionRelation
from nbits import NBits

class ParentTraceProxy(TransitionRelation):
    def __init__(self, operand : TransitionRelation, dict : dict):
        super(ParentTraceProxy, self).__init__()
        self.operand = operand
        self.dict = dict
    
    def get_roots(self):
        roots = self.operand.get_roots()
        for root in roots :
            self.dict[root] = {}
        return roots
        
    def next(self, source):
        neighbours = self.operand.next(source)
        for neighbour in neighbours :
            if neighbour not in self.dict :
                self.dict[neighbour] = source
        return neighbours
    
    def get_trace(self, target):
        trace = []
        while target :
            parent = self.dict[target]
            trace.append("Le Noeud %s mene au Noeud %s" % (str(parent), str(target)))
            target = parent
        print("---------- TRACE ----------")
        for s in reversed(trace):
            print(s)
        print("---------------------------")
        return trace
                      
        
        
if __name__ == "__main__" :
    from graph import bfs
    from hanoi import Hanoi, HanoiConfiguration
    hanoiConfiguration = HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})

    hanoi = Hanoi([hanoiConfiguration])
    d = {}
    p = ParentTraceProxy(hanoi, d)
    bfs(p, None)
    res= p.get_trace(HanoiConfiguration({1: [], 2: [], 3: [3, 2, 1]}))
    print('res', res)

    nbits = NBits([0], 2)
    ptp = ParentTraceProxy(nbits, {})
    bfs(ptp, None)
    res = ptp.get_trace(1)
    print('res', res)

    """
    d = {0: [1, 2], 
         1: [0, 1], 
         2: [1, 0, 3], 
         3 : [0, 1, 2, 4], 
         4 : [3], 
         5 : [10],
         7 : [],
         32 : [7, 5],
         10 : [32]}
    dictGraph = DictGraph([0], d)
    dic = {}
    p = ParentTraceProxy(dictGraph, dic)
    bfs(p, None)
    p.get_trace(2)
    """