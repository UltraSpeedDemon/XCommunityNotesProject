import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('communityNotesFinalNoRatings.tsv', sep='\t')
botId = "111F4A03D7F1923DCEC73DD8595474B5BFA1C4E88D3224D24348DD08B82C38D9"
df = df[df['noteAuthorParticipantId'] != botId]

accountCounts = df['noteAuthorParticipantId'].value_counts().head(10)

# display results
top10 = accountCounts.head(10)
print("Top 10 Accounts by Number of Community Notes:")
print(top10)

print("\nTweet of each top 10 account to find the account name:")
for account in top10.index:
    sampleTweetId = df.loc[df['noteAuthorParticipantId'] == account, 'tweetId'].iloc[0]
    print(f"Account ID: {account} | Tweet ID: {sampleTweetId}")
    
plt.figure(figsize=(10, 6))
top10.plot(kind='bar', color='blue')
plt.xlabel('Account')
plt.ylabel('Number of Community Notes')
plt.title('Top 10 Accounts by Number of Community Notes')
plt.xticks(rotation=90, ha='right')
plt.tight_layout()
plt.show()