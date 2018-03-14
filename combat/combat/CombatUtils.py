
from enum import Enum
from Player import Player

class CompOp(Enum):
    NONE = ''
    EQU = '=='
    NEQ = '!='
    LSS = '<'
    LTQ = '<='
    GTR = '>'
    GTQ = '<='


class BoolOp(Enum):
    NONE = ''
    NOT = '~'
    AND = '&&'
    OR = '||' # NAND, NOR, XOR, XNOR

class ConditionalStatement():
    '''
    Reference can be whatever you want. Just needs to be a pointer to something. Examples:
    ConditionalStatement(self.myHealth, CompOp.EQU, 0)
    ConditionalStatement(self.myTarget, CompOp.EQU, self)
    ConditionalStatement(len(self.myTargets), CompOp.LSS, 5)
    '''
    def __init__(self, _reference=None, _operator:CompOp=CompOp.NONE, _value=None):
        self.ref = _reference #reference to item to evaluate
        self.op = _operator
        self.val = _value #what the expected value of the item is to evaluate to true

    def Evaluate(self):
        try:
            if   ((self.op == CompOp.EQU) or (self.op == '==')):
                return self.ref == self.val
            elif ((self.op == CompOp.NEQ) or (self.op == '!=')):
                return self.ref != self.val
            elif ((self.op == CompOp.LSS) or (self.op == '<')):
                return self.ref < self.val
            elif ((self.op == CompOp.LTQ) or (self.op == '<=')):
                return self.ref <= self.val
            elif ((self.op == CompOp.GTR) or (self.op == '>')):
                return self.ref > self.val
            elif ((self.op == CompOp.GTQ) or (self.op == '>=')):
                return self.ref >= self.val
            else: # (self.op == ConditionalComparisonOperator.NONE):
                raise Exception('Conditional statement was not provided with a valid comparison operator')
                return False
        except Exception as e:
            print("Conditional statement was invalid/undefined. Exception {0} occurred. Arguments:\n{1!r}".format(type(e).__name__, e.args))
            return False


class Condition():
    '''
    Create a Condition with at least one conditional statement and either another statement or another condition
    TODO: Create a condition with two other Conditions.
    If you want to specify that only the first conditional statement needs to evaluate to True, then don't provide a BoolOp parameter
    '''
    def __init__(self, _statement_1:ConditionalStatement, _bool:BoolOp=BoolOp.NONE, _statement_or_condition=None):
        self.first = _statement_1
        self.bool = _bool
        self.second = _statement_or_condition

    def Evaluate(self):
        try:
            if   (self.bool == BoolOp.NONE): # the second condition or statement will not be evaluated!
                return self.first.Evaluate()
            elif ((self.bool == BoolOp.NOT) or (self.bool == '~')): # the second condition or statement will not be evaluated!
                return not self.first.Evaluate()
            elif ((self.bool == BoolOp.AND) or (self.bool == '&&')):
                return self.first.Evaluate() and self.second.Evaluate()
            elif ((self.bool == BoolOp.OR) or (self.bool == '||')):
                return self.first.Evaluate() or self.second.Evaluate()
            else:
                raise Exception('Condition was not provided with a valid boolean operator')
                return
        except Exception as e:
            print("Condition could not be evaluated. Exception {0} occurred. Arguments:\n{1!r}".format(type(ex).__name__, ex.args))
            return False


class Damage():
    '''
    '''
    def __init__(self, _amt:int=-1):
        self.amount = _amt # needs to be set
        self.target = None
        self.owner = None # the one inflicting the damage
        self.damage_type = None

class CombatEffect():
    '''
    Effects run on a time basis, not per frame/tick/update.

    Every actor in combat has a queue of current effect (buffs/debuffs/DoTs/etc.); All such effects have an expiration timer. -1 is infinite. When the expiration timer reaches 0 the effect is removed from the queue.

    During each damage "frame" we evaluate actions between all combat actors and their targets.

    All effects have "owners" and "targets". If an effect has multiple targets, each target recieves their own effect that is added to its respective queue. Exceptions might be:
        (1) The effect is the same, and was applied by the same owner to the same target. In this case, several things can happen:
            (i)     The effect is discarded as a duplicate (e.g., a passive effect should definitely not be applied every step!)
            (ii)    The effect has a condition that is not met for its application (i.e., a passive effect that an actor applies only to other actors within a certain radius--actors who leave this radius should no longer be under this effect)
            (iiI)   The effect is added to the queue as part of a stack. A stack contains all of the same effects, and they can be evaluated based on the size of the stack or per each effect in it. It might be easier to organize the queue as a queue of stacks and non-stacking effects are simply stacks in the queue of size = 1.

    When we know all of the actions that took place between the previous tick and the current one (maybe need another queue of combat actions--order matters this time!), we add those effects to the appropriate actor effect queues.

    For each actor, we then evaluate their queue to determine what must happen during this frame. There should be a certain order to how these evaluations are done (e.g., we want to apply defensive buffs before we calculate damage)

    To determined what must happen to the actor that frame, we:
        (1) Apply relevant stat changes that must occur before the damage step (if they haven't been applied).
        (2) Evaluate damage and/or healing calculations (changes to health).
        (3) Whether or not that actor has perished.
    '''
    class Priority(Enum):
        '''
        '''
        LOWEST, MEDIUM, HIGHEST = range(1, 3)

    def __init__(self):
        self.target = None
        self.owner = None # the 'caster'
        self.duration_ms = 0
        self.name = ""
        self.conditionals = []
        self.priority = Priority.LOWEST
        self.effect_functor = None

    def Evaluate(self):
        for cond in self.conditionals:
            if (not cond.Evaluate()):
                return False
        return True

class CombatEffectQueue():
    '''
    '''
    def __init__(self):
        self.__queue = []

    def __getitem__(self, key):
        return self.__queue[key]
    def __setitem__(self, key):
        return self.__queue[key]
    def add_effect(self, _effect:CombatEffect):
        '''
        Adds an effect into the queue based on the priority
        '''
        if len(self.__queue) == 0: self.__queue.append(_effect); return
        for idx, itm in enumerate(self.__queue):
            if (itm.priority > _effect.priority):
                self.__queue.insert[(idx if idx > 0 else 0) : idx] = [_effect]
    def __iadd__(self, _effect:CombatEffect):
        self.add_effect(_effect)
        return self

class CombatActor():
    '''
    '''
    def __init__(self, _actor:Player, ):
        self.actor = None
        self.effect_queue = CombatEffectQueue()