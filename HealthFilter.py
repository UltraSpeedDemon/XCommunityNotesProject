# This class will take the raw 800mb data of community notes and filter it using keywords to only include health related community notes

import pandas as pd

# create health key words
# this array was generated using AI
keywords = [
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

# this function checks to see if any keyword is in the community note summary
def isHealthRelated(text):
    if pd.isna(text):  
        return False
    lowerCase = text.lower()
    return any(keyword in lowerCase for keyword in keywords)

# save health related community notes to new file
df = pd.read_csv("rawCommunityNotes.tsv", sep="\t", low_memory=False)
filtered = df[df['summary'].apply(isHealthRelated)]
filtered.to_csv("healthCommunityNotes.tsv", sep="\t", index=False)
