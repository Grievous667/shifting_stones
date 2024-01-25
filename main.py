import pygame

from src.slot import Slot

class PygameEnvironment():
    def __init__(self, sx, sy, caption, mode=0) -> None:
        self.caption = caption
        self.sx = sx
        self.sy = sy

        self.running = True
        self.can_click = True

        pygame.init()
        pygame.display.set_caption(self.caption)
        self.s = pygame.display.set_mode((self.sx, self.sy))
        self.bg = pygame.Surface((self.sx, self.sy))

        self.grid = []
        gx = Slot.tile_size
        gy = Slot.tile_size / 2
        
        for i in range(3): 
            self.grid.append([])
            for _ in range(3):
                self.grid[i].append(Slot(self.s, gx, gy))
                gx += Slot.tile_size + 10
            gx = Slot.tile_size
            gy += Slot.tile_size + 10

        while self.running == True:
            self.mainloop()

    def exit(self):
        self.running = False

    def mainloop(self):
        self.catch_events()
        self.get_input()
        self.restrict_clicks()
        self.game_logic()

        pygame.display.update()

    def catch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.exit()
                exit()

    def get_input(self):
        self.keys = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()

    def restrict_clicks(self):
        if pygame.mouse.get_pressed()[0]:
            self.can_click = False
        else:
            self.can_click = True

    def game_logic(self):
        self.s.blit(self.bg, [0,0])
        for r in self.grid:
            for g_item in r:
                g_item.draw()
                self.grid = g_item.logic(self.mouse_pos, self.keys, self.grid)
            

if __name__ == '__main__':
    print(__file__)      
    PygameEnvironment(1000, 750, 'Shifting Stones', 0)