# Import necessary libraries
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the dataset
file_path = 'preprocessed_dataset.csv'
df = pd.read_excel(file_path)
print("Dataset loaded successfully!")

# Load T5 Model and Tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")

# Function to generate SQL from natural language
def generate_sql(nlp_query):
    # Update the input text to specify the need for a SQL query in English
    input_text = f"Convert this question to a SQL query in English syntax: {nlp_query}"
    inputs = tokenizer.encode(input_text, return_tensors="pt")

    outputs = model.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Post-process to ensure SQL starts with "SELECT" or provide a rule-based fallback
    if not sql_query.strip().lower().startswith("select"):
        sql_query = rule_based_sql(nlp_query)
    return sql_query

# Fallback function with rule-based SQL generation for common queries
def rule_based_sql(nlp_query):
    if "average number of companies applied by year" in nlp_query.lower():
        return "SELECT Year, AVG(Companies_Applied) FROM student_data GROUP BY Year;"
    elif "distribution of students placed in jobs" in nlp_query.lower():
        return "SELECT Job_Title, COUNT(Student_ID) FROM student_data GROUP BY Job_Title;"
    elif "relationship between CGPA and Salary" in nlp_query.lower():
        return "SELECT CGPA, Salary FROM student_data;"
    else:
        return "SELECT * FROM student_data;  -- General fallback for unsupported queries"

# Example usage with inputs from the dataset
for index, row in df.iterrows():
    nlp_query = row['question']
    print("\nQuestion:", nlp_query)
    
    # Generate and print SQL
    sql_query = generate_sql(nlp_query)
    print("Generated SQL Query:", sql_query)
