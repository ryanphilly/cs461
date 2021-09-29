
class Population(object):
  def __init__(self, chromosomes, fitnesses, avg_fitness=None):
    self._update(chromosomes, fitnesses, avg_fitness)
  def __str__(self):
    return 'Avg Fitness: {}\nBest Fitness: {}\nNum Items selected in best: {}\n\nBest Selection: {}'.format(
      self.avg_fitness, self.best_fitness, len(self.best_chromosome), self.best_chromosome
    )
  def __repr__(self):
    return 'Avg Fitness: {}\nBest Fitness: {}\nNum Items selected in best: {}\nBest Selection: {}'.format(
      self.avg_fitness, self.best_fitness, len(self.best_chromosome), self.best_chromosome
    )

  def _update(self, chromosomes, fitnesses, avg_fitness=None):
    self.avg_fitness = avg_fitness if avg_fitness is not None \
      else sum(fitnesses) / len(fitnesses)
    best_idx = max(range(len(chromosomes)), key=fitnesses.__getitem__)
    self.best_chromosome = chromosomes[best_idx]
    self.best_fitness = fitnesses[best_idx]
    self.chromosomes = chromosomes
    self.fitnesses = fitnesses
    self.is_useable = True

  def deallocate_for_logging(self):
    self.fitnesses = None
    self.chromosomes = None
    self.is_useable = False


  

