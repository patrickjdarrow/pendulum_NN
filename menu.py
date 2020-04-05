import pygame

class Menu():
    def __init__(self,
                win,
                w,
                h,
                params,
                sf=0.10,
                padding=20,
                fontsize=None):
        
        '''
        - Standalone multi-slider menu
        - Updates by checking pygame.type == pygame.MOUSEBUTTONDOWN
        
        #TODO:
            1) create pause scheme in main

        - Args
            win: pygame.display
                - Pygame window which will serve as the display canvas
            params: dict {'value name': (cur, min, max)}
                - Dictionary mapping values to their ranges 
                - ex: params =  {'friction': (0.2, 0.0, 1.0),
                                'acceleration: (7, 0, 10)'}
        - KWArgs
            sf: float
                - Slider size scale factor, relative to window size
            padding: int (default) or float
                - Int padding for a number of pixels, float for padding relative to window width
            fontsize: int
                - pygame.font.SysFont size, defaults to (window height)/30
        '''

        self.win = win
        self.params = params
        self.w = w
        self.h = h
        self.sw = int(sf * self.w)
        self.padding = padding
        self.fontsize = fontsize
        # slider height
        self.sh = 25
        # number of drawers
        self.nd = len(self.params)

        self._init_blueprints()

        # mouse state (clicked, not clicked)
        self.ms = False

        self.update()

    class _Drawer():
        def __init__(self, win, x, y, width, height, range, color=(0,255,0)):
            self.win = win
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.min = range[0]
            self.max = range[1]
            self.range = self.max - self.min

        def update(self, x=None):
            if self.x != x:
                self.x = x
            pygame.draw.rect(self.win,
                            self.color,
                            (self.x,self.y,self.width,self.height))


    def update(self):
        ''' 
        Uses mouse state to update menu. 

        -Args:
            md: bool
                - Use in main loop as shown:
                    # loop start
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_down = True
                    menu.update(md=mouse_down)

        '''
        # get mouse state
        self.ms = pygame.mouse.get_pressed()[0]
        if self.ms:
            mpos = pygame.mouse.get_pos()

        # refresh rails and update sliders
        self._draw_lines()
        for i, knob in enumerate(self.knobs):
            # update slider coordinates
            if self.ms and self._check_collision(mpos, knob):
                dx = self._constrain(mpos[0], self.x1, self.x2)
            else:
                # dx = int(self.x1 + 
                #         self.sw * self.params[param][0] /
                #         (self.params[param][2] - self.params[param][1]))
                dx = knob.x

            self.knobs[i].update(dx)

        return None

    def _constrain(self, a, min, max):
        if a < min:
            return min
        elif a > max:
            return max
        return a


    def _init_blueprints(self):
        '''
        Creates blueprints for slider spacing based on pos
        '''
        if self.fontsize:
            self.font = pygame.font.SysFont(None, self.fontsize)
        else:
            self.font = pygame.font.SysFont(None, int(self.h/30))

        if type(self.padding) == float:
            self.padding = int(self.padding * self.w)

        self.x1 = self.padding 
        self.x2 = self.padding + self.sw

        self.knobs = [self._Drawer(
                            win=self.win,
                            x=self.x1,
                            y=self.padding + i * 2 * self.sh,
                            width=int(self.sh/5),
                            height=self.sh,
                            range=(self.params[param][1], self.params[param][2]),
                            color=(0,255,0))
                        for i, param in enumerate(self.params)]

    def _draw_lines(self):
        # rails extend from x1 to x2 + knob width
        for i in range(self.nd):
            pygame.draw.line(
                    self.win,
                    (0,225,0),
                    (self.x1,
                        self.padding + i * 2 * self.sh + int(self.sh/2)),
                    (self.x2 + int(self.sh/3),
                        self.padding + i * 2 * self.sh + int(self.sh/2)))

    def _check_collision(self, mpos, knob):
        if mpos[0] > self.x1-25 and \
            mpos[0] < self.x2+25 and \
            mpos[1] > knob.y-15 and \
            mpos[1] < knob.y+knob.height+15:
            return True
        return False
