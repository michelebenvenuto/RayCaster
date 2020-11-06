import pygame
from math import cos, pi, sin, atan2


colors = {
    "1":(255,0,0),
    "2":(0,255,0),
    "3":(0,0,255)
}

wall1 = pygame.image.load('textures/wall1.png')
wall2 = pygame.image.load('textures/wall2.png')
wall3 = pygame.image.load('textures/wall3.png')
end = pygame.image.load('textures/finish line.jpg')

enemies = [
  {
    "x": 100,
    "y": 200,
    "texture": pygame.image.load('textures/sprite4.png')
  },
  {
    "x": 280,
    "y": 190,
    "texture": pygame.image.load('textures/sprite3.png')
  },
  {
    "x": 225,
    "y": 340,
    "texture": pygame.image.load('textures/sprite4.png')
  },
  {
    "x": 220,
    "y": 425,
    "texture": pygame.image.load('textures/sprite3.png')
  },
  {
    "x": 320,
    "y": 420,
    "texture": pygame.image.load('textures/sprite4.png')
  }
]

textures = {
    "1": wall1,
    "2": wall2,
    "3": wall3,
    "4": end,
}

black = (0,0,0)
hp = pygame.image.load('textures/healthbar.png')
hud = pygame.image.load('textures/HUD.png')

aspect_ratio = 128/50
block_aspect_ratio = 128/25
class Raycaster:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.blocksize = 50
        self.map = []
        self.player = {
            "x": self.blocksize + 25,
            "y": self.blocksize +25,
            "a": 0,
            "fov": pi/3
        }
        self.half_fov= self.player["fov"] * 0.5
        self.fov_div_mapsize = self.player["fov"] / 1000
        self.zbuffer = [-float('inf') for z in range(0, 1000)]

    def point(self, x, y, c):
        screen.set_at((x, y), c)

    def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + 25):
            for cy in range(y, y + 25):
                tx = int((cx - x) * block_aspect_ratio) 
                ty = int((cy - y) * block_aspect_ratio)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c) 

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def cast_ray(self, a):
        d = 0.0
        while 1:
            x = self.player["x"] + d * cos(a)
            y = self.player["y"] + d * sin(a)

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)
            if self.map[j][i] != ' ':
                hitx = x - i*50
                hity = y - j*50

                if 1< hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit* aspect_ratio)

                return d, self.map[j][i], tx
            d += 1

    def draw_stake(self, x, h, texture, tx):
        start = int(250 - h*0.5)
        end = int(250 + h*0.5)
        for y in range(start, end):
            ty = int(((y - start)*128)/(end - start))
            c = texture.get_at((tx, ty))
            self.point(x, y, c)
    
    def draw_sprite(self, sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        sprite_size = (500/sprite_d) * 70

        sprite_x = 500 + (sprite_a - self.player["a"]) * 1/self.fov_div_mapsize + 250 - sprite_size/2
        sprite_y = 250 - sprite_size/2

        sprite_x = int(sprite_x)
        sprite_y = int(sprite_y)
        sprite_size = int(sprite_size)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 0 < x < 1000 and self.zbuffer[x-1000] >= sprite_d:
                    tx = int((x-sprite_x) * 128/sprite_size)
                    ty = int((y-sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx,ty))
                    if c!= (152,0,136,255):
                        self.point(x,y,c)
                        self.zbuffer[x-1000] = sprite_d

    def draw_healthbar(self,xi,yi, w = 300, h = 100):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 500/w)
                ty = int((y - yi) * 280/h)
                c = hp.get_at((tx, ty))
                if c != (246,246,246):
                    self.point(x,y,c)

    def draw_HUD(self,xi,yi, w = 1000, h = 100):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 320/w)
                ty = int((y - yi) * 40/h)
                c = hud.get_at((tx, ty))
                self.point(x,y,c)

    def render(self):
        
        for i in range(0,1000):
            a = self.player["a"] - self.half_fov + i * self.fov_div_mapsize
            d, c, tx = self.cast_ray(a)

            x = i
            h = 500/(d* cos(a- self.player["a"])) * 75
            self.draw_stake(x, h, textures[c], tx)
            self.zbuffer[i] = d

        for x in range(0, 250,25):
            for y in range(0, 250,25):
                i = int(x/25)
                j = int(y/25)
                if self.map[j][i] != ' ' :
                    self.draw_rectangle(x, y, textures[self.map[j][i]])
        
        for enemy in enemies:
            self.draw_sprite(enemy)
        
        self.draw_healthbar(800, 0)
        self.draw_HUD(0,400)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def main_menu():
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
        screen.fill((255,255,255))
        largeText = pygame.font.Font('freesansbold.ttf', 100)
        TextSurf, TextRect = text_objects("Press enter to start", largeText)
        TextRect.center = (500,250)
        screen.blit(TextSurf,TextRect)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)
def win_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        screen.fill((255,255,255))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Thx for playing the game", largeText)
        TextRect.center = (500,250)
        screen.blit(TextSurf,TextRect)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

pygame.init()
screen = pygame.display.set_mode((1000, 500))
r = Raycaster(1000, 500)
r.load_map('Proyecto/level.txt')

clock = pygame.time.Clock()
main_menu()
# render loop
while 1:
    d = 10
    screen.fill((0, 0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                r.player["a"] -= pi/20
            if e.key == pygame.K_RIGHT:
                r.player["a"] += pi/20

            if e.key == pygame.K_UP:
                r.player["x"] += int(d * cos(r.player["a"]))
                r.player["y"] += int(d * sin(r.player["a"]))
            if e.key == pygame.K_DOWN:
                r.player["x"] -= int(d * cos(r.player["a"]))
                r.player["y"] -= int(d * sin(r.player["a"]))
    
    if(400<r.player["x"]<450 and 400<r.player["y"]<450):
        break
    r.render()
    pygame.display.flip()
win_screen()