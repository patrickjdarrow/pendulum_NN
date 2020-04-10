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

    model = Seq()
    # p = Pendulum(model=model, sim=False)

    p = Pendulum(model=model, sim=True)
    # p.play()
    ind = np.load('checkpoints/161833.npy')
    p.nn(train=False, ind=ind)

    pop = Pop(popsize=100,
                n_traits=model.n_params,
                ngen=10000,
                lr=.0005,
                elitesize=0.01,
                weight_domain=[-1,1],
                seed_arr=161833)

    pop.evolve(fitness_fn=lambda ind: p.nn(train=True, ind=ind), sequential=True)

if __name__ == '__main__':
    main()
