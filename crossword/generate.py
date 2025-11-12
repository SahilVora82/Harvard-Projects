import sys
from os import WCONTINUED

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable in self.crossword.variables:
            wordsToBeRemoved = [domainWord for domainWord in self.domains[variable] if len(domainWord) != variable.length]

            for removeWord in wordsToBeRemoved: # Remove words that don't match the size constraint.
                self.domains[variable].remove(removeWord)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # If there is no overlap, no revision is necessary
        if self.crossword.overlaps[(x,y)] is None:
            return False

        else:
            changeMade = False
            i , j = self.crossword.overlaps[(x,y)]
            xWordsToRemove = []

            for xWord in self.domains[x]:

                if not any(xWord[i] == yWord[j] for yWord in self.domains[y]):
                    changeMade = True
                    xWordsToRemove.append(xWord)

            # Remove values that didn't have at least one match from x's domain
            self.domains[x] -= set(xWordsToRemove)
            return changeMade

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            arcs = [(x,y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]

        i = 0
        # Better not to use .pop() as using .pop() increases runtime substantially
        while i < len(arcs):
            x, y = arcs[i]
            i +=1

            if self.revise(x,y):
                for neighbor in self.crossword.neighbors(x) - {y}:
                    arcs.append((neighbor, x))

                if len(self.domains[x]) == 0: # See if any domains are empty
                    return False
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Checks if all the variables in the crossword have been assigned a word
        return True if set(assignment.keys()) == self.crossword.variables else False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        assignedWords = list(assignment.values())

        # Check for distinct values
        if len(set(assignedWords)) != len(assignedWords):
            return False

        # Every value length is correct
        if not all(len(assignment[wordVariable]) == wordVariable.length for wordVariable in assignment):
            return False

        # No conflicts between neighboring values
        for x in assignment:
            for y in assignment:
                if x == y or self.crossword.overlaps[(x,y)] is None:
                    continue

                i , j= self.crossword.overlaps[(x,y)]
                if assignment[x][i] != assignment[y][j]:
                    return False

        return True




    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        probabilityWords = {word : 0 for word in self.domains[var]}

        # Only check for those that are unassigned
        for neighbor in self.crossword.neighbors(var) - assignment.keys():
            if self.crossword.overlaps[(var, neighbor)] is None:
                continue

            i, j = self.crossword.overlaps[(var,neighbor)]
            for word in probabilityWords:
                for neighboringWord in self.domains[neighbor]:
                    if word[i] != neighboringWord[j]:
                        probabilityWords[word] += 1

        # Sorted words ascendingly
        sortedProbabilityWords = sorted(probabilityWords.items(), key=lambda item: item[1])
        return [word[0] for word in sortedProbabilityWords]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassignedVariables = self.crossword.variables - assignment.keys()
        listVariables = [(variable,len(self.domains[variable]),len(self.crossword.neighbors(variable))) for variable in unassignedVariables]
        # listVariables will look like: [(v1, domains1, neighbors1), (v2, domains2, neighbors2) ...]

        # Lower domain takes precedence over which has the most neighbors
        minOfDomains = min([item[1] for item in listVariables])
        listVariablesSortedDomains  = [item for item in listVariables if item[1] == minOfDomains]

        maxNeighbors = max([item[2] for item in listVariablesSortedDomains])
        listVariablesFullySorted = [item for item in listVariablesSortedDomains if item[2] == maxNeighbors]

        return listVariablesFullySorted[0][0] # Can return one arbitrarily, so if there is more than 1 thing in the list, can return the first one

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        testingVariable = self.select_unassigned_variable(assignment)
        testingWords = self.order_domain_values(testingVariable, assignment)

        for word in testingWords:
            copyOfAssignment = {variable: assignment[variable] for variable in assignment}
            copyOfAssignment[testingVariable] = word # Add new word to the assignment

            if self.consistent(copyOfAssignment):
                nextIteration = self.backtrack(copyOfAssignment)
                if nextIteration is not None:
                    return nextIteration

        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
