import pygame

class Menu():
    def __init__(self,
                win,
                w,
                h,
                params,
                sf=0.05,
                padding=20,
                fontsize=None):
        
        '''
        - Standalone multi-slider menu
        - Updates by checking pygame.type == pygame.MOUSEBUTTONDOWN
        
        #TODO:
            1) create pause scheme in main
            2) generalize collision fn
            3) accomodate int rounding for sliders

        - Args
            win: pygame.display
                - Pygame window which will serve as the display canvas
            w: int
                - Pygame window width
            h: int
                - Pygame window height
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
        def __init__(self, win, var, val, xbounds, y, width, height, range, font, fontx, color=(0,255,0)):
            self.win = win
            self.var = var
            self.xbounds = xbounds
            self.sw = self.xbounds[1] - self.xbounds[0]
            self.x = self.xbounds[0] + self.sw * (val - range[0])/(range[1]-range[0])
            self.y = y
            self.width = width
            self.height = height
            self.color = color
            self.min = min(range)
            self.max = max(range)
            self.range = self.max - self.min
            self.font = font
            self.fontx = fontx

        def update(self, x=None):
            if self.x != x:
                self.x = x

            val = self.min + self.range * (self.x-self.xbounds[0])/(self.sw)

            if type(self.var)==int:
                val = int(val)

            pygame.draw.rect(self.win,
                            self.color,
                            (self.x,self.y,self.width,self.height))
            self.win.blit(self.font.render('{}: {:.3f}'.format(self.var, val), True, (0,255,0)), (self.fontx + 15, self.y))

            return val


    def update(self):
        ''' 
        - Uses mouse state to update menu. 
        
        Returns:
            updated values: list

        '''
        values = []

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
                dx = knob.x

            val = knob.update(dx)
            values.append(val)

        return values


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
                            var=param,
                            val=self.params[param][0],
                            xbounds = (self.x1, self.x2),
                            y=self.padding + i * 2 * self.sh,
                            width=int(self.sh/5),
                            height=self.sh,
                            range=(self.params[param][1], self.params[param][2]),
                            font=self.font,
                            fontx=self.x2,
                            color=(0,255,0))
                        for i, param in enumerate(self.params)]

    def _draw_lines(self):
        # rails extend from x1 to x2 + knob width
        for i, param in enumerate(self.params):
            y = self.padding + i * 2 * self.sh + int(self.sh/2)
            pygame.draw.line(
                    self.win,
                    (0,225,0),
                    (self.x1, y),
                    (self.x2 + int(self.sh/3), y))

    def _check_collision(self, mpos, knob):
        if mpos[0] > self.x1-0.1*self.sw and \
            mpos[0] < self.x2+0.1*self.sw and \
            mpos[1] > knob.y-0.15*self.sh and \
            mpos[1] < knob.y+knob.height+0.15*self.sh:
            return True
        return False

    def _constrain(self, a, min, max):
        if a < min:
            return min
        elif a > max:
            return max
        return a
