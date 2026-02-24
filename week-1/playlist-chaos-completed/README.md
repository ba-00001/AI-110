# Playlist Chaos

This folder contains a **fully fixed** version of the Playlist Chaos Streamlit app.

## Preview

<img src="https://github.com/user-attachments/assets/9ce0ae14-a7ed-410b-afa5-306cbf3c92ef" alt="Playlist Chaos Preview" width="600" />

## Video Walkthrough

Here is the video walkthrough: [Watch/Download the video](https://github.com/ba-00001/AI-110/blob/main/week-1/playlist-chaos-completed/week1-vid-playlist-chaos-completed.mp4)

I commented the code so it’s clear what I changed and why (and so it’s easier to follow during review, demos, or grading).

## What was fixed (matches the "Intended Behavior" rules)

- **Song classification**
  - Hype / Chill / Mixed logic follows the benchmark rules.
  - Clear precedence to avoid weird edge cases:
    - If the **title contains chill keywords** (lofi/ambient/sleep) → **Chill**
    - Else apply **Hype rules** (energy >= 7, favorite genre match, or hype genre keywords like rock/punk/party)
    - Else apply **Chill-by-energy** (energy <= 3)
    - Else → **Mixed**
- **Search**
  - Case-insensitive **partial match** (`query in value`) — so `"AC"` matches `"AC/DC"`.
- **Lucky Pick**
  - Never crashes on empty playlists.
  - `"hype"` picks only from Hype, `"chill"` only from Chill, `"any"` picks from all playlists.
- **Stats**
  - Total songs uses a **unique** count (deduped by normalized title + normalized artist + energy).
  - Average energy is computed over all unique songs.
  - Hype ratio is `hype_count / total_songs`.
- **Normalization**
  - Title trims whitespace.
  - Artist + genre are normalized to lowercase for consistent comparison.
  - Tags are normalized to a clean list.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Optional: quick sanity checks (no pytest needed)

```bash
python sanity_checks.py
```

## Starter zip included

The original starter repo zip is included **inside this solution zip** at:

`starter/ai110-module1tinker-playlistchaos-starter-main.zip`

---
## Original activity context

Your AI assistant tried to build a smart playlist generator. The app runs, but some of the behavior is unpredictable. Your task is to explore the app, investigate the code, and use an AI assistant to debug and improve it.




