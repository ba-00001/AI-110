# Model Card: Applied AI Music Intelligence System

## Model Name

`Applied AI Music Intelligence System`

## Base Project

This project is an extension of my original Module 3 project, `ai110-module3show-musicrecommendersimulation-starter-main`. That earlier system recommended songs using a weighted content-based scoring formula across genre, mood, energy, valence, danceability, and acousticness. The Week 8 version keeps that reasoning core but adds retrieval, confidence estimation, logging, and evaluation.

## Intended Use

This system is designed for classroom demonstration and portfolio use. Its purpose is to show how an applied AI system can combine retrieval, reasoning, guardrails, and testing to make recommendations in a transparent way. It is not intended for commercial music streaming or high-stakes personalization.

## System Components

- `data/songs.csv`: the structured music catalog
- `data/listening_guides.json`: the small retrieval knowledge base
- `src/retrieval.py`: validation, normalization, and context retrieval
- `src/recommender.py`: weighted scoring logic from the original project
- `src/system.py`: end-to-end orchestration, confidence scoring, and logging
- `src/evaluation.py`: reliability test harness

## How It Works

1. The system receives user preferences for genre, mood, energy, and acoustic preference.
2. Guardrails normalize the request and add warnings when values are unsupported.
3. Retrieval selects candidate songs from the catalog and guidance snippets from the knowledge base.
4. The recommender scores the retrieved candidates and generates an explanation.
5. The system estimates confidence and logs the run for later review.

## Reliability Summary

The included evaluation harness runs 3 predefined scenarios:

- happy pop drive
- quiet study session
- focused coding block

Current results:

- `3 of 3` cases passed
- average confidence: `0.88`

The system performed best when the requested genre and mood existed directly in the dataset. Out-of-scope requests were still handled safely, but confidence dropped because the evidence was weaker.

## Strengths

- The retrieval and scoring pipeline is transparent and easy to explain.
- The model does not hide uncertainty; it exposes confidence and warnings.
- The code is modular enough that each stage can be tested separately.
- The project is lightweight and reproducible because it only uses Python standard library features plus `pytest`.

## Limitations and Biases

- The catalog only contains 10 songs, so the system is narrow and not representative of real music diversity.
- The knowledge base reflects my own assumptions about genres and moods, which can bias how the model explains recommendations.
- Confidence is heuristic rather than statistically calibrated.
- Unknown genres are forced into fallback behavior, which can make outputs look plausible without being truly personalized.

## Misuse Risks and Mitigation

Possible misuse:

- A user could overtrust the recommendations because the explanations sound polished.
- Someone could interpret the confidence score as a guarantee instead of a heuristic.

Mitigation:

- The README and output warnings state that this is a classroom-scale system.
- Confidence is shown alongside warnings, not by itself.
- Guardrails explicitly flag out-of-scope requests.

## Testing Reflection

The biggest surprise was how much reliability improved once I separated retrieval from scoring. The system became more consistent because the scorer worked on a smaller, more relevant candidate set. I also learned that fallback behavior matters a lot: even when the model cannot answer perfectly, it should still fail safely and explain why confidence is lower.

## Collaboration With AI

Helpful AI suggestion:

- AI helped me break the final project into clear modules instead of stuffing all the logic into one file. That made the system easier to document and test.

Flawed AI suggestion:

- One AI suggestion leaned toward making the system sound more advanced than it really was, almost like a large-scale recommender. I corrected that by keeping the claims honest, using a tiny local knowledge base, and clearly labeling confidence as heuristic.

## What This Project Taught Me

This project taught me that responsible AI engineering is mostly about the layer around the model: how we validate inputs, retrieve evidence, surface uncertainty, and test behavior. A simple model can still become a strong portfolio artifact when the whole system is designed thoughtfully.
