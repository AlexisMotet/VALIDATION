from enum import Enum
from semantic import RuleAbstract
from copy import copy
from semantic import SoupConfig, SoupProgram, SoupSemantic, STR2TR


class Etat(Enum):
    HOME = 0
    INTERMEDIATE = 1
    GARDEN = 2
    
class AliceAndBobConfig(SoupConfig):
    def __init__(self, alice, bob, flag_alice, flag_bob):
        self.alice = alice
        self.bob = bob
        self.flag_alice = flag_alice
        self.flag_bob = flag_bob
        
    def __copy__(self):
        return AliceAndBobConfig(copy(self.alice),
                                 copy(self.bob),
                                 copy(self.flag_alice),
                                 copy(self.flag_bob))
    def __str__(self):
        return "[Alice %s Flag %s - Bob %s Flag %s]" % (self.alice, 
                                                                 self.flag_alice,
                                                                 self.bob, 
                                                                 self.flag_bob)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.alice == other.alice and self.bob == other.bob and \
                self.flag_alice == other.flag_alice and self.flag_bob == other.flag_bob
    
    def __hash__(self) :
        return hash(frozenset([self.alice, self.flag_alice, self.bob, self.flag_bob]))
    
class RuleAliceToIntermediate(RuleAbstract):
    def __init__(self):
         super().__init__("alice to intermediate", 
                          lambda config : config.alice==Etat.HOME)
    def execute(self, new_config): 
        new_config.alice = Etat.INTERMEDIATE
        new_config.flag_alice = True
        return new_config
    
class RuleAliceToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("alice to garden", lambda config : 
            config.alice == Etat.INTERMEDIATE and config.flag_bob!=True)
        
    def execute(self, new_config): 
        new_config.alice = Etat.GARDEN
        return new_config
    
class RuleAliceToHome(RuleAbstract):
    def __init__(self):
        super().__init__("alice to home", lambda config : config.alice==Etat.GARDEN)

    def execute(self, new_config): 
        new_config.alice = Etat.HOME
        new_config.flag_alice = False
        return new_config
    
class RuleBobToIntermediate(RuleAbstract):
    def __init__(self):
         super().__init__("bob to intermediate", 
                          lambda config : config.bob==Etat.HOME)
    def execute(self, new_config): 
        new_config.bob = Etat.INTERMEDIATE
        new_config.flag_bob = True
        return new_config
    
class RuleBobToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("bob to garden", lambda config : 
            config.bob == Etat.INTERMEDIATE and config.flag_alice!=True)
        
    def execute(self, new_config): 
        new_config.bob = Etat.GARDEN
        return new_config
    
class RuleBobToHome(RuleAbstract):
    def __init__(self):
        super().__init__("bob to home", lambda config : config.bob==Etat.GARDEN)
        
    def execute(self, new_config): 
        new_config.bob = Etat.HOME
        new_config.flag_bob = False
        return new_config
    
class RuleBobIntermediateToHome(RuleAbstract):
    def __init__(self):
        super().__init__("bob to intermediate from home", 
                         lambda config : config.bob==Etat.INTERMEDIATE
                         and config.flag_alice==True)
        
    def execute(self, new_config): 
        new_config.bob = Etat.HOME
        new_config.flag_bob = False
        return new_config
    
if __name__=="__main__":
    config_start = AliceAndBobConfig(Etat.HOME, Etat.HOME, False, False)
    program = SoupProgram(config_start)
    program.add(RuleAliceToGarden())
    program.add(RuleAliceToHome())
    program.add(RuleAliceToIntermediate())
    program.add(RuleBobToGarden())
    program.add(RuleBobToHome())
    program.add(RuleBobToIntermediate())
    #program.add(RuleBobIntermediateToHome())
    soup_semantic = SoupSemantic(program)
    str2tr = STR2TR(soup_semantic)
    
    from trace_ import ParentTraceProxy
    d = {}
    p = ParentTraceProxy(str2tr, d)
    
    o = [None, soup_semantic, None]
    
    
    def on_discovery(source, n, o) :
        res = n.alice == Etat.GARDEN and n.bob == Etat.GARDEN
        if res : o[0] = n
        if len(o[1].enabled_rules(n)) == 0 :
            print("deadlock trouve pour la config : %s" % n)
            o[2] = n
        return res
    
    p.bfs(o, on_discovery=on_discovery)
    res= p.get_trace(o[2])
