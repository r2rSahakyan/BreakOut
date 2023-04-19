import math
import random
import time

import pygame
from pygame import K_RIGHT
from pygame.locals import KEYDOWN, K_LEFT, KEYUP

#GLOBALS
SCREEN_HEIGHT =600
SCREEN_WIDTH =800

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, x, y):
        super().__init__()
        self.image = pygame.Surface((radius*2, radius*2))
        self.image.fill((255,255,255))
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = ( x , y)
        self.speed =[random.randint(2,5),random.randint(2,5)]
    def update(self):
        self.rect.move_ip(self.speed[0],self.speed[1])
        if self.rect.top < 0 :
            self.speed[1] = -self.speed[1]
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed[0] = -self.speed[0]


class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100,15))
        self.image.fill((255,255,255))
        pygame.draw.ellipse(self.image,(0,0,255),(self.image.get_rect().x,self.image.get_rect().x,self.image.get_rect().width,self.image.get_rect().height*2))
        self.rect =self.image.get_rect()
        self.rect.center = (screen.get_rect().width/2,screen.get_rect().height-15)
        self.speed = [0,0]
    def update(self):
        self.rect.move_ip(self.speed[0],0)
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed[0] = -self.speed[0]
class Bricks(pygame.sprite.Sprite):
    def __init__(self,posX,posY):
        super().__init__()
        self.image = pygame.Surface((49 , 20))
        self.image.fill((random.randint(122,255),122,122))
        pygame.draw.rect(self.image,(0,0,0),self.image.get_rect(),2)
        pygame.draw.circle(self.image,(255,255,255),(4,4),2)
        self.rect = self.image.get_rect()
        self.rect.topleft=(posX,posY)

if __name__ == '__main__':
    pygame.init()

    screen= pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    ball = Ball((255, 0, 0), 10,screen.get_rect().centerx,screen.get_rect().centery)
    all_balls =pygame.sprite.Group(ball)
    board =Board()
    all_boards = pygame.sprite.Group(board)
    pygame.display.set_caption("BreakOut")
    clock = pygame.time.Clock()
    running = True
    all_bricks =pygame.sprite.Group()
    for i in range(16):
        for j in range(6):
            brick = Bricks(i*50,j*21)
            all_bricks.add(brick)
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running= False
                break
            if event.type == KEYDOWN :
                if event.key == K_RIGHT:
                    board.speed[0]=5
                if event.key == K_LEFT:
                    board.speed[0] = -5
            if event.type == KEYUP :
                if event.key == K_RIGHT:
                    board.speed[0]=0
                if event.key == K_LEFT:
                    board.speed[0] = 0


        all_balls.update()
        all_boards.update()
        all_bricks.update()
        if ball.rect.bottom > screen.get_height():
            screen.fill((255, 255, 255))
            font = pygame.font.Font(None, 36)
            text = font.render("You Lost", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)
            pygame.display.flip()
            time.sleep(3)
            break
        if ball.rect.colliderect(board.rect):
            angle = board.rect.centerx-ball.rect.centerx
            angle =angle/70
            cangle =math.sqrt(1-angle**2)
            module =math.sqrt( ball.speed[0]**2 + ball.speed[1]**2)
            vector = [-angle*module,-cangle*module]
            ball.speed=vector
        if pygame.sprite.groupcollide(all_balls,all_bricks, False, False, pygame.sprite.collide_mask):
            for brick in all_bricks:
                if brick.rect.colliderect(ball.rect):
                    collision_rect = ball.rect.clip(brick.rect)
                    if collision_rect.width>collision_rect.height:
                        ball.speed[1]=-ball.speed[1]
                    elif collision_rect.width<collision_rect.height:
                        ball.speed[0] = -ball.speed[0]
                    else:
                        ball.speed[1] = -ball.speed[1]
                        ball.speed[0] = -ball.speed[0]
                    all_bricks.remove(brick)
                    break

        if not all_bricks :
            screen.fill((255, 255, 255))
            font = pygame.font.Font(None,36)
            text =font.render("You won",True,(0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text,text_rect)
            pygame.display.flip()
            time.sleep(3)
            break

        screen.fill((255, 255, 255))
        all_balls.draw(screen)
        all_boards.draw(screen)
        all_bricks.draw(screen)
        pygame.display.flip()
    pygame.quit()
