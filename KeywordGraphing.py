###################################
## GRAPHING INTERESTING KEYWORDS ##
###################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

df = pd.read_csv("communityNotesFinalWithRatings.tsv", sep="\t", low_memory=False)

# create list of spicy healthcare terms to get data for
graphHealthTerms = ['Cancer', 'Covid', 'Diabetes', 'Heart', 'Brain', 'Vaccine', 'Obesity', 'Mental', 'Stroke', 'Alzheimer', 'Hypertension']
termAnalysis = {}

for term in graphHealthTerms:
    # filter rows that only show the keyword
    termRow = df['summary'].str.contains(term, case=False, na=False)
    terms = df[termRow]
    totalNotes = len(terms)

    # get helpfulness
    termHelpfulnessCount = terms['helpfulnessLevel'].value_counts()
    termHelpfulnessPercent = terms['helpfulnessLevel'].value_counts(normalize=True) * 100
    
    termAnalysis[term] = {
        'totalNotes': totalNotes,
        'helpfulnessCount': termHelpfulnessCount,
        'helpfulnessPercentages': termHelpfulnessPercent
    }
    
    # display results
    
    # via console
    print(f"\nTerm: '{term}' (Total Notes: {totalNotes})")
    print("Helpfulness Counts:")
    print(termHelpfulnessCount)
    print("Helpfulness Percentages:")
    print(termHelpfulnessPercent.round(2))
    
    # via graph
    plt.figure(figsize=(10, 8))
    ax = sns.barplot(
        x=termHelpfulnessCount.index,
        y=termHelpfulnessCount.values,
        hue=termHelpfulnessCount.index,
        palette="viridis",
        dodge=False
    )
    
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()

    plt.title(f"Health Information Quality on Twitter Community Notes Containing {term}")
    plt.xlabel("Helpfulness Level")
    plt.ylabel("Count")
    plt.show()