from enum import Enum
from semantic import RuleAbstract
from copy import copy
from semantic import SoupConfig, SoupProgram, SoupSemantic, STR2TR

class Etat(Enum):
    HOME = 0
    GARDEN = 1
    
class AliceAndBobConfig(SoupConfig):
    def __init__(self, alice, bob):
        self.alice = alice
        self.bob = bob
        
    def __copy__(self):
        return AliceAndBobConfig(copy(self.alice),
                           copy(self.bob))
    def __str__(self):
        return "Config : {Alice %s - Bob %s}" % (self.alice, self.bob)
    
    def __repr__(self):
        return "Config : {Alice %s - Bob %s}" % (self.alice, self.bob)
    
    def __eq__(self, other):
        return self.alice == other.alice and self.bob == other.bob
    
    def __hash__(self) :
        return hash(frozenset([self.alice, self.bob]))
    
class RuleAliceToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("alice to garden", lambda config : config.alice==Etat.HOME)
        
    def execute(self, new_config): 
        new_config.alice = Etat.GARDEN
        return new_config
    
class RuleAliceToHome(RuleAbstract):
    def __init__(self):
        super().__init__("alice to home", lambda config : config.alice==Etat.GARDEN)
        
    def execute(self, new_config): 
        new_config.alice = Etat.HOME
        return new_config
    
class RuleBobToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("bob to garden", lambda config : config.bob==Etat.HOME)
        
    def execute(self, new_config): 
        new_config.bob = Etat.GARDEN
        return new_config
    
class RuleBobToHome(RuleAbstract):
    def __init__(self):
        super().__init__("bob to home", lambda config : config.bob==Etat.GARDEN)
        
    def execute(self, new_config): 
        new_config.bob = Etat.HOME
        return new_config

    
if __name__=="__main__":
    config_start = AliceAndBobConfig(Etat.HOME, Etat.HOME)
    program = SoupProgram(config_start)
    program.add(RuleAliceToGarden())
    program.add(RuleAliceToHome())
    program.add(RuleBobToGarden())
    program.add(RuleBobToHome())
    soup_semantic = SoupSemantic(program)
    str2tr = STR2TR(soup_semantic)
    def on_discovery(source, n, o) :
        print(n)
    str2tr.bfs(None, on_discovery=on_discovery)  
    """
    from trace_ import ParentTraceProxy
    d = {}
    p = ParentTraceProxy(str2tr, d)
    def on_discovery(source, n, o) :
        res = n.alice == Etat.GARDEN and n.bob == Etat.GARDEN
        if res : o[0] = n
        return res
    
    def on_discovery(source, n, o) :
        print(n)
        return False
    
    o = [None]
    p.bfs(o, on_discovery=on_discovery)
    print(o)
    res= p.get_trace(o[0])
    """