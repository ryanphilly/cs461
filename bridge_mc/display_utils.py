'''
Ryan Phillips

bridge_mc/display_utils.py
Utility functions to display results and prompt the player
'''
from __future__ import print_function

def display_episode_results(outcomes, n):
  '''
  Displays the mc episode to match
  the assignment example output
  '''
  pass_prob = outcomes['Pass']
  part_score_prob = outcomes['Part Score']
  game_prob = outcomes['Game']
  small_slam_prob = outcomes['Small Slam']
  grand_slam_prob = outcomes['Grand Slam']
  print('The estimated probability based on {} simulated hands:'.format(n))
  print('Pass: {}%'.format(round(pass_prob * 10e1, 2)))
  print('Part Score: {}%'.format(round(part_score_prob * 10e1, 2)))
  print('Game: {}%'.format(round(game_prob * 10e1, 2)))
  print('Small Slam: {}%'.format(round(small_slam_prob * 10e1, 2)))
  print('Grand Slam: {}%'.format(round(grand_slam_prob * 10e1, 2)))

def display_player_hand(player_hand, player_score):
  print('Here is your hand:\n{}'.format(player_hand))
  print('This hand is worth {} points.'.format(player_score))

def prompt_another_episode():
  response = input('\nAnother Hand? [Y/N]? ').lower()
  if response in ('y', 'yes'):
    return True
  if response in ('n', 'no', 'q'):
    return False

  print('Unknown response "{}"....'.format(response))
  return prompt_another_episode()
