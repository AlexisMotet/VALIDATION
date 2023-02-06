from copy import copy, deepcopy
from unittest import TestCase
from AandB_deadlock import AliceAndBobConfig, RuleAliceToGarden, RuleAliceToHome, State, RuleBobToGarden, RuleAliceToIntermediate, RuleBobToHome, RuleBobToIntermediate, RuleBobIntermediateToHome
from AandB import AliceAndBobConfig as ABconf
from AandB import RuleAliceToGarden as ratg
from AandB import RuleAliceToHome as rath
from AandB import RuleBobToGarden as rbtg
from AandB import RuleBobToHome as rbth
from composition import MaConfig, configProperty, StepSynchronousProduct
from graph import DictGraph
from hanoi import HanoiConfiguration, Hanoi
from model import TransitionRelation
from nbits import NBits
from property import PropertyRuleLambda, PropertySoupSemantic
from semantic import SoupProgram, SoupConfig, RuleLambda, SoupSemantic, STR2TR
from trace_ import ParentTraceProxy
# from AandB import State

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
        model_step.source.x > 3, etatTrue))

        rules.append(PropertyRuleLambda("x <= 3", lambda model_step, target:
        model_step.source.x <= 3, etatFalse))

        self.soup_semantic_property = PropertySoupSemantic(start_config_property, rules)

    def test_step_synchronous_product(self):
        step_sync = StepSynchronousProduct(self.soup_semantic, self.soup_semantic_property)
        tr = STR2TR(step_sync)
        d = {}
        p = ParentTraceProxy(tr, d)
        o = [None]

        def on_discovery(source, n, o):
            if n.model_config.x > 4 or n.model_config.x < -4:
                o[0] = n
                return True
            return False

        p.bfs(o=o, on_discovery=on_discovery)
        res = p.get_trace(o[0])

        assert res[0] == 'Le Noeud Model Config : [Ma Config : 4 2] Property Config : [config : [False pc=0]] mene au Noeud Model Config : [Ma Config : 6 2] Property Config : [config : [True pc=1]]'

# __ALICE&BOB_DEADLOCK__________________________________________________________________

class TestAliceBobDeadLock(TestCase):
    """
    Teste la classe AandB_deadlock
    """
    def setUp(self):
        config_start = AliceAndBobConfig(State.HOME, State.HOME, False, False)
        self.program = SoupProgram(config_start)
        # Ajout des différentes règles
        self.program.add(RuleAliceToGarden())
        self.program.add(RuleAliceToHome())
        self.program.add(RuleAliceToIntermediate())
        self.program.add(RuleBobToGarden())
        self.program.add(RuleBobToHome())
        self.program.add(RuleBobToIntermediate())

        # Semantic
        self.soup_semantic = SoupSemantic(self.program)
        str2tr = STR2TR(self.soup_semantic)
        d = {}
        self.p = ParentTraceProxy(str2tr, d)
        self.o = [None, self.soup_semantic, None]

        # On discovery pour trouver le deadlock
        def on_discovery(source, n, o):
            res = n.alice == State.INTERMEDIATE and n.bob == State.INTERMEDIATE
            if res: o[0] = n
            if len(o[1].enabled_rules(n)) == 0:
                print("deadlock trouve pour la config : %s" % n)
                o[2] = n
            return res

        self.p.bfs(self.o, on_discovery=on_discovery)
        self.res = self.p.get_trace(self.o[2])

    def test_alice_bob_deadlock(self):
        res = self.p.get_trace(self.o[2])
        print('res', res[0])
        assert res[0] == 'Le Noeud [Alice State.INTERMEDIATE Flag True - Bob State.HOME Flag False] mene au Noeud [Alice State.INTERMEDIATE Flag True - Bob State.INTERMEDIATE Flag True]'

    def test_alice_bob_no_deadlock(self):
        self.program.add(RuleBobIntermediateToHome())
        self.soup_semantic = SoupSemantic(self.program)
        str2tr = STR2TR(self.soup_semantic)
        d = {}
        self.p = ParentTraceProxy(str2tr, d)
        self.o = [None, self.soup_semantic, None]
        res = self.p.get_trace(self.o[2])
        assert res == []

# __ALICE&BOB___________________________________________________________________________

class TestAliceBob(TestCase):
    """
    Teste la classe AandB
    """
    def setUp(self):
        config_start = ABconf(State.HOME, State.HOME)
        program = SoupProgram(config_start)
        program.add(ratg())
        program.add(rath())
        program.add(rbtg())
        program.add(rbth())
        soup_semantic = SoupSemantic(program)
        str2tr = STR2TR(soup_semantic)
        d = {}
        p = ParentTraceProxy(str2tr, d)

        def on_discovery(source, n, o):
            res = n.alice == State.INTERMEDIATE and n.bob == State.INTERMEDIATE
            if res: o[0] = n
            return res

        o = [None]
        p.bfs(o, on_discovery=on_discovery)
        self.res = p.get_trace(o[0])

    def test_rule_alice_to_garden(self):
        config_start = ABconf(State.HOME, State.HOME)
        rule = ratg() #Alias de RuleAliceToGarden
        rule.execute(config_start)
        assert ((config_start.alice == State.GARDEN) and (config_start.bob == State.HOME))

    def test_rule_alice_to_home(self):
        config_start = ABconf(State.GARDEN, State.HOME)
        rule = rath() #Alias de RuleAliceToHome
        rule.execute(config_start)
        assert config_start.alice == State.HOME and config_start.bob == State.HOME

    def test_rule_bob_to_garden(self):
        config_start = ABconf(State.HOME, State.HOME)
        rule = rbtg() #Alias de RuleAliceToHome
        rule.execute(config_start)
        assert config_start.alice == State.HOME and config_start.bob == State.GARDEN

    def test_rule_bob_to_home(self):
        config_start = ABconf(State.HOME, State.GARDEN)
        rule = rbth() #Alias de RuleAliceToHome
        rule.execute(config_start)
        assert config_start.alice == State.HOME and config_start.bob == State.HOME

    def test_alice_bob(self):
       assert self.res[0] in ['Le Noeud Config : {Alice State.GARDEN - Bob State.HOME} mene au Noeud Config : {Alice State.GARDEN - Bob State.GARDEN}', 'Le Noeud Config : {Alice State.HOME - Bob State.GARDEN} mene au Noeud Config : {Alice State.GARDEN - Bob State.GARDEN}' ]






