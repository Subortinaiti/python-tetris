import random,time
import pygame as pg
pg.init()

scale = 26.1
fancyblocks = True
move_interval = 1.5

boardsize = (10,20)
displaysize = (scale*(boardsize[0]+6),scale*(boardsize[1]))

blocktemplates = {
    "L": [
        [[0, 1], [0, 2], [2, 1], [1, 1]],
        [[1, 2], [0, 0], [1, 0], [1, 1]],
        [[0, 1], [2, 1], [1, 1], [2, 0]],
        [[1, 2], [2, 2], [1, 0], [1, 1]]
        ],
    "O": [
        [[1, 1], [1, 2], [2, 1], [2, 2]]
        ],
    "I":[
        [[2, 1], [2, 0], [2, 3], [2, 2]],
        [[0, 1], [3, 1], [1, 1], [2, 1]],
        [[1, 2], [0, 2], [2, 2], [3, 2]],
        [[1, 2], [1, 1], [1, 0], [1, 3]]
        ],
    "J": [    
        [[3, 1], [3, 2], [1, 2], [2, 2]],
        [[2, 1], [2, 3], [3, 3], [2, 2]],
        [[1, 2], [2, 2], [3, 2], [1, 3]],
        [[2, 1], [1, 1], [2, 3], [2, 2]]
        ],

    "T": [
        [[3, 2], [1, 2], [2, 1], [2, 2]],
        [[2, 1], [2, 3], [2, 2], [3, 2]],
        [[1, 2], [2, 3], [2, 2], [3, 2]],
        [[1, 2], [2, 1], [2, 3], [2, 2]]
        ],
    "S": [
        [[1, 1], [2, 1], [3, 2], [2, 2]],
        [[3, 1], [3, 2], [2, 3], [2, 2]],
        [[2, 3], [1, 2], [3, 3], [2, 2]],
        [[1, 2], [2, 1], [2, 2], [1, 3]]
        ],
    "Z": [
        [[1, 2], [2, 1], [3, 1], [2, 2]],
        [[2, 1], [3, 3], [2, 2], [3, 2]],
        [[2, 3], [2, 2], [3, 2], [1, 3]],
        [[1, 2], [1, 1], [2, 3], [2, 2]]
        ]

    }

blocktemplatecolors = {
    "L": (0, 0, 255),
    "O": (255, 255, 0),
    "I": (0, 255, 255),
    "J": (255, 127, 0),
    "T": (128, 0, 128),
    "S": (0, 255, 0),
    "Z": (255, 0, 0)
}

