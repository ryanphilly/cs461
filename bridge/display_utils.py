'''
bridge/display_utils.py
Utility functions to display results and prompt the player
'''
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
  print(f'The estimated probability based on {n} simulated hands:')
  print(f'Pass: {round(pass_prob * 10e1, 2)}%')
  print(f'Part Score: {round(part_score_prob * 10e1, 2)}%')
  print(f'Game: {round(game_prob * 10e1, 2)}%')
  print(f'Small Slam: {round(small_slam_prob * 10e1, 2)}%')
  print(f'Grand Slam: {round(grand_slam_prob * 10e1, 2)}%')

def display_player_hand(player_hand, player_score):
  print(f'Here is your hand:\n{player_hand}')
  print(f'This hand is worth {player_score} points.')
  print('Running Simulation......\n')

def prompt_another_episode():
  response = input('\nAnother Hand? [Y/N]? ').lower()
  if response in ('y', 'yes'):
    return True
  if response in ('n', 'no', 'q'):
    return False

  print(f'Unknown response "{response}"....')
  return prompt_another_episode()
