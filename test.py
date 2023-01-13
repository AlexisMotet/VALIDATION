from unittest import TestCase


#__GRAPH_______________________________________________________________________________
from graph import DictGraph, Node
from hanoi import HanoiConfiguration, Hanoi
from nbits import NBits


class TestNode(TestCase):
    def setUp(self):
        self.dad = Node(3)
        self.child_dad = Node(1)

    def test_init(self):
        assert self.dad.value == 3
        assert self.dad.children == []

    def test_str(self):
        assert str(self.dad) == "Node 3"

    def test_repr(self):
        assert repr(self.dad) == "Node 3"

    def test_addchild(self):
        self.dad.addchild(self.child_dad)
        assert self.dad.children == [self.child_dad]

class TestTransitionRelation(TestCase):
    def test_get_roots(self):
     pass

    def test_next(self):
     pass

class TestDictGraph(TestCase):
    def setUp(self):
        self.dictGraph = DictGraph([0],{0: [1, 2], 1: [0, 1], 2: [1, 0]})

    def test_init(self):
     assert self.dictGraph.roots == [0]
     assert self.dictGraph.d == {0: [1, 2], 1: [0, 1], 2: [1, 0]}

    def test_get_roots(self):
     assert self.dictGraph.get_roots() == 0

    def test_next(self):
     assert self.dictGraph.next(0) == [1, 2]
     assert self.dictGraph.next(1) == [0, 1]
     assert self.dictGraph.next(2) == [1, 0]

class TestGraphFunction(TestCase):
    def test_width_traversal(self):
        self.fail()

    def test_traversal_depth(self):
        self.fail()

    def test_bfs(self):
        #TODO
        self.fail()



#__NBITS_______________________________________________________________________________

class TestNBits(TestCase):

    def setUp(self):
        self.nbits = NBits([0], 3)

    def test_init(self):
        assert self.nbits.roots == [0]
        assert self.nbits.n == 3

    def test_get_roots(self):
        assert self.nbits.get_roots() == 0

    def test_next(self):
        assert self.nbits.next(0) == [1, 2, 4]
        assert self.nbits.next(1) == [0, 3, 5]

#__HANOI_______________________________________________________________________________
class TestHanoiConfiguration(TestCase):
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


class TestHanoi(TestCase):
    def setUp(self) -> None:
        self.hanoiConfiguration = HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})
        self.hanoi = Hanoi([self.hanoiConfiguration])

    def test_init(self):
        assert self.hanoi.roots == [self.hanoiConfiguration]

    def test_get_roots(self):
        assert self.hanoi.get_roots() == [self.hanoiConfiguration]

    def test_next(self):
        for hanoiConfiguration in self.hanoi.next(HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})):
            assert hanoiConfiguration in [HanoiConfiguration({1: [3, 2], 2: [1], 3: []}), HanoiConfiguration({1: [3, 2], 2: [], 3: [1]})]

        for hanoiConfiguration in self.hanoi.next(HanoiConfiguration({1: [3, 2], 2: [1], 3: []})):
            assert hanoiConfiguration in [HanoiConfiguration({1: [3], 2: [1], 3: [2]}), HanoiConfiguration({1: [3, 2], 2: [], 3: [1]}), HanoiConfiguration({1: [3, 2, 1], 2: [], 3: []})]
