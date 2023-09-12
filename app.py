from flask import Flask, render_template, request, jsonify
import random
from itertools import islice

app = Flask(__name__)

base  = 3
side  = base*base

# pattern for a baseline valid solution
def pattern(r,c): return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers (of valid base pattern)
from random import sample
def shuffle(s): return sample(s,len(s)) 
rBase = range(base) 
rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
nums  = shuffle(range(1,base*base+1))

# produce board using randomized baseline pattern
sudoku_board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

squares = side*side
empties = squares * 3//4
for p in sample(range(squares),empties):
    sudoku_board[p//side][p%side] = 0

def Solve(board):
    side   = len(board)
    base   = int(side**0.5)
    board  = [n for row in board for n in row ]
    blanks = [i for i,n in enumerate(board) if n == 0 ]
    cover  = { (n,p):{*zip([2*side+r, side+c, r//base*base+c//base],[n]*(n and 3))}
                for p in range(side*side) for r,c in [divmod(p,side)] for n in range(side+1) }
    used   = set().union(*(cover[n,p] for p,n in enumerate(board) if n))
    placed = 0
    while placed>=0 and placed<len(blanks):
        pos        = blanks[placed]
        used      -= cover[board[pos],pos]
        board[pos] = next((n for n in range(board[pos]+1,side+1) if not cover[n,pos]&used),0)
        used      |= cover[board[pos],pos]
        placed    += 1 if board[pos] else -1
        if placed == len(blanks):
            solution = [board[r:r+side] for r in range(0,side*side,side)]
            yield solution
            placed -= 1


solved_board = next(Solve(sudoku_board))

while True:
    solved  = [*islice(Solve(sudoku_board),2)]
    if len(solved)==1:break
    diffPos = [(r,c) for r in range(9) for c in range(9)
               if solved[0][r][c] != solved[1][r][c] ] 
    r,c = random.choice(diffPos)
    sudoku_board[r][c] = solved_board[r][c]

print(sudoku_board)
print(solved_board)
flat_solved_board = []
for r in range(9):
    for c in range(9):
        if sudoku_board[r][c] == 0:
            flat_solved_board.append(solved_board[r][c])

@app.route('/')
def index():
    return render_template('index.html', board=sudoku_board)

@app.route('/check', methods=['POST'])
def check():
    # Call the Sudoku solver function (implement this)
    return jsonify({'solved_board': solved_board})

if __name__ == '__main__':
    app.run(debug=True)
