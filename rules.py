from enum import Enum
from config import AliceAndBobConfig
from semantic import RuleAbstract, SoupProgram, SoupSemantic, STR2TR


class Etat(Enum):
    HOME = 0
    GARDEN = 1
    INTERMEDIATE = 2


class RuleAliceToGarden(RuleAbstract):
    def guard(self, config):
        return (config.alice == Etat.INTERMEDIATE) and (config.flagBob == False)

    def __init__(self):
        super().__init__("alice to garden", self.guard)

    def execute(self, new_config):
        new_config.alice = Etat.GARDEN
        new_config.flagAlice = True
        return new_config


class RuleAliceToHome(RuleAbstract):
    def guard(self, config):
        return config.alice == Etat.GARDEN

    def __init__(self):
        super().__init__("alice to home", self.guard)

    def execute(self, new_config):
        new_config.alice = Etat.HOME
        new_config.flagAlice = False
        return new_config


class RuleAliceToIntermediate(RuleAbstract):

    def guard(self, config):
        return config.alice == Etat.HOME

    def __init__(self):
        super().__init__("alice to intermediate", self.guard)

    def execute(self, new_config):
        new_config.alice = Etat.INTERMEDIATE
        new_config.flagAlice = True

        return new_config


class RuleBobToGarden(RuleAbstract):
    def guard(self, config):
        return (config.bob == Etat.INTERMEDIATE) and (config.flagAlice == False)

    def __init__(self):
        super().__init__("bob to garden", self.guard)

    def execute(self, new_config):
        new_config.bob = Etat.GARDEN
        new_config.flagBob = True
        return new_config


class RuleBobToHome(RuleAbstract):
    def guard(self, config):
        return config.bob == Etat.GARDEN

    def __init__(self):
        super().__init__("bob to home", self.guard)

    def execute(self, new_config):
        new_config.bob = Etat.HOME
        new_config.flagBob = False
        return new_config


class RuleBobToIntermediate(RuleAbstract):
    def guard(self, config):
        return config.bob == Etat.HOME

    def __init__(self):
        super().__init__("bob to intermediate", self.guard)

    def execute(self, new_config):
        new_config.bob = Etat.INTERMEDIATE
        new_config.flagBob = True
        return new_config


if __name__ == "__main__":
    config_start = AliceAndBobConfig(Etat.HOME, Etat.HOME, False, False)
    program = SoupProgram(config_start)
    program.add(RuleAliceToGarden())
    program.add(RuleAliceToHome())
    program.add(RuleAliceToIntermediate())
    program.add(RuleBobToGarden())
    program.add(RuleBobToHome())
    program.add(RuleBobToIntermediate())
    soup_semantic = SoupSemantic(program)
    str2tr = STR2TR(soup_semantic)

    #
    # def on_discovery(source, n, o):
    #     print(n)
    #
    # str2tr.bfs(None, on_discovery=on_discovery)

    from trace_ import ParentTraceProxy

    d = {}
    p = ParentTraceProxy(str2tr, d)


    def on_discovery(source, config, o):
        res = config.alice == Etat.INTERMEDIATE and config.bob == Etat.INTERMEDIATE and config.flagAlice and config.flagBob
        if res: o[0] = config
        return res


    o = [None]
    p.bfs(o, on_discovery=on_discovery)
    print(o)
    res = p.get_trace(o[0])
