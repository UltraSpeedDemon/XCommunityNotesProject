from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import matplotlib.pyplot as plt

notes = pd.read_csv('communityNotesFinalNoRatings.tsv', sep='\t', header=0, dtype={'believable': str, 'harmful': str, 'validationDifficulty': str})

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(notes['summary'])

# nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Apply sentiment analysis
notes['sentiment'] = notes['summary'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Classify as positive, negative, or neutral
notes['label'] = notes['sentiment'].apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral'))

# Count occurrences
sentiment_counts = notes['label'].value_counts()

print(sentiment_counts)

plt.figure(figsize=(10, 6))
sentiment_counts.plot(kind='bar', color='blue')
plt.xlabel('Sentiment')
plt.ylabel('Number of Community Notes')
plt.title('Sentiment Count')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.show()