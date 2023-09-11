from flask import Flask, render_template, request, jsonify

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
    sudoku_board[p//side][p%side] = None

@app.route('/')
def index():
    return render_template('index.html', board=sudoku_board)

#@app.route('/solve', methods=['POST'])
#def solve():
    # Get the Sudoku board from the frontend
    board = request.json['board']

    # Call the Sudoku solver function (implement this)
    solved_board = sudoku_solver.solve(board)

    return jsonify({'solved_board': solved_board})

if __name__ == '__main__':
    app.run(debug=True)
