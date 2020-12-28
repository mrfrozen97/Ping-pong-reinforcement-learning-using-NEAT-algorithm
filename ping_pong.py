# PONG pygame

import random
import pygame, sys
from pygame.locals import *
import neat
import os

pygame.init()
fps = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]
ball_pos = [[0, 0]]
ball_vel = [[0, 0]]
paddle1_vel = []
paddle2_vel = 0
l_score = 0
r_score = 0
gen = 0

# canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hello World')


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    horz = random.randrange(2, 4)
    vert = random.randrange(1, 3)

    if right == False:
        horz = - horz

    ball_vel = [horz, -vert]













# keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0




def main(genomes, config):
    #global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
    global gen

    ball_pos = []
    BALL_RADIUS = 20
    horz = 3
    vertz = 2
    ball_vel = []

    paddle1_pos = []
    paddle1_vel = []
    score = []
    nets = []
    ge = []

    gen += 1
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        #ball_pos.append([WIDTH // 2, HEIGHT // 2 + 150])
        ball_pos.append([random.randint(100, 500), random.randint(25, 375)])
        paddle1_vel.append(0)

        if random.random()>0.5:
            ball_vel.append([random.randrange(2,4), random.randrange(1,3)])
        else:
            ball_vel.append([random.randrange(2,4), -random.randrange(1,3)])

        paddle1_pos.append([HALF_PAD_WIDTH - 1, HEIGHT // 2])
        g.fitness = 0
        ge.append(g)
        score.append(0)



    # game loop

    game_over = True
    while game_over:
        canvas = window


        if len(ball_pos) == 0:
            game_over = False
        else:
            pygame.display.update()
            fps.tick(200)
            canvas.fill(BLACK)

        for x, ball in enumerate(ball_pos):


            pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 1)
            pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
            pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)
            pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

            # update paddle's vertical position, keep paddle on the screen
            if paddle1_pos[x][1] > HALF_PAD_HEIGHT and paddle1_pos[x][1] < HEIGHT - HALF_PAD_HEIGHT:
                ge[x].fitness += 1
                paddle1_pos[x][1] += paddle1_vel[x]
            elif paddle1_pos[x][1] == HALF_PAD_HEIGHT and paddle1_vel[x] > 0:
                paddle1_pos[x][1] += paddle1_vel[x]
                ge[x].fitness += 1
            elif paddle1_pos[x][1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel[x] < 0:
                paddle1_pos[x][1] += paddle1_vel[x]
                ge[x].fitness += 1

            ge[x].fitness += 0.1
            dir = 0
            #if ball_vel[x][0]>0:
             #   dir = 100
           # output = nets[x].activate((paddle1_pos[x][1], ball[0], ball[1], dir))
            #output = nets[x].activate((paddle1_pos[x][1],ball[0], ball[1]))
            output = nets[x].activate((paddle1_pos[x][1]-ball[1], ball[0]))

            if output[0]>0.8:
                paddle1_vel[x] = -4
            elif output[0]<=-0.8:
                paddle1_vel[x] = 4
            else:
                paddle1_vel[x] = 0




            # update ball
            ball[0] += int(ball_vel[x][0])
            ball[1] += int(ball_vel[x][1])

            # draw paddles and ball
            pygame.draw.circle(canvas, RED, ball_pos[x], 20, 0)
            pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[x][0] - HALF_PAD_WIDTH, paddle1_pos[x][1] - HALF_PAD_HEIGHT],
                                                [paddle1_pos[x][0] - HALF_PAD_WIDTH, paddle1_pos[x][1] + HALF_PAD_HEIGHT],
                                                [paddle1_pos[x][0] + HALF_PAD_WIDTH, paddle1_pos[x][1] + HALF_PAD_HEIGHT],
                                                [paddle1_pos[x][0] + HALF_PAD_WIDTH, paddle1_pos[x][1] - HALF_PAD_HEIGHT]], 0)


            # ball collision check on top and bottom walls
            if int(ball[1]) <= BALL_RADIUS:

                ball_vel[x][1] = - ball_vel[x][1]

            if int(ball[1]) >= HEIGHT + 1 - BALL_RADIUS:

                ball_vel[x][1] = -ball_vel[x][1]

            # ball collison check on gutters or paddles
            if int(ball[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball[1]) in range(paddle1_pos[x][1] - HALF_PAD_HEIGHT- BALL_RADIUS +3,paddle1_pos[x][1] + HALF_PAD_HEIGHT + BALL_RADIUS-3 , 1):


                score[x]+=1
                ge[x].fitness += 10
                ball_vel[x][0] = -ball_vel[x][0]
                ball_vel[x][0] *= 1.1 #+  ball_vel[x][0]
                ball_vel[x][1] *= 1.1# +  ball_vel[x][1]
            elif int(ball[0]) <= BALL_RADIUS + PAD_WIDTH:
                ge[x].fitness -= 30
                nets.pop(x)
                ge.pop(x)
                ball_vel.pop(x)
                ball_pos.pop(x)
                score.pop(x)
                paddle1_pos.pop(x)


            if int(ball[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
                if random.random() > 0.5 and ball_vel[x][0] < 3:
                     ball_vel[x][0] = -ball_vel[x][0] - random.random()
                elif ball_vel[x][0] > 0.5:
                    ball_vel[x][0] = -ball_vel[x][0] + random.random()
                else:
                    ball_vel[x][0] = -ball_vel[x][0]


            # update scores
        if len(score)>0:
            myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
            label1 = myfont1.render("Score " + str(score[0]), 1, (255, 255, 0))
            canvas.blit(label1, (50, 20))
        myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont1.render("Generation " + str(gen), 1, (255, 255, 0))
        canvas.blit(label1, (350, 20))



        for event in pygame.event.get():

            #if event.type == KEYDOWN:
              #  keydown(event)
            #elif event.type == KEYUP:
               # keyup(event)
            if event.type == QUIT:
                pygame.quit()
                #sys.exit()





def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)
    print(winner)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "ping_pong_neat.txt")
    run(config_path)
