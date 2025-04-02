#This takes about 800mb of community notes and filters it down to only health related terms.
#Which uses NLP's and ML to find the best community note to answer a users question.

#NLP - Vectorization
#ML - Similarities (Cosine Similarity)

#This file when ran, loads and filters all the notes for health related topics/terms, vectorizes, then prompts the user for a health related question.
# It then finds all notes similar to the question asked and provides the Top 3 notes for the users question.
# users can then mark the notes as relevant or not relevant.
# The notes marked as not relevant will not be shown again in the future.

import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer #nlp vectorization
from sklearn.metrics.pairwise import cosine_similarity #ml similarities
import tkinter as tk
from tkinter import ttk, messagebox

# all health related terms that are used to filter the notes and find similarities.
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
    "oncology", "urology", "gynecology", "aids", "treatment", "medication", "rehab",
    "diagnostic", "clinical", "symptom", "condition", "disorder", "ailment", "healthcare",
    "prevention", "screening", "monitoring", "management", "intervention", "consultation", "examination",
    "assessment", "evaluation", "follow-up", "advice", "recommendation", "guidance", "support", "education",
    "awareness", "research", "study", "trial", "experiment", "analysis", "finding", "discovery", "blood pressure",
    "cholesterol levels", "blood sugar", "glucose", "insulin resistance", "body mass index",
    "BMI", "waist circumference", "waist-to-hip ratio", "physical activity", "exercise regimen",
]
#loads the data from the TSV file and filters it for health-related notes.
def load_and_filter_data(file_path):
    """
    Load the TSV data and filter for health-related notes.
    """
    try:
        df = pd.read_csv(file_path, sep="\t", low_memory=False) # Load the TSV file
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)
    
    df['summary_lower'] = df['summary'].fillna('').str.lower()
    health_mask = df['summary_lower'].apply(lambda text: any(term in text for term in generalHealthTerms))
    df_health = df[health_mask].copy()
    
    if df_health.empty:
        print("No health-related notes found.")
        sys.exit(1)
    
    return df_health
#vectorizes the text documents using CountVectorizer from sklearn.
def vectorize_texts(texts):
    vectorizer = CountVectorizer(stop_words='english') # Initialize CountVectorizer
    X = vectorizer.fit_transform(texts)
    return X, vectorizer

#searches for the most relevant notes based on the user's query.
def search_notes(query, df, X, vectorizer, top_n=3):
    query_vec = vectorizer.transform([query]) # Vectorize the query
    similarities = cosine_similarity(query_vec, X).flatten()
    sorted_indices = np.argsort(similarities)[::-1]
    
    unique_results = []
    seen_summaries = set()
    for idx in sorted_indices:
        summary = df.iloc[idx]['summary'].strip() # Get the summary text
        if summary not in seen_summaries:
            seen_summaries.add(summary)
            row = df.iloc[idx].copy()
            row['similarity'] = similarities[idx] # Add similarity score to the row
            unique_results.append(row)  
        if len(unique_results) == top_n:
            break
    return pd.DataFrame(unique_results) # This function is used to display a message box with the given title and message.

