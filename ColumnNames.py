import pandas as pd

def print_column_names(df):
    print("Column names:")
    for col in df.columns:
        print(col)

if __name__ == "__main__":
    file_path = "communityNotesFinalWithRatings.tsv"
    df = pd.read_csv(file_path, sep="\t", low_memory=False)
    print_column_names(df)