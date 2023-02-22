from settings import *
from level import Level
from level_data import level_data 

class Game:
    def __init__(self):
        self.level = Level(level_data, screen)
        self.music = pygame.mixer.Sound('music/Story.ogg')
        self.music.set_volume(0.1)
        self.music.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            self.level.run() 
            pygame.display.update()
            clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()

    