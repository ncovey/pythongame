
import random
import math
import Player
from CombatUtils import *



# entry point:
def main():

    name = 'Bob'
    num = 2

    cs = ConditionalStatement(name, '==', 'Tim')
    cs2 = ConditionalStatement(num, '<', len(name))

    cond = Condition(cs, '||', cs2)
    cond2 = Condition(cs, '&&', ('Steve', CompOp.EQU, 'Steven'))

    cond3 = Condition(cond2, '||', cond)
    cond4 = cond2
    cond5 = Condition(cond3, '&&', cond4)
    cs3 = ConditionalStatement(cond5, '!=', cond2)
    cs3.Evaluate()

    cls = [cs, cs2, cond, cond2, cond3, cond4, cond5, cs3]

    for c in cls:
        if (not c.Evaluate()):
            print ("{}".format(c));

    if (cond5.Evaluate()):
        print ('Bob is not Tim!')

    return
    
	#p1 = Player()
	#p2 = Player()
	
	#p1.name = "One"
	#p2.name = "Two"
	#p1.attributes.strength = 20
	#p2.attributes.constitution = 30
	#p1.stats.update_stats()
	#p1.reset_current_stats()
	#p2.stats.update_stats()
	#p2.reset_current_stats()
	
	#p1.print()
	#p2.print()

	### need to take into account the levels of the players and base the dmg and dmg res off of their respective levels to one another

	#dmg = p1.do_primary_attack()
	#tdmg = p2.calculate_true_damage(dmg)
	#print(dmg)
	#print(tdmg)

	#p2.current_stats.hit_points -= tdmg
	
	
	#print("HP: {}/{}".format(p2.current_stats.hit_points, p2.stats.hit_points))
	
	#p1.print()
	#p2.print()
	
	#p2.reset_current_stats()
	#p2.print()
	
if (__name__ == "__main__"):
	main()