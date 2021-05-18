import pygame
import numpy as np

from config import *
from display import Menu
from model import Seq
from pop import Pop


class Pendulum():
    '''
    #TODO:
        1) implement board reset so pygame doesn't have to load/quit/reload...
    '''

    def __init__(self, model=None, sim=True):
        self.model = model
        self.sim = sim

        self.w = int(w)
        self.h = int(self.w/2)

        if self.sim:
            pygame.init()
            self.win = pygame.display.set_mode((self.w,self.h))
            pygame.display.set_caption("Inverse Pendulum")
            self.font = pygame.font.SysFont(None, 24)

    def nn(self, train=False, ind=None):
        '''
        Plays the game with a neural net player
        
        - Args
            train: If train, return the fitness score after a number of game ticks, \
                    else play forever

        Returns:
            fitness score
        '''

        self.model._set_weights(ind)

        return self.play(play=not train, nn=True)

    def play(self, play=True, nn=False, ticks=250):
        '''
        The main loop for simulated or non-simulated playing
        
        - Args
            play (bool):
                False limits the time played to the provided number of game ticks
            nn (bool):
                True uses nn for simulation inputs. Use True during training or model testing
            ticks (int):
                Number of game ticks used when play=False

        Returns:
            Fitness score if play=False, else continues until closed
        '''

        global defaults

        w, h, fitness_loc, cb, cdg, clg, ra, rb, o0, do, rdx, r1, r2, a0, a1, b0, b1, vd, vax, dv, adv, fw, fr, fj, g, menu_params = defaults

        fitness = 0

        ####################
        ### Menu loading ###
        ####################

        if play:
            menu = Menu(win=self.win, 
                        w=self.w,
                        h=self.h,
                        params=menu_params)


        #######################
        ### game state loop ###
        #######################

        while True:

            if self.sim:
                # delta T = 40 ms -> 25fps
                pygame.time.delay(40 * play)        

                # reset screen
                self.win.fill(cb)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

            ##############
            ### NN IOs ###
            ##############

            # normalized distance from A to center, [0, 1]
            dist_from_right = (r2[0] - a0) / (2*rdx)
            dist_from_left = (a0 - r1[0]) / (2*rdx)
            # normalized unit distances from A to B, [0, 1]
            ball_dx = (float(b0) - a0) / ra
            ball_dx_pos = ball_dx>0
            ball_dx_neg = ball_dx<0
            ball_dx = np.abs(ball_dx)
            ball_dy = (a1 - float(b1) + 75) / ra
            # horizontal velocity of A / 100
            horizontal_vel = float(vax) / 100
            vax_pos = horizontal_vel>0
            vax_neg = horizontal_vel<0
            horizontal_vel = np.abs(horizontal_vel)
            # angular velocity
            angular_vel = float(o0) / np.pi
            angular_vel_pos = angular_vel>0
            angular_vel_neg = angular_vel<0
            angular_vel = np.abs(angular_vel)


            #################################
            ### input/NN response updates ###
            #################################
            if play:
                g, fr, fj, fw = menu.update()
            if self.sim:
                keys = pygame.key.get_pressed()
                left = keys[pygame.K_LEFT]
                right = keys[pygame.K_RIGHT]
                if keys[pygame.K_r]:
                    self.play(play, nn)
            if nn:
                inputs = np.array([[dist_from_right,
                                    dist_from_left,
                                    ball_dx,
                                    ball_dx_pos,
                                    ball_dx_neg,
                                    ball_dy,
                                    horizontal_vel,
                                    vax_pos,
                                    vax_neg,
                                    angular_vel,
                                    angular_vel_pos,
                                    angular_vel_neg]])

                out = self.model.pred(inputs)
                left = out==0
                right = out==1

            if left and right:
                pass
            elif left:
                vax -= vd
                dv = -vd
            elif right:
                vax += vd
                dv = vd
            # decelerate if no keys pressed
            else:
                if vax >= fr:
                    vax -= fr
                    dv = -fr
                elif vax <= -fr:
                    vax += fr
                    dv = fr
                else:
                    vax = 0
                    dv = 0

            ########################
            ### position updates ###
            ########################

            # check boundary conditions for A and update
            if vax < 0 and a0 + vax <= r1[0]:
                a0 = int(r1[0])
                dv = -vax
                vax = int(-fw * vax)
                dv += vax 
            elif vax > 0 and a0 + vax >= r2[0]:
                a0 = r2[0]
                dv = -vax
                vax = int(-fw * vax)
                dv += vax 
            else:
                a0 += vax

            #######################
            ### angular updates ###
            #######################

            # Tune the impact to angular acceleration caused by player/NN movements 
            dv *= adv
            # Store the net angular velocity
            # 1st component: last time steps angular velocity, reduced by friction at the joint
            # 2nd: angular acceleration due to gravity
            # 3rd: angular acceleration due to movement
            do = (fj * do) + np.arctan2(g * np.cos(o0), ra) - (dv * np.sin(o0))
            # Adjust theta naught accordingly
            o0 += do

            ######################
            ### pygame updates ###
            ######################

            # Lastly, we update B 
            b0 = a0 - int(ra * np.cos(o0))
            b1 = a1 - int(ra * np.sin(o0))

            # Draw simulation components 
            if self.sim:
                # fitness display
                self.win.blit(self.font.render(f'fitness={int(fitness)}', True, (0,255,0)), fitness_loc)

                # rail
                pygame.draw.line(self.win, clg, r1, r2, 3)
                # a
                pygame.draw.circle(self.win, cdg, (int(a0), a1), rb)
                # b
                pygame.draw.circle(self.win, cdg, (int(b0), b1), rb)
                # # arm
                pygame.draw.line(self.win, cdg, (a0, a1), (b0, b1), 5)

                pygame.display.update() 

            # Fitness function
            # 1) Exponential reward for pendulum height
            # 2) Linear punishment for pendulum height
            # 3) Linear punishment for pendulum location 
            fitness += np.exp((a1-b1+150)/55) + (0.15 * (a1-b1)) - (0.2 * np.abs(a0 - self.w/2))

            if not play:
                ticks -= 1
                if not ticks:
                    return fitness