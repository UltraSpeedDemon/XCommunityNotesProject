import pandas as pd
import matplotlib.pyplot as plt

########################################
# STEP 1: LOAD DATA & PREPARE ENGAGEMENT METRIC
########################################
df = pd.read_csv("communityNotesFinalWithRatings.tsv", sep="\t", low_memory=False)

# Convert 'helpful' and 'notHelpful' to numeric values (treating non-numeric as 0)
for col in ['helpful', 'notHelpful']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    else:
        df[col] = 0

# Define engagement as the sum of likes and dislikes
df['engagement'] = df['helpful'] + df['notHelpful']

########################################
# STEP 2: FILTER FOR HEALTH-RELATED NOTES
########################################
generalHealthTerms = [
    "cancer", "covid", "diabetes", "heart", "brain", "vaccine", "obesity", "mental", "stroke", "alzheimer",
    "hypertension", "infection", "immunity", "therapy", "surgery", "arthritis", "asthma", "flu", "epidemic", "pandemic",
    "malaria", "tuberculosis", "cholesterol", "neuro", "wellness", "nutrition", "exercise", "hormone", "blood", "sugar",
    "anemia", "anxiety", "depression", "migraine", "pneumonia", "allergy", "eczema", "psoriasis", "autoimmune", "fibromyalgia",
    "sepsis", "hepatitis", "cirrhosis", "kidney", "renal", "liver", "insulin", "endocrine", "thyroid", "cardiac",
    "arrhythmia", "myocardial", "coronary", "sclerosis", "osteoporosis", "fracture", "bone", "dementia", "parkinson",
    "multiple sclerosis", "sleep", "chronic", "pain", "inflammation", "bacteria", "virus", "antibiotic", "immunotherapy",
    "chemotherapy", "radiation", "biopsy", "diagnosis", "prognosis", "rehabilitation", "psychotherapy", "counseling",
    "diet", "calorie", "cardio", "sedentary", "lifestyle", "smoking", "alcohol", "substance", "abuse", "anaphylaxis",
    "immune", "cell", "genetic", "mutation", "gene", "protein", "molecule", "seizure", "epilepsy", "dermatology",
    "oncology", "urology", "gynecology"
]

# Lowercase the summary text for matching
df['summary_lower'] = df['summary'].fillna('').str.lower()

# Filter rows that mention any health term
health_mask = df['summary_lower'].apply(lambda text: any(term in text for term in generalHealthTerms))
df_health = df[health_mask].copy()

print("Number of health-related rows:", len(df_health))
if len(df_health) == 0:
    print("No health-related notes found. Exiting...")
    exit()

########################################
# STEP 3: AGGREGATE ENGAGEMENT BY HEALTH TERM
########################################
# For each health term, sum the engagement (likes + dislikes)
engagement_by_term = {}
helpful_by_term = {}
notHelpful_by_term = {}

for term in generalHealthTerms:
    mask = df_health['summary_lower'].str.contains(term)
    total_eng = df_health.loc[mask, 'engagement'].sum()
    total_helpful = df_health.loc[mask, 'helpful'].sum()
    total_notHelpful = df_health.loc[mask, 'notHelpful'].sum()
    engagement_by_term[term] = total_eng
    helpful_by_term[term] = total_helpful
    notHelpful_by_term[term] = total_notHelpful

# Convert the dictionary to a DataFrame
eng_df = pd.DataFrame({
    'HealthTerm': list(engagement_by_term.keys()),
    'TotalEngagement': list(engagement_by_term.values()),
    'TotalHelpful': list(helpful_by_term.values()),
    'TotalNotHelpful': list(notHelpful_by_term.values())
})

# Sort by TotalEngagement (from greatest to least) and select the top 10
top10_eng_df = eng_df.sort_values(by='TotalEngagement', ascending=False).head(10)
print("Top 10 Health Terms by Total Engagement (Likes + Dislikes):")
print(top10_eng_df)

########################################
# STEP 4: PLOT THE RESULTS
########################################
# Plot 1: Total Engagement Bar Chart for Top 10 Health Terms
plt.figure(figsize=(12, 6))
plt.bar(top10_eng_df['HealthTerm'], top10_eng_df['TotalEngagement'], color='dodgerblue')
plt.xlabel('Health Term')
plt.ylabel('Total Engagement')
plt.title('Top 10 Health Terms by Total Engagement')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Breakdown of Likes vs. Dislikes for Top 10 Health Terms
import numpy as np
x = np.arange(len(top10_eng_df))
width = 0.35

plt.figure(figsize=(12, 6))
plt.bar(x - width/2, top10_eng_df['TotalHelpful'], width, color='green', label='Likes')
plt.bar(x + width/2, top10_eng_df['TotalNotHelpful'], width, color='red', label='Dislikes')
plt.xlabel('Health Term')
plt.ylabel('Engagement Count')
plt.title('Breakdown of Likes vs. Dislikes for Top 10 Health Terms')
plt.xticks(x, top10_eng_df['HealthTerm'], rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
 