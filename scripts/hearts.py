# Hearts - hearts.py
# Copyright 2006 Sander Marechal
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# This is an attempted translation of hearts.lua
# Cards are defined as tuples, so card = (suit, rank)
# Multiple cards are passed around as lists of tuples.

import os
import sys
import string

sys.path.append("/usr/share/gnome-hearts");
sys.path.append("/usr/share/gnome-hearts/players");

from definitions import *
from stock_ai import *

# Load all the available player AI's
for script in os.listdir(os.path.abspath("/usr/share/gnome-hearts/players")):
	module_name, ext = os.path.splitext(script)
	if ext == '.py':
		module = __import__(module_name)
		for method in dir(module):
			if method.startswith('PlayerAI'):
				# Make the AI class a global
				globals()[method] = getattr(module, method)
				# Register the AI in C
				ai = globals()[method](None, None, None, None)
				register_ai(ai.name, method)

# The Trick class
class Trick:
	"""A trick of cards, equal to the C version"""
	
	def __init__(self):
		self.card = []
		self.trump = None
		self.num_played = 0
		self.first_played = None
	
	def set(self, list, trump, num_played, first_played):
		self.card = list
		self.trump = trump
		self.num_played = num_played
		self.first_played = first_played
	
	def winner(self):
		"""Return who played the highest card on the trick"""
		if self.num_played > 0:
			return self.card.index(self.get_highest_card())
		return None
	
	def get_highest_card(self):
		"""Return the highest trump card in the list"""
		highest_card = (0, 0)
		for card in self.card:
			if card != None and card[0] == self.trump and card[1] > highest_card[1]:
				highest_card = card
		return highest_card

trick = Trick()

# The score class
class Score:
	"""This object contains the score of this round and the entire game so far"""

	def __init__(self):
		self.round = [0, 0, 0, 0]
		self.game = [0, 0, 0, 0]
	
	def set(self, round, game):
		self.round = round
		self.game = game

score = Score()

# The rules class
class Rules:
	"""This object contains all the rules for the game"""

	def __init__(self):
		self.ruleset = "standard"
		self.clubs_lead = True
		self.hearts_break = True
		self.queen_breaks_hearts = False
		self.no_blood = True

	def set(self, ruleset, clubs_lead, hearts_break, queen_breaks_hearts, no_blood):
		self.ruleset = ruleset
		self.clubs_lead = clubs_lead
		self.hearts_break = hearts_break
		self.queen_breaks_hearts = queen_breaks_hearts
		self.no_blood = no_blood

rules = Rules()

# General setting functions used by C
def player_set(object, direction):
	player[direction] = object

# The list of players
player = [None, None, None, None]

