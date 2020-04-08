import pygame
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from display import Menu
from pop import Pop
from debug import db
from game import Pendulum
from model import Seq, n_traits

def main():

    ###########################
    ### Model and evolution ###
    ###########################

    model = Seq()
    p = Pendulum(model=model, sim=True)
    p.play()

    # ind = np.load('checkpoints/7230.npy')
    # p.nn(train=False, ind=ind)

    pop = Pop(popsize=100,
                n_traits=n_traits,
                ngen=10000,
                lr=.1,
                elitesize=0.1,
                weight_domain=[-1,1],
                seed_arr=26008)

    pop.evolve(fitness_fn=lambda ind: p.nn(train=True, ind=ind), sequential=True)

if __name__ == '__main__':
    main()
