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

class InputSemTransRelation (SemanticTransitionRelation):
    def initial_configurations(self):
        pass
    def enabled_rules(self, model, source):
        pass
    def execute(self, rule, model, source):
        pass

class InputSoupSemantics (InputSemTransRelation):
    def __init__(self, program):
        self.program = program

    def initial_configurations(self):
        return [self.program.init]

    def enabled_rules(self, model, source):
        filter(lambda rule: rule.guard(model, source), self.program.rules)

    def execute(self, rule, model, source):
        new_source = copy.deepcopy(source)
        n = rule.execute(model, new_source)
        return [new_source]

class AbstractStep:
    pass

class MaybeStutter(AbstractStep):
    pass

class StutterStep(AbstractStep):
    pass

class Step(AbstractStep):
    def __init__(self, source, rule, target):
        self.source = source
        self.rule = rule
        self.target = target

class Rule(MaybeStutter):
    def __init__(self, rule):
        self.rule = rule

class StepSynchronousProduct(SemanticTransitionRelation):

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def initial_configurations(self):
        return [(lhs_init, rhs_init) for lhs_init in self.lhs.initial_configurations() for rhs_init in self.rhs.initial_configurations()]

    def enabled_rules(self, source):
        lhs_source, rhs_source = source
        syncA = []
        lhs_enA = self.lhs.enabled_rules(lhs_source)
        numRules = len(lhs_enA)
        for la in lhs_enA:
            lTarget = self.lhs.execute(la, lhs_source)
            if len(lTarget) == 0:
                numRules -= 1
            for lt in lTarget:
                step = Step(lhs_source, Rule(la), lt)
                rhs_enA = self.rhs.enabled_rules(step, rhs_source)
                syncA.extend(map(lambda ra: (step, ra), rhs_enA))
            if numRules == 0:
                step = Step(lhs_source, StutterStep(), lhs_source)
                rhs_enA = self.rhs.enabled_rules(step, rhs_source)
                syncA.extend(map(lambda ra: (step, ra), rhs_enA))

        return syncA




