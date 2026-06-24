from dataclasses import dataclass
from typing import Literal


@dataclass
class EvalCase:
    user_message: str
    expected_destination: Literal["knowledge_agent", "general_agent"]


eval_cases: list[EvalCase] = [
    EvalCase(
        user_message="O que foi a Guerra Fria?",
        expected_destination="knowledge_agent",
    ),
    EvalCase(
        user_message="Qual foi o papel da OTAN na Guerra Fria?",
        expected_destination="knowledge_agent",
    ),
    EvalCase(
        user_message="Quem foi Nikita Khrushchev?",
        expected_destination="knowledge_agent",
    ),
    EvalCase(
        user_message="O que foi a Cortina de Ferro?",
        expected_destination="knowledge_agent",
    ),
    EvalCase(
        user_message="Me fale sobre a corrida espacial",
        expected_destination="knowledge_agent",
    ),
    EvalCase(
        user_message="Qual a capital da França?",
        expected_destination="general_agent",
    ),
    EvalCase(
        user_message="Me explique o que é machine learning",
        expected_destination="general_agent",
    ),
    EvalCase(
        user_message="Quem escreveu Dom Casmurro?",
        expected_destination="general_agent",
    ),
    EvalCase(
        user_message="Quanto é 2 + 2?",
        expected_destination="general_agent",
    ),
    EvalCase(
        user_message="Como funciona um motor a combustão?",
        expected_destination="general_agent",
    ),
]
