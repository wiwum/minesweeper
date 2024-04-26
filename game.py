import random
import itertools

#minesweeper game:
    #fullBoard: 2d array of [0-9] that represents mine locations and hidden tile values.
    #visBoard: 2d array of [-2-9] that represents board visible to player
        #-2 = flag
        #-1 = unknown tile
    #bombs: number of bombs
class Game:
    def __init__(self, fullBoard, visBoard, bombs):
        self.bombs = bombs
        self.fullBoard = fullBoard
        self.visBoard = visBoard
    
    #print board visible to player, 0 tiles print as [space], flags print as *, unknown tiles print as #
    def printVisBoard(self):
        print("\n")
        print("bombs: ", self.bombs)
        #print border with col indexes
        print(" ", " ", "", end='')
        for i in range(len(self.visBoard[0])):
            print(self.numberToCoord(i), "", end='')
        print("")
        print(" ", "+ ", end='')
        for j in range(len(self.visBoard[0])):
            print("- ", end='')
        print("")
        #print rows with border with row indexes
        ri = 0
        for r in self.visBoard:
            print(self.numberToCoord(ri), "| ", end='')
            ri+=1
            for c in r:
                if c == -2:
                    print("* ", end='')
                elif c == -1:
                    print("# ", end='')
                elif c == 0:
                    print(" ", "", end='')
                else:
                    print(c, "", end='')
            print(" ", " ")
        print("\n")
    
    def coordToNumber(self, coord):
        arr = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        return arr.index(coord)
    
    def numberToCoord(self, n):
        arr = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        return arr[n]
    
    #return true if any 0, -1 are adjecent
    def adj0(self):
        for r in range(len(self.visBoard)):
            for c in range(len(self.visBoard[r])):
                if self.visBoard[r][c] == 0:
                    if r > 0 and c > 0:
                        if self.visBoard[r-1][c-1] == -1:
                            return True
                    if r > 0:
                        if self.visBoard[r-1][c] == -1:
                            return True
                    if r > 0 and c < len(self.visBoard[r])-1:
                        if self.visBoard[r-1][c+1] == -1:
                            return True
                    if c < len(self.visBoard[r])-1:
                        if self.visBoard[r][c+1] == -1:
                            return True
                    if r < len(self.visBoard)-1 and c < len(self.visBoard[r])-1:
                        if self.visBoard[r+1][c+1] == -1:
                            return True
                    if r < len(self.visBoard)-1:
                        if self.visBoard[r+1][c] == -1:
                            return True
                    if r < len(self.visBoard)-1 and c > 0:
                        if self.visBoard[r+1][c-1] == -1:
                            return True
                    if c > 0:
                        if self.visBoard[r][c-1] == -1:
                            return True
        return False

    def updateBoard(self, cr, cc, flag):

        #convert single digit base 36 coord to int
        r = self.coordToNumber(cr)
        c = self.coordToNumber(cc)

        #if placing flag, set to -2 or -1 to remove flag
        if flag:
            if self.visBoard[r][c] == -1:
                self.visBoard[r][c] = -2
                self.bombs-=1
                return
            if self.visBoard[r][c] == -2:
                self.visBoard[r][c] = -1
                self.bombs+=1
                return
            return
        
        #if square already cleared return
        if self.visBoard[r][c] >= 0:
            return
        
        #clearing unknown tile, set to true value
        if self.visBoard[r][c] == -1:
            self.visBoard[r][c] = self.fullBoard[r][c]
        
        #clear all unknown tiles adjacent to a 0
        while(self.adj0()):
            for r in range(len(self.visBoard)):
                for c in range(len(self.visBoard[0])):
                    if self.visBoard[r][c] == 0:
                        #set all 8 tiles around 0 to their true value
                        if r > 0 and c > 0:
                            self.visBoard[r-1][c-1] = self.fullBoard[r-1][c-1]
                        if r > 0:
                            self.visBoard[r-1][c] = self.fullBoard[r-1][c]
                        if r > 0 and c < len(self.visBoard[r])-1:
                            self.visBoard[r-1][c+1] = self.fullBoard[r-1][c+1]
                        if c < len(self.visBoard[r])-1:
                            self.visBoard[r][c+1] = self.fullBoard[r][c+1]
                        if r < len(self.visBoard)-1 and c < len(self.visBoard[r])-1:
                            self.visBoard[r+1][c+1] = self.fullBoard[r+1][c+1]
                        if r < len(self.visBoard)-1:
                            self.visBoard[r+1][c] = self.fullBoard[r+1][c]
                        if r < len(self.visBoard)-1 and c > 0:
                            self.visBoard[r+1][c-1] = self.fullBoard[r+1][c-1]
                        if c > 0:
                            self.visBoard[r][c-1] = self.fullBoard[r][c-1]
        
        return 
    
    #check status of game
    #return -1 if game lost (9 (bomb) tile in vis)
    #return 0 if game still going
    #return 1 if game won
    def over(self):
        #check if bomb in vis
        for r in self.visBoard:
            for c in r:
                if c == 9:
                    return -1

        #check if all non bomb tiles cleared
        for r in range(len(self.fullBoard)):
            for c in range(len(self.fullBoard[r])):
                if self.fullBoard[r][c] != 9:
                    if self.visBoard[r][c] < 0:
                        return 0
        return 1

