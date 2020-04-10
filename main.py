import pygame
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from display import Menu
from pop import Pop
from debug import db
from game import Pendulum
from model import Seq

def main():
    '''
    # TODO:
        1) argparse
    '''

    ###########################
    ### Model and evolution ###
    ###########################

    # Play it yourself
    # p = Pendulum(sim=True)
    # p.play()

    # # Let the NN play it
    # model = Seq()
    # p = Pendulum(model=model, sim=True)
    # ind = np.load('checkpoints/19370.npy')
    # p.nn(train=False, ind=ind)

    # Train a NN
    model = Seq()
    p = Pendulum(model=model, sim=False)
    pop = Pop(popsize=100,
                n_traits=model.n_params,
                ngen=10000,
                lr=.01,
                elitesize=0.1,
                weight_domain=[-1,1],
                seed_arr=20288)

    pop.evolve(fitness_fn=lambda ind: p.nn(train=True, ind=ind), sequential=True)

if __name__ == '__main__':
    main()
