from settings import *
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, spawner_index, type, obstacle_sprites):
        super().__init__()
        
        # enemy type
        if type=='bamboo':
            self.image = pygame.image.load('graphics/enemies/bamboo/0.png').convert_alpha()
            self.speed = 3
            self.type = 'bamboo'

            self.notice_radius = 300
            self.attack_radius = 75
            self.attack_cooldown = 0

            # graphics
            self.idle_image = import_folder('graphics/enemies/bamboo/idle')
            self.attack_image = import_folder('graphics/enemies/bamboo/move')
            self.move_image = import_folder('graphics/enemies/bamboo/move')

        elif type=='squid':
            self.image = pygame.image.load('graphics/enemies/squid/0.png').convert_alpha()
            self.speed = 3
            self.type = 'squid'

            self.notice_radius = 250
            self.attack_radius = 75
            self.attack_cooldown = 0

            # graphics
            self.idle_image = import_folder('graphics/enemies/squid/idle')
            self.attack_image = import_folder('graphics/enemies/squid/move')
            self.move_image = import_folder('graphics/enemies/squid/move')

        self.rect = self.image.get_rect(topleft=(x, y))

        # stats
        self.HP = 100
        self.hurt_cooldown = 0
        self.gotHit = False
        self.status = 'stop'
        self.direction = pygame.math.Vector2()

        # animations
        self.frame_index = 0
        self.animation_speed = 0.1

        # sounds
        self.gotHit_sound = pygame.mixer.Sound('sounds/Hit.wav')
        self.gotHit_sound.set_volume(0.15)

        self.player = player
        self.index = spawner_index
        self.obstacle_group = obstacle_sprites

    def animate(self):
        if self.status == 'stop':
            self.image = self.idle_image[int(self.frame_index)]
        elif self.status == 'move':
            self.image = self.move_image[int(self.frame_index)]
        elif self.status == 'attack':
            self.image = self.attack_image[int(self.frame_index)]

        self.frame_index += self.animation_speed

        # reset
        if self.frame_index >= 4:
            self.frame_index = 0

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.isColliding('x')
        self.rect.y += self.direction.y * self.speed
        self.isColliding('y')

    def isColliding(self, direction):
        # checking colision on X
        if direction == 'x':
            for sprite in self.obstacle_group:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left # moving to right
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right # moving to left

        # checking colision on Y
        if direction == 'y':
            for sprite in self.obstacle_group:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top # moving to the bottom
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom # moving to the top

    def isHit(self, player_weapon):
        if self.rect.colliderect(player_weapon.rect):
            if not self.gotHit:
                self.gotHit_sound.play()
                self.HP -= self.player.base_damage + player_weapon.weapon_damage
                self.gotHit = True
                self.hurt_cooldown = 300

    def get_player(self):
        # get player distance and direction
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(self.player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector)
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self):
        distance = self.get_player()[0]

        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'stop'
    
    def hit_knockdown(self):
        if self.gotHit:
            self.direction *= -self.speed

    def reduce_cooldowns(self):
        # reduce cooldown
        if self.hurt_cooldown > 0:
            self.hurt_cooldown -= 10
        else:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 10
            self.gotHit = False

    def attack(self):
        if self.attack_cooldown <= 0:
            # decrease players hp when attacked
            self.player.gotHit = True
            self.player.who_attacked = self.type
            self.player.hp -= 10
            self.attack_cooldown = 1000

    def action(self):
        if self.status == 'attack':
            self.attack()
        elif self.status == 'move':
            self.direction = self.get_player()[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.get_player()
        self.get_status()
        self.action()
        self.hit_knockdown()
        self.move()
        self.animate()
        self.reduce_cooldowns()
