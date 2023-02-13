from copy import copy, deepcopy
from unittest import TestCase
import semantic_transition_relation.AandB_deadlock as AandB_d
import semantic_transition_relation.AandB as AandB
import semantic_transition_relation.semantic as semantic
import composition.composition as composition
import composition.property as prop
import transition_relation.graph as graph
import transition_relation.hanoi as hanoi
import transition_relation.nbits as nbits
import transition_relation.trace_ as trace
import transition_relation.model as model
import demo as demo


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
        dictGraph = graph.DictGraph([0], self.d)
        k, _ = dictGraph.bfs(None)
        k_to_found = set([0, 1, 2, 3, 4])
        assert k == k_to_found
        dictGraph = graph.DictGraph([32], self.d)
        k_to_found = set([5, 7, 10, 32])
        k, _ = dictGraph.bfs(None)
        assert k == k_to_found

# __GRAPH_______________________________________________________________________________

class TestDictGraph(TestCase):
    def setUp(self):
        self.dictGraph = graph.DictGraph([0], {0: [1, 2], 1: [0, 1], 2: [1, 0]})

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
        self.nbits = nbits.NBits([0], 3)

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
        self.hanoiConfiguration = hanoi.HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})
        self.hanoi = hanoi.Hanoi([self.hanoiConfiguration])

    def test_init(self):
        assert self.hanoi.roots == [self.hanoiConfiguration]

    def test_get_roots(self):
        assert self.hanoi.get_roots() == [self.hanoiConfiguration]

    def test_next(self):
        source = hanoi.HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})
        childs = [hanoi.HanoiConfiguration({1: [3, 2], 2: [1], 3: []}),
                  hanoi.HanoiConfiguration({1: [3, 2], 2: [], 3: [1]})]
        for hanoiConfiguration in self.hanoi.next(source):
            assert hanoiConfiguration in childs
        source = hanoi.HanoiConfiguration({1: [3, 2], 2: [1], 3: []})
        childs = [hanoi.HanoiConfiguration({1: [3], 2: [1], 3: [2]}),
                  hanoi.HanoiConfiguration({1: [3, 2], 2: [], 3: [1]}),
                  hanoi.HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})]
        for hanoiConfiguration in self.hanoi.next(source):
            assert hanoiConfiguration in childs

# __TRACE_______________________________________________________________________________
class TesttraceParentTraceProxy(TestCase):
    def setUp(self):
        # Hanoi
        self.hanoiConfiguration = hanoi.HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})
        self.hanoi = hanoi.Hanoi([self.hanoiConfiguration])
        self.d = {}
        # Nbits
        self.nbits = nbits.NBits([0], 2)

    def test_parent_trace_proxy_hanoi(self):
        parentTraceProxy = trace.ParentTraceProxy(self.hanoi)
        model.TransitionRelation.bfs(parentTraceProxy, None)
        res = parentTraceProxy.get_trace(hanoi.HanoiConfiguration({1: [], 2: [], 3: [3, 2, 1]}))
        # On vérifie que la transition finale est l'une des deux transition ci-dessous.
        print('res',res[0])
        assert res[0] in ['[TRACE] Le noeud "{1: [1], 2: [], 3: [3, 2]}" mene au noeud "{1: [], 2: [], 3: [3, 2, 1]}"', '[TRACE] Le noeud "{1: [], 2: [1], 3: [3, 2]}" mene au noeud "{1: [], 2: [], 3: [3, 2, 1]}"']

    def test_parent_trace_proxy_nbits(self):
        parentTraceProxy = trace.ParentTraceProxy(self.nbits)
        model.TransitionRelation.bfs(parentTraceProxy, None)
        res = parentTraceProxy.get_trace(3)
        print('res',res)
        assert res[0] == '[TRACE] Le noeud "1" mene au noeud "3"'

# __PROPERTY_COMPOSITION____________________________________________________________________________

class TestPropertyComposition(TestCase):
    def setUp(self):

        start_config = demo.MaConfig(2)

        def addition(config): config.x = config.x + 1

        def soustraction(config): config.x = config.x - 1

        addition = semantic.RuleLambda("addition", lambda config: True, addition)
        multiplication = semantic.RuleLambda("multiplication", lambda config: True, soustraction)
        soup_program = semantic.SoupProgram(start_config)
        soup_program.add(addition)
        soup_program.add(multiplication)
        self.soup_semantic = semantic.SoupSemantic(soup_program)

        rules = []

        start_config_property = demo.configProperty(False)

        def etatFalse(model_step, target):
            target.state = False
            target.pc += 1

        def etatTrue(model_step, target):
            target.state = True
            target.pc += 1

        rules.append(prop.PropertyRuleLambda("x == 3", lambda model_step, target:
        model_step.source.x == 3, etatTrue))

        rules.append(prop.PropertyRuleLambda("x != 3", lambda model_step, target:
        model_step.source.x != 3, etatFalse))

        self.soup_semantic_property = prop.PropertySoupSemantic(start_config_property, rules)

    def test_step_synchronous_product(self):
        step_sync = composition.StepSynchronousProduct(self.soup_semantic, self.soup_semantic_property)
        tr = semantic.STR2TR(step_sync)
        d = {}
        p = trace.ParentTraceProxy(tr)
        o = [None]

        def on_discovery(source, n, o):
            if n.model_config.x > 4 or n.model_config.x < -4:
                o[0] = n
                return True
            return False

        p.bfs(o=o, on_discovery=on_discovery)
        res = p.get_trace(o[0])
        print('res', res[0])
        assert res[0] == '[TRACE] Le noeud "Model=[4] && Property=[state=True && pc=2]" mene au noeud "Model=[5] && Property=[state=False && pc=3]"'

