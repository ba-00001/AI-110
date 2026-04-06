# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch Classroom Edition**

---

## 2. Intended Use

This model recommends a small set of songs from a classroom dataset based on the user's preferred genre, mood, energy level, and acoustic preference. It is designed for learning and experimentation, not for real consumer use.

The system assumes that a user can describe their current listening goal with a few structured preferences. That simplification makes the model easy to inspect, but it also leaves out a lot of what real music taste looks like.

---

## 3. How the Model Works

My recommender is a content-based scoring system. Each song has features like genre, mood, energy, valence, danceability, and acousticness. The user profile includes a favorite genre, a favorite mood, a target energy level, and whether the user wants an acoustic-leaning sound.

The model gives the largest bonus to exact genre matches and a smaller bonus to related genres such as `pop` and `indie pop`. It also rewards exact mood matches, then adds similarity points for energy, valence, and danceability. Acousticness adds a final bonus when it lines up with the user's preference. After that, all songs are sorted by total score and the top results are returned with a short explanation.

---

## 4. Data

The dataset contains 10 songs in `data/songs.csv`. The catalog includes genres such as pop, lofi, rock, ambient, jazz, synthwave, and indie pop, along with moods like happy, chill, intense, relaxed, focused, and moody.

I did not add or remove songs from the starter dataset. Because the dataset is so small, it reflects a narrow slice of taste and does not represent the variety of languages, cultures, eras, or listening contexts that real users bring to music platforms.

---

## 5. Strengths

This recommender works best when the user has a clear mood and energy target. The top results usually feel reasonable for profiles like `happy pop workout`, `quiet chill study`, or `relaxed acoustic`. The scoring is also easy to explain, which makes it useful for learning because I can point to each bonus and understand why a song ranked where it did.

Another strength is that related genres can still surface. That makes the output a little less rigid than exact matching alone.

---

## 6. Limitations and Bias

The model ignores many real signals such as lyrics, language, artist familiarity, recency, and listening history. It also treats musical taste as a static snapshot instead of something layered and changing.

Bias can show up because the dataset is tiny and the scoring recipe reflects my own assumptions. For example, if I give genre too much weight, the recommender becomes repetitive and may hide songs that fit the mood well. If I reduce genre too much, it may over-promote adjacent genres and lose the user's intended style. Since some genres appear more often than others, those categories are naturally easier for the model to recommend.

---

## 7. Evaluation

I checked the system in two ways. First, I ran the included pytest suite to verify that the basic ranking and explanation behavior worked. Second, I tried several manual user profiles:

- `pop + happy + 0.8 energy + non-acoustic`
- `lofi + chill + 0.4 energy + acoustic`
- `rock + intense + 0.9 energy + non-acoustic`

The results generally matched my expectations. The biggest surprise was how helpful related-genre matching felt for profiles like `pop`, where `indie pop` still seemed like a good answer.

---

## 8. Future Work

If I kept building this, I would:

- add more songs and a more balanced catalog
- support multiple simultaneous preferences instead of one favorite mood and genre
- add diversity rules so the top 5 does not cluster too tightly
- improve explanations so they sound more natural to a user

---

## 9. Personal Reflection

This project helped me see how recommenders turn messy taste into structured numbers. Even a small scoring system can feel surprisingly personal, which made me think more carefully about how much trust people place in recommendation apps.

It also reminded me that human judgment still matters. A model can rank songs, but a person has to decide whether the feature choices, weights, and tradeoffs actually represent the experience they want to create.
