'''
bridge/deck.py
'''
from enum import Enum
from collections import defaultdict
from random import seed, shuffle

class Card(object):
  def __init__(self, face, suite, points=0):
    self.face = face
    self.suite = suite
    self.points = points

  def __str__(self):
    return f'{self.face} of {self.suite}'
  def __repr__(self):
    return f'{self.face} of {self.suite}'

class _DeckConfigObject(object):

  DEFAULT_CONFIG = { # bridge config
    'suites': ['Spades', 'Hearts', 'Diamonds', 'Clubs'],
    'faces':  ['Ace', 'King', 'Queen', 'Jack', '10',
              '9', '8', '7', '6', '5', '4', '3', '2'],
    'cards_per_deal': 13,
    'suite_points': {'Ace': 4, 'King': 3, 'Queen': 2, 'Jack': 1},
    'suite_distribution_points': {2: 1, 1: 2, 0: 5},
  }

  def __init__(self, **config):
    self._set(**config)

  def _set(self, **config):
    if not config:
      config = _DeckConfigObject.DEFAULT_CONFIG
    self._suites = config.get('suites', _DeckConfigObject.DEFAULT_CONFIG['suites'])
    self._faces = config.get('faces', _DeckConfigObject.DEFAULT_CONFIG['faces'])
    self._cards_per_deal = config.get('cards_per_deal', 1)
    self._extras = config.get('extras', None)
    self._set_optionals(**config)

  def _set_optionals(self, **config):
    suite_points = config.get('suite_points', None)
    if isinstance(suite_points, dict):
      self._suit_points = defaultdict(suite_points)
    else:
      self._suit_points = defaultdict(int)

    face_points = config.get('face_points', None)
    if isinstance(face_points, dict):
      self._face_points = defaultdict(face_points)
    else:
      self._face_points = defaultdict(int)

    suite_distribution_points = config.get('suite_distribution_points', None)
    if isinstance(suite_distribution_points, dict):
      self._suite_distribution_points = defaultdict(suite_distribution_points)
    else:
      self._suite_distribution_points = defaultdict(int)

    face_distribution_points = config.get('face_distribution_points', None)
    if isinstance(face_distribution_points, dict):
      self._face_distribution_points = defaultdict(face_distribution_points)
    else:
      self._face_distribution_points = defaultdict(int)

class Deck(_DeckConfigObject):
  '''
  Base Deck object

  config:

  '''
  def __init__(self, **config):
    super(_DeckConfigObject, self).__init__(**config)
    self.create_new_deck()

  def shuffle(self):
    shuffle(self._deck)

  def create_new_deck(self, **config):
    if config:
      self._set(**config)
    self._deck = [
      Card(face, suite, self._face_points[face] + self._suit_points[suite])
        for face in self._faces for suite in self._suites
    ]

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
    if len(self._deck) < self._cards_per_hand:
      raise RuntimeError("Can't deal {} cards from Deck of size: {}"
        .format(self._cards_per_hand, len(self._deck)))

    if shuffle:
      self.shuffle()

    hand = self._deck[:self._cards_per_hand]
    if remove_from_deck:
      self._deck = self._deck[self._cards_per_hand:]

    score = self._get_hand_score(hand)
    return hand, score
    
  def _get_hand_score(self, hand, extra_scoring_func=None):
    '''Evaluates a hand and returns the hands's score'''
    freq = defaultdict(int)
    card_points = 0
    for card in hand:
      card_points += card.points
      freq[(card.suite, 'suite')] += 1
      freq[(card.face, 'face')] += 1
    
    distribution_points = 0
    for k, v in freq.items():
      if k[1] == 'suite':
        distribution_points += self._suite_distribution_points[v]
      else:
        distribution_points += self._face_distribution_points[v]

    score = card_points + distribution_points
    if isinstance(extra_scoring_func, function):
      score += extra_scoring_func(hand, self)

    return score


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

