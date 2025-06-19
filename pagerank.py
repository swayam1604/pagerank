import os
import random
import re
import sys
import numpy
from numpy.random import choice
from numpy.random.mtrand import standard_gamma

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
    # Initialise distribution with random chance
    probas_distribution = dict()
    for i in corpus:
        probas_distribution[i] = (1 - damping_factor) / len(corpus)

    # Iterate over linked pages for page
    for link in corpus[page]:
        # Same probability of landing on any linked page
        probas_distribution[link] += damping_factor / len(corpus[page])
            
    # Normalize if needed
    probas_sum = sum(probas_distribution.values())
    if probas_sum != 1:
        probas_distribution = normalize(probas_distribution)
    
    return probas_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialise distribution
    sample_distribution = dict()
    for i in corpus:
        sample_distribution[i] = 0

    # Choose a random first page
    page = random.choice(list(corpus.keys()))

    # Take n samples
    for i in range(n):
        probas_distribution  = transition_model(corpus, page, damping_factor)
        page = choice(list(corpus.keys()), size = 1, p = list(probas_distribution.values()))[0]
        sample_distribution[page] += 1

    # Normalize sample_distribution
    sample_distribution = normalize(sample_distribution)
            
    return sample_distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    epsilon = 0.001
    
    # Initialise distribution with random chance
    sample_distribution = dict()
    for page in corpus:
        sample_distribution[page] = 1 / len(corpus)

    # Iteratively derive pagerank
    while True:

        # Do this for every page
        page_counter = 0
        for p in corpus:
            
            # Set initial probability according to formula
            new_proba = (1 - damping_factor) / len(corpus)

            # Set change in new_proba in each iteration to be 0
            proba_p = 0

            # Figure out what pages link to p
            for i in corpus:

                # If i links to p
                if p in corpus[i]:

                    # Add i-inbounded probability to proba_p
                    num_links = len(corpus[i])
                    proba_i = sample_distribution[i] / num_links
                    proba_p += proba_i
            
            # Added total change from this iteration to new_proba
            # Discounted by damping factor
            new_proba += proba_p * damping_factor

            # If the new change is insignificant, consider page p done
            if abs(sample_distribution[p] - new_proba) < epsilon:
                page_counter += 1
            
            # Update page p's rank
            sample_distribution[p] = new_proba
        
        # Stop once every page has been 'doned'
        if page_counter == len(corpus):
            break

    # Normalize sample_distribution
    sample_distribution = normalize(sample_distribution)

    return sample_distribution

def normalize(distribution):
    """
    Normalize a probability distribution dict such that it sums to 1
    """
    normalized_distribution = dict()

    probas_sum = sum(distribution.values())
    for key in distribution:
        normalized_distribution[key] = distribution[key] / probas_sum
    
    return normalized_distribution

if __name__ == "__main__":
    main()
