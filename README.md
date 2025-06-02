# clean-corpus

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/clean-corpus/actions)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A data cleaning toolkit for Large Language Model (LLM) pre-training datasets.

## Overview

This repository contains tools and scripts for cleaning and preprocessing text data intended for LLM pre-training. It implements various quality filters and cleaning techniques to ensure high-quality training data.

## Features

### Syntax Quality Checks
- Implementation based on Gopher quality filtering techniques [1]
- Ensures text meets basic syntactic and structural requirements

### PII Protection
- Masks sensitive personal information:
  - Email addresses
  - Phone numbers

### Language Filtering
- Uses Facebook's FastText language identification model [2]
- Removes non-English text segments
- Threshold: Removes text with English probability < 0.65

### Deduplication
- Line-level deduplication
  - Removes lines that appear more than 5 times in the dataset
- Near-duplicate detection [3]
  - Uses Locality Sensitive Hashing (LSH) MinHash
  - Analyzes 3-gram sentences to identify similar content
  - Groups and filters near-duplicate text segments

## Installation

# Coming soon

pip install clean-corpus

## Usage
```python
# Coming soon
from clean_corpus import DataCleaner

cleaner = DataCleaner()
cleaned_data = cleaner.process("path/to/your/data")
```

## Evaluation

We conducted an experiment to demonstrate the effectiveness of our cleaning pipeline by training GPT-2 models on both raw and cleaned datasets:

### Experimental Setup
- Base Model: GPT-2 Small (124M parameters)
- Training Data: [Dataset details to be added]
- Training Duration: [Duration to be added]
- Hardware: [Hardware details to be added]

### Results
| Metric | Raw Data | Cleaned Data | Improvement |
|--------|----------|--------------|-------------|
| Perplexity | TBD | TBD | TBD |
| Training Loss | TBD | TBD | TBD |

[Add visualization/graphs here]

## License

MIT License

Copyright (c) 2024 Mariano Crosetti

See [LICENSE](LICENSE) for full terms.

## References

[1] Rae, J. W., Borgeaud, S., Cai, T., Millican, K., Hoffmann, J., Song, F., ... & Irving, G. (2021). [Scaling Language Models: Methods, Analysis & Insights from Training Gopher](https://arxiv.org/abs/2112.11446). *arXiv preprint arXiv:2112.11446*. 

[2] [FastText Language Identification](https://fasttext.cc/docs/en/language-identification.html) (Facebook AI Research)

[3] [Deduplicate-text-datasets](https://github.com/google-research/deduplicate-text-datasets) (Google Research)