#return new Game with r rows, c cols, and b bombs
def genGame(r, c, b):

    #make r by c array of all -1 for vis
    mv = [[]]
    for i in range(r):
        if i != 0:
            mv.append([])
        for j in range(c):
            mv[i].append(-1)

    #make full
    mf = []
    arr1d = []
    p = b
    e = 0
    #make 1d arr of len r*c with first b elems set to 9, rest to 0
    for k in range(r*c):
        if p > 0:
            arr1d.append(9)
            p-=1
        else:
            arr1d.append(0)
    #shuffle 1d arr (disperse bombs randomly)
    random.shuffle(arr1d)
    #convert 1d arr to 2d arr
    for n in range(r):
        mf.append([])
        for nn in range(c):
            mf[n].append(arr1d[e])
            e+=1
    #update values of all non bomb tiles (init to 0) to be sum of num bombs in 8 adjacent tiles
    for w in range(r):
        for ww in range(c):
            if mf[w][ww] == 0:
                www = 0
                if w > 0:
                    if mf[w-1][ww] == 9:
                        www+=1
                if w > 0 and ww > 0:
                    if mf[w-1][ww-1] == 9:
                        www+=1
                if w > 0 and ww < len(mf[w])-1:
                    if mf[w-1][ww+1] == 9:
                        www+=1
                if w < len(mf)-1:
                    if mf[w+1][ww] == 9:
                        www+=1
                if w < len(mf)-1 and ww > 0:
                    if mf[w+1][ww-1] == 9:
                        www+=1
                if w < len(mf)-1 and ww < len(mf[w])-1:
                    if mf[w+1][ww+1] == 9:
                        www+=1
                if ww > 0:
                    if mf[w][ww-1] == 9:
                        www+=1
                if ww < len(mf[w])-1:
                    if mf[w][ww+1] == 9:
                        www+=1
                mf[w][ww] = www

    return Game(mf, mv, b)

#number to coord
def coordToNumber(coord):
        arr = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        return arr.index(coord)
    
def numberToCoord(n):
    arr = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    return arr[n]

