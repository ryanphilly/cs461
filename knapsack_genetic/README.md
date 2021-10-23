# Generating general solutions for the knapsack problem using Genetic Algorithms (python std library only)
## CS461 Project 2

## Repository Structure
### CS 461 Project White Paper/Writeup
#### /writeup/
### CS 461 output/logs genrated from running on given assignment data
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
## Implementation 
### Data Representation:
Selections - sets of indexes that represent the locations of the selected items in the input data.  In the case of a large ammount of selected items representing selections like this may potentially require more memory than a boolean array or raw bytes.  However, it seems most viable selections are a small subset of the total items. This results in sparse boolean arrays, bytes, or string representations therfore requiring needless iteration for querying and evaluating.