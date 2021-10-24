# Generating general solutions for the knapsack problem using Genetic Algorithms (python std library only)
## CS461 Project 2

## Repository Structure
### CS 461 Project White Paper/Writeup
#### /writeup/
### CS 461 output genrated from running on given assignment data and exact assignment config with inital population of 1000
#### /logs/cs461/
### Logs/Output generated when running the GA (overwritten on each run)
#### /logs/
### Input data files containing items in the knapsack
#### /data/ - WARNING: All files will be treated as input so make sure to clear this dir before using new data (comes w/ cs 461 assignment given data)

### guide to run:
```
# run on data in /data/ with cs461 assignment config
python main.py

#custom config (any may be omitted)
python main.py --max_weight=int --init_population_size=int --init_items_frac=int --mutation_rate=float --data_path=str --log_path=str --improvement_required=float --improvement_leniency=int
```
### To use a custom fitness function replace cs461_weight_constraint_fitness_func in main.py (see utils.py for a fitness function example)