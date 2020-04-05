import pygame
import numpy as np
from display import Menu
from model import Seq


def main():
    pygame.init()

    timescale = 40

    w = int(1500)
    h = int(w/2)

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
    ra = int(w/10)
    # ball radii
    rb = int(w/100)
    # current angle
    o0 = 0
    # angular velocity, delta theta
    do = 0
    # ball end coordinates (0: x, 1: y)
    a0 = int(w/2)
    a1 = int(h/2 - ra)
    b0 = a0 - int(ra * np.cos(o0))
    b1 = a1 - int(ra * np.sin(o0))
    # rail length and endpoints
    rdx = int(w/3)
    r1 = (int(w/2 - rdx), a1)
    r2 = (int(w/2 + rdx), a1)

    ################
    ### Movement ###
    ################

    # velocities
    vd = 5
    vax = 0
    vmax = np.abs(vax)
    dv = 0
    adv = 0.0035
    # friction due to wall (inelastic collision)
    fw = 0.45
    # friction due to rail (deceleration constant)
    fr = 2
    # friction at the join of a (fractional angular velocity retention)
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

    #################
    ### Load Menu ###
    #################

    # menu = Menu(win=win, 
    #             w=w,
    #             h=h,
    #             params={'g': (g,0,-10),
    #                     'fr': (fr,0,10),
    #                     'fj': (fj, 0.8,1.1),})

    #############
    ### Model ###
    #############

    model = Seq()

    #################################
    ### Draw rail, pendulum, text ###
    #################################

    def draw():

        global rmin, rmax
        # update B
        b0 = a0 - int(ra * np.cos(o0))
        b1 = a1 - int(ra * np.sin(o0))

        # # font
        # win.blit(font.render('v={}'.format(vax), True, (0,255,0)), (20, 20))
        # win.blit(font.render('vmax={}'.format(vmax), True, (0,255,0)), (20, 40))
        # win.blit(font.render('fw={}'.format(fw), True, (0,255,0)), (20, 60))
        # dist = np.sqrt( (a0 - b0)**2 + (a1 - b1)**2)
        # if dist > rmax:
        #     rmax = dist
        # elif dist < rmin:
        #     rmin = dist
        # win.blit(font.render('rmax={}'.format(rmax), True, (0,255,0)), (20, 80))
        # win.blit(font.render('rmin={}'.format(rmin), True, (0,255,0)), (20, 100))
        # win.blit(font.render('do={}'.format(do), True, (0,255,0)), (20, 120))

        # rail
        pygame.draw.line(win, clg, r1, r2, 3)
        # a
        pygame.draw.circle(win, cdg, (int(a0), a1), rb)
        # b
        pygame.draw.circle(win, cdg, (int(b0), b1), rb)
        # # arm
        pygame.draw.line(win, cdg, (a0, a1), (b0, b1), 5)


    #######################
    ### game state loop ###
    #######################

    

    while True:
        # delta T = 40 ms -> 25fps
        pygame.time.delay(timescale)        

        # reset screen
        win.fill(cb)

        ##############
        ### NN IOs ###
        ##############

        # normalized distance from A to center, [-1, 1]
        center_dist = (a0 - r1[0]) / rdx - 1
        # normalized unit distances from A to B, [-1, 1]
        ball_dx = (float(b0) - a0) / ra
        ball_dy = (float(b1) - a1) / ra
        # horizontal velocity of A / 100
        horizontal_vel = float(vax) / 100
        # angular velocity
        angular_vel = float(o0) / np.pi

        inputs = np.array([[center_dist,
                                    ball_dy,
                                    ball_dx,
                                    horizontal_vel,
                                    angular_vel]])

        # 0 = left
        # 1 = no move
        # 2 = right
        out = model.pred(inputs)

        ####################
        ### Menu updates ###
        ####################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # g, fr, fj = menu.update()


        ##############################
        ### input response updates ###
        ##############################

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

        # ###########################
        # ### NN response updates ###
        # ###########################

        # # left
        # if out == 0:
        #     vax -= vd
        #     dv = -vd
        # # right
        # elif out ==2:
        #     vax += vd
        #     dv = vd
        # # out == 1
        # # decelerate 
        # else:
        #     if vax >= fr:
        #         vax -= fr
        #         dv = -fr
        #     elif vax <= -fr:
        #         vax += fr
        #         dv = fr
        #     else:
        #         vax = 0
        #         dv = 0

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
