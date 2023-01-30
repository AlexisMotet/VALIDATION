from abc import abstractmethod
from copy import deepcopy
from abc import abstractmethod, ABC


class Step():
    def __init__(self, source, action, target):
        self.source = source
        self.action = action
        self.target = target
    def __str__(self):
        return "Step : [source : %s, action : %s, target %s]" % \
              (self.source, self.action, self.target)
    def __repr__(self):
        return self.__str__()
        
class PropertyRuleAbstract(ABC):
    @abstractmethod
    def __init__(self, name, guard):
        self.name = name
        self.guard = guard
        
    @abstractmethod # on ajoute le modele step
    def execute(self, model_step, config): pass
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    

class PropertyRuleLambda(PropertyRuleAbstract):
    def __init__(self, name, guard, action):
        super().__init__(name, guard)
        self.action = action
    def execute(self, model, config):
        return [self.action(model, config)]
        
class PropertySemanticTransitionRelation():
    @abstractmethod
    def initial_configurations(self): pass

    @abstractmethod
    def enabled_actions(self, model, source) : pass
    
    @abstractmethod
    def execute(self, rule, model, source) : pass
    
class PropertySoupSemantic(PropertySemanticTransitionRelation):
    def __init__(self, init, rules):
        self.init = init
        self.rules = rules
        
    def initial_configurations(self):
        return [self.init]
    
    def enabled_rules(self, model_step, source):
        return [rule for rule in self.rules if rule.guard(model_step, source)]
    
    def execute(self, rule, model_step, source):
        target = deepcopy(source)
        rule.execute(model_step, target)
        return [target]
        
    
    
    