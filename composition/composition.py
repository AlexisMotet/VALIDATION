import semantic_transition_relation.semantic as semantic
from composition.property import Step, PropertySoupSemantic, PropertyRuleLambda
from copy import copy, deepcopy


class SyncConfig():
    def __init__(self, model_config, property_config):
        self.model_config = model_config
        self.property_config = property_config
        
    def __copy__(self): 
            return SyncConfig(copy(self.model_config), 
                                  copy(self.property_config))
        
    def __deepcopy__(self, memo=None): 
        return SyncConfig(deepcopy(self.model_config, memo),
                          deepcopy(self.property_config, memo))
    
    def __eq__(self, other):
        return self.model_config == other.model_config and \
                self.property_config == other.property_config
    
    def __hash__(self): 
        return hash(frozenset([self.model_config, self.property_config]))
    
    def __str__(self):
        return "Model=[%s] && Property=[%s]" % (self.model_config, 
                                                self.property_config)
    def __repr__(self):
        return self.__str__()
    
class StepSynchronousProduct(semantic.SemanticTransitionRelation):
    def __init__(self, model, property_):
        self.model = model
        self.property_ = property_
    
    def initial_configurations(self):
        configs = []
        for model_config in self.model.initial_configurations():
            for property_config in self.property_.initial_configurations():
                configs.append(SyncConfig(model_config, property_config))
        return configs
    
    # retourne une liste de regles : (model_step, property_rule)
    def enabled_rules(self, source):
        sync_rules = []
        model_config, property_config = source.model_config, source.property_config
        model_rules = self.model.enabled_rules(model_config)
        n_model_rules = len(model_rules)
        for model_rule in model_rules :
            targets = self.model.execute(model_rule, model_config)
            if len(targets) == 0 : n_model_rules -= 1 # deadlock
            for target in targets :
                model_step = Step(model_config, model_rule, target)
                property_rules = self.property_.enabled_rules(model_step, 
                                                              property_config)
                sync_rules += [(model_step, rule) for rule in property_rules]
        if n_model_rules == 0:
            model_step = Step(model_config, semantic.Stutter(), model_config)
            property_rules = self.property_.enabled_rules(model_step, property_config)
            sync_rules += [(model_step, rule) for rule in property_rules]
        return sync_rules
    
    # retourne une liste de configs : (model_config, property_config)
    def execute(self, sync_rule, source) :
        model_step, property_rule = sync_rule
        _, property_config = source.model_config, source.property_config
        targets = self.property_.execute(property_rule, model_step, property_config)
        return [SyncConfig(model_step.target, target) for target in targets]


if __name__ == "__main__":
    start_config = MaConfig(4)
    
    def addition(config): 
        config.x = config.x + 1
    
    def soustraction(config): 
        config.x = config.x - 1
    
    addition = RuleLambda("addition", lambda config : True, addition)
    multiplication = RuleLambda("multiplication", lambda config : True, soustraction)
    soup_program = SoupProgram(start_config)
    soup_program.add(addition)
    soup_program.add(multiplication)
    soup_semantic = SoupSemantic(soup_program)
    rules = []

    start_config_property = configProperty(False)
    
    def etatFalse(model_step, target):
        target.state = False
        target.pc +=1
        
    def etatTrue(model_step, target):
        target.state = True
        target.pc +=1
         
    rules.append(PropertyRuleLambda("x == 6", lambda model_step, target :
        model_step.source.x ==  6, etatTrue))
    
    rules.append(PropertyRuleLambda("x != 6", lambda model_step, target :
        model_step.source.x != 6, etatFalse))
    
    soup_semantic_property = PropertySoupSemantic(start_config_property, rules)
    step_sync = StepSynchronousProduct(soup_semantic, soup_semantic_property)
    transition_relation = STR2TR(step_sync)
    dic_ = {}
    parent_trace_proxy = ParentTraceProxy(transition_relation, dic_)
    o = [None]

    def on_discovery(source, n, o) :
        if n.property_config.state :
            o[0] = n
            soup_program_ = SoupProgram(n)
            soup_semantic_ = SoupSemantic(soup_program)
            step_sync_ = StepSynchronousProduct(soup_semantic_, soup_semantic_property)
            transition_relation_ = STR2TR(step_sync_)
            dic__ = {}
            parent_trace_proxy_ = ParentTraceProxy(transition_relation_, dic__)
            def on_discovery_(new_source, new_n, new_o):
                new_o[0] = new_n
                if new_n == n:
                    print("cycle trouve")
                    return True
                return False
            new_o = [None]
            parent_trace_proxy_.bfs(o=new_o, on_discovery=on_discovery_)
            parent_trace_proxy_.get_trace(new_o[0])
            return True
        return False

    parent_trace_proxy.bfs(o=o, on_discovery=on_discovery)
    res = parent_trace_proxy.get_trace(o[0])
    