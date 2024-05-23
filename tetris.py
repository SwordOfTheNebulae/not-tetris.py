from input import InputHandler
from time import monotonic, sleep
from pynput.keyboard import Key
import random

class TetrisGame:
    boardwidth = 10
    boardheight = 40
    visibleheight = 20
    frametime = 1/60
    # I O T S Z J L
    pieces = [
        [ # I
            [
                [0,0,0,0],
                [1,1,1,1],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,0,1,0],
                [0,0,1,0],
                [0,0,1,0],
                [0,0,1,0]
            ],
            [
                [0,0,0,0],
                [0,0,0,0],
                [1,1,1,1],
                [0,0,0,0]
            ],
            [
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0],
                [0,1,0,0]
            ],
        ],
        [ # O
            [
                [0,2,2,0],
                [0,2,2,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,2,2,0],
                [0,2,2,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,2,2,0],
                [0,2,2,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,2,2,0],
                [0,2,2,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
        ],
        [ # T
            [
                [0,3,0,0],
                [3,3,3,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,3,0,0],
                [0,3,3,0],
                [0,3,0,0],
                [0,0,0,0]
            ],
            [
                [0,0,0,0],
                [3,3,3,0],
                [0,3,0,0],
                [0,0,0,0]
            ],
            [
                [0,3,0,0],
                [3,3,0,0],
                [0,3,0,0],
                [0,0,0,0]
            ],
        ],
        [ # S
            [
                [0,4,4,0],
                [4,4,0,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,4,0,0],
                [0,4,4,0],
                [0,0,4,0],
                [0,0,0,0]
            ],
            [
                [0,0,0,0],
                [0,4,4,0],
                [4,4,0,0],
                [0,0,0,0]
            ],
            [
                [4,0,0,0],
                [4,4,0,0],
                [0,4,0,0],
                [0,0,0,0]
            ],
        ],
        [ # Z
            [
                [5,5,0,0],
                [0,5,5,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,0,5,0],
                [0,5,5,0],
                [0,5,0,0],
                [0,0,0,0]
            ],
            [
                [0,0,0,0],
                [5,5,0,0],
                [0,5,5,0],
                [0,0,0,0]
            ],
            [
                [0,5,0,0],
                [5,5,0,0],
                [5,0,0,0],
                [0,0,0,0]
            ],
        ],
        [ # J
            [
                [6,0,0,0],
                [6,6,6,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,6,6,0],
                [0,6,0,0],
                [0,6,0,0],
                [0,0,0,0]
            ],
            [
                [0,0,0,0],
                [6,6,6,0],
                [0,0,6,0],
                [0,0,0,0]
            ],
            [
                [0,6,0,0],
                [0,6,0,0],
                [6,6,0,0],
                [0,0,0,0]
            ],
        ],
        [ # L
            [
                [0,0,7,0],
                [7,7,7,0],
                [0,0,0,0],
                [0,0,0,0]
            ],
            [
                [0,7,0,0],
                [0,7,0,0],
                [0,7,7,0],
                [0,0,0,0]
            ],
            [
                [0,0,0,0],
                [7,7,7,0],
                [7,0,0,0],
                [0,0,0,0]
            ],
            [
                [7,7,0,0],
                [0,7,0,0],
                [0,7,0,0],
                [0,0,0,0]
            ],
        ],
    ]
    # blank I O T S Z J L
    tilescolour =      ["  ", "██", "██", "██", "██", "██", "██", "██"]
    
    ghosttilescolour = ["  ", "▒▒", "▒▒", "▒▒", "▒▒", "▒▒", "▒▒", "▒▒"]
    
    tiles =            ["  ", "██", "▓▓", "▒▒", "░░", "╪╪", "{}", "[]"]
    
    ghosttiles =       ["  ", "::", "::", "::", "::", "::", "::", "::"]
    
    # white cyan yellow purple green red blue orange
    tilecolours = ["015", "045", "226", "129", "082", "196", "027", "208"]
    _playfieldtemplate: list[tuple[int,str]] = [
        (4,  "|        |{}|        |"),
        (1,  "|--------|{}|        |"),
        (15, "         |{}|        |"),
    ]
    playfieldtemplate = [line for number,text in _playfieldtemplate for line in [text]*number]
    
    def __init__(self, usecolour = True) -> None:
        # print("\n\n".join(["\n".join(["".join([str(i) for i in line]) for line in piece[0]]) for piece in self.pieces]))
        # exit(0)
        self.usecolour = usecolour
        
        self.input = InputHandler()
        self.board = [[0 for _ in range(self.boardwidth)] for _ in range(self.boardheight)]
        
        self.queue = self.get_bag() + self.get_bag()
        self.tilecharwidth = len(self.gettilegraphic(1))
        self.holdpiece = -1
        
        self.currentpiece = -1
        self.currentpiecerot = 0
        self.currentpiecex = 3
        self.currentpiecey = -2
        
        self.canhold = True
        
        # self.nextpiece()
        
        
    def nextpiece(self, place=True):
        self.setpiece(self.queue.pop(0), place)
        if len(self.queue) < 7: self.queue += self.get_bag()
        
    def setpiece(self, piece: int, place=True):
        self.canhold = place
        if place and self.currentpiece != -1:
            for localy in range(4):
                for localx in range(4):
                   if tile := self.pieces[self.currentpiece][self.currentpiecerot][localy][localx]:
                       x = self.currentpiecex + localx
                       y = self.currentpiecey + localy
                       self.board[y][x] = tile
        self.currentpiece = piece
        self.currentpiecerot = 0
        self.currentpiecex = 3
        self.currentpiecey = -2
        self.movepiece(y=1,dontstick=True)
        
    def _keep_running(self):
        return self.input.listener.is_alive()
    
    @staticmethod
    def get_bag() -> list[int]:
        return random.sample(range(7),7)
    
    def __str__(self) -> str:
        out = ["\x1b[38;5;15m-- TETANUS -- V 0.1 -- [?] for controls",
               "|--HOLD--|" + "-"*20 + "|--NEXT--|"]
        # for y in range(self.visibleheight):
        #     out.append("|" + "".join([self.chars[tile] for tile in self.board[y]]) + "|")
        out += [self.playfieldtemplate[y].format("".join(
            [self.gettile(x,y,*self.ghostpiece()) 
                for x in range(self.boardwidth)]
            )) for y in range(self.visibleheight)]
        out.append("         |" + "-"*20 + "|--------|")
        out.append("SCORE: N/A | TIME: N/A | LINES: N/A | LEVEL: N/A\x1b[0m")
        for piece in range(7):
            for y in range(2):
                pos = piece*3+y + 2
                out[pos] = (out[pos][:11 + 10*self.tilecharwidth] + 
                                  self.getpiecerow(self.queue[piece], y) + 
                                  out[pos][19 + 10*self.tilecharwidth:])
        if self.holdpiece >= 0:
            for y in range(2):
                pos = y + 2
                out[pos] = (out[pos][:1] + 
                                  self.getpiecerow(self.holdpiece, y) + 
                                  out[pos][9:])
        return "\x1b[38;5;15m\n".join(out)
    
    def gettile(self, x: int, y: int, ghostx: int, ghosty: int):
        if (self.currentpiecex <= x < self.currentpiecex + 4
                and self.currentpiecey <= y < self.currentpiecey + 4
                and self.currentpiece != -1
                and (curr := self.getcurrentpiece()[y-self.currentpiecey][x-self.currentpiecex]) != 0):
            return self.gettilegraphic(curr)
        elif (ghostx <= x < ghostx + 4
                and ghosty <= y < ghosty + 4
                and self.getcurrentpiece()[y-ghosty][x-ghostx] != 0
                and  self.currentpiece != -1):
            return self.getghostgraphic(self.getcurrentpiece()[y-ghosty][x-ghostx])
        else: 
            return self.gettilegraphic(self.board[y][x])
        
    def gettilegraphic(self, tile: int):
        if self.usecolour:
            return f"\x1b[38;5;{self.tilecolours[tile]}m{self.tilescolour[tile]}\x1b[38;5;15m"
        else:
            return self.tiles[tile]
        
    def getghostgraphic(self, tile: int):
        if self.usecolour:
            return f"\x1b[38;5;{self.tilecolours[tile]}m{self.ghosttilescolour[tile]}\x1b[38;5;15m"
        else:
            return self.ghosttiles[tile]
    
    def getpiecerow(self, piece:int, localy: int):
        return "".join([self.gettilegraphic(self.pieces[piece][0][localy][localx]) for localx in range(4)])

    
    def getcurrentpiece(self):
        return self.pieces[self.currentpiece][self.currentpiecerot]
    
    def getdelay(self):
        return 1
    
    def ghostpiece(self):
        piece = self.pieces[self.currentpiece][self.currentpiecerot]
        done = False
        y = 0
        x = self.currentpiecex
        while not done:
            for localy in range(4):
               for localx in range(4):
                    if piece[localy][localx]:
                        testy = y + localy
                        testx = x + localx
                        if testy >= self.boardheight - self.visibleheight or self.board[testy][testx] != 0: 
                            done = True
            y += 1
        return (x,y-2)
    
    def movepiece(self, x = 0, y = 0, dontstick = False):
        newx = self.currentpiecex + x
        newy = self.currentpiecey + y
        
        piece = self.pieces[self.currentpiece][self.currentpiecerot]
        for localy in range(4):
            for localx in range(4):
                if piece[localy][localx]:
                    x = newx + localx
                    y = newy + localy
                    if x < 0 or x >= self.boardwidth: return False # cancel movement
                    if y < self.visibleheight - self.boardheight: return False
                    if y >= self.boardheight - self.visibleheight: 
                        # hit bottom of board
                        self.nextpiece()
                        return False# cancel movement
                    if self.board[y][x] != 0: 
                        if not dontstick: self.nextpiece()
                        return  False
                    
        self.currentpiecex = newx
        self.currentpiecey = newy
        return True
        
    def rotpiece(self, rot):
        x = self.currentpiecex
        y = self.currentpiecey
        newrot = (self.currentpiecerot + rot) % 4
        
        testpiece = self.pieces[self.currentpiece][newrot]
        # todo: impliment SRS rotation properly
        for localy in range(4):
            for localx in range(4):
                if testpiece[localy][localx]:
                    if x + localx < 0: x += 1
                    if x + localx >= self.boardwidth: x -= 1
                    if y + localy < self.visibleheight - self.boardheight: y += 1
                    if y + localy >= self.boardheight - self.visibleheight: y -= 1
                    
        self.currentpiecex = x
        self.currentpiecey = y
        self.currentpiecerot = newrot
    
    def run(self):
        cumulativetime = 0
        lasttime = monotonic()
        while self._keep_running(): 
            time = monotonic()
            cumulativetime += time - lasttime
            lasttime = time
            
            if cumulativetime > (delay:=self.getdelay()):
                cumulativetime -= delay
                self.movepiece(y=1)
                if self.currentpiece == -1: self.nextpiece()
            
            move = [0,0]
            rot = 0
                
            if self.input.get_justpressed('a') or self.input.get_justpressed(Key.left):
                move[0] = max(move[0]-1,-1)
            if self.input.get_justpressed('d') or self.input.get_justpressed(Key.right):
                move[0] = min(move[0]+1,1)
            if self.input.get_justpressed('s') or self.input.get_justpressed(Key.down):
                move[1] = min(move[1]+1,1)
            if self.input.get_justpressed('w') or self.input.get_justpressed(Key.up) or self.input.get_justpressed('x'):
                rot = min(rot+1,1)
            if self.input.get_justpressed('z') or self.input.get_justpressed(Key.ctrl_l):
                rot = max(rot-1,-1)
            if self.input.get_justpressed('c') or self.input.get_justpressed(Key.shift):
                if self.canhold:
                    temp = self.currentpiece
                    if(self.holdpiece != -1): self.setpiece(self.holdpiece, False)
                    else: self.nextpiece(False)
                    self.holdpiece = temp
            if(self.input.get_justpressed(Key.space)):
                move = [0,0]
                while self.movepiece(y=1): pass
            if(self.input.get_justpressed(Key.esc) or self.input.get_justpressed(Key.f1)):
                pass # todo pause
             
            
            self.movepiece(*move)
            self.rotpiece(rot)
            
            # self.nextpiece()
            
            print(self, end="\x1b[2J\x1b[H")
            elapsed = monotonic() - time
            sleep(self.frametime - elapsed)
            
import sys
sys.stdin.readable

if __name__ == "__main__":
    TetrisGame((not sys.argv[1].lower().startswith("f")) if len(sys.argv) > 1 else True).run()
    