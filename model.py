from abc import abstractmethod, ABC

class TransitionRelation(ABC) :
    @abstractmethod
    def get_roots(self):
        pass
    @abstractmethod
    def next(self, source):
        pass

    
