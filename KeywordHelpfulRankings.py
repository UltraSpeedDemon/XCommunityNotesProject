#################################################
## LISTING MOST HELPING AND UNHELPFUL KEYWORDS ##
#################################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Read your data
df = pd.read_csv("communityNotesFinalWithRatings.tsv", sep="\t", low_memory=False)

# This array was generated using AI
generalHealthTerms = [
    "cancer", "covid", "diabetes", "heart", "brain", "vaccine", "obesity", "mental", "stroke", "alzheimer",
    "hypertension", "infection", "immunity", "therapy", "surgery", "arthritis", "asthma", "flu", "epidemic", "pandemic",
    "malaria", "tuberculosis", "cholesterol", "neuro", "wellness", "nutrition", "exercise", "hormone", "blood", "sugar",
    "anemia", "anxiety", "depression", "migraine", "pneumonia", "allergy", "eczema", "psoriasis", "autoimmune", "fibromyalgia",
    "sepsis", "hepatitis", "cirrhosis", "kidney", "renal", "liver", "insulin", "endocrine", "thyroid", "cardiac",
    "arrhythmia", "myocardial", "coronary", "sclerosis", "osteoporosis", "fracture", "bone", "dementia", "parkinson", "multiple sclerosis",
    "sleep", "chronic", "pain", "inflammation", "bacteria", "virus", "antibiotic", "immunotherapy", "chemotherapy", "radiation",
    "biopsy", "diagnosis", "prognosis", "rehabilitation", "psychotherapy", "counseling", "diet", "calorie", "cardio",
    "sedentary", "lifestyle", "smoking", "alcohol", "substance", "abuse", "anaphylaxis", "immune", "cell", "genetic",
    "mutation", "gene", "protein", "molecule", "seizure", "epilepsy", "dermatology", "oncology", "urology", "gynecology"
]

# Get which rows are helpful and unhelpful
helpfulnessLevel = ['HELPFUL', 'SOMEWHAT_HELPFUL']
unhelpfulnessLevel = ['NOT_HELPFUL']

helpfulNotes = df[df['helpfulnessLevel'].isin(helpfulnessLevel)]
unhelpfulNotes = df[df['helpfulnessLevel'].isin(unhelpfulnessLevel)]

helpfulCounts = {term: 0 for term in generalHealthTerms}
unhelpfulCounts = {term: 0 for term in generalHealthTerms}

helpfulSummaries = helpfulNotes['summary'].dropna().str.lower().tolist()
unhelpfulSummaries = unhelpfulNotes['summary'].dropna().str.lower().tolist()

# Count occurrences in helpful summaries
for text in helpfulSummaries:
    for term in generalHealthTerms:
        if term in text:
            helpfulCounts[term] += 1

# Count occurrences in unhelpful summaries
for text in unhelpfulSummaries:
    for term in generalHealthTerms:
        if term in text:
            unhelpfulCounts[term] += 1

helpfulTotal = len(helpfulSummaries)
unhelpfulTotal = len(unhelpfulSummaries)

results = []
for term in generalHealthTerms:
    helpfulCount = helpfulCounts[term]
    unhelpfulCount = unhelpfulCounts[term]
    hPct = (helpfulCount / helpfulTotal * 100) if helpfulTotal else 0
    uPct = (unhelpfulCount / unhelpfulTotal * 100) if unhelpfulTotal else 0
    results.append({
        'term': term,
        'helpfulCount': helpfulCount,
        'unhelpfulCount': unhelpfulCount,
        'helpfulPct': round(hPct, 2),
        'unhelpfulPct': round(uPct, 2)
    })

results_df = pd.DataFrame(results)

# Sort by helpfulCount descending and keep the top 10
results_df = results_df.sort_values(by='helpfulCount', ascending=False)
top_10 = results_df.head(10)

print("\nTop 10 Health Terms by Helpful Count:")
print(top_10.to_string(index=False))

############################################################################
# PIE CHART (top 10 terms by helpfulCount) showing exact occurrences & pct
############################################################################

def make_autopct(values):
    """
    Returns a function that formats each pie wedge with:
      - The percentage to 1 decimal place
      - The raw count in parentheses
    """
    def my_autopct(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f"{pct:.1f}%\n({count})"
    return my_autopct

plt.figure(figsize=(8, 8))
plt.pie(
    top_10['helpfulCount'],
    labels=top_10['term'],
    autopct=make_autopct(top_10['helpfulCount']),
    startangle=140
)
plt.title("Top 10 Health Terms by Helpful Count")
plt.tight_layout()
plt.show()
