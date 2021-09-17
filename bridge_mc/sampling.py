'''
bridge_mc/sampling.py
'''
from collections import defaultdict

def greedy_bridge_policy(score):
  '''
  Outcome Policy
  returns: str:
    Pass: Less than 20 points
    Part score: 20-25 points
    Game: 26-31 points
    Small slam (take all tricks but 1): 32-35 points
    Grand slam (take all tricks): 36+ points
  '''
  if score < 20:
    return 'Pass'
  if score < 26:
    return 'Part Score'
  if score < 32:
    return 'Game'
  if score < 36:
    return 'Small Slam'

  return 'Grand Slam'

def bridge_monte_carlo_n_hands(n, player_score, deck, policy):
  '''
  Performs one episode of outcome sampling
  params:
    n: int: number of outcomes to sample
    player_score: int: score of players current hand
    deck: CardDeck: deck w/ player hand already dealt out
    policy: (int) -> str: poilicy to sample from
  returns:
    outcome_probs: ddict(float) probabilities of outcomes

  '''
  outcome_probs = defaultdict(float)

  for _ in range(n):
    teamate_hand, teamate_score = deck.deal_hand(
      remove_from_deck=False, shuffle=True)
    team_score = player_score + teamate_score
    outcome = policy(team_score)
    outcome_probs[outcome] += 1.0

  for k in outcome_probs.keys():
    outcome_probs[k] =  outcome_probs[k] / n

  return outcome_probs