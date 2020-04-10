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

    ###########################
    ### Model and evolution ###
    ###########################

    # Play it yourself
    # p = Pendulum(sim=True)
    # p.play()

    # Let the NN play it
    # model = Seq()
    # p = Pendulum(model=model, sim=True)
    # ind = np.load('checkpoints/demo/161833.npy')
    # p.nn(train=False, ind=ind)

    # Train a NN
    model = Seq()
    p = Pendulum(model=model, sim=False)
    pop = Pop(popsize=1000,
                n_traits=model.n_params,
                ngen=10000,
                lr=.05,
                elitesize=0.01,
                weight_domain=[-1,1],
                seed_arr=161833)

    pop.evolve(fitness_fn=lambda ind: p.nn(train=True, ind=ind), sequential=True)

if __name__ == '__main__':
    main()
