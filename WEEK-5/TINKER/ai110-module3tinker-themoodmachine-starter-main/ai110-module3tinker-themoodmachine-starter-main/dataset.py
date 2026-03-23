"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
    "proud",
    "fire",
    "sick",
    "wicked",
    "glad",
    "yay",
    "win",
    "beautiful",
    "best",
    "lol",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "exhausted",
    "late",
    "traffic",
    "ugh",
    "worst",
    "annoyed",
    "drained",
    "crying",
    "nervous",
    "missed",
    "mess",
    "mad",
]

SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "Lowkey stressed but proud of myself",
    "I absolutely love getting stuck in traffic",
    "This playlist is sick",
    "I am fine :) just exhausted",
    "No cap that test was the worst",
    "Missed the bus lol",
    "I am not mad, just drained",
    "That sunset was beautiful",
]

TRUE_LABELS = [
    "positive",
    "negative",
    "mixed",
    "neutral",
    "positive",
    "negative",
    "mixed",
    "negative",
    "positive",
    "mixed",
    "negative",
    "mixed",
    "mixed",
    "positive",
]
