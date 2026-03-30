# Music Recommender Simulation

## Project Overview

For Week 6, I am building a simple music recommender simulation in Python. The goal of this project is to show how a system can take song features and a user's preferences, turn them into scores, and then rank songs as recommendations. This project is a simplified version of how real apps like Spotify, TikTok, or YouTube might suggest content, but mine focuses on a small song dataset and a clear scoring process that I can explain.

## What I Am Learning

In this project, I am practicing how to:

- turn user preferences into structured data
- compare those preferences to song features
- build a weighted scoring system
- rank songs from strongest match to weakest match
- think about limits, bias, and fairness in recommendation systems

<img src="https://github.com/user-attachments/assets/cc4bac2b-2e23-408a-95cb-074c0c9acf59" width="600" />

## Project Instructions

### Phase 1: Understanding the Problem

First, I need to understand how recommendation systems work in real life. I will research how music and video platforms predict what users might like next. I also need to understand the difference between collaborative filtering, which uses patterns from many users, and content-based filtering, which uses the actual features of a song or item.

Then I will look at `data/songs.csv` and decide which song features matter most for my own recommender. I will use that information to describe my system in the `How The System Works` section below.

### Phase 2: Designing the Simulation

In this phase, I will design my own recommender before writing the full code. I will review the starter dataset, add more songs if needed, and decide what the user profile should include. I will also create my own scoring recipe so the system can judge how well each song matches a user.

I also want to think ahead about possible bias. For example, if I give genre too much weight, then my recommender might ignore songs that match the mood and energy really well.

### Phase 3: Implementation

This is the phase where I build the actual recommender in Python. I will use `src/recommender.py` for the main logic. My program needs to:

- load songs from the CSV file
- score each song based on the user's preferences
- rank the songs by score
- return the top recommendations
- explain why each song was recommended

I will run the project from `src/main.py` and make sure the output is clear in the terminal.

### Phase 4: Evaluate and Explain

After the recommender works, I will test it with different user profiles to see if the results feel reasonable. I also need to try at least one experiment, like changing a weight or removing a feature, so I can see how sensitive the system is.

This part matters because it helps me notice patterns, surprises, and bias. I will write about those findings in `model_card.md`.

### Phase 5: Reflection and Model Card

To finish the project, I will complete the model card and reflect on what I learned. I want to explain not only what my recommender does, but also where it struggles. Even a simple system can create unfair patterns or over-focus on certain kinds of songs, so I want to be honest about its limits.

## Starter Files Included

The starter files for Week 6 are already added in this folder.

```text
ai110-module3show-musicrecommendersimulation-starter-main/
|-- data/
|   |-- songs.csv
|-- src/
|   |-- main.py
|   |-- recommender.py
|-- tests/
|   |-- test_recommender.py
|-- model_card.md
|-- README.md
|-- requirements.txt
```

## How to Build and Run the Project

I should open a terminal in this folder:

`WEEK-6/ai110-module3show-musicrecommendersimulation-starter-main/ai110-module3show-musicrecommendersimulation-starter-main`

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

On Mac or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the project

```bash
python -m src.main
```

### 5. Run the tests

```bash
pytest
```

## How The System Works

In my version of this project, the recommender will compare a user's preferences to the features of each song in the dataset. I expect to focus on features like genre, mood, energy, and possibly other values such as danceability or acousticness if I decide to use them. The user profile will store the kind of music the user wants, and the recommender will calculate a score for each song based on how closely it matches that profile. After that, the program will rank the songs and return the top results as recommendations.

I want my recommender to be simple enough to understand clearly, but still realistic enough to show how recommendation systems make decisions. Instead of trying to be perfect, I want it to be explainable so I can see why a song ranked where it did.

## Experiments I Plan to Try

As I work on this project, I want to test how the recommender changes when I adjust the scoring logic. For example, I might:

- increase or decrease the genre weight
- test what happens if mood matters more than energy
- add another feature like danceability
- compare several user profiles with very different tastes

These experiments should help me understand whether my recommender is actually matching songs well or just over-favoring one feature.

## Limitations and Risks

I already know this recommender will have some limitations. The dataset is small, so the recommendations will only be as good as the songs available. The system also does not understand lyrics, context, or changing taste over time. If I rely too heavily on one feature like genre, then the recommendations might become repetitive and narrow instead of feeling diverse or surprising.

Another risk is bias in the data itself. If the dataset contains more songs from one genre or mood, then the system may keep favoring those songs even when the user might like something else.

## Reflection

I will complete [`model_card.md`](model_card.md) as part of this project. In my reflection, I want to write about what I learned from building the recommender, what AI tools helped me with, and where I had to slow down and double-check the logic for myself. I also want to reflect on how even simple scoring systems can start to feel surprisingly personalized, even though they are really just following rules.
