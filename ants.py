# ants civ
import pygame as py
import random


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = py.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = py.font.SysFont("Arial", 24)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255)) # White text

    def draw(self, screen):
        mouse_pos = py.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        py.draw.rect(screen, current_color, self.rect)
        
        # Center the text on the button
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def handle_event(self, event):
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

class Ant:
    

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.move_left = True
        self.speed = 7
        self.holding_object = False
        self.freeze_time = 0
        scale = 1


        """self.b = 1
        self.n = 2
        self.m = 3
        self.bg = random.randint(20, 100)
        self.ng = random.randint(20, 150)
        self.mg = random.randint(20, 200)


        personality_dict = {self.b : self.bg, self.n : self.ng, self.m : self.mg} # higher values is the amount of frames they will idle for
        o = random.randint(0, 2)
        if o == 0:
            num = self.b
        if o == 1:
            num = self.n
        if 0 == 2:
            num = self.m
        else:
            num = self.m
        self.personality = personality_dict[num]
        self.idle = 0"""
        
        ant_imgL = py.image.load('ant_imgright.png').convert_alpha()
        ant_imgL = py.transform.scale(ant_imgL, (ant_imgL.get_width()*scale,ant_imgL.get_height()*scale))
        ant_imgR = py.image.load('ant_imgleft.png').convert_alpha()
        ant_imgR = py.transform.scale(ant_imgR, (ant_imgR.get_width()*scale,ant_imgR.get_height()*scale))

        self.img_left = ant_imgL
        self.img_right = ant_imgR

    def draw_ant(self, screen):
        if self.move_left:
            screen.blit(self.img_left, (self.x, self.y))
            return self.img_left.get_rect(topleft=(self.x, self.y))
        else:
            screen.blit(self.img_right, (self.x, self.y))
            return self.img_right.get_rect(topleft=(self.x, self.y))
    def move_towards(self, tx, ty):
            
        if self.freeze_time > 0:
            self.freeze_time -= 1
            return
        else:
            i_list = []
            for i in range(self.speed):
               i_list.append(tx-i)
               i_list.append(tx+i)
               i_list.append(ty-i)
               i_list.append(ty+i)
            if self.x not in i_list:
                if self.x  < tx:
                    self.x += self.speed
                    self.move_left = True
                if self.x > tx:
                    self.x -= self.speed
                    self.move_left = False
              
            elif self.y not in i_list:    
                if self.y < ty:
                    self.y += self.speed
                if self.y > ty:
                    self.y -= self.speed


class Nest:
    def __init__(self, x, y, img1):
        self.font = py.font.SysFont('javanesetext', 30)
        self.x = x
        self.y = y
        self.img1 = img1
        self.contents = []
        self.anim_list = []
        self.nest_anim = False
        self.n_nest_anim = 0
        self.spawnant = 0
        self.ants = []
        ant1 = Ant(self.x, self.y)
        self.ants.append(ant1)


        self.sound_effect = py.mixer.Sound("sounds/nest_steam.mp3")

        for i in range(15):
            self.anim_list.append(py.image.load(f'sprites/nest/nest_img ({i}).png').convert_alpha())
            self.anim_list[i] = py.transform.scale(self.anim_list[i], (self.anim_list[i].get_width()*3, self.anim_list[i].get_height()*3))

    def draw_nest(self, screen):
        # our main nest func
        # It even spawns the ants!!!

        
        screen.blit(self.img1, (self.x, self.y))
        self.draw_contents(screen)
        if self.spawnant > 9:
            self.spawnant = 0
            self.ants.append(Ant(x=self.x, y=self.y))
        return self.img1.get_rect(topleft=(self.x, self.y))
    
    def draw_contents(self, screen):
        
        text_im = f"Contents: {len(self.contents)}"
        text = self.font.render(text_im, True, (0, 0, 0))
        screen.blit(text, (self.x-5,self.y+90))
    
    def get_nest_cord(self):
        return (self.x, self.y)
    
    def animation(self, screen, i):
        if i >= 0 and i < 14:
            screen.blit(self.anim_list[i], (self.x, self.y))
            self.draw_contents(screen)
        if i >= 14:
            screen.blit(self.anim_list[i-1], (self.x, self.y))
            self.draw_contents(screen)
            self.contents.pop(0)
            
            # STEAM SOUND EFFECT #
            sound_effect = py.mixer.Sound('sounds/nest_steam.mp3')
            sound_effect.set_volume(0.025)
            sound_effect.play()
            
            self.spawnant += 1
class Food:
    
    def __init__(self, x, y, foods_constructed = 0):
        foods_constructed += 1
        self.x = x
        self.y = y
        self.pixels_taken = 0
        self.sprite_list = []
        for i in range(15):
            self.sprite_list.append(py.image.load(f'sprites/food/food ({i+1}).png'))
            self.sprite_list[i] = py.transform.scale(self.sprite_list[i], (self.sprite_list[i].get_width()*3,self.sprite_list[i].get_height()*3))

    def get_food_cordx(self):
        return self.x
    
    def get_food_cordx(self):
        return self.y

    def draw_food(self, screen):
        # this needs to be fixed (final pixel taken cant be taken)
        screen.blit(self.sprite_list[self.pixels_taken], (self.x, self.y))
        self.food_rect = self.sprite_list[self.pixels_taken].get_rect(topleft=(self.x, self.y))

    def take_pixel(self):
        if self.pixels_taken < 14:
            self.pixels_taken += 1
        else:
            self.pixels_taken = -1
            self.x = random.randint(50,1050)
            self.y = random.randint(50,500)
    




