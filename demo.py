from unittest import TestCase
from copy import copy, deepcopy

import transition_relation.trace_ as trace_
import transition_relation.dict_graph as dict_graph
import transition_relation.nbits as nbits
import transition_relation.hanoi as hanoi

import semantic_transition_relation.semantic as semantic
import semantic_transition_relation.AandB as AandB
import semantic_transition_relation.AandB_deadlock as AandB_deadlock

import composition.composition as composition
import composition.property as property

class DemoTransitionRelation(TestCase):
    def demo_dict_graph(self):
        print("Le graphe a trouver : 0 ---> 1 ---> 2 -- \\\n"
              "                             |      ^ -- / \n"
              "                             v             \n"
              "                             4 ---> 3      \n")
        print("On cherche le noeud 3")
        graph =  {
            0 : [1],
            1 : [2, 4],
            2 : [2, 1],
            3 : [],
            4 : [3]
        }
        dict_graph_ = dict_graph.DictGraph(roots=[0], dict_=graph)
        parent_trace_proxy = trace_.ParentTraceProxy(dict_graph_)
        parent_trace_proxy.bfs()
        parent_trace_proxy.get_trace(3)
        
    def demo_nbits(self):
        print("On part de 00000 et on cherche 11111 (31)")
        print("L'un des chemins est :\n"
              "\"00000 -> 00001 -> 00011 -> 00111 -> 01111 -> 11111\"")
        nbits_ = nbits.NBits([0], 5)
        parent_trace_proxy = trace_.ParentTraceProxy(nbits_)
        parent_trace_proxy.bfs()
        parent_trace_proxy.get_trace(31)
        nbits_.bfs()
        
    def demo_hanoi(self):
        print("La config de depart est :\n"
              "    |          |          |\n"
              "    |          |          |\n"
              "    |          |          |\n"
              "1   -       2  _          |\n"
              "4 _____     3 ___         |\n"
              " =======    =======    =======\n"
              "    0          1          2  "
              )
    
        print("La config attendue est :\n"
              "    |          |          |\n"
              "    |          |      1   -\n"
              "    |          |      2   _\n"
              "    |          |      3  ___\n"
              "    |          |      4 _____\n"
              " =======    =======    =======\n"
              "    0          1          2  "
              )

        config_start = hanoi.HanoiConfiguration({0: [4, 1], 1: [3, 2], 2: []})
        hanoi_ = hanoi.Hanoi([config_start])
        parent_trace_proxy = trace_.ParentTraceProxy(hanoi_)
        parent_trace_proxy.bfs()
        parent_trace_proxy.get_trace(hanoi.HanoiConfiguration({0: [], 1: [], 2: [4, 3, 2, 1]}))
        
class DemoSemanticTransitionRelation(TestCase):
    def demo_alice_and_bob(self):
        print("La configuration du programme est : \"Alice=(HOME|GARDEN) & Bob=(HOME|GARDEN)\"\n"
              "Les deux peuvent se retrouver dans le jardin en meme temps comme on le montre")
        config_start = AandB.AliceAndBobConfig(AandB.State.HOME, AandB.State.HOME)
        program = semantic.SoupProgram(config_start)
        program.add(AandB.RuleAliceToGarden())
        program.add(AandB.RuleAliceToHome())
        program.add(AandB.RuleBobToGarden())
        program.add(AandB.RuleBobToHome())
        soup_semantic = semantic.SoupSemantic(program)
        tr = semantic.STR2TR(soup_semantic)
        parent_trace_proxy = trace_.ParentTraceProxy(tr)
        parent_trace_proxy.bfs()
        parent_trace_proxy.get_trace(AandB.AliceAndBobConfig(AandB.State.GARDEN, 
                                                             AandB.State.GARDEN))
        
    def demo_alice_and_bob_deadlock(self):
        print("La configuration du programme est :\n"
              "-> \"Alice=(HOME|INTERMEDIATE|GARDEN)"
              " & flag_alice=(True|False)"
              " & Bob=(HOME|INTERMEDIATE|GARDEN)"
              " & flag_bob=(True|False)\"")
        print("On cherche le deadlock theorique qui arrive quand les deux sont en etat intermediaire avec leurs flags up")
        config_start = AandB_deadlock.AliceAndBobConfig(AandB_deadlock.State.HOME, AandB_deadlock.State.HOME,
                                                        flag_alice=False, flag_bob=False)
        program = semantic.SoupProgram(config_start)
        program.add(AandB_deadlock.RuleAliceToGarden())
        program.add(AandB_deadlock.RuleAliceToHome())
        program.add(AandB_deadlock.RuleBobToGarden())
        program.add(AandB_deadlock.RuleBobToHome())
        program.add(AandB_deadlock.RuleBobToIntermediate())
        program.add(AandB_deadlock.RuleAliceToIntermediate())
        soup_semantic = semantic.SoupSemantic(program)
        tr = semantic.STR2TR(soup_semantic)
        parent_trace_proxy = trace_.ParentTraceProxy(tr)
        o = [soup_semantic, None]
        def on_discovery(source, n, o) :
            if len(o[0].enabled_rules(n)) == 0 :
                o[1] = n
                return True
            return False
        parent_trace_proxy.bfs(o, on_discovery=on_discovery)
        parent_trace_proxy.get_trace(o[1])
        
    def demo_alice_and_bob_deadlock_solution(self):
        print("La configuration du programme est :\n"
              "-> \"Alice=(HOME|INTERMEDIATE|GARDEN)"
              " & flag_alice=(True|False)"
              " & Bob=(HOME|INTERMEDIATE|GARDEN)"
              " & flag_bob=(True|False)\"")
        print("En ajoutant une nouvelle regle \"BobIntermediateToHome\" on resout le deadlock")
        config_start = AandB_deadlock.AliceAndBobConfig(AandB_deadlock.State.HOME, AandB_deadlock.State.HOME,
                                                        flag_alice=False, flag_bob=False)
        program = semantic.SoupProgram(config_start)
        program.add(AandB_deadlock.RuleAliceToGarden())
        program.add(AandB_deadlock.RuleAliceToHome())
        program.add(AandB_deadlock.RuleBobToGarden())
        program.add(AandB_deadlock.RuleBobToHome())
        program.add(AandB_deadlock.RuleBobToIntermediate())
        program.add(AandB_deadlock.RuleAliceToIntermediate())
        program.add(AandB_deadlock.RuleBobIntermediateToHome())
        soup_semantic = semantic.SoupSemantic(program)
        tr = semantic.STR2TR(soup_semantic)
        parent_trace_proxy = trace_.ParentTraceProxy(tr)
        o = [soup_semantic, None]
        def on_discovery(source, n, o) :
            if len(o[0].enabled_rules(n)) == 0 :
                o[1] = n
                return True
            return False
        parent_trace_proxy.bfs(o, on_discovery=on_discovery)
        try :
            parent_trace_proxy.get_trace(o[1])
        except KeyError:
            print("KeyError -> plus de deadlock")
        
        
