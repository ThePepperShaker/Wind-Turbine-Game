import pygame as pg 
from settings import * 
from os import path
import time 

# Image directory 
img_dir = path.join(path.dirname(__file__), 'img')
vec = pg.math.Vector2 

class Turbines(pg.sprite.Sprite): 
    def __init__(self, game, x, y): 
        self.groups = game.turbines, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = []
        self.images.append(pg.image.load(path.join(img_dir, 'turbines1.png')))
        self.images.append(pg.image.load(path.join(img_dir, 'turbines2.png')))
        self.images.append(pg.image.load(path.join(img_dir, 'turbines3.png')))
        self.images.append(pg.image.load(path.join(img_dir, 'turbines4.png')))
        self.index = 0
        self.image = pg.transform.scale(self.images[self.index], (50, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.pos = vec(x,y)
        self.click = False
        self.holding = False
        self.in_slot = False
        self.spinning = False

    def update(self): 
        '''
        Update turbine sprites
        '''
        self.mouse_pos = self.get_mouse_position() 
        if self.click:
            self.rect.center = self.mouse_pos
        if self.in_slot: 
            self.animate()
            self.spinning = True
  
    def get_mouse_position(self):
        '''
        Get the current position of the mouse 
        returns the x and y position of the mouse 
        '''
        mouse_pos = pg.Vector2(pg.mouse.get_pos()) 
        return mouse_pos
    
    def animate(self): 
        '''
        Animate the turbines using 4 images
        '''
        self.index += 1
        if self.index >= len(self.images): 
            self.index = 0 
        self.image = pg.transform.scale(self.images[self.index], (50, 100))
        
    def check_collision(self, mouse):
        '''
        Check if mouse collides with turbine 
        '''
        hit = self.rect.collidepoint(mouse) 
        if hit:  
            return True
        False


class TurbineSlot(pg.sprite.Sprite): 
    def __init__(self, game, x, y): 
        self.groups = game.slots, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((75, 50))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

class Regions(pg.sprite.Sprite): 
    def __init__(self, game, x, y): 
        self.groups = game.regions, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((300, 350))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        self.num_turbines = 0


class EarthEmotion(pg.sprite.Sprite): 
    def __init__(self, game, x, y): 
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = []
        self.images.append(pg.image.load(path.join(img_dir, 'emotion_earth2.png')))
        self.images.append(pg.image.load(path.join(img_dir, 'emotion_earth1.png')))
        self.index = 0
        self.image =self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y
        self.num_turbines = 0
        self.animating = False

    def animate(self): 
        '''
        Animate earth
        '''
        if self.animating: 
            self.index = 1
        self.image = self.images[self.index]
    
    def update(self): 
        self.animate()
