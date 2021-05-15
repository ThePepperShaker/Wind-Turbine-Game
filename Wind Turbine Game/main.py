# Wind Turbine Allocation Game 

# import libraries 
import pygame as pg 
import random 
from settings import * 
from sprites import * 
from windspeed import *
import time 
from os import path



###### Game Idea ######## 
# Regions 
# - Implement 2-4 regions / on-shore and off-shore locations
# - Implement slots where wind turbines can be placed 
# - Implement functionality as soon as wind turbine is placed, turbine interacts with
#   wind in that region to generate power 
# - Use simple collision and drag and drop system 


# Turbines 
# - Implement wind turbines in inventory 
# - Begin with 5 turbines 
# - Turbines have HP 
# - More energy production leads to faster degradation of turbine 
# - Have to implement placement of wind turbines 

# Wind 
# - Implement function that generates a random wind speed for each region 
# - Update 5 seconds 
# - Wind speed determines power/energy generation of wind turbines 
# - 

# Energy 
# - Calculate energy generated each second
# - Energy generation determined by number of turbines in region and wind speed 
# - 


# Earth Satisfaction 
# - Dependent on energy levels 
# - Earth happy if energy generation rate > threshhold level 
# - Timer resets everytime earth emotion changes 
# - What should the threshold level be? 


# Game Over condition 
# - Earth happy for 2 minutes = Game Over (Win) 
# - Earth sad for 1 minute = Game Over (Lose)

# Animations 
# - Flowing wind turbines 
# - Animated clouds 
# - Animated ocean 

