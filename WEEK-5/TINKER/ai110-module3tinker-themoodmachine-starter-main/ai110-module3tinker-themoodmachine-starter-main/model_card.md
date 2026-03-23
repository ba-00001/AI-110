# Model Card: Mood Machine

This project compares two versions of a mood classifier:

1. A rule based model in `mood_analyzer.py`
2. A machine learning model in `ml_experiments.py`

## 1. Model Overview

**Model type:**  
I compared both models, but the main system I designed was the rule based model.

**Intended purpose:**  
The model classifies short posts as `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**  
The rule based model tokenizes text, looks for positive and negative signals, flips sentiment after simple negation words, gives extra weight after contrast words like `but`, and then maps the score to a mood label. The ML model uses bag-of-words features from `CountVectorizer` and trains a logistic regression classifier on the labeled examples in `dataset.py`.

## 2. Data

**Dataset description:**  
The dataset contains 14 short posts in `SAMPLE_POSTS`. I started from the 6 starter examples and added 8 more examples with slang, sarcasm, emoticons, and mixed emotions.

**Labeling process:**  
I labeled each post based on the overall tone I thought a human reader would most likely infer. Some examples were intentionally ambiguous, especially posts mixing pride with stress or calm wording with a negative detail.

**Important characteristics of the dataset:**  

- Contains slang such as `lowkey`, `no cap`, `sick`
- Contains sarcasm like `I absolutely love getting stuck in traffic`
- Includes mixed-emotion posts
- Includes short posts and informal online phrasing

**Possible issues with the dataset:**  

- The dataset is very small
- Several labels are subjective
- Some words like `fine` or `lol` can change meaning depending on context
- The examples mostly reflect a narrow style of English-language social posts

## 3. How the Rule Based Model Works

**Scoring rules:**  

- Positive words add points and negative words subtract points
- Strong words like `love` and `terrible` have heavier weights
- Negation words like `not` flip the next sentiment token
- Contrast words like `but` boost the sentiment that follows
- Emoticons such as `:)` count as a small positive signal
- If both positive and negative evidence appear together, the model can return `mixed`

**Strengths of this approach:**  

- Easy to debug and explain
- Works well on obvious examples
- Handles some negation and mixed signals better than the starter version

**Weaknesses of this approach:**  

- Sarcasm is still hard
- Tone can depend on context the model never sees
- Slang meaning changes quickly and is easy to misread

## 4. How the ML Model Works

**Features used:**  
Bag-of-words features using `CountVectorizer`.

**Training data:**  
The model trains directly on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**  
When I added more labeled examples, the ML model had more vocabulary coverage, but because the dataset is tiny, small label changes can noticeably shift predictions.

**Strengths and weaknesses:**  
The ML model can learn patterns without me hand-coding every rule, but it also overfits easily because it is trained and evaluated on the same small dataset.

## 5. Evaluation

**How I evaluated the model:**  
I ran `python main.py` for the rule based system and `python ml_experiments.py` for the ML system. Both were evaluated on the labeled examples in `dataset.py`.

**Examples of correct predictions:**  

- `Today was a terrible day` is correctly labeled `negative` because `terrible` is a strong negative word.
- `That sunset was beautiful` is correctly labeled `positive` because `beautiful` is treated as a strong positive signal.
- `Feeling tired but kind of hopeful` is correctly labeled `mixed` because it contains both negative and positive evidence.

**Examples of incorrect predictions or fragile predictions:**  

- `I absolutely love getting stuck in traffic` may still lean too positive or rely too heavily on the negative word `traffic`, showing that sarcasm is not truly understood.
- `Missed the bus lol` is hard because `lol` can soften frustration, but it does not necessarily make the message positive.
- `I am fine :) just exhausted` contains a positive emoticon and a negative emotion, so the label depends heavily on the hand-tuned balance between them.

## 6. Limitations

- The dataset is small and not representative
- The rule based model only sees local word cues
- The ML model is evaluated on training data, so its reported performance is optimistic
- Neither model truly understands context, intent, or speaker background

## 7. Ethical Considerations

Mood detection can be misleading in real settings. A system like this could misread distress, sarcasm, cultural slang, or emotional masking. If it were used on real personal messages, it would raise privacy concerns and could unfairly misinterpret certain communities or dialects.

## 8. Ideas for Improvement

- Add more labeled examples from a wider range of language styles
- Create a held-out test set instead of evaluating only on training data
- Improve emoji and slang normalization
- Add stronger sarcasm heuristics for patterns like positive words followed by clearly negative situations
- Compare against TF-IDF or a small transformer model
