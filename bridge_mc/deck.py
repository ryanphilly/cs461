'''
Ryan Phillips

bridge_mc/deck.py

This is really over engineered for the cs 461 assignment
but its being used as an enviroment for testing rl algorithms
from Barto and Suttons book https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf
'''
from collections import defaultdict
from random import shuffle

class Card(object):
  '''
  Card(utility object)
  **extras: any extra information about the card
  '''
  def __init__(self, face, suite, points, **extras):
    self.face = face
    self.suite = suite
    self.points = points
    self.extras = extras

  def __str__(self):
    if not str(self.suite):
      return str(self.face)
    return '{} of {}'.format(str(self.face), str(self.suite))
  def __repr__(self):
    if not str(self.suite):
      return str(self.face)
    return '{} of {}'.format(str(self.face), str(self.suite))

class _DeckConfigObject(object):
  '''
  _DeckConfigObject
  Sets up the deck configuration and
  provides helpful error messages when
  creating a new configuration incorrectly

  **config: (any can be omitted and will be set to respective in DEFAULT_CONFIG)
    "suites" - iterable of Any
    "faces" - iterable of Any
    "card_extras" - dict[tuple: dict]
    "cards_per_deal" - int
    "suite_points" - dict[Any: float or int], int, or float
    "face_points" - dict[Any: float or int], int, or float
    "suite_distribution_points" - dict[int: float oor int]
    "face_distribution_points" - dict[int: float or int]
  '''

  DEFAULT_CONFIG = { # normal 52 card deck config with no scoring
    'suites': ['Spades', 'Hearts', 'Diamonds', 'Clubs'],
    'faces':  ['Ace', 'King', 'Queen', 'Jack', '10',
              '9', '8', '7', '6', '5', '4', '3', '2'],
    "card_extras": {},
    'cards_per_deal': 1,
    "suite_points": {},
    "face_points": {},
    "suite_distribution_points": {},
    "face_distribution_points": {}
  }

  def __init__(self, **config):
    self._set(**config)

  def _set(self, **config):
    self._suites = config.get('suites', _DeckConfigObject.DEFAULT_CONFIG['suites'])
    if not isinstance(self._suites, (list, tuple, set)):
      raise ValueError('"suites" must be an iterable')
    if not self._suites: # handle decks wiith no suites e.g. pokemon deck
      self._suites.append('')

    self._faces = config.get('faces', _DeckConfigObject.DEFAULT_CONFIG['faces'])
    if not isinstance(self._faces, (list, set, tuple)):
      raise ValueError('"faces" must be an iterable')

    self._cards_per_deal = config.get('cards_per_deal', _DeckConfigObject.DEFAULT_CONFIG['cards_per_deal'])
    if not isinstance(self._cards_per_deal, int):
      raise ValueError('"cards_per_deal" must be of type int')
    
    suite_points = config.get('suite_points', _DeckConfigObject.DEFAULT_CONFIG['suite_points'])
    if isinstance(suite_points, dict):
      self._suit_points = defaultdict(float, suite_points)
    elif isinstance(suite_points, (int, float)):
      self._suit_points = defaultdict(lambda: suite_points)
    else:
      raise ValueError('"suite_points" must be of type dict, int, or float')

    face_points = config.get('face_points', _DeckConfigObject.DEFAULT_CONFIG['face_points'])
    if isinstance(face_points, dict):
      self._face_points = defaultdict(float, face_points)
    elif isinstance(face_points, (int, float)):
      self._face_points = defaultdict(lambda: face_points)
    else:
      raise ValueError('"face_points" must be of type dict[str: int or float], int, or float')

    suite_distribution_points = config.get(
      'suite_distribution_points', _DeckConfigObject.DEFAULT_CONFIG['suite_distribution_points'])
    if isinstance(suite_distribution_points, dict):
      self._suite_distribution_points = defaultdict(float, suite_distribution_points)
    else:
      raise ValueError('"suite_distribution_points" must be of type dict[int: int or float]')

    face_distribution_points = config.get(
      'face_distribution_points', _DeckConfigObject.DEFAULT_CONFIG['face_distribution_points'])
    if isinstance(face_distribution_points, dict):
      self._face_distribution_points = defaultdict(float, face_distribution_points)
    else:
      raise ValueError('"face_distribution_points" must be of type dict[int: int or float]')

    card_extras = config.get('card_extras', _DeckConfigObject.DEFAULT_CONFIG['card_extras'])
    if isinstance(card_extras, dict):
      self._card_extras = defaultdict(dict, card_extras)
    else:
      raise ValueError('"card_extras" must be of type dict[tuple: dict]')

