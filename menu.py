import pygame

class menu():
    def __init__(self,
                win,
                params,
                sf=0.15,
                padding=20,
                fontsize=None):
    ''' Standalone multi-slider menu
    #TODO:
        1) create pause scheme in main

    Args:
        win: pygame.display
            - Pygame window which will serve as the display canvas
        params: dict {'value name': (min, max)}
            - Dictionary mapping values to their ranges 
            - ex: params =  {'friction': (0.0, 1.0),
                            'acceleration: (0, 10)'}
    KWArgs:
        sf: float
            - Slider size scale factor, relative to window size
        padding: int (default) or float
            - Int padding for a number of pixels, float for padding relative to window width
        fontsize: int
            - pygame.font.SysFont size, defaults to (window height)/30
    '''

        self.win = win
        self.params = params
        self.w = self.win.get_bounding_rect()[2]
        self.h = self.win.get_bounding_rect()[3]
        self.sw = sf * self.w
        self.padding = padding
        self.fontsize = fontsize
        # slider height
        self.sh = 15
        self._init_blueprints()

        self.values = []
        # mouse state (clicked, not clicked)
        self.ms = False
        # last mouse state
        self.lms = False


    def update(self):
        ''' 
        Uses mouse state to update menu. 
        '''
       mpos = pygame.mouse.get_pos()

        # draw slider rails
        for i, param in enumerate(self.params):
            pygame.draw.line(self.win,
                            (0,225, 0),
                            (self.x1, i * self.sh),
                            (self.x2, i * self.sh)

        # mouse state machine


        return ()



    def _init_blueprints(self):
        '''
        Creates blueprints for slider spacing based on pos
        '''
        if self.fontsize:
            self.font = pygame.font.SysFont(None, self.fontsize)
        else:
            self.font = pygame.font.SysFont(None, int(self.h/30))

        if self.padding.__type__ == float:
            self.padding = int(self.padding * self.w)

        self.x1 = self.padding 
        self.x2 = self.padding + self.sw
