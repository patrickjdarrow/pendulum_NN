import numpy as np
import matplotlib.pyplot as plt
import seaborn
import multiprocessing

plt.rcParams['figure.figsize'] = 16, 13

np.random.seed(1)

# Dummy model class
class Model():
  def __init__(self,
               n_params):
    self.n_params = np.zeros(n_params)
  
  @property
  def get_weights(self):
    return self.n_params

class Pop():
  def __init__(self,
               popsize,
               model,
               ngen,
               elitesize=0.1,
               early_stop=False
               ):
    # Set population parameters
    self.popsize = popsize
    self.ngen = ngen
    self.elitesize = elitesize
    self.n_elites = int(self.popsize * self.elitesize)
    self.n_nonelites = self.popsize - self.n_elites
    self.early_stop = early_stop

    # Track current generation
    self.generation = 0

    # Initialize population with n_traits
    self.n_traits = np.sum([np.prod(layer.shape) for layer in model.get_weights()])
    self.pop = self.init_pop()
    self.scores = np.ndarray(self.popsize)
    self._update_scores()
    self.pop_history = [self.pop]

    self.fig = plt.figure()
    self.ims = []
  
  def init_pop(self):
    self.generation = 0
    return 2 * (np.random.sample((self.popsize, self.n_traits)) - 0.5) + 6 * np.pi

  # Test surfaces: 
  def _eval1(self, x, y):
    # ripple
    sqsum = (np.power(x, 2) + \
            np.power(y, 2)) * 0.2
    return ((np.power(np.cos(2 * np.sqrt(sqsum)), 2) + 2)) * np.exp(-0.01*sqsum) 
  def _eval2(self, x, y):
    # ripple
    sqsum = (np.power(x, 2) + \
            np.power(y, 2)) * 0.2
    return ((np.power(np.cos(.2 * sqsum), 2) + 2)) * np.exp(-0.01*sqsum) 

  # Update population scores in place and order population
  def _update_scores(self, fitness_fn=None, multiprocess=False):
    if fitness_fn:
      if multiprocess:
        # p = multiprocessing.Pool(multiprocessing.cpu_count())
        # self.scores = np.array(p.map(fitness_fn, [ind for ind in self.pop]))
        self.scores = np.array([fitness_fn(ind) for ind in self.pop])
      else:
        self.scores = fitness_fn(self.pop)
    else:
      self.scores = self._eval2(self.pop[:,0], self.pop[:,1])
                        
    order = np.argsort(self.scores).reshape(self.popsize, 1)
    self.pop = np.take_along_axis(self.pop, order, axis=0)

  @property
  def get_scores(self):
    return self.scores

  # TODO: replace plotting with logging
  # TODO: assign replacement scheme for each strat
  def evolve(self,
            fitness_fn=None,
            multiprocess=False,
            plot_fitness=False,):
    
    starting_gen = self.generation
    averages = []

    for gen in range(1, self.ngen+1):
      self._update_scores(fitness_fn=fitness_fn, multiprocess=multiprocess)
      print(f'ngen: {gen}, fittest: {self.scores[0]}')
      
      if plot_fitness:
        plt.scatter([self.generation]*self.popsize, self.scores)
        averages.append(np.mean(self.scores))
        # fittest.append(np.max(self.scores)) 
    
      # Replace the nonelite
      elites = self.pop[-self.n_elites:]
      self.pop[:-self.n_elites] = np.array(
                                  [np.random.choice(elites[:,i],
                                                    (self.n_nonelites)) 
                                  for i in range(self.n_traits)]
                                  ).reshape((self.n_nonelites, self.n_traits))
      
      # Mutate population with noise = lr*std(axis)
      lr = 1
      std = np.array([lr * np.std(self.pop[:,i]) for i in range(self.n_traits)])
      self.pop += std * (np.random.random((self.popsize, self.n_traits)) - 0.5)
      
      self._update_scores()
      self.generation += 1
      self.pop_history.append(self.pop)

      # TODO:
      # implement early stopping

    # Lay over average and fittest lines
    if plot_fitness:
      plt.xlabel('Generation')
      plt.ylabel('Fitness')
      plt.title('Generation vs. Fitness')
      # plt.plot([*range(starting_gen, self.generation)], fittest, color='g')
      plt.plot([*range(starting_gen, self.generation)], averages, color='r')

  # Call after evolving n generations
  def show_weights(self):
    # TODO: 
    # gif evolution

    xs = self.pop[:,0]
    ys = self.pop[:,1]

    intervals = 400
    lim=25
    x = np.linspace(-lim, lim, intervals)
    y = np.linspace(-lim, lim, intervals)
    X, Y = np.meshgrid(x, y)
    Z = self._eval2(X,Y)
    plt.contourf(X, Y, Z, 12, cmap='cubehelix')
    plt.colorbar()
    # plt.imshow(Z, extent=[-lim, lim, -lim, lim], cmap='cubehelix')

    plt.title('Population Progress gen #{}'.format(self.generation))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(min(-lim, min(xs)), max(lim, max(xs)))
    plt.ylim(min(-lim, min(ys)), max(lim, max(ys)))
    plt.scatter(xs, ys, c='b')
    plt.scatter(np.average(xs), np.average(ys), c='r', linewidth=3)
    plt.scatter(xs[-1], ys[-1], c='cyan')




# model = Model(n_params=2)

# a = Pop(popsize=10000,
#         model=model,
#         ngen=25,
#         elitesize=0.5,
#         early_stop=True)
