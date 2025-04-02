import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0
df = pd.read_csv("noHealthCommunityNotes.tsv", sep="\t", low_memory=False)

def englishCheck(text):
    if not isinstance(text, str): 
        return False
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False

df['english'] = df['summary'].apply(englishCheck)
englishDf = df[df['english']].drop(columns=["english"])

# Save English-only data to a new file
englishDf.to_csv("communityNotesFinalNoHealth.tsv", sep="\t", index=False)