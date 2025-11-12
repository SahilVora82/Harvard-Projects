import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# I made the NONTERMINALS by going through each .txt file and seeing what is the simplest, most general statement I can add
NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP 

NP -> N | Adj NP | Det NP | NP PP | Det Adj N | Adj N

VP -> V | VP NP | VP PP | Adv VP | VP Adv

PP -> P NP 

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence.lower()) # List of lowercase words in sentence

    # Counts the word if any of the characters is a letter. It's not applicable in this case,
    # but it means that words with an apostrophe would still be included
    return [word for word in words if any(char.isalpha() for char in word)]

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NP_chunks = []
    subtrees = list(tree.subtrees())

    for subtree in subtrees:
        sub_subtree = list(subtree.subtrees())

        # Remove the first index, which is the same as the local "subtree" variable. We should only check its children
        sub_subtree.pop(0)

        # Topmost label must be a NP, but the rest of the children should not be
        if subtree.label() == "NP" and not any(child.label() =="NP" for child in sub_subtree):
            NP_chunks.append(subtree)

    return NP_chunks


if __name__ == "__main__":
    main()
