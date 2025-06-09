# Analysis of Illegal Advertisements

This repository contains code and resources for analyzing and detecting illegal advertisements using Retrieval-Augmented Generation (RAG) methods, data crawling, vector databases, and ensemble approaches.

## Project Overview

The goal of this project is to build a system that can analyze text content to identify illegal advertisements. We leverage web scraping to collect candidate texts, construct semantic vector databases, and apply a mixture of AI-driven approaches — ranging from simple prompting to advanced retrieval-augmented generation and ensemble techniques — to improve detection accuracy.

## Repository Structure

```
├── data_crawler.py           # Scripts to crawl and collect advertisement data
├── create_vectordb.py        # Build vector database from crawled data
├── direct_prompt.py          # Baseline method using direct prompting
├── RAG_original_without_laws.py     # RAG implementation without denoising
├── RAG_denoised_without_laws.py     # RAG implementation with heuristic denoising
├── ensemble.py               # Ensemble predictions from multiple methods
├── convert_output_to_reason.py     # Convert raw outputs into human-readable reasoning
├── convert_output_to_submission.py # Format final predictions for submission
├── denoise_history.py        # Utilities for denoising text history
├── requirements.txt          # Python dependencies
├── final_project_query.csv    # Sample queries used for evaluation
├── submission_ensemble.csv    # Final ensemble results
└── README.md                 # This file
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/youchen0620/Analysis-of-Illegal-Advertisements.git
   cd Analysis-of-Illegal-Advertisements
   ```

2. Install dependencies (Python 3.10+):

   ```bash
   pip install -r requirements.txt
   ```

## Data Crawling

Use `data_crawler.py` to fetch and preprocess advertisement texts from target websites. Configure the crawler parameters at the top of the script.

## Vector Database Construction

After crawling, build Chroma DBs with `create_vectordb.py`. This script reads preprocessed data and creates Chroma DBs.

## Modeling Methods

### Baseline: Direct Prompting

Use `direct_prompt.py` to apply a heuristic prompt directly to text without retrieval. This serves as a simple baseline.

### Retrieval-Augmented Generation (RAG)

`RAG_original_without_laws.py` implements a RAG pipeline that retrieves top-k similar documents from the vector database and conditions a language model on the retrieved context.

### Denoised RAG

To improve signal quality, `RAG_denoised_without_laws.py` applies a heuristic-based denoising step on retrieved passages before generation.

### Ensemble Methods

Combine outputs from multiple runs or methods using `ensemble.py`. This can improve robustness and classification performance.

## 

## Scripts and Usage

Below is a typical workflow:

```bash
# 1. Crawl data
python data_crawler.py

# 2. Denoise text histories
python denoise_history.py

# 3. Preprocess and Build vector DB
python create_vectordb.py

# 4. Run baseline
python direct_prompt.py

# 5. Run RAG
python RAG_original_without_laws.py

# 6. Run denoised RAG
python RAG_denoised_without_laws.py

# 7. Convert raw outputs into human-readable reasoning
python convert_output_to_reason.py

# 8. Format predictions for submission
python convert_output_to_submission.py

# 9. Ensemble predictions
python ensemble.py
```
