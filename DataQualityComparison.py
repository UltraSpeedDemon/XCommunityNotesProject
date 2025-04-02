#############################
## DATA QUALITY COMPARISON ##
#############################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

df = pd.read_csv("communityNotesFinalWithRatings.tsv", sep="\t", low_memory=False)

# get helpfulness distribution
helpfulnessCount = df['helpfulnessLevel'].value_counts()
helpfulnessPercent = df['helpfulnessLevel'].value_counts(normalize=True) * 100

# display reslts

# via console
print("Helpfulness Count:")
print(helpfulnessCount)
print("\nHelpfulness Percentages:")
print(helpfulnessPercent )

# via graph
plt.figure(figsize=(10, 8))
helpfulnessPercent.plot(kind='pie', autopct='%1.1f%%')
plt.title("Health Information Quality on Twitter Community Notes")
plt.ylabel("")
plt.show()