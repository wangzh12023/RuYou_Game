# -*- coding:utf-8 -*-

import pygame

from Settings import *
from random import random, randint

class Block(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0, width=SceneSettings.tileWidth, height=SceneSettings.tileHeight):
        super().__init__()
        ##### Your Code Here ↓ #####
        self.image=image
        self.image=pygame.transform.scale(self.image,(width,height))

        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        self.rect=self.rect.move(dx,dy)
        window.blit(self.image,self.rect)
        ##### Your Code Here ↑ #####

def gen_wild_map():
    ##### Your Code Here ↓ #####
    images=[pygame.image.load(tile) for tile in GamePath.groundTiles]
    images=[pygame.transform.scale(image,(SceneSettings.tileWidth,SceneSettings.tileHeight)) for image in images]
    mapObj=[]
    for i in range(SceneSettings.tileXnum):
        tmp=[]
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0,len(images)-1)])
        mapObj.append(tmp)
    return mapObj
    ##### Your Code Here ↑ #####

def gen_city_map():
    ##### Your Code Here ↓ #####
    images=[pygame.image.load(tile) for tile in GamePath.cityTiles]
    images=[pygame.transform.scale(image,(SceneSettings.tileWidth,SceneSettings.tileHeight)) for image in images]
    mapObj=[]
    for i in range(SceneSettings.tileXnum):
        tmp=[]
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0,len(images)-1)])
        mapObj.append(tmp)
    return mapObj
    ##### Your Code Here ↑ #####

def gen_boss_map():
    ##### Your Code Here ↓ #####
    images=[pygame.image.load(tile) for tile in GamePath.bossTiles]
    images=[pygame.transform.scale(image,(SceneSettings.tileWidth,SceneSettings.tileHeight)) for image in images]
    mapObj=[]
    for i in range(SceneSettings.tileXnum):
        tmp=[]
        for j in range(SceneSettings.tileYnum):
            tmp.append(images[randint(0,len(images)-1)])
        mapObj.append(tmp)
    return mapObj
    ##### Your Code Here ↑ #####

def gen_city_obstacle():
    ##### Your Code Here ↓ #####
    image = pygame.image.load(GamePath.cityWall)
    obstacles = pygame.sprite.Group()

    midX = SceneSettings.tileXnum // 2
    midY = SceneSettings.tileYnum // 2

    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            if random() < SceneSettings.obstacleDensity and \
                ((i not in range(midX - 3, midX + 4))\
                or (j not in range(midY - 3, midY + 4)))\
                and (i > midX or j > midY):
                obstacles.add(Block(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles
    ##### Your Code Here ↑ #####

def gen_wild_obstacle():
    ##### Your Code Here ↓ #####
    image = pygame.image.load(GamePath.tree)
    obstacles = pygame.sprite.Group()

    midX = SceneSettings.tileXnum // 2
    midY = SceneSettings.tileYnum // 2

    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            if random() < SceneSettings.obstacleDensity and \
                ((i not in range(midX - 3, midX + 4))\
                or (j not in range(midY - 3, midY + 4)))\
                and (i > midX or j > midY):
                obstacles.add(Block(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
                
    return obstacles
    ##### Your Code Here ↑ #####

def gen_boss_obstacle():
    ##### Your Code Here ↓ #####
    image = pygame.image.load(GamePath.bossWall)
    obstacles = pygame.sprite.Group()

    midX = SceneSettings.tileXnum // 2
    midY = SceneSettings.tileYnum // 2

    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            if random() < SceneSettings.obstacleDensity and \
                ((i not in range(midX - 3, midX + 4))\
                or (j not in range(midY - 3, midY + 4)))\
                and (i > midX or j > midY):
                obstacles.add(Block(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    return obstacles
    ##### Your Code Here ↑ #####
