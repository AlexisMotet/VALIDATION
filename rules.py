from semantic import RuleAbstract, Etat


class RuleAliceToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("alice to garden", lambda config: (config.alice == Etat.INTERMEDIATE) and (config.flagBob == False))

    def execute(self, new_config):
        new_config.alice = Etat.GARDEN
        new_config.flagAlice = True
        return new_config


class RuleAliceToHome(RuleAbstract):
    def __init__(self):
        super().__init__("alice to home", lambda config: config.alice == Etat.GARDEN)

    def execute(self, new_config):
        new_config.alice = Etat.HOME
        new_config.flagAlice = False
        return new_config

class RuleAliceToIntermediate(RuleAbstract):
    def __init__(self):
        super().__init__("alice to intermediate", lambda config: config.alice == Etat.HOME)

    def execute(self, new_config):
        new_config.alice = Etat.INTERMEDIATE
        new_config.flagAlice = True
        return new_config


class RuleBobToGarden(RuleAbstract):
    def __init__(self):
        super().__init__("bob to garden", lambda config: (config.bob == Etat.INTERMEDIATE) and (config.flagAlice == False))

    def execute(self, new_config):
        new_config.bob = Etat.GARDEN
        new_config.flagBob = True
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