# Game class 
class Game: 
    def __init__(self):
        # initialize everything 
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Wind Turbine Game')
        self.clock = pg.time.Clock()
        self.running = True 
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname('__file__')
        self.img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')
        # Sounds 
        pg.mixer.music.load(path.join(self.snd_dir, 'wind.wav'))
    
    def new(self): 
        # New game
        # Power generated 
        self.power = 0 
        self.win = False
        # Sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.turbines = pg.sprite.Group()
        self.slots = pg.sprite.Group()
        self.regions = pg.sprite.Group()
        self.earth = EarthEmotion(self, 450,450)
        # Wind speed initial values
        self.offshore_region_1_windspeed = 0 
        self.offshore_region_2_windspeed = 0 
        self.onshore_region_1_windspeed = 0 
        self.onshore_region_2_windspeed = 0 
        # Keep track of time
        self.wind_timer = 0 
        self.power_timer = 0
        self.img_timer = 0
        self.start_time = pg.time.get_ticks()
        self.count_seconds = 0
        # Background images
        self.offshore_region_imgs = []
        self.offshore_region_imgs.append(pg.image.load(path.join(self.img_dir, 'offshore1.png')). convert())
        self.offshore_region_imgs.append(pg.image.load(path.join(self.img_dir, 'offshore2.png')). convert())
        self.offshore_region_imgs.append(pg.image.load(path.join(self.img_dir, 'offshore3.png')). convert())
        self.offshore_region_imgs.append(pg.image.load(path.join(self.img_dir, 'offshore4.png')). convert())
        self.index = 0 
        self.offshore_region = self.offshore_region_imgs[self.index]
        self.onshore_region = pg.image.load(path.join(self.img_dir, 'onshore.png')).convert()
        # Spawn some turbines
        x = 25
        for i in range(6): 
            Turbines(self, x, 800)
            x += 100
        self.turbine_origin = []
        for turbine in self.turbines: 
            self.turbine_origin.append([turbine.rect.x, turbine.rect.y])
        # Create the grid under the map
        self.grid = self.create_grid()
        # Spawn turbine slots, where the grid is equal to turbine
        for x in range(36): 
            for y in range(36): 
                if self.grid[x][y] == 'turbine': 
                    TurbineSlot(self,(x*25),(y*25))
                if self.grid[x][y] == 'region1' or "region2" or "region3" or "region4" : 
                    Regions(self, (x*25), (y*25))
        
        # Draw Earth 
        self.run()
    
    def run(self): 
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500) 

    def get_mouse_position(self):
        '''
        Returns mouse position 
        '''
        mouse_pos = pg.Vector2(pg.mouse.get_pos()) 
        return mouse_pos

    def update(self): 
        # Update game loop 
        # Set timer
        count_time = pg.time.get_ticks() - self.start_time

        # Count the time 
        self.count_minutes = int(count_time / 60000) % 60 
        if self.count_seconds < 61: 
            self.count_seconds = int(count_time / 1000) % 60
        self.all_sprites.update()
        # Get current mouse position
        self.mouse_pos = self.get_mouse_position()

        # Store the information under mouse 
        self.piece, self.x, self.y = self.get_square_under_mouse(self.grid)

        # Check if turbine is colliding with slot 
        for turbine in self.turbines: 
            if pg.sprite.spritecollide(turbine, self.slots, False):
                turbine.in_slot = True 
            else: 
                turbine.in_slot = False

        # Update wind speeds  
        now = pg.time.get_ticks()   
        if now - self.wind_timer > 5000: 
            self.wind_timer = now
            # Wind speed for first offshore region
            self.offshore_region_1_windspeed = Wind_speed(WS, 6, 3)
            # Wind speed for second offshore region
            self.offshore_region_2_windspeed = Wind_speed(WS, 6, 3)
            # Wind speed for first onshore region
            self.onshore_region_1_windspeed = Wind_speed(WS, 6, 2)
            # Wind speed for first onshore region
            self.onshore_region_2_windspeed = Wind_speed(WS, 6, 2)
            if self.win: 
                self.playing = False


        # Update power generation
        power_now = pg.time.get_ticks()
        if power_now - self.power_timer > 2000: 
            for turbine in self.turbines:
                if turbine.in_slot: 
                    if self.piece == 'region1': 
                        self.power += Power_output(self.offshore_region_1_windspeed)
                    elif self.piece == 'region2': 
                        self.power += Power_output(self.offshore_region_2_windspeed)
                    elif self.piece == 'region3': 
                        self.power += Power_output(self.onshore_region_1_windspeed)
                    else: 
                        self.power += Power_output(self.onshore_region_2_windspeed)
            self.power_timer = power_now 


        if self.power > 10000: 
            self.earth.animating = True
            self.win = True

        # Game Over Condition 
        print(self.count_minutes)
        if self.count_minutes > 0:
            self.playing = False
        
        

    def events(self): 
        # Events loop
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.playing = False 
                self.running = False
            if event.type == pg.MOUSEBUTTONDOWN: 
                for turbine in self.turbines: 
                    if turbine.check_collision(self.mouse_pos):
                        turbine.click = True
                        break
            if event.type == pg.MOUSEBUTTONUP: 
                for turbine in self.turbines:
                    turbine.click = False
                    
              
    def draw(self): 
        # Draw sprites
        background = pg.image.load(path.join(self.img_dir, 'Background.png')).convert()
        background_rect = background.get_rect()
        offshore_region_rect = self.offshore_region.get_rect()
        onshore_region_rect = self.onshore_region.get_rect()
        # Set appropriate offsets to draw the background images
        offshore_region_rect_offset1 = (offshore_region_rect[0] + 25, offshore_region_rect[1] + 100)
        offshore_region_rect_offset2 = (offshore_region_rect[0] + 575, offshore_region_rect[1] + 100)
        onshore_region_rect_offset1 = (onshore_region_rect[0] + 25, onshore_region_rect[1] + 475)
        onshore_region_rect_offset2 = (onshore_region_rect[0] + 575, onshore_region_rect[1] + 475)
        self.screen.blit(background, background_rect)
        # Draw background for region 1 
        self.screen.blit(self.offshore_region, offshore_region_rect_offset1)
        self.screen.blit(self.offshore_region, offshore_region_rect_offset2)
        self.screen.blit(self.onshore_region, onshore_region_rect_offset1)
        self.screen.blit(self.onshore_region, onshore_region_rect_offset2)
        self.draw_text('Wind Speed: '+ str(self.offshore_region_1_windspeed) + 'm/s', 18, BLACK, WIDTH - 750, HEIGHT - 830)
        self.draw_text('Wind Speed: '+ str(self.offshore_region_2_windspeed) + 'm/s', 18, BLACK, WIDTH - 200, HEIGHT - 830)
        self.draw_text('Wind Speed: '+ str(self.onshore_region_1_windspeed) + 'm/s', 18, BLACK, WIDTH - 750, HEIGHT - 460)
        self.draw_text('Wind Speed: '+ str(self.onshore_region_2_windspeed) + 'm/s', 18, BLACK, WIDTH - 200, HEIGHT - 460)
        self.draw_text('Time: ' + str(self.count_minutes) + ' : '+ str(self.count_seconds), 18, BLACK, WIDTH / 2, HEIGHT - 850)
        self.draw_text('Power generated: ' + str(self.power) + ' kW', 18, BLACK, WIDTH / 2, HEIGHT - 250)
        self.all_sprites.draw(self.screen)
        # self.draw_grid()
        # Draw the rectangle around the square the mouse is above
        if self.x != None:
            rect = (BOARD_POS[0] + self.x * TILESIZE, BOARD_POS[1] + self.y * TILESIZE, TILESIZE, TILESIZE)
            pg.draw.rect(self.screen, (255, 0, 0, 50), rect, 2)
        
        for slot in self.slots: 
            if slot.rect.collidepoint(self.mouse_pos): 
                pg.draw.rect(self.screen, (127, 255, 0, 50), rect, 2)
        pg.display.flip()
    
    def create_grid(self): 
        grid = []
        for y in range(36): 
            grid.append([])
            for x in range(36): 
                grid[y].append(None)
        
        # regions 
        grid[1][2] = ('region1')
        grid[23][2] = ('region2')
        grid[1][17] = ('region3')
        grid[23][17] = ('region4')

        # Offshore 1 first slots 
        grid[2][13] = ('turbine')
        
        # Offshore 1 second slots
        grid[9][13] = ('turbine')

        # Offshore 2 first slots 
        grid[24][13] = ('turbine')

        # Offshore 2 second slots
        grid[31][13] = ('turbine')

        # Onshore 1 first slots
        grid[2][28] = ('turbine')

        # Onshore 1 second slots
        grid[6][27] = ('turbine')

        # Onshore 1 third slots
        grid[10][29] = ('turbine')

        # Onshore 2 first slots
        grid[24][28] = ('turbine')

        # Onshore 2 second slots
        grid[28][27] = ('turbine')

        # Onshore 2 third slots
        grid[32][29] = ('turbine')

        return grid

    def get_square_under_mouse(self, grid): 
        '''
        Takes in the 36 x 36 grid of the map and returns the x and y position 
        of the current tile under the mouse. 
        It also returns the string assigned to the tile, if any. 

        '''
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        x, y = [int(v // TILESIZE) for v in mouse_pos]
        try: 
            if x >= 0 and y >= 0: return (grid[y][x], x, y)
        except IndexError: pass
        return None, None, None

    def get_square_under_turbine(self, grid): 
        '''
        Returns the tile under each turbine 
        '''
        turbine_pos_list = []
        self.turbine_tile_list = []
        for turbine in self.turbines: 
            turbine_pos = turbine.pos
            turbine_pos_list.append(turbine_pos)
            x, y = [int(pos // TILESIZE) for pos in turbine_pos]
            self.turbine_tile_list.append([x,y])
        

    def draw_grid(self): 
        '''
        Draws the 36 x 36 grid on the map
        '''
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE): 
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))
            
    def show_start_screen(self):
        '''
        Game start screen
        '''
        # Made this using procreate following tutorial by 'Art with Flo'
        background = pg.image.load(path.join(self.img_dir, 'earth.png')).convert()
        background_rect = background.get_rect()
        self.screen.blit(background, background_rect)

        # Print some informatino about how to play
        self.draw_text('Generate 10,000kW of Power in under 1 Minute to Save the Earth!', 28, GREEN, WIDTH / 2, HEIGHT - 850)
        self.draw_text('Place Turbines in slots to generate power. More Wind = More Power!.',  28, GREEN, WIDTH / 2, (HEIGHT - 100))
        self.draw_text('Press any key to play', 28, GREEN, WIDTH / 2, HEIGHT - 150)
        pg.display.flip()
        self.wait_for_key()
    
    def show_end_screen(self): 
        '''
        Game over screen
        '''
        if not self.running: 
            return 
        if self.win: 
            self.screen.fill(BLACK)
            self.draw_text('Game Over. You Saved Earth!', 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text('Press any key to play again', 22, WHITE, WIDTH / 2, (HEIGHT + 50) / 2)
        else: 
            self.screen.fill(BLACK)
            self.draw_text('Game Over. Earth is Doomed!', 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text('Press any key to play again', 22, WHITE, WIDTH / 2, (HEIGHT +50) / 2)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        '''
        If called set a variable waiting equal to False
        '''
        pg.event.wait()
        waiting = True 
        while waiting: 
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False 
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
    
    def draw_text(self, text, size, color, x, y):
        '''
        ...
        '''
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
g = Game()
g.show_start_screen()
while g.running: 
    g.new()
    g.show_end_screen()

pg.quit()