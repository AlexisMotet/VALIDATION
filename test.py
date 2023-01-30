from copy import copy, deepcopy
from unittest import TestCase

from AandB import AliceAndBobConfig, RuleAliceToGarden, RuleAliceToHome, State
from composition import MaConfig, configProperty, StepSynchronousProduct
from graph import DictGraph
from hanoi import HanoiConfiguration, Hanoi
from model import TransitionRelation
from nbits import NBits
from property import PropertyRuleLambda, PropertySoupSemantic
from semantic import SoupProgram, SoupConfig, RuleLambda, SoupSemantic, STR2TR
from trace_ import ParentTraceProxy

# pour run : python -m unittest test.py

# __MODEL_______________________________________________________________________________

class TestTransitionRelation(TestCase):
    def setUp(self):
        self.d = {0: [1, 2],
             1: [0, 1],
             2: [1, 0, 3],
             3: [0, 1, 2, 4],
             4: [3],
             5: [10],
             7: [],
             32: [7, 5],
             10: [32]}
    def test_bfs(self):
        dictGraph = DictGraph([0], self.d)
        k, _ = dictGraph.bfs(None)
        k_to_found = set([0, 1, 2, 3, 4])
        assert k == k_to_found
        dictGraph = DictGraph([32], self.d)
        k_to_found = set([5, 7, 10, 32])
        k, _ = dictGraph.bfs(None)
        assert k == k_to_found

# __GRAPH_______________________________________________________________________________

class TestDictGraph(TestCase):
    def setUp(self):
        self.dictGraph = DictGraph([0], {0: [1, 2], 1: [0, 1], 2: [1, 0]})

    def test_init(self):
        assert self.dictGraph.roots == [0]
        assert self.dictGraph.d == {0: [1, 2], 1: [0, 1], 2: [1, 0]}

    def test_get_roots(self):
        assert self.dictGraph.get_roots() == [0]

    def test_next(self):
        assert self.dictGraph.next(0) == [1, 2]
        assert self.dictGraph.next(1) == [0, 1]
        assert self.dictGraph.next(2) == [1, 0]

# __NBITS_______________________________________________________________________________

class TestNBits(TestCase):
    def setUp(self):
        self.nbits = NBits([0], 3)

    def test_init(self):
        assert self.nbits.roots == [0]
        assert self.nbits.n == 3

    def test_get_roots(self):
        assert self.nbits.get_roots() == [0]

    def test_next(self):
        assert self.nbits.next(0) == [1, 2, 4]
        assert self.nbits.next(1) == [0, 3, 5]


# __HANOI_______________________________________________________________________________
class TestHanoiConfiguration(TestCase):
    """
    TODO
    def test_init(self):
        self.fail()

    def test_hash(self):
        self.fail()

    def test_str(self):
        self.fail()

    def test_repr(self):
        self.fail()

    def test_eq(self):
        self.fail()
    """
class TestHanoi(TestCase):
    def setUp(self) -> None:
        self.hanoiConfiguration = HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})
        self.hanoi = Hanoi([self.hanoiConfiguration])

    def test_init(self):
        assert self.hanoi.roots == [self.hanoiConfiguration]

    def test_get_roots(self):
        assert self.hanoi.get_roots() == [self.hanoiConfiguration]

    def test_next(self):
        source = HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})
        childs = [HanoiConfiguration({1: [3, 2], 2: [1], 3: []}),
                  HanoiConfiguration({1: [3, 2], 2: [], 3: [1]})]
        for hanoiConfiguration in self.hanoi.next(source):
            assert hanoiConfiguration in childs
        source = HanoiConfiguration({1: [3, 2], 2: [1], 3: []})
        childs = [HanoiConfiguration({1: [3], 2: [1], 3: [2]}),
                  HanoiConfiguration({1: [3, 2], 2: [], 3: [1]}),
                  HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})]
        for hanoiConfiguration in self.hanoi.next(source):
            assert hanoiConfiguration in childs

# __TRACE_______________________________________________________________________________
class TestParentTraceProxy(TestCase):
    def setUp(self):
        # Hanoi
        self.hanoiConfiguration = HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})
        self.hanoi = Hanoi([self.hanoiConfiguration])
        self.d = {}
        # Nbits
        self.nbits = NBits([0], 2)

    def test_parent_trace_proxy_hanoi(self):
        parentTraceProxy = ParentTraceProxy(self.hanoi, self.d)
        TransitionRelation.bfs(parentTraceProxy, None)
        res = parentTraceProxy.get_trace(HanoiConfiguration({1: [], 2: [], 3: [3, 2, 1]}))

        # On vérifie que la transition finale est l'une des deux transition ci-dessous.
        assert res[0] in ['Le Noeud {1: [1], 2: [], 3: [3, 2]} mene au Noeud {1: [], 2: [], 3: [3, 2, 1]}', 'Le Noeud {1: [], 2: [1], 3: [3, 2]} mene au Noeud {1: [], 2: [], 3: [3, 2, 1]}']

    def test_parent_trace_proxy_nbits(self):
        parentTraceProxy = ParentTraceProxy(self.nbits, self.d)
        TransitionRelation.bfs(parentTraceProxy, None)
        res = parentTraceProxy.get_trace(3)
        assert res[0] == 'Le Noeud 1 mene au Noeud 3'

# __PROPERTY_COMPOSITION____________________________________________________________________________

class TestPropertyComposition(TestCase):
    def setUp(self):

        start_config = MaConfig(4, 2)

        def addition(config): config.x = config.x + config.y

        def soustraction(config): config.y = config.y - config.x

        addition = RuleLambda("addition", lambda config: True, addition)
        multiplication = RuleLambda("multiplication", lambda config: True, soustraction)
        soup_program = SoupProgram(start_config)
        soup_program.add(addition)
        soup_program.add(multiplication)
        self.soup_semantic = SoupSemantic(soup_program)

        rules = []

        start_config_property = configProperty(False)

        def etatFalse(model_step, target):
            target.state = False
            target.pc += 1

        def etatTrue(model_step, target):
            target.state = True
            target.pc += 1

        rules.append(PropertyRuleLambda("x > 3", lambda model_step, target:
        model_step.source.x > 8, etatTrue))

        rules.append(PropertyRuleLambda("x <= 3", lambda model_step, target:
        model_step.source.x <= 8, etatFalse))

        self.soup_semantic_property = PropertySoupSemantic(start_config_property, rules)

    def test_step_synchronous_product(self):
        step_sync = StepSynchronousProduct(self.soup_semantic, self.soup_semantic_property)
        tr = STR2TR(step_sync)
        d = {}
        p = ParentTraceProxy(tr, d)
        o = [None]

        def on_discovery(source, n, o):
            if n.model_config.x > 10 or n.model_config.x < -10:
                o[0] = n
                return True
            return False

        p.bfs(o=o, on_discovery=on_discovery)
        res = p.get_trace(o[0])

        assert res == False

# __ALICE&BOB_DEADLOCK__________________________________________________________________

# __ALICE&BOB_NO_DEADLOCK_______________________________________________________________