class Deck(_DeckConfigObject):
  '''
  Dynamic Deck Enviroment

  **config: (any can be omitted and will be set to respective in DEFAULT_CONFIG)
    "suites" - iterable of Any
    "faces" - iterable of Any
    "card_extras" - dict[tuple: dict]
    "cards_per_deal" - int
    "suite_points" - dict[Any: float or int], int, or float
    "face_points" - dict[Any: float or int], int, or float
    "suite_distribution_points" - dict[int: float oor int]
    "face_distribution_points" - dict[int: float or int]
  '''
  def __init__(self, **config):
    super(Deck, self).__init__(**config)
    self.create_new_deck()

  def shuffle(self):
    '''Shuffles the deck'''
    shuffle(self._deck)

  def create_new_deck(self, **config):
    '''
    Creates a new deck

    If **config is not empty then updates deck config before creation
    WARNING: DOES NOT SHUFFLE AFTER CRREATION
    '''
    if config: self._set(**config)
    self._deck = [
      Card(face, suite, self._face_points[face] + self._suit_points[suite],
          **self._card_extras[(suite, face)])
        for face in self._faces for suite in self._suites
    ]

  def deal_hand(self, shuffle=False, remove_from_deck=True, custom_cards_scoring=0):
    '''
    Deal self._cards_per_deal cards from the deck

    params:
      shuffle: bool: shuffle before dealing?

      remove_from_deck: bool: remove the dealt hand from deck?

      custom_cards_scoring: function(list, Deck), int, or float:
        - custom cards scoring on top of distibution scores and card scores

    returns:
      cards: List[Card]: dealt cards

      score: int or float: score of dealt hand
    '''
    if len(self._deck) < self._cards_per_deal:
      raise RuntimeError("Can't deal {} cards from Deck of size: {}"
        .format(self._cards_per_deal, len(self._deck)))

    if shuffle: self.shuffle()

    cards = self._deck[:self._cards_per_deal]
    if remove_from_deck:
      self._deck = self._deck[self._cards_per_deal:]

    score = self._get_hand_score(cards, custom_cards_scoring)
    return cards, score
    
  def _get_cards_score(self, hand, custom_cards_scoring):
    '''Evaluates a list of cards and returns the hands's score'''
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

    try:
      if hasattr(custom_cards_scoring, '__call__'):
        score += custom_cards_scoring(hand, self)
      else:
        score += custom_cards_scoring
    except TypeError:
      raise TypeError('"extra_scoring_func" should be of type {}, {}'
        .format('function(list, Deck)', 'int, or float'))

    return score


if __name__ == '__main__':
  from random import seed
  seed(33)

  print('Testing Deck with cs461 bridge config...\n')
  c = Deck(cards_per_deal=13,
        face_points={'Ace': 4, 'King': 3, 'Queen': 2, 'Jack': 1},
        suite_distribution_points={2: 1, 1: 2, 0: 5})

  hand, score = c.deal_hand(shuffle=True)
  assert(len(hand) ==  13)
  assert(len(c._deck) == 39)
  assert(score == 16)

  hand, score = c.deal_hand(shuffle=True, remove_from_deck=False)
  assert(len(hand) ==  13)
  assert(len(c._deck) == 39)
  assert(score == 7)

  print('Tests passed...Exiting')

