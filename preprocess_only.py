# Import necessary libraries
import pandas as pd
import re
import nltk
import spacy
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from sklearn.preprocessing import MinMaxScaler

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))


# Define a synonym replacement dictionary
synonym_dict = {
    'graph': 'chart',
    'diagram': 'chart',
    'visualization': 'chart',
    'show': 'display',
    'total': 'sum'
}

# Load SpaCy's English model for lemmatization
nlp = spacy.load('en_core_web_sm')

# Load the dataset
file_path = 'Major_project_dataset.xlsx'  # Ensure this file is in the same directory as the script or provide the full path
df = pd.read_excel(file_path)
print("Dataset loaded successfully!")

# Step 1: Handle Missing Values
df.ffill(inplace=True)

# Step 2: Text Preprocessing function (lemmatization, stopword removal, punctuation removal, tokenization, lowercase)
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    doc = nlp(text)  # Apply SpaCy model
    tokens = [token.lemma_ for token in doc if token.lemma_ not in stop_words and not token.is_punct]  # Lemmatize and remove stopwords
    return " ".join(tokens)  # Join tokens back into a single string

# Apply text preprocessing to 'query' and 'question' columns
df['query_processed'] = df['query'].apply(preprocess_text)
df['question_processed'] = df['question'].apply(preprocess_text)

# Step 3: Convert 'chart' column to lowercase
df['chart'] = df['chart'].str.strip().str.lower()

# Step 4: Encode 'hardness' column
hardness_encoder = LabelEncoder()
df['hardness_encoded'] = hardness_encoder.fit_transform(df['hardness'])

# Step 5: Scale encoded features (optional if needed for further analysis)
scaler = MinMaxScaler()
df[['hardness_encoded_scaled']] = scaler.fit_transform(df[['hardness_encoded']])

# Drop redundant columns for the final preprocessed dataset
df_preprocessed = df.drop(columns=['tvBench_id', 'hardness', 'query', 'question', 'hardness_encoded'])

# Save the preprocessed data
output_path = 'preprocessed_dataset.csv'
df_preprocessed.to_csv(output_path, index=False)
print(f"Preprocessed data saved to {output_path}")
