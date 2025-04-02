import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load data
df = pd.read_csv("communityNotesFinalWithRatings.tsv", sep="\t", low_memory=False)

# define health-related terms to search for in notes
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

# filter for health-related notes
df['summary_lower'] = df['summary'].fillna('').str.lower()
health_mask = df['summary_lower'].apply(lambda text: any(term in text for term in generalHealthTerms))
df_health = df[health_mask].copy()

# create a column for text length
df_health['textLength'] = df_health['summary_lower'].str.len()

# filter to keep only notes between 0 and 1300 characters
df_health = df_health[df_health['textLength'].between(0, 1300, inclusive='both')]

# create subplots with extra vertical space
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 14))
plt.subplots_adjust(hspace=0.4)  # increase vertical spacing

# subplot 1: Frequency Histogram --
ax1.hist(df_health['textLength'], bins=50, color='skyblue', edgecolor='black')
ax1.set_title("Frequency of Health-Related Notes by Text Length")
ax1.set_xlabel("Text Length (characters)")
ax1.set_ylabel("Frequency (Count of Notes)")
ax1.set_xlim(0, 1300)

# helpfulness
helpfulness_map = {"HELPFUL": 1, "SOMEWHAT_HELPFUL": 0.5, "NOT_HELPFUL": 0}
df_health['helpfulnessScore'] = df_health['helpfulnessLevel'].map(helpfulness_map)

# text lengths into 50 bins between 0 and 1300
bins = np.linspace(0, 1300, 51)
df_health['lengthBin'] = pd.cut(df_health['textLength'], bins=bins, include_lowest=True)

avg_helpfulness = df_health.groupby('lengthBin')['helpfulnessScore'].mean()

bin_midpoints = (bins[:-1] + bins[1:]) / 2
ax2.plot(bin_midpoints, avg_helpfulness.values, marker='o', linestyle='-', color='red')
ax2.set_title("Average Helpfulness Score vs. Text Length")
ax2.set_xlabel("Text Length (characters)")
ax2.set_ylabel("Average Helpfulness Score\n(0 = Not Helpful, 1 = Helpful)")
ax2.set_ylim(0, 1)
ax2.grid(True)

plt.show()