# __ALICE&BOB_DEADLOCK__________________________________________________________________

class TestAliceBobDeadLock(TestCase):
    """
    Teste la classe AandB_deadlock
    """
    def setUp(self):
        config_start = AandB_d.AliceAndBobConfig(AandB_d.State.HOME, AandB_d.State.HOME, False, False)
        self.program = semantic.SoupProgram(config_start)
        # Ajout des différentes règles
        self.program.add(AandB_d.RuleAliceToGarden())
        self.program.add(AandB_d.RuleAliceToHome())
        self.program.add(AandB_d.RuleAliceToIntermediate())
        self.program.add(AandB_d.RuleBobToGarden())
        self.program.add(AandB_d.RuleBobToHome())
        self.program.add(AandB_d.RuleBobToIntermediate())

        # Semantic
        self.soup_semantic = semantic.SoupSemantic(self.program)
        str2tr = semantic.STR2TR(self.soup_semantic)
        self.p = trace.ParentTraceProxy(str2tr)
        self.o = [self.soup_semantic, None]

        # On discovery pour trouver le deadlock
        def on_discovery(source, n, o):
            if len(o[0].enabled_rules(n)) == 0:
                print("deadlock trouve pour la config : %s" % n)
                o[1] = n
                return True
            return False

        self.p.bfs(self.o, on_discovery=on_discovery)
        self.res = self.p.get_trace(self.o[1])

    def test_alice_bob_deadlock(self):
        self.o != None

    def test_alice_bob_no_deadlock(self):
        self.program.add(AandB_d.RuleBobIntermediateToHome())
        self.soup_semantic = semantic.SoupSemantic(self.program)
        str2tr = semantic.STR2TR(self.soup_semantic)

        def on_discovery(source, n, o):
            if len(o[0].enabled_rules(n)) == 0:
                print("deadlock trouve pour la config : %s" % n)
                o[1] = n
                return True
            return False

        self.p = trace.ParentTraceProxy(str2tr)
        self.p.bfs(self.o, on_discovery=on_discovery)
        self.o = [self.soup_semantic, None]
        # res = self.p.get_trace(self.o[1])
        assert self.o[1] == None

# __ALICE&BOB___________________________________________________________________________

class TestAliceBob(TestCase):
    """
    Teste la classe AandB
    """
    def setUp(self):
        config_start = AandB.AliceAndBobConfig(AandB.State.HOME, AandB.State.HOME)
        program = semantic.SoupProgram(config_start)
        program.add(AandB.RuleAliceToGarden())
        program.add(AandB.RuleAliceToHome())
        program.add(AandB.RuleBobToGarden())
        program.add(AandB.RuleBobToHome())
        soup_semantic = semantic.SoupSemantic(program)
        str2tr = semantic.STR2TR(soup_semantic)
        d = {}
        p = trace.ParentTraceProxy(str2tr)

        def on_discovery(source, n, o):
            res = n.alice == AandB.State.GARDEN and n.bob == AandB.State.GARDEN
            if res: o[0] = n
            return res

        o = [None]
        p.bfs(o, on_discovery=on_discovery)
        self.res = p.get_trace(o[0])

    def test_rule_alice_to_garden(self):
        config_start = AandB.AliceAndBobConfig(AandB.State.HOME, AandB.State.HOME)
        rule = AandB.RuleAliceToGarden() #Alias de RuleAliceToGarden
        rule.execute(config_start)
        assert ((config_start.alice == AandB.State.GARDEN) and (config_start.bob == AandB.State.HOME))

    def test_rule_alice_to_home(self):
        config_start = AandB.AliceAndBobConfig(AandB.State.GARDEN, AandB.State.HOME)
        rule = AandB.RuleAliceToHome() #Alias de RuleAliceToHome
        rule.execute(config_start)
        assert config_start.alice == AandB.State.HOME and config_start.bob == AandB.State.HOME

    def test_rule_bob_to_garden(self):
        config_start = AandB.AliceAndBobConfig(AandB.State.HOME, AandB.State.HOME)
        rule = AandB.RuleBobToGarden() #Alias de RuleAliceToHome
        rule.execute(config_start)
        assert config_start.alice == AandB.State.HOME and config_start.bob == AandB.State.GARDEN

    def test_rule_bob_to_home(self):
        config_start = AandB.AliceAndBobConfig(AandB.State.HOME, AandB.State.GARDEN)
        rule = AandB.RuleBobToHome() #Alias de RuleAliceToHome
        rule.execute(config_start)
        assert config_start.alice == AandB.State.HOME and config_start.bob == AandB.State.HOME

    def test_alice_bob(self):
        print('res', self.res[0])
        assert self.res[0] in ['[TRACE] Le noeud "Alice=State.GARDEN - Bob=State.HOME" mene au noeud "Alice=State.GARDEN - Bob=State.GARDEN"', '[TRACE] Le noeud "Alice=State.HOME - Bob=State.GARDEN" mene au noeud "Alice=State.GARDEN - Bob=State.GARDEN"']