# GUI class to build the application using tkinter.
class HelpfulResultsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Helpful Results") 
        self.geometry("900x600")
        self.configure(bg="light blue")
        
        self.irrelevant_indices = set()
        self.df_health = None
        self.vectorizer = None
        self.texts = None
        self.current_df = None
        self.current_vectorizer = None
        self.current_X = None
        self.top_results = None
        self.feedback_vars = {}
        
        self.container = ttk.Frame(self, style="Custom.TFrame")
        self.container.pack(fill="both", expand=True)
        
        style = ttk.Style(self)
        style.configure("Custom.TFrame", background="light blue")
        style.configure("Custom.TLabel", background="light blue", font=("Times New Roman", 12))
        style.configure("Custom.TButton", font=("Times New Roman", 12))
        style.configure("White.TFrame", background="white")
        style.configure("White.TLabel", background="white", font=("Times New Roman", 14))
        style.configure("Large.TButton", font=("Times New Roman", 16), padding=10)
        
        self.create_loading_screen()
        self.after(100, self.load_data)

    def create_loading_screen(self):
        self.clear_container()
        loading_label = ttk.Label(
            self.container, 
            text="Filtering Data...\n", 
            font=("Times New Roman", 22), 
            anchor="center",
            style="Custom.TLabel"
        )
        loading_label.pack(expand=True)
        loading_label2 = ttk.Label(
            self.container, 
            text="Please wait a few seconds...", 
            font=("Times New Roman", 22), 
            anchor="center",
            style="Custom.TLabel"
        )
        loading_label2.pack(expand=True)
    #load the data from the TSV file and filter it for health-related notes.
    def load_data(self): 
        file_path = "communityNotesFinalWithRatings.tsv" # Path to the TSV file
        self.df_health = load_and_filter_data(file_path)
        self.texts = self.df_health['summary_lower'].tolist() 
        _, self.vectorizer = vectorize_texts(self.texts)
        self.show_question_screen()
    #clear the container of all widgets before displaying a new screen.
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
    #show the question screen where the user can enter their health-related question.
    def show_question_screen(self):
        self.clear_container()
        question_frame = ttk.Frame(self.container, style="Custom.TFrame")
        question_frame.pack(expand=True)
        
        prompt_label = ttk.Label(question_frame, text="Enter your health-related question:", font=("Times New Roman", 18), style="Custom.TLabel")
        prompt_label.pack(pady=10)
        
        self.query_entry = ttk.Entry(question_frame, width=60, font=("Times New Roman", 16))
        self.query_entry.pack(pady=10)
        self.query_entry.focus()
        
        self.search_button = ttk.Button(question_frame, text="Search for Similar Community Notes", command=self.on_search, style="Custom.TButton")
        self.search_button.pack(pady=10)
        
        self.searching_label = ttk.Label(question_frame, text="", font=("Times New Roman", 14), style="Custom.TLabel")
        self.searching_label.pack()
    #search for relevant notes based on the user's query and display the results.
    def on_search(self):
        query = self.query_entry.get().strip().lower()
        if not query:
            messagebox.showerror("Error", "Please enter a question.") 
            return
        
        self.searching_label.config(text="Searching...")
        self.update_idletasks()
        
        df_current = self.df_health.drop(self.irrelevant_indices)
        if df_current.empty:
            messagebox.showinfo("Info", "No remaining notes after filtering out irrelevant ones.")
            self.searching_label.config(text="")
            return
        
        texts_current = df_current['summary_lower'].tolist()
        X_current, vectorizer_current = vectorize_texts(texts_current)
        self.current_df = df_current
        self.current_vectorizer = vectorizer_current
        self.current_X = X_current
        
        self.top_results = search_notes(query, df_current, X_current, vectorizer_current, top_n=3)
        self.searching_label.config(text="")
        self.show_results_screen()
    #screen for results where the top matching notes are displayed.
    def show_results_screen(self):
        self.clear_container()
        
        title_label = ttk.Label(self.container, text="Top matching notes:", font=("Times New Roman", 26, "bold"), style="Custom.TLabel")
        title_label.pack(pady=10)
        
        canvas = tk.Canvas(self.container, bg="light blue", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        results_frame = ttk.Frame(canvas, style="Custom.TFrame")
        results_window = canvas.create_window((0, 0), window=results_frame, anchor="nw")
        
        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_canvas_configure(event):
            canvas.itemconfig(results_window, width=event.width)
        
        results_frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)
        
        self.feedback_vars = {}
        for idx, row in self.top_results.iterrows():
            card_frame = ttk.Frame(results_frame, style="White.TFrame", relief="groove", borderwidth=2)
            card_frame.pack(fill="x", pady=5, padx=0)
            
            summary_text = row['summary_lower']
            matching_terms = [term for term in generalHealthTerms if term in summary_text]
            note_date = pd.to_datetime(row['createdAtMillis_x'], unit='ms').strftime("%d %B %Y")
            
            hl = row['helpfulnessLevel']
            if hl == "HELPFUL":
                display_hl = "HELPFUL"
            elif hl == "NOT_HELPFUL":
                display_hl = "NOT HELPFUL"
            else:
                display_hl = hl
            
            similarity_percent = row['similarity'] * 100
            
            details = (
                f"Summary: {row['summary']}\n\n"
                f"Note Index: {idx}\n"
                f"Similarity Score: {similarity_percent:.2f}%\n"
                f"Matching Health Terms: {', '.join(matching_terms) if matching_terms else 'None'}\n"
                f"Note Date: {note_date}\n"
                f"Helpfulness Rating: {display_hl}"
            )
            
            # Wrap length set to 700 so text doesn't run too far horizontally
            label = ttk.Label(
                card_frame, text=details, font=("Times New Roman", 14),
                justify="left", style="White.TLabel", wraplength=700
            )
            label.pack(side="left", padx=10, pady=10, fill="both", expand=True)
            
            var = tk.StringVar(value="relevant")
            self.feedback_vars[idx] = var
            feedback_frame = ttk.Frame(card_frame, style="White.TFrame")
            feedback_frame.pack(side="right", padx=10, pady=10)
            
            ttk.Label(feedback_frame, text="Mark as:", font=("Times New Roman", 14), background="white").pack(anchor="w")
            ttk.Radiobutton(feedback_frame, text="Relevant", variable=var, value="relevant").pack(anchor="w")
            ttk.Radiobutton(feedback_frame, text="Not Relevant", variable=var, value="not_relevant").pack(anchor="w")
        
        # Bottom frame for disclaimer & button
        bottom_frame = ttk.Frame(self.container, style="Custom.TFrame")
        bottom_frame.pack(pady=10)
        
        disclaimer_label = ttk.Label(
            bottom_frame, 
            text="Disclaimer: This app is currently being run on only 800MB of data.", 
            font=("Times New Roman", 12), 
            background="light blue"
        )
        disclaimer_label.pack(pady=5)
        
        feedback_button = ttk.Button(
            bottom_frame, 
            text="Ask Another Question & Submit Feedback", 
            command=self.process_feedback, 
            style="Large.TButton"
        )
        feedback_button.pack(pady=5)
    #finally process the feedback from the user and show the question screen again.
    def process_feedback(self):
        for idx, var in self.feedback_vars.items():
            if var.get() == "not_relevant":
                self.irrelevant_indices.add(idx)
        
        messagebox.showinfo("Feedback Sent", "Feedback has been sent.\nThe notes marked as Not Relevant will not appear again in the future.")
        self.show_question_screen()
# # This function is used to run the application.
if __name__ == "__main__":
    app = HelpfulResultsApp()
    app.mainloop()
