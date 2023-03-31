# Whale Animations

First, make sure you have all dependencies installed, there shouldn't be any weird ones (except maybe Librosa, you might need version: 0.8.0, that's what I have).

Dependencies:
- numpy
- matplotlib
- librosa
- soundfile
- scipy.io

Code to generate animation visualizations of the sperm whale data.

## To run:

`generate_conversation_animation_jsons.py` will generate the json files that describe how to make the animations. Then, run `generate_animations.py`, passing in 2 command line arguments saying where the previously generated json files are, and where they should be moved to after generating animations.

Examples:

```
python generate_conversation_animation_jsons.py
```

```
python generate_animations.py conversation_animation_jsons conversation_animation_jsons_done
```

## Code files:
- `whale_animation_functions` contains all of the different animation pieces.
- `create_full_animation.py` combines all the pieces into a single animation and task file for the annotator.

## Other files:
- `coda_metadata.csv` contains info on when clicks happen in the files.
- `wav_file_durations_2014_2015_2016.csv` contains the length of all audio files for use in making animation jsons.
- See annotation directory for instructions on how to host animations on the online annotator.
