from abc import abstractmethod, ABC
from copy import copy
from model import Config


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