def main():
    py.init()

    py.mixer.pre_init(44100, -16, 2, 512)
    py.mixer.init()

    screen = py.display.set_mode((1300,600))


    sound_effect = py.mixer.Sound("sounds/antsoundwalk2.wav")
    sound_effect = py.mixer.Sound("sounds/antsoundwalk3.wav")
    sound_effect.set_volume(0.1)


    nests = []
    foods = []
    running = True
    player_control = False
    m = 0
    time = 0
    time_mins = 0
    time_hours = 0
    nest_add_contents = False

    playing = True
    



    
    
    
    nest_img1 = py.image.load('sprites/nest/nest_img (1).png').convert_alpha()
    nest_img1 = py.transform.scale(nest_img1, (nest_img1.get_width()*3, nest_img1.get_height()*3))


    xnest = random.randint(1000,1200)
    ynest = random.randint(100, 200)

    font = py.font.SysFont('javanesetext', 30)

    clock = py.time.Clock()

    xfood = random.randint(50,1050)
    yfood = random.randint(50,500)


    

    
    
    nest1 = Nest(xnest, ynest, nest_img1)
    nests.append(nest1)

    food1 = Food(xfood, yfood)
    foods.append(food1)
    
    while playing:
        while running:
            screen.fill((255,255,255))

            for food in foods:
                food.draw_food(screen)

            for nest in nests:
                if nest_add_contents == True:
                    nest.contents.append("bit")
                    nest_add_contents = False

                if len(nest.contents) == 0:
                    nest.nest_anim = False

                if nest.nest_anim == False:
                    if len(nest.contents) > 9:
                        nest.nest_anim = True

                if nest.nest_anim == False:
                    nest_rect = nest.draw_nest(screen)
                else:
                    
                    if nest.n_nest_anim < 15:
                        nest.animation(screen, nest.n_nest_anim) 
                        nest.n_nest_anim += 1
                    else:
                        nest_rect = nest.draw_nest(screen)
                        
                        nest.n_nest_anim = 0
            


                for ant in nest.ants:
                    
                    ant.rect = ant.draw_ant(screen)
                    for food in foods:
                        if ant.holding_object == False:
                            if ant.rect.colliderect(food.food_rect):
                            
                                food.take_pixel()
                                ant.holding_object = True
                                """p = random.randint(0, 3)
                                if p == ant.b or p == ant.n or p == ant.m:
                                    ant.idle += ant.personality"""

                    
                    if ant.rect.colliderect(nest_rect):
                        
                        if ant.holding_object == True:
                            sound_effect = py.mixer.Sound('sounds/deposit_nest.mp3')
                            sound_effect.set_volume(0.1)
                            sound_effect.play()
                            
                            ant.holding_object = False
                            nest_add_contents = True
                            """p = random.randint(0, 30)
                            if p == ant.b or p == ant.n or p == ant.m:
                                ant.idle += ant.personality"""
                    
                    
                    
                    for food in foods:
                        if food.pixels_taken == -1:
                            food.pixels_taken = 0
                            

                            
                            
                        
                            rannum = random.randint(0, 2)
                            if rannum == 1:
                                sound_effect = py.mixer.Sound("sounds/ding3.mp3")
                                sound_effect.set_volume(0.1)
                                sound_effect.play()
                            if rannum == 0:
                                sound_effect = py.mixer.Sound("sounds/ding2.mp3")
                                sound_effect.set_volume(0.1)
                                sound_effect.play()
                            if rannum == 2:
                                sound_effect = py.mixer.Sound("sounds/ding1.mp3")
                                sound_effect.set_volume(0.1)
                                sound_effect.play()
                            
                        

                    
                    
                
                    if player_control == False:
                        if ant.holding_object == False:
                            ant.move_towards(food1.x, food1.y)
                        if ant.holding_object == True:
                            ant.move_towards(xnest, ynest)
                        if m >= 2:
                            rannum = random.randint(0, 1)
                            if rannum == 1:
                                sound_effect = py.mixer.Sound("sounds/antsoundwalk1.wav")
                                sound_effect.set_volume(0.05)
                                sound_effect.play()
                            if rannum == 0:
                                sound_effect = py.mixer.Sound("sounds/antsoundwalk2.wav")
                                sound_effect.set_volume(0.05)
                                sound_effect.play()
                                
                            m = 0
                        
                    m +=1
                for i in range(len(nest.ants)):
                    for j in range(i + 1, len(nest.ants)):
                        antA = nest.ants[i]
                        antB = nest.ants[j]

                        if antA.rect.colliderect(antB.rect):

                            # If one is already frozen, do nothing
                            if antA.freeze_time > 0 or antB.freeze_time > 0:
                                continue  # Skip freezing entirely

                            # If both are free, freeze ONE at random
                            chosen = antB
                            chosen.freeze_time = 4

            keys = py.key.get_pressed()

            if keys[py.K_j]:
                player_control = not player_control
            if player_control == True:
                if keys[py.K_LSHIFT]:
                    move_speed = 20
                else:
                    move_speed = 10

                if keys[py.K_d]:
                    x += move_speed
                if keys[py.K_a]:
                    x -= move_speed
                if keys[py.K_w]:
                    y -= move_speed
                if keys[py.K_s]:
                    y += move_speed

            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                

                
            # do not remove
            delta_time = clock.tick(25) 


            
            if int(time/60) == 1:
                time -= 60
                time_mins +=1
            if int(time_mins/60) == 1:
                time_mins -= 60
                time_hours += 1

            time_str = f"Time Elapsed: {time_hours:02}:{time_mins:02}:{time:02}"

            timetext = font.render(time_str, True, (0, 0, 0))

            screen.blit(timetext, (10, 10))

            ant_str = f"Ants: {len(nest.ants)}"

            anttext = font.render(ant_str, True, (0, 0, 0))

            screen.blit(anttext, (10, 35))

            py.display.flip()

            time += 1

            
        py.quit()
        

    

    

    
main()