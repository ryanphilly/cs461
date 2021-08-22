'''
Ryan Phillips
UMKC 461 Assignment 1
bridge/main.py
'''
from argparse import ArgumentParser
from random import seed

from deck import CardDeck
from sampling import greedy_policy, monte_carlo_n_hands
from display_utils import (
  display_episode_results,
  display_player_hand,
  prompt_another_episode
)

def main(args):
  if args.seed is not None:
    seed(args.seed)

  deck = CardDeck()
  while True:
    player_hand, player_score = deck.deal_hand(
      shuffle=True, remove_from_deck=True)
    display_player_hand(player_hand, player_score)
    # sample outcomes
    outcome_probs = monte_carlo_n_hands(
      args.n, player_score, deck, greedy_policy)
    display_episode_results(outcome_probs, args.n)

    if not prompt_another_episode():
      break
    deck.create_new_deck()

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('-n', type=int, default=500)
  parser.add_argument('-seed', type=int, default=None)
  main(parser.parse_args())