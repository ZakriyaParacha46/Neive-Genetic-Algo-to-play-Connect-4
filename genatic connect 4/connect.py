import genetic as gn
import numpy as np
import pygame
import sys
from sympy import true

width = 6
height = 6
squresize = 30
Connect = 4
pausetime = 100
senstivty = 30


def create_board(height, width):
    board = np.zeros((height, width))
    return board


def game_loop(board, netA, netB):
    gaveover = False
    turn = 1
    count = 0
    max = [0, 0]

    draw_board(board)

    pygame.display.update()
    while (not gaveover):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()

            if (event.type == pygame.MOUSEMOTION):
                pygame.draw.rect(
                    screen, "BLACK", (0, 0, width*squresize, squresize))
                if(event.pos[0] < (width*squresize)-10):
                    if (turn):
                        pygame.draw.circle(
                            screen, "RED", (int(event.pos[0]), int(squresize/2)), squresize*2/5)
                    else:
                        pygame.draw.circle(
                            screen, "GREEN", (int(event.pos[0]), int(squresize/2)), squresize*2/5)
                pygame.display.update()

            # if (event.type == pygame.MOUSEBUTTONDOWN):
            #    x = int(math.floor(event.pos[0]/squresize))
        if (turn):
            x = np.argmax(netA.predict(
                board.reshape((width*height, 1))*senstivty))
            board = playturn("A", 1, board, x)

            if (type(board) == int):
                return (count/(width*height)) + max[0]/Connect, netA

                if(max[0] > max[1]):
                    return (count/(width*height)) + max[0]/Connect, netA
                elif(max[1] >= max[0]):
                    return (count/(width*height)) + max[1]/Connect, netB

        else:
            # x = np.argmax(netB.predict(
            #   board.reshape((width*height, 1))*senstivty))
            x = int(input("Enter the number 0-5: "))
            board = playturn("B", 2, board, x)

            if (type(board) == int):
                return (count/(width*height)) + max[0]/Connect, netA

                if(max[0] > max[1]):
                    return (count/(width*height)) + (max[0]/Connect), netA
                elif(max[1] >= max[0]):
                    return (count/(width*height)) + (max[1]/Connect), netB

        turn = not(turn)

        count = count+1
        draw_board(board)
        pygame.display.update()

        m, w = check_winner(board, turn)
        if(not(w)):
            if(max[turn] < m):
                max[turn] = m

        pygame.time.wait(pausetime)
        if(w):
            if(w == 1):
                print("player {} won".format("A"))
                exit()
                return (count/(width*height))+m, netA
            else:
                print("player {} won".format("B"))
                exit()
                return count/(width*height)-0.1, netA
                # pygame.time.wait(2000)
                # sys.exit()


def playturn(player, c, board, x):
    width = board.shape[1]
    height = board.shape[0]

    # x = int(input("{} turn: select from 1-{}: ".format(player, width)))-1
    if(x < 0 or x > width-1):
        print("Wrong Input: ")
        playturn(player, c, board)
    else:
        if(board[0][x] != 0):
            return -1

        for ind, row in enumerate(board):
            if (row[x] != 0):
                board[ind-1][x] = c
                break

            elif (ind == height-1):
                board[ind][x] = c
                break

    return board


def check_winner(board, turn):
    max = 0
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):

            k, c = check_line(board, turn, x, y, 0, 1)
            if(1.1*k > max):
                max = 1.1*k
            if(c):
                print("horizontal!!")
                return 0.8, c

            k, c = check_line(board, turn, x, y, 1, 0)
            if(k > max):
                max = k
            if(c):
                return 0.5, c

            k, c = check_line(board, turn, x, y, 1, 1)
            if(1.2*k > max):
                max = 1.2*k
            if(c):
                print("Diaogonal!!")
                return 0.9, c

            k, c = check_line(board, turn, x, y, 1, -1)
            if(1.2*k > max):
                max = 1.2*k
            if(c):
                print("Diaogonal!!")
                return 0.9, c
    return max, 0


