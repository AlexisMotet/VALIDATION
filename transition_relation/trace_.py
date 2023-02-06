import transition_relation.model as model

class ParentTraceProxy(model.TransitionRelation):
    def __init__(self, operand : model.TransitionRelation):
        super().__init__()
        self.operand = operand
        self.dict_ = {}
    
    def get_roots(self):
        roots = self.operand.get_roots()
        for root in roots :
            self.dict_[root] = "ROOT"
        return roots
        
    def next(self, source):
        neighbours = self.operand.next(source)
        for neighbour in neighbours :
            if neighbour not in self.dict_ :
                self.dict_[neighbour] = source
        return neighbours
    
    def get_trace(self, target):
        trace = []
        while True :
            parent = self.dict_[target]
            if str(parent) == "ROOT" :
                trace.append("[TRACE] Le noeud racine est \"%s\"" % str(target))
                break
            trace.append("[TRACE] Le noeud \"%s\" mene au noeud \"%s\"" % (str(parent), str(target)))
            target = parent
            
        print("---------- TRACE ----------")
        for s in reversed(trace):
            print(s)
        print("-------- FIN TRACE --------")
        return trace             
        
        
if __name__ == "__main__" :
    from model import TransitionRelation
    from hanoi import Hanoi, HanoiConfiguration
    hanoiConfiguration = HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})

    hanoi = Hanoi([hanoiConfiguration])
    d = {}
    p = ParentTraceProxy(hanoi, d)
    TransitionRelation.bfs(p, None)
    res= p.get_trace(HanoiConfiguration({1: [], 2: [], 3: [3, 2, 1]}))
    print('res -1', res[0])

    nbits = NBits([0], 2)
    ptp = ParentTraceProxy(nbits, {})
    TransitionRelation.bfs(ptp, None)
    res = ptp.get_trace(3)
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