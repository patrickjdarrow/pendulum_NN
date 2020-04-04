import pygame
import numpy as np
# from model import Model

class menu(win):
    def __init__(self, pos=0, sf=0.15, padding=20):
    ''' Standalone multi-slider menu
    #TODO:

    Args:
        pos {int}
            Menu position
            0: upper left
            1: upper right
            2: lower left
            4: lower right
        sf {float}
            Slider size scale factor, relative to window size
        padding {int}
            pixel padding

    '''

        self.win = win
        self.w = self.win.get_bounding_rect()[2]
        self.h = self.win.get_bounding_rect()[3]
        self.sf = sf
        self.padding = padding
        self.pos = pos
        self._init()
        

    def update(self, mpos=None):
        ''' 
        Uses mouse state to update menu 
        '''
        if not mpos:
            mpos = pygame.mouse.get_pos()

    def _init(self):
        '''
        Creates a blueprint for slider spacing based on pos
        '''

        if self.pos in [0, 2]:
            self.x1 = self.padding 
            self.dx = 1
        elif self.pos in [1, 3]:
            self.x1 = self.w - self.padding
            self.dx = -1
        else:
            raise AttributeError
        if self.pos in [0, 1]:
            self.y1 = self.padding
            self.dy = 1
        else:
            self.y1 = self.h - self.padding
            self.dy = -1







def main():
    pygame.init()

    timescale = 40

    w = 1500
    h = w/2

    win = pygame.display.set_mode((w,h))
    pygame.display.set_caption("Inverse Pendulum")
    font = pygame.font.SysFont(None, 24) 

    ##############
    ### Colors ###
    ##############

    cb = (0, 0, 0)
    cdg = (252, 252, 252)
    clg = (70, 70, 70)

    ###########################
    ### Physical properties ###
    ###########################

    # arm radius
    ra = w/10
    # ball radii
    rb = w/100
    # current angle
    o0 = 0
    # angular velocity, delta theta
    do = 0
    # ball end coordinates (0: x, 1: y)
    a0 = w/2
    a1 = h/2 - ra
    b0 = a0 - int(ra * np.cos(o0))
    b1 = a1 - int(ra * np.sin(o0))
    # rail length and endpoints
    rdx = w/3
    r1 = (w/2 - rdx, a1)
    r2 = (w/2 + rdx, a1)

    ################
    ### Movement ###
    ################

    # velocities
    vd = 5
    vax = 0
    vmax = np.abs(vax)
    w = 0
    dv = 0
    adv = 0.0035
    # friction due to wall (inelastic collision)
    fw = 0.45
    # friction due to rail (deceleration constant)
    fr = 2
    # friction at the join of a (angular deceleration)
    fj = 0.991
    # gravity
    g = - 4

    #################
    ### Test vars ###
    #################

    #TODO: get rid of globals
    global rmin, rmax
    rmin = np.sqrt( (a0 - b0)**2 + (a1 - b1)**2)
    rmax = rmin

    #################
    ### NN Params ###
    #################

    load_weights = True

    #################################
    ### Draw rail, pendulum, text ###
    #################################

    def draw():

        global rmin, rmax
        # update B
        b0 = a0 - int(ra * np.cos(o0))
        b1 = a1 - int(ra * np.sin(o0))

        # reset screen
        win.fill(cb)

        # font
        win.blit(font.render('v={}'.format(vax), True, (0,255,0)), (20, 20))
        win.blit(font.render('vmax={}'.format(vmax), True, (0,255,0)), (20, 40))
        win.blit(font.render('fw={}'.format(fw), True, (0,255,0)), (20, 60))
        dist = np.sqrt( (a0 - b0)**2 + (a1 - b1)**2)
        if dist > rmax:
            rmax = dist
        elif dist < rmin:
            rmin = dist
        win.blit(font.render('rmax={}'.format(rmax), True, (0,255,0)), (20, 80))
        win.blit(font.render('rmin={}'.format(rmin), True, (0,255,0)), (20, 100))
        win.blit(font.render('do={}'.format(do), True, (0,255,0)), (20, 120))

        # rail
        pygame.draw.line(win, clg, r1, r2, 3)
        # a
        pygame.draw.circle(win, cdg, (a0, a1), rb)
        # b
        pygame.draw.circle(win, cdg, (b0, b1), rb)
        # # arm
        pygame.draw.line(win, cdg, (a0, a1), (b0, b1), 5)


    #######################
    ### game state loop ###
    #######################

    while True:
        # delta T = 40 ms -> 25fps
        pygame.time.delay(timescale)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        

        #################
        ### NN Inputs ###
        #################

        # normalized distance from A to center, [-1, 1]
        center_dist = 2 * (a0 - r1[0]) / rdx - 1
        # normalized unit distances from A to B, [-1, 1]
        ball_dx = (b0 - a0) / ra
        ball_dy = (b1 - a1) / ra
        # horizontal velocity of A / 100
        horizontal_vel = vax / 100
        # angular velocity
        angular_vel = o0


        ###################
        ### vax updates ###
        ###################

        # asssess key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            pass
        elif keys[pygame.K_LEFT]:
            vax -= vd
            dv = -vd
        elif keys[pygame.K_RIGHT]:
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
            a0 = r1[0]
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
        # update B
        b0 = a0 - int(ra * np.cos(o0))
        b1 = a1 - int(ra * np.sin(o0))

        #######################
        ### angular updates ###
        #######################

        dv *= adv
        do = fj * do + np.arctan2(g * np.cos(o0), ra) - dv * np.sin(o0)
        o0 += do

        # log vmax
        if np.abs(vax) > vmax:
            vmax = np.abs(vax)

        ######################
        ### pygame updates ###
        ######################

        draw()

        pygame.display.update() 
        
if __name__ == '__main__':
    main()
