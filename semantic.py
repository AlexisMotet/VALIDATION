from abc import abstractmethod, ABC
from model import TransitionRelation
from copy import deepcopy
from model import Config


class SemanticTransitionRelation(ABC):
    @abstractmethod
    def initial_configurations(self): pass

    @abstractmethod
    def enabled_rules(self, source) : pass
    
    @abstractmethod
    def execute(self, rule, source) : pass
    
class STR2TR(TransitionRelation):
    def __init__(self, semantic):
        self.semantic = semantic
    def get_roots(self):
        return self.semantic.initial_configurations()
    def next(self, source):
        enabled_rules = self.semantic.enabled_rules(source)
        new_configs = []
        for rule in enabled_rules:
            new_configs += self.semantic.execute(rule, source)
        return new_configs
        # retourne les nouvelles configs

class RuleAbstract(ABC):
    @abstractmethod
    def __init__(self, name, guard):
        self.name = name
        self.guard = guard
        
    @abstractmethod
    def execute(self, config): pass
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    

class RuleLambda(RuleAbstract):
    def __init__(self, name, guard, action):
        super().__init__(name, guard)
        self.action = action
    def execute(self, config):
        self.action(config)
        return [config]
    
    
class Stutter(RuleAbstract):
    def __init__(self):
        super().__init__(None, None)
    
    def execute(self, config):
        return [config]
        
class SoupConfig(Config):
    @abstractmethod
    def __copy__(self): 
        pass
    
    @abstractmethod
    def __deepcopy__(self, memo=None): 
        pass
    
    @abstractmethod
    def __eq__(self): pass
    
    @abstractmethod
    def __hash__(self): pass
    
class SoupProgram():
    def __init__(self, init):
        self.init = init
        self.rules = []

    def add(self, rule):
        self.rules.append(rule)

class SoupSemantic(SemanticTransitionRelation):
    def __init__(self, program):
        self.program = program

    def initial_configurations(self):
        return [self.program.init]
    
    def enabled_rules(self, source):
        return [rule for rule in self.program.rules if rule.guard(source)]
    
    def execute(self, rule, source):
        target = deepcopy(source)
        rule.execute(target)
        return [target]
