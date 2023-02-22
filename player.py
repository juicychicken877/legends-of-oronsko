from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacle_group, destroy_attack):
        super().__init__()
        self.image = pygame.image.load('graphics/player/not_moving/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topright=(x, y))

        # stats
        self.speed = 4
        self.max_hp = 100
        self.hp = 100
        self.xp = 0
        self.points = 0
        self.level = 1
        self.base_damage = 5

        # type of enemy who attacked player, used for drawing proper attack effect
        self.who_attacked = ''
        self.gotHit = False

        self.direction = pygame.math.Vector2()

        self.destroy_attack = destroy_attack
        self.animation_speed = 0.2
        self.weapon_index = 1

        # importing walk images and making animations
        self.run_frames_up = import_folder('graphics/player/up') 
        self.run_frames_down = import_folder('graphics/player/down') 
        self.run_frames_left = import_folder('graphics/player/left') 
        self.run_frames_right = import_folder('graphics/player/right') 
        self.frame_index = 0

        # idle images
        self.up_idle = pygame.image.load('graphics/player/not_moving/up_idle/idle_up.png').convert_alpha()
        self.down_idle = pygame.image.load('graphics/player/not_moving/down_idle/idle_down.png').convert_alpha()
        self.left_idle = pygame.image.load('graphics/player/not_moving/left_idle/idle_left.png').convert_alpha()
        self.right_idle = pygame.image.load('graphics/player/not_moving/right_idle/idle_right.png').convert_alpha()
        
        # attack images 
        self.attack_up = pygame.image.load('graphics/player/up_attack/attack_up.png').convert_alpha()
        self.attack_down = pygame.image.load('graphics/player/down_attack/attack_down.png').convert_alpha()
        self.attack_left = pygame.image.load('graphics/player/left_attack/attack_left.png').convert_alpha()
        self.attack_right = pygame.image.load('graphics/player/right_attack/attack_right.png').convert_alpha()
        self.isAttacking = False

        # cooldowns
        self.attack_cooldown = 400
        self.attack_durability = 0
        self.weapon_change_cooldown = 0
        self.hurt_cooldown = 0
        self.upgrade_cooldown = 0

        # heal
        self.heal_cooldown = 8000
        self.heal_power = 20
        self.isHealing = False

        # bool variables telling us what direction player faces atm
        self.right = False
        self.left = False
        self.up = False
        self.down = True

        # sound effects
        self.attack_sound = pygame.mixer.Sound('sounds/attack/claw.wav')
        self.attack_sound.set_volume(0.5)

        self.heal_sound = pygame.mixer.Sound('sounds/heal.wav')
        self.heal_sound.set_volume(0.5)

        self.up_sound = pygame.mixer.Sound('sounds/Success3.wav')
        self.up_sound.set_volume(0.2)

        # groups
        self.obstacle_group = obstacle_group

    def input(self):
        keys = pygame.key.get_pressed()

        # moving
        if keys[pygame.K_SPACE] and self.attack_cooldown <= 0:
            self.weapon_change_cooldown = 100
            self.attack_cooldown = 400
            self.attack_durability = 300
            self.attack_sound.play()
            self.attack()
        else:
            self.destroy_attack()
            self.isAttacking = False

        # healing
        if keys[pygame.K_e] and self.heal_cooldown <= 0:
            self.heal_sound.play()
            self.isHealing = True

        if self.attack_durability <= 0:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1

            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1

            else:
                self.direction.x = 0

        # changing weapon
        if keys[pygame.K_q] and self.weapon_change_cooldown <= 0:
            self.weapon_index += 1
            # if out of weapon index
            if self.weapon_index > 2:
                self.weapon_index = 1
                
            print('WEAPON CHANGE CURRENT WEAPON: ', self.weapon_index)
            self.weapon_change_cooldown = 300
        
        # upgrade
        if self.upgrade_cooldown <= 0:
            if keys[pygame.K_1]:
                self.upgrade('health')
            
            if keys[pygame.K_2]:
                self.upgrade('attack')
            
            if keys[pygame.K_3]:
                self.upgrade('heal_power')

    def attack(self):
        if self.up:
            self.image = self.attack_up

        elif self.down:
            self.image = self.attack_down

        elif self.left:
            self.image = self.attack_left

        elif self.right:
            self.image = self.attack_right

        self.isAttacking = True

    def isDead(self):
        if self.hp <= 0:
            self.kill()
            pygame.quit()

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
    
    def get_lvl(self):
        if self.xp >= 100:
            self.level += 1
            # reset
            self.xp = self.xp - 100
            self.heal_cooldown = 0
            self.hp += 10

            if self.hp > 100:
                self.hp = 100

            self.up_sound.play()

    def move(self):
        if not self.isAttacking:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.rect.x += self.direction.x * self.speed
            self.isColliding('x')
            self.rect.y += self.direction.y * self.speed
            self.isColliding('y')
        else:
            pass
    
    def upgrade(self, what):
        if what == 'health':
            if self.points >= HEALTH_UPGRADE_COST:
                self.up_sound.play()

                self.max_hp += HEALTH_UPGRADE
                self.hp += HEALTH_UPGRADE
                self.points -= HEALTH_UPGRADE_COST
        
        if what == 'attack':
            if self.points >= ATTACK_UPGRADE_COST:
                self.up_sound.play()
                
                self.base_damage += ATTACK_UPGRADE
                self.points -= ATTACK_UPGRADE_COST
        
        if what == 'heal_power':
            if self.points >= HEAL_POWER_UPGRADE_COST:
                self.up_sound.play()
                
                self.heal_power += HEAL_POWER_UPGRADE
                self.points -= HEAL_POWER_UPGRADE_COST
        
        self.upgrade_cooldown = 500

    def animate_moving(self):
        # not moving
        if self.direction.x == 0 and self.direction.y == 0:
            if self.up:
                self.image = self.up_idle
            if self.down:
                self.image = self.down_idle
            if self.left:
                self.image = self.left_idle
            if self.right:
                self.image = self.right_idle
            self.frame_index = 0

        else:
            if self.frame_index >= 4:
                self.frame_index = 0
            # moving up
            if self.direction.y < 0:
                self.image = self.run_frames_up[int(self.frame_index)]
                self.right = False
                self.left = False
                self.up = True
                self.down = False
            # moving down
            if self.direction.y > 0:
                self.image = self.run_frames_down[int(self.frame_index)]
                self.right = False
                self.left = False
                self.up = False
                self.down = True
            # moving left
            if self.direction.x < 0:
                self.image = self.run_frames_left[int(self.frame_index)]
                self.right = False
                self.left = True
                self.up = False
                self.down = False
            # moving right
            if self.direction.x > 0:
                self.image = self.run_frames_right[int(self.frame_index)]
                self.right = True
                self.left = False
                self.up = False
                self.down = False
            
            self.frame_index += self.animation_speed

    def reduce_cooldowns(self):
        if self.attack_durability > 0:
            self.attack()
            self.attack_durability -= 10
        else:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 10
            if self.weapon_change_cooldown > 0:
                self.weapon_change_cooldown -= 10 
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 10
        if self.upgrade_cooldown > 0:
            self.upgrade_cooldown -= 10

    def update(self):
        self.move()
        self.animate_moving()
        self.input()
        self.reduce_cooldowns()
        self.isDead()
        self.get_lvl()