def check_line(board, turn, x, y, offx, offy):
    height = board.shape[0]
    width = board.shape[1]
    ini = board[x][y]

    if(ini == 0.0):
        return 0, 0

    if(ini != int(turn)+1):
        return 0, 0

    for i in range(Connect-1):
        x = x+offx
        y = y+offy

        if(x >= height or y >= width or y < 0 or x < 0):
            return i, 0
        if(board[x][y] != ini):
            return i, 0

    return 0, ini


def print_board(board):
    print(board)
# pygame graphics


def draw_board(board):
    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            pygame.draw.rect(screen, "BLUE", (c*squresize, r *
                             squresize+squresize, squresize, squresize))

            if(board[r][c] == 0):
                pygame.draw.circle(
                    screen, "BLACK", (int(c*squresize + squresize/2), int(r*squresize+squresize+squresize/2)), squresize*2/5)

            elif(board[r][c] == 1):
                pygame.draw.circle(
                    screen, "RED", (int(c*squresize + squresize/2), int(r*squresize+squresize+squresize/2)), squresize*2/5)

            else:
                pygame.draw.circle(
                    screen, "GREEN", (int(c*squresize + squresize/2), int(r*squresize+squresize+squresize/2)), squresize*2/5)


def Average(lst):
    return sum(lst) / len(lst)


def s(models, inscores):
    scores = []
    for i in inscores:
        scores.append(i)

    sorted = []
    for i in range(len(scores)):
        max = 0
        ind = 0
        for j in range(len(scores)):
            if(scores[j] > max):
                max = scores[j]
                scores[j] = -1
                ind = j
        sorted.append(models[ind])

    return sorted


gen = 20
pop = 40
layers = (width*height, 15, width)
size = (width*squresize, (height+1)*squresize)

pygame.init()
screen = pygame.display.set_mode(size)

netB = gn.NeuralNetwork(layers)
# netB.keep("netB")
#netB = netB.read("netB")

# uncomment for auto learn
net = gn.NeuralNetwork(layers)
net = net.read("winner")

winners = []
winner_scores = []
best = 0
avg = []

for g in range(1, gen):
    models = []
    score = []
    for i in range(int(pop)):
        if (g == 1):
            #netA = gn.NeuralNetwork(layers)
            # uncomment for auto learn
            netA = net.mutation(30)
            pass

        else:
            netA = net.mutation(40)
            pass
            #netB = net.mutation(20)

        b = create_board(height, width)
        c, winmodel = game_loop(b, netA, netB)
        # print(netA, netB, "->", winmodel)
        models.append(winmodel)
        score.append((c))

    # print("==================")
    #print("gen: ", g)
    # print(score)
    #print("Avg: ", Average(score))
    #print("Max: ", max(score))
    avg.append(Average(score))
    maxscore = max(score)
    modelsorted = s(models, score)

    # for total report
    winners.append(models[0])
    winner_scores.append(maxscore)
    if(maxscore > best):
        best = maxscore

    net = netA.evolve(modelsorted)
    g = g+1

winnermodelsorted = s(winners, winner_scores)
net = netA.evolve(winnermodelsorted)
# net.keep("winner")1

print("=======Total Report=======")
#print("all generation best score: ", winner_scores)
print("Max score: ", best)
#print("AVG of generations: ", avg)
print("max avg: ", max(avg))
print("Average of avg of generations: ", Average(avg))

'''
netA = gn.NeuralNetwork(layers)
netB = gn.NeuralNetwork(layers)
c, winmodel = game_loop(b, netA, netB)

while (true):
    print("Gen: ", gen)
    b = create_board(height, width)
    c, w = game_loop(b, winmodel, winmodel.mutation(50))
    print(c)
    if(c != 0):
        winmodel = w.mutation(200/c)
    else:
        winmodel = w
    gen = gen+1'''
