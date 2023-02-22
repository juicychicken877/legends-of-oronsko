from settings import *
from support import import_folder

class Effect(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()

        self.x = x
        self.y = y

        # path to the graphics folder
        path = 'graphics/effects/claw'

        self.images = import_folder(path)

        # the number of images in folder
        self.image_num = len(self.images)

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # animation
        self.frame_index = 0
        self.animation_speed = 0.2

    def animate(self):
        self.image = self.images[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.frame_index += self.animation_speed

        if self.frame_index >= self.image_num:
            self.kill()


    def update(self):
        self.animate()

class Claw(Effect):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)

        path = 'graphics/effects/claw'
        self.images = import_folder(path)
        self.image_num = len(self.images)

class DeadBamboo(Effect):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)

        path = 'graphics/effects/dead_bamboo'
        self.images = import_folder(path)
        self.image_num = len(self.images)

class DeadSquid(Effect):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)

        path = 'graphics/effects/dead_squid'
        self.images = import_folder(path)
        self.image_num = len(self.images)

class BambooAttack(Effect):
    def __init__(self, x, y):
        super().__init__(x, y)

        path = 'graphics/effects/bamboo_attack'
        self.images = import_folder(path)
        self.image_num = len(self.images)

class SquidAttack(Effect):
    def __init__(self, x, y):
        super().__init__(x, y)

        path = 'graphics/effects/squid_attack'
        self.images = import_folder(path)
        self.image_num = len(self.images)

class Leaf(Effect):
    def __init__(self, x, y, index) -> None:
        super().__init__(x, y)

        path = 'graphics/effects/leaf' + index
        self.images = import_folder(path)
        self.image_num = len(self.images)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

    def animate(self):
        self.image = self.images[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

        self.frame_index += self.animation_speed

        if self.frame_index >= self.image_num:
            self.kill()

class Heal(Effect):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)

        path = 'graphics/effects/heal/frames'
        self.images = import_folder(path)
        self.image_num = len(self.images)

