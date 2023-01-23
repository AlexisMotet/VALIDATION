from abc import abstractmethod, ABC
from model import TransitionRelation, Config
from copy import copy

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


class SoupConfig(Config):
    @abstractmethod
    def __copy__(self):
        pass

    @abstractmethod
    def __eq__(self): pass

    @abstractmethod
    def __hash__(self): pass


class AliceAndBobConfig(SoupConfig):
    def __init__(self, alice, bob, flagAlice=False, flagBob=False):
        self.alice = alice
        self.bob = bob
        self.flagAlice = flagAlice
        self.flagBob = flagBob

    def __copy__(self):
        return AliceAndBobConfig(copy(self.alice),
                                 copy(self.bob))

    def __str__(self):
        return "Config : {Alice %s - flag Alice %s - Bob %s - flag Bob %s}" % (self.alice, self.flagAlice, self.bob, self.flagBob)

    def __repr__(self):
        return "Config : {Alice %s - flag Alice %s - Bob %s - flag Bob %s}" % (self.alice, self.flagAlice, self.bob, self.flagBob)

    def __eq__(self, other):
        return self.alice == other.alice and self.bob == other.bob

    def __hash__(self):
        return hash(frozenset([self.alice, self.bob]))

