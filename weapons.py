from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, index) -> None:
        super().__init__()

        # images depending on player posititon

        # axe images
        self.axe_image_up = pygame.image.load('graphics/weapons/axe/up.png').convert_alpha()
        self.axe_image_down = pygame.image.load('graphics/weapons/axe/down.png').convert_alpha()
        self.axe_image_left = pygame.image.load('graphics/weapons/axe/left.png').convert_alpha()
        self.axe_image_right = pygame.image.load('graphics/weapons/axe/right.png').convert_alpha()

        # sword images
        self.sword_image_up = pygame.image.load('graphics/weapons/sword/up.png').convert_alpha()
        self.sword_image_down = pygame.image.load('graphics/weapons/sword/down.png').convert_alpha()
        self.sword_image_left = pygame.image.load('graphics/weapons/sword/left.png').convert_alpha()
        self.sword_image_right = pygame.image.load('graphics/weapons/sword/right.png').convert_alpha()

        if player.up:
            if index == 1:
                self.image = self.axe_image_up
            if index == 2:
                self.image = self.sword_image_up

            self.rect = self.image.get_rect(midbottom=(player.rect.centerx-10, player.rect.top))

        if player.down:
            if index == 1:
                self.image = self.axe_image_down
            if index == 2:
                self.image = self.sword_image_down

            self.rect = self.image.get_rect(midtop=(player.rect.centerx-10, player.rect.bottom))

        if player.left:
            if index == 1:
                self.image = self.axe_image_left
            if index == 2:
                self.image = self.sword_image_left

            self.rect = self.image.get_rect(midright=(player.rect.left, player.rect.centery+15))

        if player.right:
            if index == 1:
                self.image = self.axe_image_right
            if index == 2:
                self.image = self.sword_image_right
                
            self.rect = self.image.get_rect(midleft=(player.rect.right, player.rect.centery+15))
        
        # weapon damage 
        self.weapon_damage = 20

    
