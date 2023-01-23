
from config import *
from model import TransitionRelation
from copy import copy
from enum import Enum
from model import Config
from rules import *


class SemanticTransitionRelation(ABC):
    @abstractmethod
    def initial_configurations(self): pass

    @abstractmethod
    def enabled_rules(self, source): pass

    @abstractmethod
    def execute(self, rule, source): pass


class STR2TR(TransitionRelation):
    def __init__(self, semantic):
        self.semantic = semantic

    def get_roots(self):
        return self.semantic.initial_configurations()

    def next(self, source):
        enabled_rules = self.semantic.enabled_rules(source)
        new_rules = []
        for rule in enabled_rules:
            new_rules += self.semantic.execute(rule, source)
        return new_rules
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
        return [self.action(config)]


class Etat(Enum):
    HOME = 0
    GARDEN = 1
    INTERMEDIATE = 2

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
        new_source = copy(source)
        return [rule.execute(new_source)]


if __name__ == "__main__":
    config_start = AliceAndBobConfig(Etat.HOME, Etat.HOME)
    program = SoupProgram(config_start)
    program.add(RuleAliceToGarden())
    program.add(RuleAliceToHome())
    program.add(RuleAliceToIntermediate())
    program.add(RuleBobToGarden())
    program.add(RuleBobToHome())
    program.add(RuleBobToIntermediate())
    soup_semantic = SoupSemantic(program)
    str2tr = STR2TR(soup_semantic)

    from trace_ import ParentTraceProxy
    d = {}
    p = ParentTraceProxy(str2tr, d)
    def on_discovery(source, n, o) :
        res = n.alice == Etat.GARDEN and n.bob == Etat.GARDEN
        o.append(n)
        # if res : o[0] = n
        return res
    
    o = [None]
    p.bfs(o, on_discovery=on_discovery)
    print(o)
    res= p.get_trace(o[-1])

