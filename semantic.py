from abc import abstractmethod, ABC
from builtins import *

class SemanticTransitionRelation(ABC):
    @abstractmethod
    def initial_configurations(self): pass

    @abstractmethod
    def enabled_actions(self, source): pass

    @abstractmethod
    def execute(self, action, source): pass


class Rule():
    def __init__(self, name, guard , action):

        self.name = name
        self.guard = guard
        self.action = action

    def execute(self, config):
        return [self.action(config)]


class SoupConfig():
    pass


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

    def enabled_actions(self, source):
        return filter(lambda rule: rule.guard(source), self.program.rules)

    def execute(self, rule, source):
        new_source = source.copy()
        return rule.execute(new_source)
