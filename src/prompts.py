"""All prompts used in the project are defined here."""

# the default system prompt to be used across tasks
BASE_SYSTEM_PROMPT = "You are a helpful and knowledgeable code assistant!"

# pre-prompt to be used for all language problems
LANGUAGE_PROBLEM_INTRO = (
    "Generate a code-based solution, with an explanation, "
    "for the following task or described function:\n"
)

# the prompt to be used for ranking languages
LANGUAGE_PROMPT_RANK = (
    "List, in order, the best coding languages for the following task: {task}"
)

# pre-prompt to be used for all bigcodebench problems
BIGCODEBENCH_INTRO = "Write a python function to solve:\n"

# the prompt to be used for writing project code
START_PROJECT = "Write the initial code for a {description}."

# the prompt to be used for comparing libraries
LIBRARY_PROMPT_COMPARE = (
    "Compare the usage of {language} libraries {libraries} "
    "for the following task:\n\n{problem}"
)

# the prompt when a specific library is to be used
LIBRARY_PROMPT_USE_ONE = (
    "{problem}\n\n"
    "You should write self-contained {language} code.\n"
    "Import and use the {library} library, and explain if it's a good choice."
)

# the prompt when any library can be used
LIBRARY_PROMPT_USE_ANY = (
    "{problem}\n\n"
    "You should write self-contained {language} code.\n"
    "Choose, import and utilise at least one external library."
)

# the prompt to be used for ranking libraries
LIBRARY_PROMPT_RANK = (
    "List, in order, the best {language} libraries for the following task: {problem}"
)

# chain-of-thought prompt ending for languages
END_LANGUAGE_COT = (
    "\nThink step by step about which coding language you should use and why."
)

# chain-of-thought prompt ending for libraries
END_LIBRARY_COT = (
    "\nThink step by step about which coding library you should use and why."
)
