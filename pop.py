import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn
import pickle
import multiprocessing
from multiprocessing import Pool

plt.rcParams['figure.figsize'] = 16, 13
np.random.seed(1)

# Dummy model class
class Model():
  def __init__(self,
               n_params):
    self.n_params = n_params

    '''
    #TODO
      1) MultiProcessing
      2) Docstrings
      3) More evolution schemes

    '''
class Pop():
  def __init__(self,
               popsize,
               n_traits,
               ngen,
               lr = 1.0,
               elitesize=0.1,
               weight_domain=[6*np.pi+1, 6*np.pi-1],
               early_stop=False,
               seed_arr=None,
               ):

    # Set population parameters
    self.popsize = popsize
    self.ngen = ngen
    self.lr = lr
    self.elitesize = elitesize
    self.n_elites = int(self.popsize * self.elitesize); assert self.n_elites > 0
    self.n_nonelites = self.popsize - self.n_elites; assert self.n_nonelites > 0
    self.early_stop = early_stop
    self.seed_arr = seed_arr

    # Track current generation
    self.generation = 0

    # Initialize population with n_traits
    self.weight_domain = weight_domain
    self.n_traits = n_traits
    self.pop = self._reset_pop()
    self.scores = np.ndarray(self.popsize)
    self.fittest = None
    self.fittest_score = None

  def _reset_pop(self):

    self.generation = 0

    # Get range and mean
    r = np.ptp(self.weight_domain)
    m = np.mean(self.weight_domain)

    # Dummy population
    pop = r * (np.random.sample((self.popsize, self.n_traits)) - 0.5) + m

    # Reseed
    if self.seed_arr:
      print(f'Seeding: {self.seed_arr}.npy')
      self.fittest = self.seed_arr

      pop[-1] = np.load(f'checkpoints/{str(self.seed_arr)}.npy')

      if self.n_elites == 1:
        for i in range(self.popsize-1):
          pop[i] = pop[-1]
        pop[:-1] += np.random.normal(loc=0.0, scale = self.lr, size=(self.popsize-1, self.n_traits))

    else:
      print('Using no seed\n')
    return pop

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
  def _update_scores(self, fitness_fn=None, sequential=False, multiprocess=False):
    if fitness_fn:
      if multiprocess:
        #TODO: finish multiprocessing of model prediction
        scores = []
        print(self.scores)
        print(scores)
        p = Pool(processes=multiprocessing.cpu_count()-1)
        res = p.apply_async(fitness_fn, [ind for ind in self.pop])
        scores.append(res.get(timeout=5))
        self.scores = np.array(scores)
        print(self.scores)
        print(scores)
      elif sequential:
        self.scores = np.array([fitness_fn(ind) for ind in self.pop])        
      else:
        self.scores = fitness_fn(self.pop)
    else:
      self.scores = self._eval2(self.pop[:,0], self.pop[:,1])

    order = np.argsort(self.scores).reshape((self.popsize))
    self.pop = self.pop[order]
    self.scores = self.scores[order]

    if self.fittest_score:
      if self.scores[-1] > self.fittest_score:
        self.fittest_score = self.scores[-1]
        self.fittest = self.pop[-1]
        print(f'Saving: {int(self.fittest_score)}_{self.generation}.npy.npy')
        np.save(f'checkpoints/{int(self.fittest_score)}_{self.generation}.npy', self.fittest)
    else:
      self.fittest_score = self.scores[-1]
      self.fittest = self.pop[-1]
      print(f'Saving: {int(self.fittest_score)}_{self.generation}.npy')
      np.save(f'checkpoints/{int(self.fittest_score)}_{self.generation}.npy', self.fittest)

  @property
  def get_scores(self):
    return self.scores

  # TODO: assign replacement scheme for each strat
    #1) replace std calculation with np.along_axis
    #2) parameterize preserve fittest
    #3) better logging
    #4) parameterize example code
    #5) implement early stopping
    #6) separate plotting into it's own module

  def evolve(self,
            fitness_fn=None,
            sequential=False,
            multiprocess=False,
            plot_fitness=False,):

    print('Evolving...')
    print(f'\tpopsize: {self.popsize}\n\tngen: {self.ngen}\n\tlr: {self.lr}\n\telitesize: {self.elitesize}\n')

    if os.path.exists('checkpoints'):
      pass
    else:
      print('Creating checkpoints directory...')
      os.mkdir('checkpoints')

    starting_gen = self.generation
    averages = []

    for gen in range(1, self.ngen+1):

      print(f'Generation: {gen}')

      self._update_scores(fitness_fn=fitness_fn, sequential=sequential, multiprocess=multiprocess)
      
      # if plot_fitness:
      #   plt.scatter([self.generation]*self.popsize, self.scores)
      #   averages.append(np.mean(self.scores))
      #   fittest.append(np.max(self.scores)) 
    
      # Replace the nonelite
      self.pop[:-self.n_elites] = np.array(
                                  [np.random.choice(self.pop[-self.n_elites:][:,i],
                                                    (self.n_nonelites)) 
                                  for i in range(self.n_traits)]
                                  ).T.reshape((self.n_nonelites, self.n_traits))
      
      # Mutate population (except the fittest) with noise = lr*std(axis)
      # Use the 2 lines below to also mutate the fittest individual 
      # std = np.array([self.lr * np.std(self.pop[:,i]) for i in range(self.n_traits)])
      # self.pop[:] += std * (np.random.random((self.popsize, self.n_traits)) - 0.5)
      if self.n_elites > 1:
        std = np.array([self.lr * np.std(self.pop[:,i]) for i in range(self.n_traits)])
      else:
        std = self.lr
      self.pop[:-1] += np.random.normal(loc=0.0, scale = std, size=(self.popsize-1, self.n_traits))

      print(f'fittest: {int(np.max(self.scores))}, ',
            f'median: {int(np.median(self.scores))}, worst elite: {int(self.scores[-self.n_elites])},',
            f'mean: {int(np.mean(self.scores))}')
      self.generation += 1

    # Lay over average and fittest lines
    # if plot_fitness:
    #   plt.xlabel('Generation')
    #   plt.ylabel('Fitness')
    #   plt.title('Generation vs. Fitness')
    #   # plt.plot([*range(starting_gen, self.generation)], fittest, color='g')
    #   plt.plot([*range(starting_gen, self.generation)], averages, color='r')

  # Call after evolving n generations
  def show_weights(self):

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

# model = Model(n_params=n_params)

# a = Pop(popsize=popzise,
#         n_traits=model.n_params,
#         ngen=ngen,
#         elitesize=0.5,
#         early_stop=True)

# a.evolve()