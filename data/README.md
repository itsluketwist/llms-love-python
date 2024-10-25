# **data**

The data records used in the project and results produced.

## *contents*

- `output/` - json files containing the results from running the main code.
- `problem_texts/` - natural language coding problems used to run experiments on the models.
    - `mbpp_text.json` (964 records) - the `text` data from the MBPP dataset (18 Oct 24).
    - `mbpp_text_nopy.json` (964 records) - the `text` data from the MBPP dataset (18 Oct 24) with references to python removed.
    - `conala_rewritten_intent.json` (2879 records) - the `rewritten_intent` text data from the train and test CoNaLa dataset (18 Oct 24).
    - `conala_rewritten_intent_nopy.json` (2682 records) - only `rewritten_intent` text data that does not contain the word python, from the train and test CoNaLa dataset (18 Oct 24).

## *references*

[Mostly Basic Python Problems (MBPP)](https://huggingface.co/datasets/google-research-datasets/mbpp?row=12) - J. Austin, A. Odena, et al., ‘Program Synthesis with Large Language Models’, Aug. 16, 2021, arXiv: arXiv:2108.07732. doi: 10.48550/arXiv.2108.07732.

[CoNaLa (Coding in Natural Language)](https://huggingface.co/datasets/neulab/conala) - P. Yin, B. Deng, E. Chen, B. Vasilescu, and G. Neubig, ‘Learning to Mine Aligned Code and Natural Language Pairs from Stack Overflow’, May 23, 2018, arXiv: arXiv:1805.08949. doi: 10.48550/arXiv.1805.08949.
