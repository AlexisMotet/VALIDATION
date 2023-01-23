from config import AliceAndBobConfig
from semantic import RuleAbstract, Etat, SoupProgram, SoupSemantic, STR2TR


class RuleAliceToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("alice to garden",
                         lambda config: (config.alice == Etat.INTERMEDIATE) and (config.flagBob == False))

    def execute(self, new_config):
        new_config.alice = Etat.GARDEN
        return new_config


class RuleAliceToHome(RuleAbstract):
    def __init__(self):
        super().__init__("alice to home", lambda config: config.alice == Etat.GARDEN)

    def execute(self, new_config):
        new_config.alice = Etat.HOME
        new_config.flagAlice = False
        return new_config


class RuleAliceToIntermediate(RuleAbstract):

    def toto(self, config):
        print('config',config.alice)
        print(config.alice == Etat.HOME)
        return config.alice == Etat.HOME

    def __init__(self):
        super().__init__("alice to intermediate", self.toto)
        # super().__init__("alice to intermediate", lambda config: config.alice == Etat.HOME)

    def execute(self, new_config):
        new_config.alice = Etat.INTERMEDIATE
        new_config.flagAlice = True
        return new_config


class RuleBobToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("bob to garden",
                         lambda config: (config.bob == Etat.INTERMEDIATE) and (config.flagAlice == False))

    def execute(self, new_config):
        new_config.bob = Etat.GARDEN
        return new_config


class RuleBobToHome(RuleAbstract):
    def __init__(self):
        super().__init__("bob to home", lambda config: config.bob == Etat.GARDEN)

    def execute(self, new_config):
        new_config.bob = Etat.HOME
        new_config.flagBob = False
        return new_config


class RuleBobToIntermediate(RuleAbstract):
    def __init__(self):
        super().__init__("bob to intermediate", lambda config: config.bob == Etat.HOME)

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

    print("config alice and bob", config_start.alice, config_start.bob)
    print('enabled rules',soup_semantic.enabled_rules(config_start))
    from trace_ import ParentTraceProxy
    d = {}
    p = ParentTraceProxy(str2tr, d)
    def on_discovery(source, config, o) :
        res = config.alice == Etat.HOME and config.bob == Etat.GARDEN
        if res : o[0] = config
        print("config", config)
        return res

    o = [None]
    p.bfs(o, on_discovery=on_discovery)
    print(o)
    res= p.get_trace(o[-1])
