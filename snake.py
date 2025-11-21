# Snake
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
    def __init__(self, x, y, img_left, img_right):
        self.x = x
        self.y = y
        self.img_left = img_left
        self.img_right = img_right
        self.move_left = True
        self.speed = 5
        self.holding_object = False
    def draw_ant(self, screen):
        if self.move_left:
            screen.blit(self.img_left, (self.x, self.y))
            return self.img_left.get_rect(topleft=(self.x, self.y))
        else:
            screen.blit(self.img_right, (self.x, self.y))
            return self.img_right.get_rect(topleft=(self.x, self.y))
    def move_towards(self, tx, ty):
        if self.x != tx or self.y != ty:
            if self.x +3 < tx:
                self.x += self.speed
                self.move_left = True
            if self.x +3 > tx:
                self.x -= self.speed
                self.move_left = False

            if self.y +3 < ty:
                self.y += self.speed
            if self.y +3 > ty:
                self.y -= self.speed
class Nest:
    def __init__(self, x, y, img1):
        self.x = x
        self.y = y
        self.img1 = img1
        self.contents = []
        self.anim_list = []
        self.nest_anim = False
        self.n_nest_anim = 0
        for i in range(14):
            self.anim_list.append(py.image.load(f'sprites/nest/nest_img ({i+1}).png').convert_alpha())
            self.anim_list[i] = py.transform.scale(self.anim_list[i], (self.anim_list[i].get_width()*3, self.anim_list[i].get_height()*3))

    def draw_nest(self, screen):
        screen.blit(self.img1, (self.x, self.y))
        return self.img1.get_rect(topleft=(self.x, self.y))
    
    def get_nest_cord(self):
        return (self.x, self.y)
    
    def animation(self, screen, i):
        if i >= 0 and i < 14:
            screen.blit(self.anim_list[i], (self.x, self.y))
        if i >= 14:
            screen.blit(self.anim_list[i-1], (self.x, self.y))
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
    
def mbut(menu):
    menu = not menu

def spawn_ant(ants, score, ant_imgL, ant_imgR):
    if score >= 10:
        score -= 10
        ants.append(
            Ant(
                random.randint(0, 1200),
                random.randint(100, 600),
                ant_imgL,
                ant_imgR
            )
        )



def main():
    py.init()

    py.mixer.pre_init(44100, -16, 2, 512)
    py.mixer.init()

    screen = py.display.set_mode((1300,650))


    sound_effect = py.mixer.Sound("sounds/antsoundwalk2.wav")
    sound_effect = py.mixer.Sound("sounds/antsoundwalk3.wav")
    sound_effect.set_volume(0.1)

    nests = []
    ants = []
    foods = []
    running = True
    player_control = False
    m = 0
    score = 0
    playing = True
    nest_anim = False



    ant_imgL = py.image.load('ant_imgright.png').convert_alpha()
    ant_imgL = py.transform.scale(ant_imgL, (ant_imgL.get_width()*1.5,ant_imgL.get_height()*1.5))
    ant_imgR = py.image.load('ant_imgleft.png').convert_alpha()
    ant_imgR = py.transform.scale(ant_imgR, (ant_imgR.get_width()*1.5,ant_imgR.get_height()*1.5))
    
    pie_img = py.image.load('pie_img.png').convert_alpha()
    pie_img = py.transform.scale(pie_img, (pie_img.get_width()*3,pie_img.get_height()*3))
    
    nest_img1 = py.image.load('sprites/nest/nest_img (1).png').convert_alpha()
    nest_img1 = py.transform.scale(nest_img1, (nest_img1.get_width()*3, nest_img1.get_height()*3))

    xant = random.randint(0,1300)
    yant = random.randint(0,600)

    xnest = random.randint(1000,1200)
    ynest = random.randint(100, 200)

    font = py.font.SysFont('Calibri', 30)

    
    menubutton2 = Button(1200, 50, 150, 25, "Spawn Ant: costs 10 score", (100, 0, 0), (150, 0, 0), spawn_ant(ants, score, ant_imgL, ant_imgR))

    clock = py.time.Clock()

    xfood = random.randint(50,1050)
    yfood = random.randint(50,500)


    

    ant1 = Ant(xant, yant, ant_imgL, ant_imgR)
    ants.append(ant1)
    
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
                if nest_anim == True:
                    nest.nest_anim = True

                if nest.nest_anim == False:
                    nest_rect = nest.draw_nest(screen)
                else:
                    if nest.n_nest_anim < 15:
                        nest.animation(screen, nest.n_nest_anim) 
                        nest.n_nest_anim += 1
                    else:
                        nest_rect = nest.draw_nest(screen)
                        nest.nest_anim = False
                        nest_anim = False
                        nest.n_nest_anim = 0
            menubutton2.draw(screen)


            for ant in ants:
                
                ant_rect = ant.draw_ant(screen)
                for food in foods:
                    if ant.holding_object == False:
                        if ant_rect.colliderect(food.food_rect):
                            food.take_pixel()
                            ant.holding_object = True

                
                if ant_rect.colliderect(nest_rect):
                    if ant.holding_object == True:
                        ant.holding_object = False
                        nest_anim = True
                for food in foods:
                    if food.pixels_taken == -1:
                        food.pixels_taken = 0

                        
                        
                    
                        rannum = random.randint(0, 2)
                        if rannum == 1:
                            sound_effect = py.mixer.Sound("snake\my_env\sounds/ding3.mp3")
                            sound_effect.set_volume(0.1)
                            sound_effect.play()
                        if rannum == 0:
                            sound_effect = py.mixer.Sound("snake\my_env\sounds/ding2.mp3")
                            sound_effect.set_volume(0.1)
                            sound_effect.play()
                        if rannum == 2:
                            sound_effect = py.mixer.Sound("snake\my_env\sounds/ding1.mp3")
                            sound_effect.set_volume(0.1)
                            sound_effect.play()
                        
                    

                
                
            
                if player_control == False:
                    if ant.holding_object == False:
                        ant.move_towards(food1.x, food1.y)
                    if ant.holding_object == True:
                        ant.move_towards(xnest, ynest+70)
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
                if event.type == py.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button    
                        ant2 = Ant(random.randint(0,1300), 
                        random.randint(0,600), 
                        ant_imgL, ant_imgR)
                        ants.append(ant2)

                

            delta_time = clock.tick(25) 

            score_str = f"Score: {score}"

            text = font.render(score_str, True, (0, 0, 0))

            screen.blit(text, (10, 10))

            py.display.flip()

            
        py.quit()
        

    

    

    
main()