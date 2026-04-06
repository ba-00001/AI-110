# Music Recommender Simulation

## Project Summary

For this show project, I built a small content-based music recommender in Python. My version reads a song catalog from `data/songs.csv`, compares each track to a user taste profile, and ranks the catalog based on how well the song matches the user's genre, mood, energy, and acoustic preference. I wanted the system to feel simple enough to explain clearly while still showing how a real recommender turns features into a score.

<img src="https://github.com/user-attachments/assets/9a7225aa-02d7-4135-8a9b-6f137146c735" alt="screenshot 1" width="600" />

---

## How The System Works

I modeled each song with features that are easy to reason about:

- `genre`
- `mood`
- `energy`
- `valence`
- `danceability`
- `acousticness`

The user profile stores the kind of listening session the user wants right now:

- favorite genre
- favorite mood
- target energy
- whether the user wants something more acoustic or less acoustic

The scoring rule is weighted instead of being all-or-nothing:

- exact genre matches get the biggest bonus
- related genres like `pop` and `indie pop` get a smaller bonus
- exact mood matches add another strong bonus
- energy gets a similarity score based on how close the song is to the user's target
- valence and danceability add smaller mood-shaping bonuses
- acoustic preference adds a final bonus when the song fits that vibe

After every song gets a score, the recommender sorts the songs from highest to lowest and returns the top `k` results with a short explanation of why each song ranked well.

---

## Getting Started

### Setup

1. Create a virtual environment if you want one:

```bash
python -m venv .venv
```

2. Activate it on Windows:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
python -m src.main
```

### Running Tests

```bash
pytest
```

---

## Experiments I Tried

I tested the recommender with a few different user profiles to see whether the ranking changed in ways that made sense:

- A `pop + happy + high energy` user profile pushed `Sunrise City` and `Rooftop Lights` near the top.
- A `lofi + chill + low energy + likes acoustic` profile strongly favored `Library Rain` and `Midnight Coding`.
- When I reduced the importance of genre in my reasoning and paid more attention to energy, songs from adjacent genres started surfacing more often, which made the results feel a little more diverse but also less exact.

The most useful change I kept was adding a smaller partial match for related genres. That helped `indie pop` still feel relevant for someone who picked `pop`.

---

## Limitations and Risks

This system still has clear limits:

- It only works on a catalog of 10 songs, so the recommendations are narrow.
- It cannot understand lyrics, context, nostalgia, or evolving taste.
- It assumes one profile captures the user's taste in the moment, even though real listeners often want a mix of vibes.
- The dataset is small and uneven, so some moods and genres are represented better than others.

That means the recommender is explainable, but it is not complete or fair enough for real product use.

---

## Reflection

Building this made recommendation systems feel more concrete to me. A recommender does not need to be mysterious to feel personalized. Even a small weighted recipe can produce results that seem thoughtful as long as the features line up with what the user cares about.

What stood out most was how fast bias can creep in. If I over-reward genre, the system becomes repetitive. If I under-reward it, the results drift and stop feeling intentional. That balance made me think more carefully about how real apps shape taste, not just reflect it.

[**Model Card**](model_card.md)