class Piece:
    def __init__(self,blockstate,color,x,y):
        self.blockstate = blockstate
        self.color = color
        self.x = x
        self.y = y
        self.rot = 0

    def draw_self(self, display,board):
        ghost_color = tuple(color // 2 for color in self.color)
        ghost_x, ghost_y = self.x, self.y
        while True:
            ghost_y += 1
            for coords in self.blockstate[self.rot]:
                if coords[1] + ghost_y >= 20:
                    break
                for block in board.blocks:
                    if block[0][0] == coords[0] + self.x and block[0][1] == coords[1] + ghost_y:
                        break
                else:
                    continue
                break
            else:
                continue
            break
        

        for coords in self.blockstate[self.rot]:
            pg.draw.rect(display, ghost_color, ((ghost_x + coords[0]) * scale, (ghost_y + coords[1]-1) * scale, scale, scale))
        

        for coords in self.blockstate[self.rot]:
            pg.draw.rect(display, self.color, ((self.x + coords[0]) * scale, (self.y + coords[1]) * scale, scale, scale))
            if fancyblocks:
                pg.draw.rect(display, ghost_color, ((self.x + coords[0]) * scale, (self.y + coords[1]) * scale, scale, scale),int(scale/8))                

    def draw_self_unanchored(self,display,x,y):
        for coords in self.blockstate[self.rot]:
            pg.draw.rect(display, self.color, ((x + coords[0]) * scale, (y + coords[1]) * scale, scale, scale))
##            if fancyblocks:
##                pg.draw.rect(display, ghost_color, ((x + coords[0]) * scale, (y + coords[1]) * scale, scale, scale),int(scale/8))             


    def rl(self, board):
        self.rot -= 1
        if self.rot == -1:
            self.rot = len(self.blockstate) - 1
        if self.collidesWithBoard(board):
            original_x = self.x
            self.x -= 1
            if self.collidesWithBoard(board):
                self.x = original_x
                self.rr(board)

    def rr(self, board):
        self.rot += 1
        if self.rot == len(self.blockstate):
            self.rot = 0
        if self.collidesWithBoard(board):
            original_x = self.x
            self.x += 1
            if self.collidesWithBoard(board):
                self.x = original_x
                self.rl(board)

    def moveDown(self,board):
        self.y += 1
        for coords in self.blockstate[self.rot]:
            if coords[1]+self.y >= 20:
                self.y -= 1
                return False
            for block in board.blocks:

                if block[0][0] == coords[0]+self.x and block[0][1] == coords[1]+self.y:
                    self.y -= 1
                    return False
            
        return True
        
    def powerDrop(self,board):
        while True:
            if not self.moveDown(board):
                break
        board.advance_pieces()

    def moveLeft(self, board):
        self.x -= 1
        if self.collidesWithBoard(board):
            self.x += 1

    def moveRight(self, board):
        self.x += 1
        if self.collidesWithBoard(board):
            self.x -= 1

    def collidesWithBoard(self, board):
        for coords in self.blockstate[self.rot]:
            x, y = self.x + coords[0], self.y + coords[1]
            if x < 0 or x >= board.w or y >= board.h:
                return True
            for block in board.blocks:
                if block[0][0] == x and block[0][1] == y:
                    return True
        return False



class Board:
    def __init__(self):
        self.w,self.h = boardsize
        self.switched = False
        self.activePiece = None
        self.blocks = []
        self.nextPiece = getRandomPiece()
        self.ghostPiece = None
        self.holdPiece = None
        self.score = 0
        
    def setActivePiece(self,piece):
        self.activePiece = piece
        
    def draw_self(self,display):
        self.activePiece.draw_self(display,self)
        for block,color in self.blocks:
            pg.draw.rect(display,color,(block[0]*scale,block[1]*scale,scale,scale))
            if fancyblocks:
                ghost_color = tuple(color2 // 2 for color2 in color)
                pg.draw.rect(display, ghost_color, (block[0]*scale,block[1]*scale, scale, scale),int(scale/8))     
    def advance_pieces(self):
        res = self.activePiece.moveDown(self)
        if not res:
            for piece in self.activePiece.blockstate[self.activePiece.rot]:
                bx,by = piece[0]+self.activePiece.x,piece[1]+self.activePiece.y
                self.blocks.append([[bx,by],self.activePiece.color])

            self.activePiece = self.nextPiece
            self.nextPiece = getRandomPiece()
            self.switched = False
            self.score += self.getFull()
            
    def switchHold(self):
        if not self.switched:
            if self.holdPiece is not None:
                c = Piece(self.activePiece.blockstate,self.activePiece.color,4,-2)
                self.activePiece = self.holdPiece
                self.holdPiece = c
            else:
                self.holdPiece = Piece(self.activePiece.blockstate,self.activePiece.color,4,-2)
                self.activePiece = self.nextPiece
                self.nextPiece = getRandomPiece()
            self.switched = True


    def getFull(self):
        full_rows = []
        for row in range(self.h):
            row_blocks = [block[0][1] for block in self.blocks if block[0][1] == row]
            if len(row_blocks) == self.w:
                full_rows.append(row)

        if full_rows:
            for row in sorted(full_rows, reverse=True):
                self.blocks = [block for block in self.blocks if block[0][1] != row]
                for i in range(len(self.blocks)):
                    if self.blocks[i][0][1] < row:
                        self.blocks[i][0][1] += 1

            
        scores = [0,40,100,300,1200]
        return scores[len(full_rows)]
                    

    def checkGameOver(self):
        for coords in self.activePiece.blockstate[self.activePiece.rot]:
            x, y = coords[0] + self.activePiece.x, coords[1] + self.activePiece.y
            if [x, y] in [block[0] for block in self.blocks]:
                return True
        return False
                    

def getRandomPiece():
    r = random.choice("OITLJSZ")
    p = Piece(blocktemplates[r],blocktemplatecolors[r],4,-2)
    return p

def drawHud(display,board,font):
    pg.draw.line(display,(50,50,50),(10*scale,0),(10*scale,displaysize[1]),int(scale/5))
    display.blit(font.render(str(board.score),True,(255,255,255)),(11*scale,scale))
    display.blit(font.render(str("NEXT"),True,(255,255,255)),(12*scale,3*scale))
    board.nextPiece.draw_self_unanchored(display,10.5,4)
    display.blit(font.render(str("HOLD"),True,(255,255,255)),(12*scale,8*scale))
    if board.holdPiece:
        board.holdPiece.draw_self_unanchored(display,10.5,9)
    

def main():
    display = pg.display.set_mode(displaysize)
    board = Board()
    board.setActivePiece(getRandomPiece())
    cooldown = time.time()+move_interval
    font = pg.font.SysFont("Calibri",int(scale))
    dead = False
    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = True
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    dead = True
                    pg.quit()
                    quit()
                elif event.key == pg.K_UP:
                    board.activePiece.rl(board)
                elif event.key == pg.K_DOWN:
                    board.activePiece.moveDown(board)
                elif event.key == pg.K_LEFT:
                    board.activePiece.moveLeft(board)
                elif event.key == pg.K_RIGHT:
                    board.activePiece.moveRight(board)
                elif event.key == pg.K_SPACE:
                    board.activePiece.powerDrop(board)
                    cooldown = time.time()+move_interval
                elif event.key == pg.K_c:
                    board.switchHold()


        if time.time() >= cooldown:
            cooldown = time.time()+move_interval
            board.advance_pieces()
        display.fill((0,0,0))
        drawHud(display,board,font)
        board.draw_self(display)
        pg.display.flip()
        dead = board.checkGameOver()


        

main()
pg.quit()
quit()
