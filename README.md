# 🔍 PageRank – Simulating Web Page Importance  
**By Swayam Sharma**

PageRank is my Python-based implementation of the classic **Google PageRank algorithm**, which estimates the relative importance of web pages using link structure. This project explores how a **random surfer model** and **iterative probability distribution** can be used to calculate which web pages are most likely to be visited.

## 💡 What Inspired Me
I've always been curious about how search engines like Google decide *what to show first*. This project gave me the chance to build a simplified version of that magic from scratch — using pure Python logic and a touch of probability theory.

## 📂 About the Project
Given a corpus of HTML pages, this script:
- **Parses all links** between pages
- Simulates a "random surfer" who jumps between links based on a damping factor
- Calculates estimated page ranks using:
  - **Sampling-based model** (`sample_pagerank`)
  - **Iterative model** (`iterate_pagerank`)

The output is a dictionary with page names and their corresponding probabilities, representing the chance that a random surfer is on that page.

## ⚙️ How It Works
Two models are implemented:

### 🎲 Sampling Model
Simulates a user starting from a random page and making `n` transitions using:
- Probability `d` to follow a random outbound link
- Probability `1 - d` to jump to a random page in the corpus

### 🔁 Iterative Model
Calculates PageRank using the recursive formula:
> `PR(p) = (1 - d)/N + d * Σ (PR(i) / NumLinks(i))`

It keeps refining rank values until all ranks converge (difference ≤ 0.001).

## 🗂️ Folder Structure

