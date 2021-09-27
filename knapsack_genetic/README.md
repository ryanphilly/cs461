# Generating general solutions for the knapsack problem using Genetic Algorithms
## CS461 Project 2

### guide to run:
```
# assignment config
python main.py

#custom config (any may be omitted)
python main.py --vectorized=bool --max_weight=int --init_population=int --init_num_samples=int --mutation_rate=float --data_path=str --log_path=str
```
## Standard implementation (std library)
### Data Representation:
Selections - sets of indexes that represent the locations of the selected items in the input data.  In the case of a large ammount of selected items representing selections like this may potentially require more memory than a boolean array or raw bytes.  However, it seems most viable selections are a small subset of the total items. This results in sparse boolean arrays, bytes, or string representations therfore requiring needless iteration for querying and evaluating.

## Vectorized implementation (pytorch)
## if a CUDA supported GPU is detected it will be used
### Data Representation:
Selections - tensors (B,C,N) => (1, 2(utils, weight), ammount of items)