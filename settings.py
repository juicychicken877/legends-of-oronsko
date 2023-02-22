import pygame
from random import randint

pygame.init()

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILE_SIZE = 64

HEALTH_UPGRADE_COST = 50
ATTACK_UPGRADE_COST = 50
HEAL_POWER_UPGRADE_COST = 50
HEALTH_UPGRADE = 10
ATTACK_UPGRADE = 5
HEAL_POWER_UPGRADE = 5

font = pygame.font.Font('font/NormalFont.ttf', 40)
font2 = pygame.font.Font('font/NormalFont.ttf', 24)
font3 = pygame.font.Font('font/NormalFont.ttf', 20)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Legends of Orońsko')
clock = pygame.time.Clock()