#find move given visible board, return move as a string ("rc?" where r, c = base 36 coord, ? = flag:"f", clear:"")
def findMove(bo, n):
    #array of unknown spots, guess if no spot found
    gs = []

    for r in range(len(bo)):
        for c in range(len(bo[r])):

            #add to guess array if unkown tile
            if bo[r][c] == -1:
                gs.append((r, c))
            
            #number tile, analize adjacent
            if bo[r][c] > 0:
                uk = 0 #unkown tiles, = 0 in aa
                bmb = 0 #flags, = -1 in aa
                nm = 0 #number tiles, = 1 in aa
                aa = [] #array of adjacent tiles, tuples (r, c, type) where type = uk: 0, bmb: -1, nm: 1
                #put existing adjacent tiles in aa
                if r > 0 and c > 0:
                    if bo[r-1][c-1] == -1:
                        uk+=1
                        aa.append((r-1, c-1, 0))
                    if bo[r-1][c-1] == -2:
                        bmb+=1
                        aa.append((r-1, c-1, -1))
                    if bo[r-1][c-1] >= 0:
                        nm+=1
                        aa.append((r-1, c-1, 1))
                if r > 0:
                    if bo[r-1][c] == -1:
                        uk+=1
                        aa.append((r-1, c, 0))
                    if bo[r-1][c] == -2:
                        bmb+=1
                        aa.append((r-1, c, -1))
                    if bo[r-1][c] >= 0:
                        nm+=1
                        aa.append((r-1, c, 1))
                if r > 0 and c < len(bo[r])-1:
                    if bo[r-1][c+1] == -1:
                        uk+=1
                        aa.append((r-1, c+1, 0))
                    if bo[r-1][c+1] == -2:
                        bmb+=1
                        aa.append((r-1, c+1, -1))
                    if bo[r-1][c+1] >= 0:
                        nm+=1
                        aa.append((r-1, c+1, 1))
                if c < len(bo[r])-1:
                    if bo[r][c+1] == -1:
                        uk+=1
                        aa.append((r, c+1, 0))
                    if bo[r][c+1] == -2:
                        bmb+=1
                        aa.append((r, c+1, -1))
                    if bo[r][c+1] >= 0:
                        nm+=1
                        aa.append((r, c+1, 1))
                if r < len(bo)-1 and c < len(bo[r])-1:
                    if bo[r+1][c+1] == -1:
                        uk+=1
                        aa.append((r+1, c+1, 0))
                    if bo[r+1][c+1] == -2:
                        bmb+=1
                        aa.append((r+1, c+1, -1))
                    if bo[r+1][c+1] >= 0:
                        nm+=1
                        aa.append((r+1, c+1, 1))
                if r < len(bo)-1:
                    if bo[r+1][c] == -1:
                        uk+=1
                        aa.append((r+1, c, 0))
                    if bo[r+1][c] == -2:
                        bmb+=1
                        aa.append((r+1, c, -1))
                    if bo[r+1][c] >= 0:
                        nm+=1
                        aa.append((r+1, c, 1))
                if r < len(bo)-1 and c > 0:
                    if bo[r+1][c-1] == -1:
                        uk+=1
                        aa.append((r+1, c-1, 0))
                    if bo[r+1][c-1] == -2:
                        bmb+=1
                        aa.append((r+1, c-1, -1))
                    if bo[r+1][c-1] >= 0:
                        nm+=1
                        aa.append((r+1, c-1, 1))
                if c > 0:
                    if bo[r][c-1] == -1:
                        uk+=1
                        aa.append((r, c-1, 0))
                    if bo[r][c-1] == -2:
                        bmb+=1
                        aa.append((r, c-1, -1))
                    if bo[r][c-1] >= 0:
                        nm+=1
                        aa.append((r, c-1, 1))
                #check if any uk, save first uk
                ck = False
                gt = None
                for s in aa:
                    if s[2] == 0:
                        gt = s
                        ck = True
                        break
                if ck:
                    #check if all bmb found
                    tb = bo[r][c]
                    cb = 0
                    for t in aa:
                        if t[2] == -1:
                            cb+=1
                    if cb == tb:
                        return numberToCoord(gt[0]) + numberToCoord(gt[1])
                    #check if only bmb remaining
                    cckk = 0
                    for u in aa:
                        if u[2] == 0:
                            cckk+=1
                    if tb-cb == cckk:
                        return numberToCoord(gt[0]) + numberToCoord(gt[1]) + "f"
    #if blank board, guess random spot
    if len(gs) == len(bo) * len(bo[0]):
        rt = random.choice(gs)
        return numberToCoord(rt[0]) + numberToCoord(rt[1])
    
    #check every combination of bomb arrangements, add valid combos to ba
    ba = []
    for combo in itertools.combinations(gs, n):
        #flag all bombs in current combo (must copy first)
        tst = []
        for rrr in range(len(bo)):
            tst.append([])
            for ccc in range(len(bo[rrr])):
                tst[rrr].append(bo[rrr][ccc])
        for bb in combo:
            tst[bb[0]][bb[1]] = -2
        #check if bomb arrangement violates rules
        add = True
        for ro in range(len(tst)):
            for co in range(len(tst[r])):
                if tst[ro][co] > 0:
                    tv = tst[ro][co]
                    cv = 0
                    if ro > 0 and co > 0:
                        if tst[ro-1][co-1] == -2:
                            cv+=1
                    if ro > 0:
                        if tst[ro-1][co] == -2:
                            cv+=1
                    if ro > 0 and co < len(tst[ro])-1:
                        if tst[ro-1][co+1] == -2:
                            cv+=1
                    if co < len(tst[ro])-1:
                        if tst[ro][co+1] == -2:
                            cv+=1
                    if ro < len(tst)-1 and co < len(tst[ro])-1:
                        if tst[ro+1][co+1] == -2:
                            cv+=1
                    if ro < len(tst)-1:
                        if tst[ro+1][co] == -2:
                            cv+=1
                    if ro < len(tst)-1 and co > 0:
                        if tst[ro+1][co-1] == -2:
                            cv+=1
                    if co > 0:
                        if tst[ro][co-1] == -2:
                            cv+=1
                    if tv != cv:
                        add = False
                        break
        if add:
            ba.append(combo)
    #loop thru bo again, look for spot that is clear in every or no combo, if not clear highest percent chance
    hc = ((-1, -1), 0) #save spot with highest clear chance
    for g in gs:
        tt = 1
        ttt = 1
        for cmb in ba:
            if g not in cmb:
                tt+=1
            ttt+=1
        if tt/ttt == 1:
            return numberToCoord(g[0]) + numberToCoord(g[1])
        if tt == 1 and ttt > 1:
            return numberToCoord(g[0]) + numberToCoord(g[1]) + "f"
        if tt/ttt > hc[1]:
            hc = (g, tt/ttt)
    return numberToCoord(hc[0][0]) + numberToCoord(hc[0][1])

