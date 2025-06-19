from pagerank import transition_model, sample_pagerank, iterate_pagerank

# Testing transition_model
test_corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"}
}

test_empty_corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {},
    "3.html": {"2.html"}
}

# Testing transition_model
print(transition_model(test_corpus, "1.html", damping_factor = 0.85))

# Testing sample_pagerank
print(sample_pagerank(test_corpus, damping_factor = 0.85, n = 10000))

# Testing iterate_pagerank
print(iterate_pagerank(test_corpus, damping_factor = 0.85))