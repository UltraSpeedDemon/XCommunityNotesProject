# This class will take 2 tsv files and merge them using a key, and save them to a new file

import pandas as pd

original = pd.read_csv("communityNotesFinalNoRatings.tsv", sep="\t", low_memory=False)
ratings = pd.read_csv("ratings.tsv", sep="\t", low_memory=False)

# merge the 2 files using noteId as the key
mergedRows = pd.merge(original, ratings, on="noteId", how="inner")
mergedRows.to_csv("communityNotesFinalWithRatings.tsv", sep="\t", index=False)
