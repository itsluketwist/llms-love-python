# **llm-code-discrimination**

This project investigates this discrimination by LLMs towards lesser known coding languages and libraries.

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
    <a href="https://www.llama.com/">
        <img alt="Meta Llama" src="https://img.shields.io/badge/Meta Llama-0467DF?style=for-the-badge&logo=meta&logoColor=white" />
    </a>
</div>

## *about*

Coding language and library choice is weighted more towards current popularity than ever, rather than quality or new features, because of the vast adoption of LLMs and the way they produce code.
It's becoming impossible for less well-adopted open-source languages and libraries to gain traction in the ecosystem and build their userbase.



## *structure*

Core modules and files included in the repository:

- `data/` - Contains the data records used in the project and results produced, has it's own [README.md](data/README.md).
- `src/` - The main project code, accessing LLM model APIs and analysing the results.
- `run.ipynb` - Simple python notebook used to run the project code.

## *installation*

Clone the repository code:

```shell
git clone https://github.com/itsluketwist/llm-code-discrimination.git
```

Once cloned, install the requirements locally in a virtual environment:

```shell
python -m venv .venv

. .venv/bin/activate

pip install -r requirements.lock
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
