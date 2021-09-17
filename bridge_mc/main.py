'''
Ryan Phillips
UMKC 461 Assignment 1

bridge_mc/main.py
'''
from __future__ import print_function

from argparse import ArgumentParser

from deck import Deck
from sampling import (
  greedy_bridge_policy,
  bridge_monte_carlo_n_hands
)
from display_utils import (
  display_episode_results,
  display_player_hand,
  prompt_another_episode
)

def main(args):
  if args.seed is not None:
    from random import seed
    seed(args.seed)

  deck = Deck( # create deck w/ bridge config
    cards_per_deal=13,
    face_points= {'Ace': 4, 'King': 3, 'Queen': 2, 'Jack': 1},
    suite_distribution_points={2: 1, 1: 2, 0: 5})
    
  while True:
    player_hand, player_score = deck.deal_hand(shuffle=True, remove_from_deck=True)
    display_player_hand(player_hand, player_score)
    # sample outcomes
    print('Running Simulation......\n')
    outcome_probs = bridge_monte_carlo_n_hands(
      args.n, player_score, deck, greedy_bridge_policy)
    display_episode_results(outcome_probs, args.n)

    if not prompt_another_episode():
      break
    deck.create_new_deck()

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('-n', type=int, default=500)
  parser.add_argument('-seed', type=int, default=None)
  main(parser.parse_args())