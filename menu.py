import pygame

class Menu():
    def __init__(self,
                win,
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
        self.w = self.win.get_bounding_rect()[2]
        self.h = self.win.get_bounding_rect()[3]
        self.sw = int(sf * self.w)
        self.padding = padding
        self.fontsize = fontsize
        # slider height
        self.sh = 35

        self._init_blueprints()

        # mouse state (clicked, not clicked)
        self.ms = False
        # last mouse state
        self.lms = False
        # index of slider currently being clicked
        self.clicked = -1


    def update(self, md=False):
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
        self.ms = md
        mpos = pygame.mouse.get_pos()

        # draw slider rails
        for i, param in enumerate(self.params, start=1):
            if i == self.clicked:
                pass
            else:
                cx = self.x1 + int(self.sw * )
            cy = i * self.sh
            pygame.draw.line(self.win,
                            (0,225, 0),
                            (self.x1, cy),
                            (self.x2, cy))
            center = ()


        # mouse state machine

        self.lms = self.ms

        return None

    def _bound(self, a, b, c):
        pass


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
        self.y1 = self.padding 

        self.knobs = [pygame.draw.rect(
                            self.win,
                            (0,255,0),
                            (self.x1,
                                self.padding + i * 2 * self.sh,
                                int(self.sh/3),
                                self.sh))
                        for i in len(params)]
        self.rails = [pygame.draw.line(
                            self.win,
                            (0,225,0),
                            (self.x1,
                                self.padding + i * 2 * self.sh + int(self.sh/2)),
                            (self.x2 + int(self.sh/3),
                                self.padding + i * 2 * self.sh + int(self.sh/2)))
                        for i in len(params)]
        self.update()