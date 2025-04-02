#################################################
## LISTING MOST HELPING AND UNHELPFUL KEYWORDS ##
#################################################

import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

df = pd.read_csv("communityNotesFinalWithRatings.tsv", sep="\t", low_memory=False)

# this array was generated using AI
countries = [
    "afghanistan", "albania", "algeria", "andorra", "angola", "antigua and barbuda", "argentina", "armenia", "australia",
    "austria", "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados", "belarus", "belgium", "belize", "benin",
    "bhutan", "bolivia", "bosnia and herzegovina", "botswana", "brazil", "brunei", "bulgaria", "burkina faso", "burundi",
    "cabo verde", "cambodia", "cameroon", "canada", "central african republic", "chad", "chile", "china", "colombia",
    "comoros", "congo (congo-brazzaville)", "costa rica", "croatia", "cuba", "cyprus", "czech republic", "democratic republic of the congo",
    "denmark", "djibouti", "dominica", "dominican republic", "ecuador", "egypt", "el salvador", "equatorial guinea",
    "eritrea", "estonia", "eswatini", "ethiopia", "fiji", "finland", "france", "gabon", "gambia", "georgia", "germany",
    "ghana", "greece", "grenada", "guatemala", "guinea", "guinea-bissau", "guyana", "haiti", "honduras", "hungary",
    "iceland", "india", "indonesia", "iran", "iraq", "ireland", "israel", "italy", "ivory coast", "jamaica", "japan",
    "jordan", "kazakhstan", "kenya", "kiribati", "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho", "liberia",
    "libya", "liechtenstein", "lithuania", "luxembourg", "madagascar", "malawi", "malaysia", "maldives", "mali", "malta",
    "marshall islands", "mauritania", "mauritius", "mexico", "micronesia", "moldova", "monaco", "mongolia", "montenegro",
    "morocco", "mozambique", "myanmar", "namibia", "nauru", "nepal", "netherlands", "new zealand", "nicaragua", "niger",
    "nigeria", "north korea", "north macedonia", "norway", "oman", "pakistan", "palau", "palestine", "panama", "papua new guinea",
    "paraguay", "peru", "philippines", "poland", "portugal", "qatar", "romania", "russia", "rwanda", "saint kitts and nevis",
    "saint lucia", "saint vincent and the grenadines", "samoa", "san marino", "sao tome and principe", "saudi arabia", "senegal",
    "serbia", "seychelles", "sierra leone", "singapore", "slovakia", "slovenia", "solomon islands", "somalia", "south africa",
    "south korea", "south sudan", "spain", "sri lanka", "sudan", "suriname", "sweden", "switzerland", "syria", "taiwan",
    "tajikistan", "tanzania", "thailand", "timor-leste", "togo", "tonga", "trinidad and tobago", "tunisia", "turkey", "turkmenistan",
    "tuvalu", "uganda", "ukraine", "united arab emirates", "united kingdom", "united states", "uruguay", "uzbekistan", "vanuatu",
    "vatican city", "venezuela", "vietnam", "yemen", "zambia", "zimbabwe"
]

# get which rows are helpful and unhelpful
helpfulnessLevel = ['HELPFUL', 'SOMEWHAT_HELPFUL']
unhelpfulnessLevel= ['NOT_HELPFUL']

helpfulNotes = df[df['helpfulnessLevel'].isin(helpfulnessLevel)]
unhelpfulNotes = df[df['helpfulnessLevel'].isin(unhelpfulnessLevel)]

helpfulCounts = {term: 0 for term in countries}
unhelpfulCounts = {term: 0 for term in countries}

helpfulSummaries = helpfulNotes['summary'].dropna().str.lower()
unhelpfulSummaries = unhelpfulNotes['summary'].dropna().str.lower()

print(len(countries))

# loop over each helpful term
for text in helpfulSummaries:
    list = re.split(r"[-\':/?&.\s]", text)
    for term in countries:
        for word in list:
            if term == word:
                helpfulCounts[term] += 1

# loop over each unhelpful term
for text in unhelpfulSummaries:
    list = re.split(r"[-\':/?&.\s]", text)
    for term in countries:
        for word in list:
            if term == word:
                   unhelpfulCounts[term] += 1

helpfulTotal = len(helpfulSummaries)
unhelpfulTotal = len(unhelpfulSummaries)

results = []


for term in countries:
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

results = pd.DataFrame(results)
results = results.sort_values(by='helpfulCount', ascending=False)

# Get the top 20 countries
topResults = results.iloc[:20]

pd.set_option('display.max_rows', None)

# display results
print("\nHealth Term Frequency Analysis:")
print(results.to_string(index=False))

palette = {
    "Helpful Community Notes": "green",
    "Unhelpful Community Notes": "red"
}

# graph results
plot = topResults.melt(id_vars='term', value_vars=['helpfulCount', 'unhelpfulCount'], 
                        var_name='Group', value_name='Amount')

plot['Group'] = plot['Group'].map({
    'helpfulCount': 'Helpful Community Notes',
    'unhelpfulCount': 'Unhelpful Community Notes'
})

plt.figure(figsize=(12, 8))
sns.barplot(data=plot, x='term', y='Amount', hue='Group', palette=palette)
plt.title("Comparision of Mentioned Countries used in Helpful and Unhelpful Twitter Community Notes")
plt.xlabel("Country")
plt.ylabel("Percentage of Community Notes")
plt.xticks(rotation=90)
plt.legend(title="Community Note Group")
plt.tight_layout()
plt.show()