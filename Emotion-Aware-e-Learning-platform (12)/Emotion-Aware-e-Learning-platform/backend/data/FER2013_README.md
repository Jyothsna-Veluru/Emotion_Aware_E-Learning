# FER2013 Dataset

This folder is the home for the **FER2013** facial-expression dataset, used as
the research / future-training dataset for this platform.

## Why it's not bundled
FER2013 is ~287 MB and distributed under Kaggle's terms, so it is not committed
to the repository. Download it and place `fer2013.csv` here:

    https://www.kaggle.com/datasets/msambare/fer2013

## Layout once downloaded
    backend/data/
      fer2013.csv          # 35,887 labelled 48x48 grayscale faces
      train/  test/        # (optional) extracted image folders

## How it's used
At runtime the platform does **not** train a CNN — it uses DeepFace's
pretrained emotion model for real-time inference (see `emotion_engine.py`).
FER2013 is included so the project can later fine-tune or benchmark a custom
model offline. The 7 FER2013 labels map onto our 6-label model as:

    angry, disgust -> angry
    fear           -> fear
    happy          -> happy
    sad            -> sad
    surprise       -> surprise
    neutral        -> neutral
