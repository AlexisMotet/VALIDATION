from enum import Enum
from copy import copy, deepcopy
import semantic_transition_relation.semantic as semantic

class State(Enum):
    HOME = 0
    INTERMEDIATE = 1
    GARDEN = 2
    
class AliceAndBobConfig(semantic.SoupConfig):
    def __init__(self, alice, bob, flag_alice, flag_bob):
        self.alice = alice
        self.bob = bob
        self.flag_alice = flag_alice
        self.flag_bob = flag_bob
    
    def __copy__(self):
        return AliceAndBobConfig(copy(self.alice),
                                 copy(self.bob))
        
    def __deepcopy__(self, memo):
        return AliceAndBobConfig(deepcopy(self.alice, memo),
                                 deepcopy(self.bob, memo),
                                 deepcopy(self.flag_alice, memo),
                                 deepcopy(self.flag_bob, memo))
    def __str__(self):
        return "Alice=%s flag_alice=%s Bob=%s flag_bob=%s" % (self.alice, 
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
    
class RuleAliceToIntermediate(semantic.RuleAbstract):
    def __init__(self):
         super().__init__("alice to intermediate", 
                          lambda config : config.alice==State.HOME)
    def execute(self, new_config): 
        new_config.alice = State.INTERMEDIATE
        new_config.flag_alice = True
    
class RuleAliceToGarden(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("alice to garden", lambda config : 
            config.alice == State.INTERMEDIATE and config.flag_bob!=True)
        
    def execute(self, new_config): 
        new_config.alice = State.GARDEN
    
class RuleAliceToHome(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("alice to home", lambda config : config.alice==State.GARDEN)

    def execute(self, new_config): 
        new_config.alice = State.HOME
        new_config.flag_alice = False
    
class RuleBobToIntermediate(semantic.RuleAbstract):
    def __init__(self):
         super().__init__("bob to intermediate", 
                          lambda config : config.bob==State.HOME)
    def execute(self, new_config): 
        new_config.bob = State.INTERMEDIATE
        new_config.flag_bob = True
    
class RuleBobToGarden(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("bob to garden", lambda config : 
            config.bob == State.INTERMEDIATE and config.flag_alice!=True)
        
    def execute(self, new_config): 
        new_config.bob = State.GARDEN
    
class RuleBobToHome(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("bob to home", lambda config : config.bob==State.GARDEN)
        
    def execute(self, new_config): 
        new_config.bob = State.HOME
        new_config.flag_bob = False
    
class RuleBobIntermediateToHome(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("bob to intermediate from home", 
                         lambda config : config.bob==State.INTERMEDIATE
                         and config.flag_alice==True)
        
    def execute(self, new_config): 
        new_config.bob = State.HOME
        new_config.flag_bob = False