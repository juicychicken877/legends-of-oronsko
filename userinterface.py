from settings import *

class UI:
    def __init__(self, player_attack_cooldown, player_heal_cooldown):
        self.player_attack_cooldown = player_attack_cooldown

        self.player_heal_cooldown = player_heal_cooldown

        self.weapons = {
            1: 'graphics/weapons/axe/full.png',
            2: 'graphics/weapons/sword/full.png'
        }
        self.enemies = {
            'bamboo': 'graphics/enemies/bamboo/0.png',
            'squid': 'graphics/enemies/squid/0.png'
        }

        self.hp_bg = pygame.Rect(10, 600, 208, 24)

        self.heal_image = pygame.image.load('graphics/effects/heal/heal.png').convert_alpha()
        self.player_image = pygame.image.load('graphics/player/player.png').convert_alpha()

    def stats(self, player):
        pygame.draw.rect(screen, 'Black', pygame.Rect(1140, 10, 130, 110))

        text = font3.render('INFO', True, 'White')
        screen.blit(text, (1175, 5))
        text = font3.render(f'HP   {player.max_hp}', True, 'Red')
        screen.blit(text, (1145, 30))
        text = font3.render(f'ATT   {player.base_damage}', True, 'Orange')
        screen.blit(text, (1145, 50))
        text = font3.render(f'HEAL   {player.heal_power}', True, 'Green')
        screen.blit(text, (1145, 70))
        text = font3.render(f'LVL   {player.level}', True, 'Aqua')
        screen.blit(text, (1145, 90))

    def upgrades(self, player):
        font_color_hp = 'White'
        font_color_att = 'White'
        font_color_heal = 'White'

        if player.points < HEALTH_UPGRADE_COST:
            font_color_hp = 'Red'
        if player.points < ATTACK_UPGRADE_COST:
            font_color_att = 'Red'
        if player.points < HEAL_POWER_UPGRADE_COST:
            font_color_heal = 'Red'

        upgrade = font2.render(f'HP + {HEALTH_UPGRADE}', False, 'Red')
        cost = font2.render(f'-{HEALTH_UPGRADE_COST}', False, 'White')
        # bg rects
        pygame.draw.rect(screen, 'Black', pygame.Rect(1020, 600, 200, 30))
        screen.blit(upgrade, (1025, 597))
        screen.blit(cost, (1155,597))

        cost = font2.render(f'-{ATTACK_UPGRADE_COST}', False, 'White')
        upgrade = font2.render(f'ATT + {ATTACK_UPGRADE}', False, 'Orange')
        pygame.draw.rect(screen, 'Black', pygame.Rect(1020, 640, 200, 30))
        screen.blit(upgrade, (1025, 637))
        screen.blit(cost, (1155,637))

        cost = font2.render(f'-{HEAL_POWER_UPGRADE_COST}', False, 'White')
        upgrade = font2.render(f'HEAL + {HEAL_POWER_UPGRADE}', False, 'Green')
        pygame.draw.rect(screen, 'Black', pygame.Rect(1020, 680, 200, 30))
        screen.blit(upgrade, (1025, 677))
        screen.blit(cost, (1155,677))

        # key buttons rects
        number = font2.render('1', False, font_color_hp)
        pygame.draw.rect(screen, 'Black', pygame.Rect(1240, 600, 30, 30))
        screen.blit(number, (1249, 597))

        number = font2.render('2', False, font_color_att)
        pygame.draw.rect(screen,'Black', pygame.Rect(1240, 640, 30, 30))
        screen.blit(number, (1249, 637))

        number = font2.render('3', False, font_color_heal)
        pygame.draw.rect(screen, 'Black', pygame.Rect(1240, 680, 30, 30))
        screen.blit(number, (1249, 677))

    def HP(self, player):
        pygame.draw.rect(screen, 'Black', self.hp_bg)

        ratio = player.hp / player.max_hp
        current_width = self.hp_bg.width * ratio
        current_rect = pygame.Rect(14, 604, current_width-8, 16)

        pygame.draw.rect(screen, 'Red', current_rect)

    def attack_cooldown(self, player_attack_cooldown):
        pygame.draw.rect(screen, 'Black', pygame.Rect(10, 630, 208, 24))
        pygame.draw.rect(screen, 'Orange', pygame.Rect(14, 634, (self.player_attack_cooldown - player_attack_cooldown)//2, 16))

    def current_weapon(self, player_weapon_index):
        weapon = self.weapons[player_weapon_index]
        player_weapon = pygame.image.load(weapon)
        player_weapon_rect = player_weapon.get_rect(topleft=(10, 530))
        screen.blit(player_weapon, player_weapon_rect)

    def heal(self, player_heal_cooldown):
        pygame.draw.rect(screen, 'Black', pygame.Rect(10, 660, 208, 24))
        pygame.draw.rect(screen, 'Green', pygame.Rect(14, 664, (self.player_heal_cooldown - player_heal_cooldown) // 40, 16))

    def player_topbar(self, player_xp, player_score, player_level):
        level_text = font3.render(f'{player_level}', False, 'White')
        level_text_rect = level_text.get_rect(center=(45, 66))
        
        points_text = font2.render(f'{player_score}', False, 'White')
        points_text_rect = points_text.get_rect(center=(136, 25))

        pygame.draw.rect(screen, 'Black', pygame.Rect(10, 10, 64, 70))

        # black bars
        #top
        pygame.draw.rect(screen, 'Black', pygame.Rect(80, 10, 108, 35))
        #bottom
        pygame.draw.rect(screen, 'Black', pygame.Rect(80, 50, 108, 30))

        #xp
        pygame.draw.rect(screen, 'Green', pygame.Rect(84, 54, player_xp, 22))

        # players image
        screen.blit(self.player_image, (10, 10))
        # points bar
        screen.blit(points_text, points_text_rect)
        # level bar below players image
        pygame.draw.rect(screen, 'Black', pygame.Rect(10, 60, 64, 20))
        screen.blit(level_text, level_text_rect)

    def draw(self, player):
        self.HP(player)
        self.attack_cooldown(player.attack_cooldown)
        self.current_weapon(player.weapon_index)
        self.heal(player.heal_cooldown)
        self.player_topbar(player.xp, player.points, player.level)
        self.stats(player)
        self.upgrades(player)