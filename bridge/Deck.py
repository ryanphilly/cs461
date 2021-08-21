'''
bridge/Deck.py
'''

from enum import Enum
from collections import defaultdict

from random import shuffle

class Suite(Enum):
  Spades = 'Spades'
  Hearts = 'Hearts'
  Diamonds = 'Diamonds'
  Clubs = 'Clubs'

class FaceValue(Enum):
  Ace = 'Ace'
  King = 'King'
  Queen = 'Queen'
  Jack = 'Jack'
  Ten = '10'
  Nine = '9'
  Eight = '8'
  Seven = '7'
  Six = '6'
  Five = '5'
  Four = '4'
  Three = '3'
  Two = '2'

face_to_points = defaultdict(int)
face_to_points['Ace'] = 4
face_to_points['King'] = 3
face_to_points['Queen'] = 2
face_to_points['Jack'] = 1

class Card(object):
  def __init__(self, face, suite):
    self.face = face
    self.suite = suite
    self.points = face_to_points[face.value]
  
  def __str__(self):
    return f'{self.face.value} of {self.suite.value}'
  def __repr__(self):
    return f'{self.face.value} of {self.suite.value}'

class CardDeck(object):
  '''52 card deck'''
  def __init__(self):
    self._deck = [Card(face, suite) for face in FaceValue for suite in Suite]
  
  def shuffle(self):
    shuffle(self._deck)

  def deal_hand(self):
    assert len(self._deck) >= 13, "Deck is empty"
    self.shuffle()
    hand, self._deck = self._deck[:13], self._deck[13:]
    points = self._get_points_from_hand(hand)
    return hand, points

  def return_hand(self, hand):
    assert self._is_valid_hand(hand), "hand must be of type: List[Card]"
    self._deck.extend(hand)

  def _is_valid_hand(self, hand):
    return isinstance(hand, list) and len(hand) == 13 and \
      all(isinstance(card, Card) for card in hand)
    
  def _get_points_from_hand(self, hand):
    distribution = defaultdict(int)
    high_card_points = 0
    distribution_points = 0

    for card in hand:
      distribution[card.suite] += 1
      high_card_points += card.points
    
    for suite in Suite:
      freq = distribution[suite]
      if freq == 2: # doubleton 
        distribution_points += 1
      elif freq == 1: # singleton 
        distribution_points += 2
      elif freq == 0: # void
        distribution_points += 5

    return high_card_points + distribution_points