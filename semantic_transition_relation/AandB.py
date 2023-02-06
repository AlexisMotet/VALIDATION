from enum import Enum
from copy import copy, deepcopy
import semantic_transition_relation.semantic as semantic


class State(Enum):
    HOME = 0
    GARDEN = 1
    
class AliceAndBobConfig(semantic.SoupConfig):
    def __init__(self, alice, bob):
        self.alice = alice
        self.bob = bob
        
    def __copy__(self):
        return AliceAndBobConfig(copy(self.alice),
                                 copy(self.bob))
        
    def __deepcopy__(self, memo=None):
        return AliceAndBobConfig(deepcopy(self.alice, memo),
                           deepcopy(self.bob, memo))
    def __str__(self):
        return "Alice=%s - Bob=%s" % (self.alice, self.bob)
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.alice == other.alice and self.bob == other.bob
    
    def __hash__(self) :
        return hash(frozenset([self.alice, self.bob]))
    
class RuleAliceToGarden(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("alice to garden", lambda config : config.alice==State.HOME)
        
    def execute(self, new_config): 
        new_config.alice = State.GARDEN
    
class RuleAliceToHome(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("alice to home", lambda config : config.alice==State.GARDEN)
        
    def execute(self, new_config): 
        new_config.alice = State.HOME
    
class RuleBobToGarden(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("bob to garden", lambda config : config.bob==State.HOME)
        
    def execute(self, new_config): 
        new_config.bob = State.GARDEN
    
class RuleBobToHome(semantic.RuleAbstract):
    def __init__(self):
        super().__init__("bob to home", lambda config : config.bob==State.GARDEN)
        
    def execute(self, new_config): 
        new_config.bob = State.HOME
