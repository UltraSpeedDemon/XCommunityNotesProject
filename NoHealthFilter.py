import pandas as pd

# Create health-related keywords
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

# Function to check if a summary is health-related
def isHealthRelated(text):
    if pd.isna(text):
        return False
    lowerCase = text.lower()
    return any(keyword in lowerCase for keyword in keywords)

# Load community notes
df = pd.read_csv("rawCommunityNotes.tsv", sep="\t", low_memory=False)

# Filter health-related and non-health-related community notes
nonHealthNotes = df[~df['summary'].apply(isHealthRelated)]

# Save to separate files
nonHealthNotes.to_csv("noHealthCommunityNotes.tsv", sep="\t", index=False)
