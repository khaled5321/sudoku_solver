    #* This code is written using norvig soduko solver http://norvig.com/sudoku.html
def cross(A, B):
    "cross product AXB"
    return [a+b for a in A for b in B]


digits = "123456789"
rows = "ABCDEFGHI"
columns = digits
squares = cross(rows, columns)
#columns - rows - squares
unitlist = ([cross(rows, col) for col in columns] +
            [cross(row, columns) for row in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
             for cs in ('123', '456', '789')]
            )
units = dict((square, [unit for unit in unitlist if square in unit])
             for square in squares)
peers = dict(
    (square, set(sum(units[square], []))-set([square]))for square in squares)

#!likely to change


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [char for char in grid if char in digits or char in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    # To start, every square can be any digit; then assign values from the grid.
    values = dict((square, digits) for square in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            #!likely to change
            return False  # (Fail if we can't assign d to square s.)
    return values


def assign(values, square, digit):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[square].replace(digit, '')
    if all(eliminate(values, square, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    for unit in units[s]:
        dplaces = [s for s in unit if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


# def display(values):
#     "Display these values as a 2-D grid."
#     width = 1+max(len(values[s]) for s in squares)
#     line = '+'.join(['-'*(width*3)]*3)
#     for r in rows:
#         print (''.join(values[r+c].center(width)+('' if c in '36' else '')
#                       for c in columns))
#         if r in 'CF':
#             print(line)


def solve(grid): 
    return search(parse_grid(grid))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares): 
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) 
		for d in values[s])

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


def solved(puzzle):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    values = dict(zip(squares,puzzle))
    def unitsolved(unit): 
        return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

#!input
puzzle = '145327698839654127672918543496185372210073956753296481367542819984761235521839764'

if(solved(puzzle)):
    print("the puzzle is already solved")
else:
    sol_dic=solve(puzzle)
    solution=''.join(x for _ , x in sol_dic.items())
    print(solution)
