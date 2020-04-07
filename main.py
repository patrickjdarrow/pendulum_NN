import pygame
import numpy as np

from display import Menu
from model import Seq
from pop import Pop
from debug import db
from game import Pendulum

def main():

    ###########################
    ### Model and evolution ###
    ###########################

    model = Seq()

    # n_weights = np.sum([np.prod(layer.shape) for layer in model.get_weights()])
    # pop = np.random.random((popsize, n_weights))

    p = Pendulum(model=model)
    # ind = np.load('logs/6900.npy')
    # p.nn(train=False, ind=ind)

    pop = Pop(popsize=50,
                model=model,
                ngen=100,
                lr=2e-2,
                elitesize=0.2,
                weight_domain=[-1,1],
                seed_arr=None)

    fitness_fn = lambda ind: p.nn(train=True, ind=ind)
    pop.evolve(fitness_fn=fitness_fn, multiprocess=True)

if __name__ == '__main__':
    main()
