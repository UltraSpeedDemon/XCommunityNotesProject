import pandas as pd
import matplotlib.pyplot as plt
import re

keywords = ['health', 'covid', 'vaccine', 'disease', 'cancer', 'mental']
df = pd.read_csv('communityNotesFinalNoRatings.tsv', sep='\t', low_memory=False)

# get year
df['createdAt'] = pd.to_datetime(df['createdAtMillis'], unit='ms')
df['year'] = df['createdAt'].dt.year

# check if any health keyword is in summary
def keywordCheck(text):
    if pd.isnull(text):
        return False
    return any(re.search(r'\b' + kw + r'\b', text, flags=re.IGNORECASE) for kw in keywords)

# Filter for health-related notes
filteredKeyWords = df[df['summary'].apply(keywordCheck)]

# count num per year for each keyword
yearKeywordCounts = {kw: {} for kw in keywords}

for index, row in filteredKeyWords.iterrows():
    year = row['year']
    summaryText = row['summary']
    
    for kw in keywords:
        if re.search(r'\b' + kw + r'\b', summaryText, flags=re.IGNORECASE):
            yearKeywordCounts[kw][year] = yearKeywordCounts[kw].get(year, 0) + 1

# display results
plt.figure(figsize=(10, 6))
for kw, counts in yearKeywordCounts.items():
    years = sorted(counts.keys())
    freq = [counts[yr] for yr in years]
    plt.plot(years, freq, marker='o', label=kw)

plt.xlabel('Year')
plt.ylabel('Frequency')
plt.title('Keyword Frequency by Year')
plt.legend(title='Keywords')
plt.grid(True)

minYear = filteredKeyWords['year'].min()
maxYear = filteredKeyWords['year'].max()
plt.xticks(range(minYear, maxYear + 1))

plt.show()
