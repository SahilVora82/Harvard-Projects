import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # If no links are in the current page, just do everything in the corpus
    if not corpus[page]:
        return {reference: 1 / len(corpus) for reference in corpus}

    else:  # Consider non-linked pages
        probabilityDictionary = {reference: (1 - damping_factor) / len(corpus) for reference in corpus}

        for reference in corpus[page]:  # Consider linked pages
            probabilityDictionary[reference] += damping_factor / len(corpus[page])

    return probabilityDictionary


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRankings = {link: 0 for link in corpus}
    page = random.choice(list(pageRankings.keys()))  # Start with a random page.

    for i in range(0, n):
        pageRankings[page] += 1
        pageDistribution = transition_model(corpus, page, damping_factor)

        # Deciding the next page.
        pages = list(pageDistribution.keys())
        pageWeightage = [pageDistribution[link] for link in pages]
        page = random.choices(pages, pageWeightage, k=1)[0]

    for link in pageRankings:  # Divide by n in order to produce a sum that equals 1.
        pageRankings[link] = pageRankings[link] / n

    return pageRankings


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pages = list((corpus.keys()))
    oldPageRanking = {reference: 1 / len(pages) for reference in pages}
    newPageRanking = {reference: 1 / len(pages) for reference in pages}

    while True:
        # Assigning new probability values to each reference
        for reference in oldPageRanking:
            newPageRanking[reference] = (1 - damping_factor) / len(oldPageRanking) + damping_factor * iteration(corpus,
                                                                                                                oldPageRanking,
                                                                                                                reference)

        # Check for convergence
        if all(abs(oldPageRanking[page] - newPageRanking[page]) < 0.001 for page in oldPageRanking):
            return newPageRanking

        # Update the oldPageRanking.
        oldPageRanking = {reference: newPageRanking[reference] for reference in newPageRanking}


def iteration(corpus, oldPageRanking, reference):
    """
    Used to calculate the total sum, PR(i) / NumLinks(i)
    """

    totalSum = 0

    for page in corpus:
        links = corpus[page]
        if len(links) == 0:
            totalSum += oldPageRanking[page] / len(corpus)
        elif reference in links:
            totalSum += oldPageRanking[page] / len(links)

    return totalSum


if __name__ == "__main__":
    main()
