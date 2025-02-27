# **LLMs Love Python**

This repository contains the artifacts and full results for the paper **LMs Love Python: Investigating LLM Preferences for Coding Languages and Libraries**.

<div>
    <!-- badges from : https://shields.io/ -->
    <!-- logos available : https://simpleicons.org/ -->
    <a href="https://creativecommons.org/licenses/by-sa/4.0/">
        <img alt="CC-BY-SA-4.0 License" src="https://img.shields.io/badge/Licence-CC_BY_SA_4.0-yellow?style=for-the-badge&logo=docs&logoColor=white" />
    </a>
    <a href="https://www.python.org/">
        <img alt="Python 3" src="https://img.shields.io/badge/Python_3-blue?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://openai.com/blog/openai-api/">
        <img alt="OpenAI API" src="https://img.shields.io/badge/OpenAI_API-412991?style=for-the-badge&logo=openai&logoColor=white" />
    </a>
    <a href="https://www.anthropic.com/api/">
        <img alt="Anthropic API" src="https://img.shields.io/badge/Claude_API-D97757?style=for-the-badge&logo=claude&logoColor=white" />
    </a>
</div>

## *abstract*

    Programming language and library choices are critical decisions in software development, directly affecting code reliability, security, maintainability, and overall system integrity. Poor or inconsistent choices can lead to increased technical debt, security vulnerabilities, and even catastrophic failures in safety-critical systems.
    As Large Language Models (LLMs) play an increasing role in code generation, it is essential to understand how they make these decisions. However, little is known about their preferences when selecting programming languages and libraries for different coding tasks.

    To fill this gap, this study provides the first in-depth investigation into LLM preferences for coding languages and libraries used when generating code. We assess the preferences of \textit{\textbf{eight}} diverse LLMs by prompting them to complete various coding tasks, including widely-studied benchmarks and the more practical task of generating the initial structural code for new projects (a crucial step that often determines a project’s language or library choices).

    Our findings reveal that models heavily favour \texttt{Python} when solving language-agnostic problems, using it \textit{\textbf{90\%-97\%}} of the time, even in cases were \texttt{Python} is widely-accepted as a poor choice. Moreover, they contradict their own recommendations \textit{\textbf{58\%}} of the time for project initialisation tasks, raising concerns about their reliability in guiding language selection. LLMs exhibit similar bias towards using the most well-established libraries, leading the way to a serious discoverability problem for new open-source projects.

    These results highlight the need for improving LLMs' adaptability to diverse programming contexts and developing mechanisms to mitigate language and library bias.

## *structure*

This repository contains all of the code used for the project, to allow easy reproduction and encourage further investigation into LLMs coding preferences.
It has the following directory structure:

- `data/` - Contains the data used to conduct the experiments, including benchmark datasets. Has it's own [README.md](data/README.md) with detailed information.
- `output/` - The full results for all experiments, and other outputs from running the code.
    - `chain_of_thought/` - Results from the investigation into the use of chain-of-thought prompting.
    - `kendall_tau/` - Statistical analysis of the results.
    - `language_results/benchmark_tasks/` - Results for language preferences of LLMs when solving tasks from benchmarks.
    - `language_results/project_init_tasks/` - Results for language preferences of LLMs when writing initial project code.
    - `library_results/benchmark_tasks` - Results for library preferences of LLMs when solving tasks from benchmarks.
    - `library_results/project_init_tasks` - Results for library preferences of LLMs when writing initial project code.
    - `paper_figures` - Figures used in the paper and the data used to create them.
    - `temperature` - Results from investigation into the influence of changing temperature parameter.
- `src/` - The main project code, accessing LLM model APIs before extracting data and analysing the results.

## *installation*

First clone the repository code:

```shell
git clone **redacted**
```

Once cloned, install the requirements locally in a virtual environment:

```shell
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.lock
```

## *usage*

Once installed, I recommend using the `run.ipynb` notebook to generate your own results.
The notebook is self-contained, and gives the exact code to recreate each experiment.

This repository uses up to 3 different LLM APIs -
[OpenAI](https://platform.openai.com/docs/overview),
[Anthropic](https://www.anthropic.com/api) and
[TogetherAI](https://api.together.xyz/).
The correct API will automatically be used depending on the selected models.

They're not all required, but each API you'd like to use will need it's own access key stored as an environment variable.

```shell
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
export TOGETHER_API_KEY=...
```

## *development*

Install and use `pre-commit` to ensure code is in a good state:

```shell
pre-commit install

pre-commit autoupdate

pre-commit run --all-files
```

Use `uv` for dependency management, first add to `requirements.txt`. Then install `uv` and version lock with:

```shell
pip install uv

uv pip compile requirements.txt -o requirements.lock
```


## *citation*

todo
