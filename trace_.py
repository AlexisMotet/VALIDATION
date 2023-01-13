from model import TransitionRelation

class ParentTraceProxy(TransitionRelation):
    def __init__(self, operand : TransitionRelation, dict : dict):
        super.__init__(operand)
        self.operand = operand
        self.dict = dict
    
    def get_roots(self):
        roots = self.operand.get_roots()
        return roots
        
    def next(self, source):
        neighbours = self.operand.next(source)
        return neighbours
        
        
if __name__ == "__main__" :
    print("coucou")