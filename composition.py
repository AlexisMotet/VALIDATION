from semantic import SemanticTransitionRelation, Stutter
from property import Step

class SyncConfig():
    def __init__(self, model_config, property_config):
        self.model_config = model_config
        self.property_config = property_config
        
    def __copy__(self): 
            return configProperty(copy(self.model_config), 
                                  copy(self.property_config))
        
    def __deepcopy__(self, memo=None): 
        return configProperty(deepcopy(self.model_config, memo),
                                deepcopy(self.property_config, memo))
    
    def __eq__(self, other):
        return self.model_config == other.model_config and \
                self.property_config == other.property_config
    
    def __hash__(self): 
        return hash(frozenset([self.model_config, self.property_config]))
    
    def __str__(self):
        return "Model Config : [%s] Property Config : [%s]" % (self.model_config, 
                                                               self.property_config)

class StepSynchronousProduct(SemanticTransitionRelation):
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
        print(source)
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
            model_step = Step(model_config, Stutter(), model_config)
            property_rules = self.property_.enabled_rules(model_step, property_config)
            sync_rules += [(model_step, rule) for rule in property_rules]
        return sync_rules
    
    # retourne une liste de configs : (model_config, property_config)
    def execute(self, sync_rule, source) :
        model_step, property_rule = sync_rule
        _, property_config = source.model_config, source.property_config
        targets = self.property_.execute(property_rule, model_step, property_config)
        return [SyncConfig(model_step.target, target) for target in
                targets]
        
if __name__ == "__main__": 
    from semantic import SoupProgram, SoupSemantic, RuleLambda, SoupConfig
    from copy import copy, deepcopy
    class MaConfig(SoupConfig):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            
        def __copy__(self): 
            return MaConfig(copy(self.x), copy(self.y))
        
        def __deepcopy__(self, memo=None): 
            return MaConfig(deepcopy(self.x, memo), deepcopy(self.y, memo))
        
        def __eq__(self, other):
            return self.x == other.x and self.y == other.y
        
        def __hash__(self): 
            return hash(frozenset([self.x, self.y]))
        
        def __str__(self):
            return "Ma Config : %d %d" % (self.x, self.y)
    
        def __repr__(self):
            return "Ma Config : %d %d" % (self.x, self.y)
        
    start_config = MaConfig(4, 2)
    
    def addition(config):
        config.x = config.x + config.y
    
    def soustraction(config):
        config.y = config.y - config.x
    
    addition = RuleLambda("addition", lambda config : True, addition)
    multiplication = RuleLambda("multiplication", lambda config : True, soustraction)
    soup_program = SoupProgram(start_config)
    soup_program.add(addition)
    soup_program.add(multiplication)
    soup_semantic = SoupSemantic(soup_program)

    from property import PropertySoupSemantic, PropertyRuleLambda
  
    rules = []
    class configProperty(SoupConfig):
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
            return "config : [%s pc=%d]" % (self.state, self.pc)
        
        def __repr__(self):
            return self.__str__()

    start_config_property = configProperty(False)
    
    def etatFalse(model_step, target):
        target.state = False
        target.pc +=1
        
    def etatTrue(model_step, target):
        target.state = True
        target.pc +=1
         
    rules.append(PropertyRuleLambda("x > 3", lambda model_step, target :
        model_step.source.x > 8, etatTrue))
    
    rules.append(PropertyRuleLambda("x <= 3", lambda model_step, target :
        model_step.source.x <= 8, etatFalse))
    
    soup_semantic_property = PropertySoupSemantic(start_config_property, rules)
    step_sync = StepSynchronousProduct(soup_semantic, soup_semantic_property)
    from semantic import STR2TR
    tr = STR2TR(step_sync)
    
    from trace_ import ParentTraceProxy
    d = {}
    p = ParentTraceProxy(tr, d)
    o = [None]
    def on_discovery(source, n, o) :
        if n.model_config.x > 10 or n.model_config.x < -10 :
            o[0] = n
            return True
        return False
    p.bfs(o=o, on_discovery=on_discovery)
    res= p.get_trace(o[0])
    