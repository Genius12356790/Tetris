import time
import pygame
import sys
import os
import random


I = [[1, 0], [0, 0], [-1, 0], [-2, 0], [0, 255, 255]]
L = [[0, 1], [0, 0], [-1, 0], [-2, 0], [0, 0, 255]]
J = [[2, 0], [1, 0], [0, 0], [0, -1], [255, 150, 0]]
O = [[0, 0], [-1, 0], [0, -1], [-1, -1], [255, 255, 50]]
S = [[1, -1], [0, -1], [0, 0], [-1, 0], [0, 255, 0]]
T = [[1, 0], [0, 0], [-1, 0], [0, 1], [255, 0, 255]]
Z = [[1, 0], [0, 0], [0, -1], [-1, -1], [255, 0, 0]]
FRAMETIME = 1/60
FIGURES = [I, L, J, O, S, T, Z]


class nextfc(pygame.sprite.Sprite):
    def __init__(self, num):
        super().__init__(nextfg)
        self.num = num
        self.image = nextfl[num]['image']
        self.pos = nextfl[num]['posc']
        self.rect = self.image.get_rect()        
        self.rect.x = self.pos[0] * 32 + 385
        self.rect.y = -self.pos[1] * 32 + 120
        
    def update(self):
        self.image = nextfl[self.num]['image']
        self.pos = nextfl[self.num]['posc']      
        self.rect.x = self.pos[0] * 32 + 385
        self.rect.y = -self.pos[1] * 32 + 120          
            

class figurec(pygame.sprite.Sprite):
    def __init__(self, num):
        super().__init__(figureg)
        self.num = num
        self.image = figurel[num]['image']
        self.pos = figurel[num]['pos']
        self.posc = figurel[num]['posc']
        self.rect = self.image.get_rect()        
        self.rect.x = (self.pos[0] + self.posc[0]) * 32
        self.rect.y = (19 - self.pos[1] - self.posc[1]) * 32
        
    def update(self, event, **data):
        if event == 'update':
            self.image = figurel[self.num]['image']
            self.pos = figurel[self.num]['pos']
            self.posc = figurel[self.num]['posc']
            self.rect.x = (self.pos[0] + self.posc[0]) * 32
            self.rect.y = (19 - self.pos[1] - self.posc[1]) * 32            
        if event == 'convert':
            tilec([self.pos[b] + self.posc[b] for b in range(2)], self.image)
            

