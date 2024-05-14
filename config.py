from enum import Enum

NUMBER_OF_CASES = 3

OPENAI_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4-turbo",
    "gpt-4o",
]


class Group(Enum):
    CONTROL = "control"
    HYPOTHESIS_DRIVEN = "hypothesis_driven"
    RECOMMENDATIONS_DRIVEN = "recommendations_driven"
