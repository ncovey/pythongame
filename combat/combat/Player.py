
import random
import math
from Equipment import Equipment

MIN_ATTRIBUTE_VALUE = 10
SCALE_ATTACK_PERCENT_PER_POINT = 0.01
SCALE_HEALTH_PER_POINT_PERCENT = 0.02
SCALE_CRIT_CHANCE_PER_POINT_PERCENT = 0.01
SCALE_DAMAGE_RESIST_PER_POINT_DEFENSE = 0.0001

MIN_HIT_POINTS = 1000
MIN_CRIT_CHANCE = 0.05
MIN_CRIT_DAMAGE = 0.50
MIN_DAMAGE_RESIST = 0.05 
MAX_DAMAGE_RESIST = 0.9

MAX_LEVEL_PLAYER = 70

def max(value, max):
	if (value > max):
		value = max
	return value

# parameters are reversed because most of the time we want from 0% to the
# specified percent
def get_rand_percent(max=1.0, min=0.0):
	return random.uniform(min, max)

class Attributes:
	
	def __init__(self):
		self.strength = 15
		self.constitution = 15
		self.wisdom = 15
		self.dexterity = 15
		self.intelligence = 15
		self.charisma = 15
	
	def __mod_formula(self, value, min, scale_percent):
		return (value - min) * scale_percent
	
	def get_mod(self, attribute, scale_percent, require_min=True):
		min = MIN_ATTRIBUTE_VALUE
		if (not require_min):
			min = 0
		return self.__mod_formula(attribute, min, scale_percent)
		
	# add 1% attack power for each point over 10
	# returns a percentage
	def get_attack_power_mod(self, attribute):
		return self.get_mod(attribute, SCALE_ATTACK_PERCENT_PER_POINT)
		
	def get_health_mod(self):
		return self.get_mod(self.constitution, SCALE_HEALTH_PER_POINT_PERCENT)
		
	def get_crit_chance_mod(self):
		return self.get_mod(self.dexterity, SCALE_CRIT_CHANCE_PER_POINT_PERCENT)

	def get_crit_damage_mod(self):
		return 0
	
	def print(self):
		print("strength={} constitution={} wisdom={} dexterity={} intelligence={}, charisma={}".format(self.strength, self.constitution, self.wisdom, self.dexterity, self.intelligence, self.charisma))


class Stats:
	
	def __init__(self, attributes):
		self.attributes = attributes
		self.damage = 0
		self.damage_resist = 0.0
		self.update_stats()
		
	def update_stats(self):
		self.hit_points = MIN_HIT_POINTS * (1 + self.attributes.get_health_mod())
		self.crit_chance = MIN_CRIT_CHANCE + self.attributes.get_crit_chance_mod()
		self.crit_damage = MIN_CRIT_DAMAGE	+ self.attributes.get_crit_damage_mod()
	
	def assign(self, stats):
		# attributes.get_attack_power_mod(self.attribute.strength)
		self.damage = stats.damage
		self.damage_resist = stats.damage_resist
		self.hit_points = stats.hit_points
		self.crit_chance = stats.crit_chance
		self.crit_damage = stats.crit_damage
	
	def update_damage(self, attack_power):
		self.damage = attack_power * (1 + self.attributes.get_attack_power_mod(self.attributes.strength))
	
	def update_damage_resist(self, defense):
		self.damage_resist = max((MIN_DAMAGE_RESIST + (defense * SCALE_DAMAGE_RESIST_PER_POINT_DEFENSE)), MAX_DAMAGE_RESIST)

	def print(self):
		print("damage={} damage_resist={} hit_points={} crit_chance={} crit_damage={}".format(self.damage, self.damage_resist, self.hit_points, self.crit_chance, self.crit_damage))

class Player:

	def __init__(self):
		self.attack_power = 0
		self.defense_rating = 0
		
		self.equipmentest = Equipment()

		self.equipment_armor_body = 3500
		self.equipment_weapon_primary = 5
		
		self.attributes = Attributes()
		self.stats = Stats(self.attributes)
		self.current_stats = Stats(self.attributes)
		self.level = 1
		self.name = ""		
		
		self.gear_up()
	
	def reset_current_stats(self):
		self.current_stats.assign(self.stats)

	def gear_up(self):		
		self.equip_weapon(self.equipment_weapon_primary)
		self.equip_armor(self.equipment_armor_body)
		self.reset_current_stats()
	
	# temporary
	def equip_weapon(self, value):
		self.attack_power += value
		self.stats.update_damage(self.attack_power)
	# temporary
	def equip_armor(self, value):
		self.defense_rating += value
		self.stats.update_damage_resist(self.defense_rating)
	# temporary
	def unequip_weapon(self, value):
		self.stats.damage -= value
		self.stats.update_damage(self.attack_power)
	# temporary
	def unequip_armor(self, value):
		self.defense_rating -= value
		self.stats.update_damage_resist(self.defense_rating)
		
	# returns a generated attack number
	def do_primary_attack(self):
		if (get_rand_percent() <= self.stats.crit_chance):
			print('critical hit!')
			return self.stats.damage * (1 + self.stats.crit_damage)
		else:
			return self.stats.damage
		
	def calculate_true_damage(self, raw_damage):
		return (1 - self.stats.damage_resist) * (raw_damage)
		
	def print(self):
		print("attack_power={} defense_rating={} level={} name={}".format(self.attack_power, self.defense_rating, self.level, self.name))
		self.attributes.print()
		self.stats.print()
		self.current_stats.print()
		