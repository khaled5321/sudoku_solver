from sodokusolver import Solver
from flask import Flask, request, render_template

solver=Solver()
#* check if the puzzle is solved then return error message, else solve the puzzle
def solve_puzzle(puzzle):
    if(solver.solved(puzzle)):
        return [puzzle,"the puzzle is already solved"]
    else:
        try:
            sol_dic=solver.solve(puzzle)
            solution=''.join(x for _ , x in sol_dic.items())
            return [solution,"the solution is..."]
        #if puzzle is incorrect
        except Exception as e:
            return [puzzle,"the puzzle is incorrect, you can't repeat numbers in the same unit"]
#----------------------------------------------------------------------------

app = Flask(__name__)
#* the home page route
@app.route('/')
def index():
    return render_template('index.html',message="Please enter a correct puzzle...")

#* the results route, where we will display the solved puzzle
@app.route('/results', methods=['POST'])
def get_puzzle():
    #get the puzzle from the html
    variables = request.form.getlist("variable")
    #replace empty values with zeros
    puzzle=[x if x else "0" for x in variables]
    #check if the board is empty, then return error message to the user, else return the solution
    if all(v == "0" for v in puzzle):
        return render_template('index.html',message="please enter a correct puzzle")
    else:
        solution,message=solve_puzzle((''.join(puzzle)))
        
        return render_template('results.html',message=message,puzzle=list(solution))

app.run(debug=True)