class tilec(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__(tileg)
        self.image = image 
        self.rect = self.image.get_rect()   
        self.y = pos[1]
        self.rect.x = pos[0] * 32
        self.rect.y = (19 - pos[1]) * 32
        
    def update(self, event, **data):
        if event == 'move':
            if data['y'] < self.y:
                self.rect.y += 32
                self.y -= 1
            elif data['y'] == self.y:
                self.kill()
    
def rot90(data):
    for a in range(4):
        data[a]['posc'] = [data[a]['posc'][1], -data[a]['posc'][0]]
        data[a]['image'] = pygame.transform.rotate(data[a]['image'], 270)
    return data

def canrot90(data):
    for a in range(4):
        b = [data[a]['posc'][1], -data[a]['posc'][0]]
        aa = [data[a]['pos'][c] + b[c] for c in range(2)]
        if min(aa) < 0 or aa[0] > 9 or aa[1] > 19 or field[aa[0]][aa[1]]:
            return 0
    return 1        

def canmove(data, mod):
    for a in range(4):
        aa = [data[a]['pos'][b] + data[a]['posc'][b] + mod[b] for b in range(2)]
        if min(aa) < 0 or aa[0] > 9 or aa[1] > 19 or field[aa[0]][aa[1]]:
            return 0
    return 1

def move(data, mod):
    for a in range(4):
        data[a]['pos'] = [data[a]['pos'][b] + mod[b] for b in range(2)]
    return data

def textout(text, pos, size=30, font='Comic Sans MS', color=(255, 255, 255)):
    myfont = pygame.font.SysFont(font, size)
    textsurface = myfont.render(str(text), False, color)
    screen.blit(textsurface,(pos))
    
def terminate():
    pygame.quit()
    sys.exit()   
    
def generatefigure():
    fig = random.choice(FIGURES)
    data = []
    for a in range(4):
        data.append({'pos': [5, 19], 'posc': fig[a], 'image': drawsprite(fig, a)})
    return data
                     
def drawsprite(data, num):
    pos = data[num]
    image = pygame.Surface((32, 32))
    pygame.draw.rect(image, data[4], (0, 0, 32, 32))
    pygame.draw.line(image, [0.7 * a for a in data[4]], (0, 0), (29, 29), 3)
    pygame.draw.line(image, [0.7 * a for a in data[4]], (29, 0), (0, 29), 3)
    for a in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
        if [a[b] + pos[b] for b in range(2)] not in data:
            #pygame.draw.line(image, [0.5 * a for a in data[4]], (2 * (a[0] != 1) + 28 * (a[0] == 1), 2 * (a[1] != 1) + 28 * (a[1] == 1)), (2 * (a[1] != 0) + 28 * (a[0] != -1), 2 * (a[0] != 0) + 28 * (a[1] != -1)), 2)
            pygame.draw.line(image, [0.25 * a for a in data[4]], (30 * (a[0] == 1), 30 * (a[1] == -1)), (30 * (a[0] != -1), 30 * (a[1] != 1)), 2)
        elif a[0] + a[1] > 0:
            pygame.draw.line(image, [0.8 * a for a in data[4]], (31 * (a[0] == 1), 31 * (a[1] == -1)), (31 * (a[0] != -1), 31 * (a[1] != 1)))
    return image

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
size = width, height = 480, 640
screen = pygame.display.set_mode(size)
figureg = pygame.sprite.Group()
tileg = pygame.sprite.Group()
nextfg = pygame.sprite.Group()
lastframe = time.process_time()
field = [[0] * 21 for a in range(10)]
level = 1
score = 0
lines = 0
linesrow = 0
keys = [0] * 4
tick = 0
hold = 15
released = 1
nextfl = generatefigure()
figurel = generatefigure()
for a in range(4):
    figurec(a)
    nextfc(a)
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                keys[0] = True
            if event.key == pygame.K_LEFT:
                keys[1] = True
            if event.key == pygame.K_SPACE:
                keys[2] = True
            if event.key == pygame.K_RIGHT:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                keys[0] = False
            if event.key == pygame.K_LEFT:
                keys[1] = False
            if event.key == pygame.K_SPACE:
                keys[2] = False
                released = 1
            if event.key == pygame.K_RIGHT:
                keys[3] = False  
    
    if canmove(figurel, [-1, 0]) and keys[1] and hold == 0:
        figurel = move(figurel, [-1, 0])    
        hold = 10
    if canmove(figurel, [1, 0]) and keys[3] and hold == 0:
        figurel = move(figurel, [1, 0])        
        hold = 10
    if canrot90(figurel) and keys[2] and released:
        released = 0
        figurel = rot90(figurel)
    tick += 1
    if tick > 60 / level or (keys[0] and tick > 3):
        if canmove(figurel, [0, -1]):
            if keys[0] and tick > 3:
                score += 1            
            figurel = move(figurel, [0, -1])
        else:
            for a in figurel:
                pos = [a['pos'][b] + a['posc'][b] for b in range(2)]
                field[pos[0]][pos[1]] = 1
            figurel = nextfl
            nextfg.update()
            nextfl = generatefigure()
            figureg.update('convert')
        tick = 0
    linesrow = 0
    for a in range(20):
        if all([field[b][a] for b in range(10)]):
            linesrow += 1
            lines += 1
            level = max(1, lines // 20)
            tileg.update(y=a, event='move')
            for b in range(10):
                field[b] = field[b][:a] + field[b][a + 1:] + [0]
    score += 2 ** linesrow * 100 - 100
    figureg.update(event='update')
    if keys[1] or keys[3]:
        hold -= 1
    else:
        hold = 0
    
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 320, 640))
    pygame.draw.rect(screen, (30, 30, 50), (320, 0, 480, 640))
    pygame.draw.rect(screen, (0, 0, 0), (323, 80, 155, 110))
    textout('Next:', (340, 40))
    nextfg.draw(screen)
    textout('Score:', (340, 200))
    textout(score, (360, 230))
    textout('Lines:', (340, 260))
    textout(lines, (360, 290))
    textout('Level:', (340, 320))
    textout(level, (360, 350))
    figureg.draw(screen)
    tileg.draw(screen)
    pygame.display.flip()  
    
    while time.process_time() < lastframe + FRAMETIME:
        pass
    lastframe += FRAMETIME
    prtime = time.process_time()
    if lastframe + 0.1 < prtime:
        lastframe = prtime                    