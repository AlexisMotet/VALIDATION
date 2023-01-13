from unittest import TestCase


#__GRAPH_______________________________________________________________________________
from graph import DictGraph


class TestNode(TestCase):

    def test_init(self):
        self.fail()

    def test_str(self):
        self.fail()

    def test_repr(self):
        self.fail()

    def test_addchild(self):
        self.fail()

class TestTransitionRelation(TestCase):
    def test_get_roots(self):
        pass

    def test_next(self):
        pass

class TestDictGraph(TestCase):
    dictGraph = DictGraph(0,{0: [1, 2], 1: [0, 1], 2: [1, 0]})

    def test_init(self):
        assert self.dictGraph.roots == 0
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
    def test_init(self):
        self.fail()
    def test_get_roots(self):
        #TODO
        self.fail()

    def test_next(self):
        #TODO
        self.fail()


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
    def test_init(self):
        self.fail()
    def test_get_roots(self):
        self.fail()

    def test_next(self):
        #TODO
        self.fail()