def findMoveFast(bo):
    #array of unknown spots, guess if no spot found
    gs = []

    for r in range(len(bo)):
        for c in range(len(bo[r])):

            #add to guess array if unkown tile
            if bo[r][c] == -1:
                gs.append((r, c))
            
            #number tile, analize adjacent
            if bo[r][c] > 0:
                uk = 0 #unkown tiles, = 0 in aa
                bmb = 0 #flags, = -1 in aa
                nm = 0 #number tiles, = 1 in aa
                aa = [] #array of adjacent tiles, tuples (r, c, type) where type = uk: 0, bmb: -1, nm: 1
                #put existing adjacent tiles in aa
                if r > 0 and c > 0:
                    if bo[r-1][c-1] == -1:
                        uk+=1
                        aa.append((r-1, c-1, 0))
                    if bo[r-1][c-1] == -2:
                        bmb+=1
                        aa.append((r-1, c-1, -1))
                    if bo[r-1][c-1] >= 0:
                        nm+=1
                        aa.append((r-1, c-1, 1))
                if r > 0:
                    if bo[r-1][c] == -1:
                        uk+=1
                        aa.append((r-1, c, 0))
                    if bo[r-1][c] == -2:
                        bmb+=1
                        aa.append((r-1, c, -1))
                    if bo[r-1][c] >= 0:
                        nm+=1
                        aa.append((r-1, c, 1))
                if r > 0 and c < len(bo[r])-1:
                    if bo[r-1][c+1] == -1:
                        uk+=1
                        aa.append((r-1, c+1, 0))
                    if bo[r-1][c+1] == -2:
                        bmb+=1
                        aa.append((r-1, c+1, -1))
                    if bo[r-1][c+1] >= 0:
                        nm+=1
                        aa.append((r-1, c+1, 1))
                if c < len(bo[r])-1:
                    if bo[r][c+1] == -1:
                        uk+=1
                        aa.append((r, c+1, 0))
                    if bo[r][c+1] == -2:
                        bmb+=1
                        aa.append((r, c+1, -1))
                    if bo[r][c+1] >= 0:
                        nm+=1
                        aa.append((r, c+1, 1))
                if r < len(bo)-1 and c < len(bo[r])-1:
                    if bo[r+1][c+1] == -1:
                        uk+=1
                        aa.append((r+1, c+1, 0))
                    if bo[r+1][c+1] == -2:
                        bmb+=1
                        aa.append((r+1, c+1, -1))
                    if bo[r+1][c+1] >= 0:
                        nm+=1
                        aa.append((r+1, c+1, 1))
                if r < len(bo)-1:
                    if bo[r+1][c] == -1:
                        uk+=1
                        aa.append((r+1, c, 0))
                    if bo[r+1][c] == -2:
                        bmb+=1
                        aa.append((r+1, c, -1))
                    if bo[r+1][c] >= 0:
                        nm+=1
                        aa.append((r+1, c, 1))
                if r < len(bo)-1 and c > 0:
                    if bo[r+1][c-1] == -1:
                        uk+=1
                        aa.append((r+1, c-1, 0))
                    if bo[r+1][c-1] == -2:
                        bmb+=1
                        aa.append((r+1, c-1, -1))
                    if bo[r+1][c-1] >= 0:
                        nm+=1
                        aa.append((r+1, c-1, 1))
                if c > 0:
                    if bo[r][c-1] == -1:
                        uk+=1
                        aa.append((r, c-1, 0))
                    if bo[r][c-1] == -2:
                        bmb+=1
                        aa.append((r, c-1, -1))
                    if bo[r][c-1] >= 0:
                        nm+=1
                        aa.append((r, c-1, 1))
                #check if any uk, save first uk
                ck = False
                gt = None
                for s in aa:
                    if s[2] == 0:
                        gt = s
                        ck = True
                        break
                if ck:
                    #check if all bmb found
                    tb = bo[r][c]
                    cb = 0
                    for t in aa:
                        if t[2] == -1:
                            cb+=1
                    if cb == tb:
                        return numberToCoord(gt[0]) + numberToCoord(gt[1])
                    #check if only bmb remaining
                    cckk = 0
                    for u in aa:
                        if u[2] == 0:
                            cckk+=1
                    if tb-cb == cckk:
                        return numberToCoord(gt[0]) + numberToCoord(gt[1]) + "f"
    
    #no move found, guess
    rt = random.choice(gs)
    return numberToCoord(rt[0]) + numberToCoord(rt[1])

