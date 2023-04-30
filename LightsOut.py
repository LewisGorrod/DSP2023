
import random
import turtle

# Constants
GRID_SIZE = 5
N_BUTTONS = 25
BUTTON_SIZE = 80
SCREEN_SIZE = GRID_SIZE * (BUTTON_SIZE + 10)
MAX_LEVEL = 10

# Button press matrix
A = [
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
]

class Button:
    def __init__(self, index):
        self.turtle = turtle.Turtle()
        self.turtle.shape('square')
        self.turtle.shapesize(4, 4, 1)
        self.turtle.speed(0)
        self.turtle.penup()
        self.turtle.onclick(self.press)
        self.index = index
        row = int(index / GRID_SIZE)
        col = index - GRID_SIZE * row
        self.turtle.sety((SCREEN_SIZE / 2) - (BUTTON_SIZE / 2) - row * (BUTTON_SIZE + 10))
        self.turtle.setx(-(SCREEN_SIZE / 2) + (BUTTON_SIZE / 2) + col * (BUTTON_SIZE + 10))

    def setState(self, state):
        if state == 0:
            self.turtle.color(60, 60, 60)
        else:
            self.turtle.color(0, 162, 232)

    def press(self, x, y):
        update(self.index)

def genSolution(level):
    x = [0 for i in range(N_BUTTONS)]
    for i in range(level):
        x[random.randint(0, N_BUTTONS-1)] = 1
    return x

def printSolution(x):
    for i in range(N_BUTTONS):
        print(x[i], end='')
        if (i + 1) % GRID_SIZE == 0:
            print()

def genStartingConfig(x):
    p = [0 for i in range(N_BUTTONS)]
    for i in range(N_BUTTONS):
        if x[i] == 1:
            for j in range(N_BUTTONS):
                p[j] ^= A[i][j]
    return p

def getNextState(r, buttonPressed):
    rNew = r[:]
    for i in range(N_BUTTONS):
        rNew[i] ^= A[buttonPressed][i]
    return rNew

def isCompleted(r):
        for i in r:
            if i == 1:
                return False
        return True

def updateColors(r, buttons):
    for i in range(N_BUTTONS):
        buttons[i].setState(r[i])

def main():
    turtle.colormode(255)
    turtle.bgcolor(30, 30, 30)
    turtle.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
    buttons = [Button(i) for i in range(N_BUTTONS)]
    level, x, p, r = 0, [], [], []

    global update
    def update(buttonPressed):
        if buttonPressed != None:
            nonlocal buttons, r
            r = getNextState(r, buttonPressed)
            if isCompleted(r):
                genNextLevel()
        updateColors(r, buttons)

    def genNextLevel():
        nonlocal level, x, p, r
        if level == MAX_LEVEL:
            turtle.title(f'Pyghts Out! Game Completed!')
        else:
            level += 1
            turtle.title(f'Pyghts Out! Level {level}')
            x = genSolution(level)
            p = genStartingConfig(x)
            r = p[:]

    genNextLevel()
    update(None)

if __name__ == '__main__':
    main()
    turtle.done()