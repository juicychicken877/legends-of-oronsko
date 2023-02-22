from settings import *
from support import import_csv_layout, import_graphics, import_folder
from tile import StaticTile, StaticBigTile
from player import Player
from weapons import Weapon
from enemy import *
from effects import Claw, DeadBamboo, DeadSquid, BambooAttack, SquidAttack, Leaf, Heal
from userinterface import UI

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface

        self.enemy_spawners = []
        self.spawn_cooldowns = []

        self.player_weapon = None

        # main sprite group containing all of the sprites
        self.visible_sprites = Camera()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.grass_sprites = pygame.sprite.Group()

        # player
        self.player = Player(1024, 1280, self.obstacle_sprites, self.destroy_weapon)
        self.player_hurt_sound = pygame.mixer.Sound('sounds/Hit2.wav')
        self.player_hurt_sound.set_volume(0.5)

        # importing graphics and images
        self.floor_tile_list = import_graphics('graphics/background/Floor.png')
        self.grass_image_list = import_folder('graphics/grass')
        self.objects_image_list = import_folder('graphics/objects')

        # importing csv , placing tiles on proper position & adding to sprite groups
        self.create_map_elements(import_csv_layout(level_data['floor']), 'floor')
        self.create_map_elements(import_csv_layout(level_data['grass_details']), 'grass_details')
        self.create_map_elements(import_csv_layout(level_data['objects']), 'objects')
        self.create_map_elements(import_csv_layout(level_data['enemies']), 'enemies')
        self.create_map_elements(import_csv_layout(level_data['barrier']), 'barrier')

        # sounds
        self.enemy_sprite_death = pygame.mixer.Sound('sounds/death.wav')
        self.enemy_sprite_death.set_volume(0.5)

        self.visible_sprites.add(self.player)

        self.user_interface = UI(self.player.attack_cooldown, self.player.heal_cooldown)

    def create_map_elements(self, layout, type):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type=='floor':
                        tile_surface = self.floor_tile_list[int(value)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)

                        self.visible_sprites.add(sprite)
                    
                    if type=='grass_details':
                        tile_surface = self.grass_image_list[int(value)]
                        sprite = StaticTile(TILE_SIZE,x, y, tile_surface)

                        self.visible_sprites.add(sprite)
                        self.grass_sprites.add(sprite)

                    if type=='objects':
                        object_surface = pygame.image.load('graphics/objects/' + value + '.png').convert_alpha()
                        surface_size = object_surface.get_size()
                        sprite = StaticBigTile(surface_size[0], surface_size[1], x, y, object_surface)

                        self.visible_sprites.add(sprite)
                        self.obstacle_sprites.add(sprite)
                    
                    if type=='barrier':
                        barrier_surface = self.floor_tile_list[int(value)]
                        sprite = StaticTile(TILE_SIZE, x, y, barrier_surface)

                        self.obstacle_sprites.add(sprite)

                    if type=='enemies':
                        if value == '390':
                            self.enemy_spawners.append([x, y, 'bamboo'])
                        elif value == '393':
                            self.enemy_spawners.append([x, y, 'squid'])
                        self.spawn_cooldowns.append(0)

    def create_weapon(self):
        if self.player.isAttacking:
            self.player_weapon = Weapon(self.player, self.player.weapon_index)
            
            self.visible_sprites.add(self.player_weapon)

            # check if any enemy got hit
            for sprite in self.enemy_sprites:
                sprite.isHit(self.player_weapon)
            
            # check if player hit grass
            self.destroy_grass()

    def destroy_grass(self):
        sprite_collide = pygame.sprite.spritecollide(self.player_weapon, self.grass_sprites, True)
        if sprite_collide:
            for sprite in sprite_collide:
                x = sprite.rect.centerx
                y = sprite.rect.centery
                sprites = [Leaf(x, y, '1'), Leaf(x, y, '2'), Leaf(x, y, '3'), Leaf(x, y, '4'), Leaf(x, y, '5'), Leaf(x, y, '6')]
                self.visible_sprites.add(sprites)
    
    def player_heal(self):
        if self.player.isHealing:
            self.player.hp += self.player.heal_power

            if self.player.hp > self.player.max_hp:
                self.player.hp = self.player.max_hp

            sprite = Heal(self.player.rect.x, self.player.rect.y)
            self.visible_sprites.add(sprite)
            self.player.isHealing = False
            self.player.heal_cooldown = 8000

    def reduce_cooldowns(self):
        # reduce spawn cooldowns
        # when cooldown = -1 that means enemy on spawner is alive
        # when cooldown = 0 enemy is ready to be spawn
        for i in range(len(self.spawn_cooldowns)):
            if self.spawn_cooldowns[i] > 0:
                self.spawn_cooldowns[i] -= 10
            elif self.spawn_cooldowns[i] == 0:
                self.spawn_enemy(i)
                self.spawn_cooldowns[i] = -1
            else:
                pass

    def spawn_enemy(self, index):
        sprite = Enemy(self.enemy_spawners[index][0], self.enemy_spawners[index][1], self.player, index, self.enemy_spawners[index][2], self.obstacle_sprites)
        print('ENEMY', index, 'SPAWN')

        self.enemy_sprites.add(sprite)  
        self.visible_sprites.add(sprite)

    def isEnemyKilled(self):
        # if enemy dead set spawn cooldown 
        for sprite in self.enemy_sprites:
            if sprite.HP <= 0:
                if sprite.type == 'bamboo':
                    effect = DeadBamboo(sprite.rect.x, sprite.rect.y)
                    self.visible_sprites.add(effect)

                elif sprite.type == 'squid':
                    effect = DeadSquid(sprite.rect.x, sprite.rect.y)
                    self.visible_sprites.add(effect)

                # increase player's xp and points
                self.player.points += 10
                self.player.xp += 10

                sprite.kill()
                print('ENEMY', sprite.index, 'DEAD')
                self.spawn_cooldowns[sprite.index] = 30000
                self.enemy_sprite_death.play()

    def attacked_player_effect(self):
        if self.player.gotHit:
            if self.player.who_attacked == 'bamboo':
                sprite = BambooAttack(self.player.rect.x, self.player.rect.y)
            elif self.player.who_attacked == 'squid':
                sprite = SquidAttack(self.player.rect.x, self.player.rect.y)

            self.visible_sprites.add(sprite)
            self.player_hurt_sound.play()
            self.player.gotHit = False

    def destroy_weapon(self):
        if self.player_weapon:
            self.player_weapon.kill()

        self.player_weapon = None

    def run(self):
        self.reduce_cooldowns()
        self.isEnemyKilled()
        self.create_weapon()
        self.attacked_player_effect()
        self.player_heal()
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.user_interface.draw(self.player)

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)
        