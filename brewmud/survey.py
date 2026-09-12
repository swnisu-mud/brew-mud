"""Shared definitions for BrewMUD's anonymous student evaluation."""

from __future__ import annotations


SURVEY_SCALE_MIN = 1
SURVEY_SCALE_MAX = 10
SURVEY_SCALE_LOW_LABEL = "Strongly disagree"
SURVEY_SCALE_HIGH_LABEL = "Strongly agree"
SURVEY_MINIMUM_RESULTS = 5
SURVEY_COMMENT_LIMIT = 2_000

SURVEY_QUESTIONS = (
    "BrewMUD helped me learn the course material.",
    "BrewMUD was more useful to me than a traditional written study guide.",
    "The amount of time required to use BrewMUD felt reasonable.",
    "The amount of reading in BrewMUD felt manageable.",
    "BrewMUD held my attention while I studied.",
    "I usually understood what I was supposed to do next.",
    "The maps and navigation commands were easy to use.",
    "The quests helped me connect ideas rather than memorize isolated facts.",
    "The pop quizzes helped me remember and review material.",
    "I would use a similar game to study future course material.",
)


def validate_ratings(values: object) -> list[int | None]:
    """Validate the ten optional 1–10 responses received from the browser."""
    if not isinstance(values, list) or len(values) != len(SURVEY_QUESTIONS):
        raise ValueError(f"Submit exactly {len(SURVEY_QUESTIONS)} survey ratings.")
    ratings: list[int | None] = []
    for value in values:
        if value is None:
            ratings.append(None)
            continue
        # bool is an int subclass but is not a meaningful rating.
        if type(value) is not int or not SURVEY_SCALE_MIN <= value <= SURVEY_SCALE_MAX:
            raise ValueError("Each survey rating must be 1–10 or left unanswered.")
        ratings.append(value)
    return ratings


def validate_comment(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("The survey comment must be text.")
    comment = value.strip()
    if len(comment) > SURVEY_COMMENT_LIMIT:
        raise ValueError(f"Please keep the survey comment under {SURVEY_COMMENT_LIMIT:,} characters.")
    return comment
