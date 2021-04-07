import argparse
import pygame
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from display import Menu
from pop import Pop
from game import Pendulum
from model import Seq


def main():

    args = get_args()

    # User plays
    if args.purpose == 'play':
        p = Pendulum(sim=True)
        p.play()

    # NN plays
    elif args.purpose == 'nn':
        model = Seq()
        p = Pendulum(model=model, sim=True)
        ind = np.load(args.weights)
        p.nn(train=False, ind=ind)

    # Train a NN
    elif args.purpose == 'train':
        model = Seq()
        p = Pendulum(model=model, sim=False)
        pop = Pop(popsize=args.pop_size,
                    n_traits=model.n_params,
                    ngen=args.ngen,
                    lr=args.lr,
                    elitesize=args.elite_size,
                    weight_domain=[-1,1],
                    seed_arr=args.seed_arr)
        pop.evolve(fitness_fn=lambda ind: p.nn(train=True, ind=ind), sequential=True)


def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--purpose',
                        default='play',
                        action='store',
                        choices=['play', 'nn', 'train'],
                        help='Purpose of this run.')

    parser.add_argument('--weights',
                        default='demo/161833.npy',
                        action='store',
                        help='Numpy file holding serialized model weights from training.')

    parser.add_argument('--pop_size',
                        default=100,
                        action='store',
                        help='Number of individuals in the evolving population.')

    parser.add_argument('--ngen',
                        default=10000,
                        action='store',
                        help='Number of generations for evolving the population.')

    parser.add_argument('--lr',
                        default=.1,
                        action='store',
                        help='Learning rate or step size for evolutionary algorithm.')

    parser.add_argument('--elite_size',
                        default=.2,
                        action='store',
                        help='Percentage of individuals to be considered elite.')

    parser.add_argument('--seed_arr',
                        default=None,
                        action='store',
                        help='Numpy file holding serialized model weights from training to seed the population.')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    main()