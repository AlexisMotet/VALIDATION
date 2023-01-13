from model import TransitionRelation
from graph import DictGraph, bfs

class ParentTraceProxy(TransitionRelation):
    def __init__(self, operand : TransitionRelation, dict : dict):
        super(ParentTraceProxy, self).__init__()
        self.operand = operand
        self.dict = dict
    
    def get_roots(self):
        roots = self.operand.get_roots()
        for root in roots :
            self.dict[root] = {None}
        return roots
        
    def next(self, source):
        neighbours = self.operand.next(source)
        for neighbour in neighbours :
            if neighbour not in self.dict :
                self.dict[neighbour] = source
        return neighbours
    
    def get_trace(self, target):
        print("---------- TRACE ----------")
        while target :
            parent = self.dict[target]
            print("Le Noeud %s a pour parent le Noeud %s" % (str(target), str(parent)))  
            target = parent
        print("---------------------------")
                      
        
        
if __name__ == "__main__" :
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