#play game with r rows, c cols, b bombs with input from console
def playGame(r, c, b):
    g = genGame(r, c, b)
    while(g.over() == 0):
        g.printVisBoard()
        #u = input("move: ") #human player
        #u = findMove(g.visBoard, g.bombs) #full solver
        u = findMoveFast(g.visBoard) #fast solver
        if len(u) == 2:
            g.updateBoard(u[0], u[1], False)
        elif len(u) == 3:
            if u[2] == "f":
                g.updateBoard(u[0], u[1], True)
            else:
                print("invalid move")
        else:
            print("invalid move")
    g.printVisBoard()
    if g.over() == -1:
        print("you lost!")
    if g.over() == 1:
        print("you won!")

def playTest(g):
    while(g.over() == 0):
        g.printVisBoard()
        #u = input("move: ") #human player
        u = findMove(g.visBoard, g.bombs) #full solver
        #u = findMoveFast(g.visBoard)
        if len(u) == 2:
            g.updateBoard(u[0], u[1], False)
        elif len(u) == 3:
            if u[2] == "f":
                g.updateBoard(u[0], u[1], True)
            else:
                print("invalid move")
        else:
            print("invalid move")
    g.printVisBoard()
    if g.over() == -1:
        print("you lost!")
    if g.over() == 1:
        print("you won!")

testGame = Game(
    fullBoard=[
        [ 0, 0, 0, 0, 1, 9 ],
        [ 0, 0, 0, 0, 1, 1 ],
        [ 0, 0, 0, 0, 1, 1 ],
        [ 0, 0, 0, 0, 1, 9 ],
        [ 1, 2, 1, 1, 1, 1 ],
        [ 9, 2, 9, 1, 0, 0 ]
    ],
    visBoard=[
        [-1,-1,-1,-1,-1,-1 ],
        [-1,-1,-1,-1,-1,-1 ],
        [-1,-1,-1,-1,-1,-1 ],
        [-1,-1,-1,-1,-1,-1 ],
        [-1,-1,-1,-1,-1,-1 ],
        [-1,-1,-1,-1,-1,-1 ]
    ],
    bombs=4
)

def main():
    #playTest(testGame)
    ur = input("num rows: ")
    uc = input("num collumns: ")
    ub = input("num bombs: ")
    playGame(int(ur), int(uc), int(ub))
    
if __name__ == "__main__":
    main()

"""
access 8 surrounding tiles:

if r > 0 and c > 0:
    pass
if r > 0:
    pass
if r > 0 and c < len(self.visBoard[r])-1:
    pass
if c < len(self.visBoard[r])-1:
    pass
if r < len(self.visBoard)-1 and c < len(self.visBoard[r])-1:
    pass
if r < len(self.visBoard)-1:
    pass
if r < len(self.visBoard)-1 and c > 0:
    pass
if c > 0:
    pass

"""