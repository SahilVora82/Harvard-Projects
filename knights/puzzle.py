from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

AStatementKnight = Symbol("A said 'I am a knight'") # used in puzzle 3
AStatementKnave = Symbol("A said 'I am a knave'")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A has to be a Knight or a Knave, but can't be both
    Biconditional(AKnight,Not(AKnave)),
    # If A is a Knight, his statement is true
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a Knave, his statement is false
    Implication(AKnave, Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # A has to be a Knight or a Knave, but can't be both
    Biconditional(AKnight,Not(AKnave)),

    # B has to be a Knight or a Knave, but can't be both
    Biconditional(BKnight,Not(BKnave)),

    # If A is a Knight, his statement is true
    Implication(AKnight, And(AKnave, BKnave)),

    #If A is a knave, his statement is false
    Implication(AKnave,Not(And(AKnave, BKnave))),

    # No statements to consider for B.
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A has to be a Knight or a Knave, but can't be both
    Biconditional(AKnight,Not(AKnave)),

    # B has to be a Knight or a Knave, but can't be both
    Biconditional(BKnight,Not(BKnave)),

    # If A is a knight, then A and B are the same kind. His statement is true
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # If A is a knave, then A and B are not the same kind. His statement is false
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight,BKnight)))),

    # If B is a Knight, his statement is true -- they are of different kinds
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    # If B is a Knave, his statement is false -- they are of the same kind
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(

    # A has to be a Knight or a Knave, but can't be both
    Biconditional(AKnight,Not(AKnave)),

    # B has to be a Knight or a Knave, but can't be both
    Biconditional(BKnight,Not(BKnave)),

    # C has to be a Knight or a Knave, but can't be both
    Biconditional(CKnight,Not(CKnave)),

    # A's Statement -- if Knight, he's either a knight or knave. But if he's a knave, then he's neither a knight of knave
    # (this means A must be a Knight)
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # Solution can actually be found without B's first Statement

    # B's second statement. If B is a knight, the statement is true and C is a knave.
    Implication(BKnight, CKnave),

    # And if B is a knave, C is not a knave; statement is false.
    Implication(BKnave, Not(CKnave)),

    # C's statement. If knight, A must be a knight. C's statement must be true.
    Implication(CKnight, AKnight),

    # And if C is a knave, A must not be a knight. C's statement is false.
    Implication(CKnave, Not(AKnight)),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
