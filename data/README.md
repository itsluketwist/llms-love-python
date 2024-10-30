# **data**

The data records used in the project and results produced.

## *contents*

- `output/` - json files containing the results from running the main code.
- `problem_texts/` - natural language coding problems from existing datasets, used to run experiments on the models.
    - `aixbench.json` (129 records) - the `raw_nl` data from the Aix-Bench NL task dataset, 2022.
        - *Cuts: problems containing chinese characters have been removed.*
    - `apps_competition.json` (1361 records) - the `question` data from the APPS (train and test) dataset, for problems with `difficulty = competition`, 2021.
    - `apps_interview.json` (4716 records) - the `question` data from the APPS (train and test) dataset, for problems with `difficulty = interview`, 2021.
    - `apps_introductory.json` (2701 records) - the `question` data from the APPS (train and test) dataset, for problems with `difficulty = introductory`, 2021.
    - `bigcodebench.json` (515 records) - the `text` data from the MBPP dataset, 2024.
        - *Edits: the function definition provided at the end of each problem has been removed.*
    - `conala.json` (2255 records) - the `rewritten_intent` data from the CoNaLa (train and test) dataset, 2018.
    - `humaneval.json` (80 records) - the `description` data from the HumanEval-XL english dataset, 2024.
    - `mbpp.json` (964 records) - the `text` data from the MBPP dataset, 2021.
        - *Edits: references to python have been replaced.*
    - `pecc_aoc.json` (200 records) - the `part1_converted` data from the PECC Advent of Code dataset, 2024.
    - `pecc_euler.json` (806 records) - the `title` and `problem` data from the PECC Project Euler dataset, 2024.

*The following datasets had problems that referenced a coding language or library removed: Aix-Bench, APPS, BigCodeBench, CoNaLa.*

## *references*

[Aix-Bench](https://huggingface.co/datasets/xin1997/aixbench-manual_all_only_input) - Y. Hao et al., ‘AixBench: A Code Generation Benchmark Dataset’, Jul. 21, 2022, arXiv: arXiv:2206.13179. doi: 10.48550/arXiv.2206.13179.

[APPS (Automated Programming Progress Standard)](https://huggingface.co/datasets/codeparrot/apps) - D. Hendrycks et al., ‘Measuring Coding Challenge Competence With APPS’, Nov. 08, 2021, arXiv: arXiv:2105.09938. doi: 10.48550/arXiv.2105.09938.

[BigCodeBench](https://huggingface.co/datasets/bigcode/bigcodebench) - T. Y. Zhuo et al., ‘BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions’, Oct. 07, 2024, arXiv: arXiv:2406.15877. doi: 10.48550/arXiv.2406.15877.

[CoNaLa (Coding in Natural Language)](https://huggingface.co/datasets/neulab/conala) - P. Yin, B. Deng, E. Chen, B. Vasilescu, and G. Neubig, ‘Learning to Mine Aligned Code and Natural Language Pairs from Stack Overflow’, May 23, 2018, arXiv: arXiv:1805.08949. doi: 10.48550/arXiv.1805.08949.

[HumanEval-XL](https://huggingface.co/datasets/FloatAI/humaneval-xl) - [1] Q. Peng, Y. Chai, and X. Li, ‘HumanEval-XL: A Multilingual Code Generation Benchmark for Cross-lingual Natural Language Generalization’, in Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), N. Calzolari, M.-Y. Kan, V. Hoste, A. Lenci, S. Sakti, and N. Xue, Eds., Torino, Italia: ELRA and ICCL, May 2024, pp. 8383–8394. Accessed: Oct. 29, 2024. [Online]. Available: https://aclanthology.org/2024.lrec-main.735

[MBPP (Mostly Basic Python Problems)](https://huggingface.co/datasets/google-research-datasets/mbpp) - J. Austin, A. Odena, et al., ‘Program Synthesis with Large Language Models’, Aug. 16, 2021, arXiv: arXiv:2108.07732. doi: 10.48550/arXiv.2108.07732.

[PECC (Problem Extraction and Coding Challenges)](https://huggingface.co/datasets/PatrickHaller/pecc) - [1] P. Haller, J. Golde, and A. Akbik, ‘PECC: Problem Extraction and Coding Challenges’, Apr. 29, 2024, arXiv: arXiv:2404.18766. doi: 10.48550/arXiv.2404.18766.
