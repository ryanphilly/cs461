'''
bridge/deck.py
'''
from enum import Enum
from collections import defaultdict

from random import seed, shuffle

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
  '''52 card deck, no bridge game dynamics besides score evaluation'''
  def __init__(self):
    self.create_new_deck()
  
  def shuffle(self):
    shuffle(self._deck)

  def create_new_deck(self):
    self._deck = [
      Card(face, suite)
    for face in FaceValue for suite in Suite]

  def deal_hand(self, shuffle=False, remove_from_deck=True):
    '''
    Deal 13 cards from the deck
    params:
      shuffle: bool: shuffle before dealing?
      remove_from_deck: bool: remove the dealt hand from deck
    returns:
      hand: List[Card]: 13 card hand
      score: int: score of dealt hand
    '''
    if len(self._deck) < 13:
      raise RuntimeError(f"Can't deal 13 cards from deck of size: {len(self._deck)}.")
    if shuffle:
      self.shuffle()

    hand = self._deck[:13]
    if remove_from_deck:
      self._deck = self._deck[13:]

    points = self._get_points_from_hand(hand)
    return hand, points
    
  def _get_points_from_hand(self, hand):
    '''Evaluate a hand and return its score'''
    distribution = defaultdict(int)
    high_card_points = 0
    for card in hand:
      distribution[card.suite] += 1
      high_card_points += card.points
    
    distribution_points = 0
    for suite in Suite:
      freq = distribution[suite]
      if freq == 2: # doubleton 
        distribution_points += 1
      elif freq == 1: # singleton 
        distribution_points += 2
      elif freq == 0: # void
        distribution_points += 5

    return high_card_points + distribution_points


if __name__ == '__main__':
  print('Testing Card Deck...\n')

  seed(33)
  c = CardDeck()
  hand, score = c.deal_hand()
  assert(len(hand) ==  13)
  assert(len(c._deck) == 39)
  assert(score == 16)

  hand, score = c.deal_hand(remove_from_deck=False)
  assert(len(hand) ==  13)
  assert(len(c._deck) == 39)
  assert(score == 7)

  print('Tests passed...Exiting')