class MaConfig(semantic.SoupConfig):
    def __init__(self, x):
        self.x = x

    def __copy__(self):
        return MaConfig(copy(self.x))

    def __deepcopy__(self, memo=None):
        return MaConfig(deepcopy(self.x, memo))

    def __eq__(self, other):
        return self.x == other.x

    def __hash__(self):
        return hash(frozenset([self.x]))

    def __str__(self):
        return "%d" % (self.x)

    def __repr__(self):
        return self.__str__()

def addition(config): 
    config.x = config.x + 1
    
def soustraction(config): 
    config.x = config.x - 1
    
addition = semantic.RuleLambda("addition", lambda config : True, addition)
multiplication = semantic.RuleLambda("multiplication", lambda config : True, soustraction)    
           
class configProperty(semantic.SoupConfig):
    def __init__(self, start, pc=0):
        self.state = start
        self.pc = pc

    def __copy__(self):
        return configProperty(copy(self.state), copy(self.pc))

    def __deepcopy__(self, memo=None):
        return configProperty(deepcopy(self.state, memo),
                              deepcopy(self.pc, memo))

    def __eq__(self, other):
        return self.state == other.state and self.state == other.state

    def __hash__(self):
        return hash(frozenset([self.state, self.pc]))

    def __str__(self):
        return "state=%s && pc=%d" % (self.state, self.pc)

    def __repr__(self):
        return self.__str__()

start_config_property = configProperty(False)
    
def etatFalse(model_step, target):
    target.state = False
    target.pc +=1
    
def etatTrue(model_step, target):
    target.state = True
    target.pc +=1

rules = []

rules.append(property.PropertyRuleLambda("x == 6", lambda model_step, target :
model_step.source.x ==  6, etatTrue))

rules.append(property.PropertyRuleLambda("x != 6", lambda model_step, target :
    model_step.source.x != 6, etatFalse)) 



class DemoComposition(TestCase):
    def demo_composition(self):
        print("La configuration du programme principal est simplement une variable x\n"
              "Les deux regles sont l'addition : \"x = x + 1\" et \"x = x - 1\"\n"
              "Le property regarde quand x est egal a 6 en passant dans l'etat True")
        start_config = MaConfig(2)
        soup_program = semantic.SoupProgram(start_config)
        soup_program.add(addition)
        soup_program.add(multiplication)
        soup_semantic = semantic.SoupSemantic(soup_program)
        soup_semantic_property = property.PropertySoupSemantic(start_config_property, rules)
        step_sync = composition.StepSynchronousProduct(soup_semantic, soup_semantic_property)
        tr = semantic.STR2TR(step_sync)
        parent_trace_proxy = trace_.ParentTraceProxy(tr)
        o = [None]
        def on_discovery(source, n, o) :
            if n.property_config.state :
                o[0] = n
                soup_program_ = semantic.SoupProgram(n.model_config)
                soup_program_.add(addition)
                soup_program_.add(multiplication)
                soup_semantic_ = semantic.SoupSemantic(soup_program_)
                start_config_property_ = configProperty(False)
                soup_semantic_property_ = property.PropertySoupSemantic(start_config_property_, rules)
                step_sync_ = composition.StepSynchronousProduct(soup_semantic_, 
                                                                soup_semantic_property_)
                tr_ = semantic.STR2TR(step_sync_)
                parent_trace_proxy_ = trace_.ParentTraceProxy(tr_)
                def on_discovery_(new_source, new_n, new_o):
                    new_o[0] = new_n
                    if new_n == n:  
                        return True
                    return False
                new_o = [None]
                parent_trace_proxy_.bfs(o=new_o, on_discovery=on_discovery_)
                parent_trace_proxy_.get_trace(new_o[0])
                return True
            return False
        parent_trace_proxy.bfs(o=o, on_discovery=on_discovery)
        parent_trace_proxy.get_trace(o[0])
            
        print("Il y a un cycle car en partant de l'etat 6 grace a l'addition a l'etat 7\n"
              "on peut retourner a l'etat 6 avec la soustraction")
        