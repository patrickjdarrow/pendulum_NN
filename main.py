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

    pop = Pop(popsize=10,
                model=model,
                ngen=2,
                elitesize=0.1)

    fitness_fn = lambda ind: p.nn(train=True, ind=ind)
    pop.evolve(fitness_fn=fitness_fn, multiprocess=True)

if __name__ == '__main__':
    main()
