from unittest import TestCase
from graph import DictGraph
from hanoi import HanoiConfiguration, Hanoi
from nbits import NBits
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
        self.hanoiConfiguration = HanoiConfiguration({1: [3, 2, 1], 
                                                      2: [], 
                                                      3: []})
        self.hanoi = Hanoi([self.hanoiConfiguration])
        self.parentTraceProxy = ParentTraceProxy(self.hanoi, {})
