import pygame
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from display import Menu
from pop import Pop
from debug import db
from game import Pendulum
from model import Seq

'''
# TODO:
    1) argparse
'''
def main():

    # # Play the game yourself
    # p = Pendulum(sim=True)
    # p.play()

    # # Let the NN play
    # model = Seq()
    # p = Pendulum(model=model, sim=True)
    # ind = np.load('checkpoints/51393.npy')
    # p.nn(train=False, ind=ind)

    # Train a NN
    model = Seq()
    p = Pendulum(model=model, sim=False)
    pop = Pop(popsize=100,
                n_traits=model.n_params,
                ngen=10000,
                lr=.1,
                elitesize=0.2,
                weight_domain=[-1,1],
                seed_arr=None)
    pop.evolve(fitness_fn=lambda ind: p.nn(train=True, ind=ind), sequential=True)

if __name__ == '__main__':
    main()
