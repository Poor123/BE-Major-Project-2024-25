import pandas as pd
import re

# Load the dataset
df = pd.read_csv('preprocessed_dataset_with_pos.csv')

# Define schema mappings for NLP phrases to SQL columns or operations
# Adjust mappings with actual table columns when available
column_mapping = {
    'average': 'AVG(query)',  # Replace 'column_name' with actual column name if known
    'count': 'COUNT(query)',
    'total': 'SUM(query)',
    'highest': 'MAX(query)',
    # Add other mappings based on actual columns in the db_id table
}

# Define the function to map NLP tokens to SQL syntax
def nlp_to_sql_mapping(tokens):
    sql_parts = {
        'select': [],
        'from': None,
        'where': [],
        'group_by': [],
        'order_by': []
    }
    
    for token, pos in tokens:
        # Map tokens to SQL columns or functions based on POS tags and mappings
        if pos == 'NOUN' and token in column_mapping:
            sql_parts['select'].append(column_mapping[token])
        elif pos == 'NOUN':
            sql_parts['select'].append(f"{token}")  # Assume noun refers to a column directly
        elif pos == 'ADJ':
            sql_parts['where'].append(f"{token} = value")  # Placeholder for conditions
        elif pos == 'VERB' and token == 'group':
            sql_parts['group_by'].append("column_name")  # Placeholder; adjust with actual grouping column
    
    return sql_parts

# Function to build SQL query from parsed tokens
def build_sql_query(row):
    db_id = row['db_id']
    
    # Parse tokens, assuming tokens are stored as a list of tuples
    try:
        question_tokens = eval(row['question_processed_tokens'])  # Parse tokens from string
    except Exception as e:
        print(f"Error parsing tokens: {e}")
        return "Error in token parsing"
    
    # Step 1: Parse tokens to identify SQL elements
    sql_parts = nlp_to_sql_mapping(question_tokens)
    
    # Step 2: Set FROM clause using db_id as the table name
    sql_parts['from'] = db_id
    
    # Step 3: Construct the SQL query
    select_clause = ", ".join(sql_parts['select'])
    from_clause = f"FROM {sql_parts['from']}"
    where_clause = f"WHERE {' AND '.join(sql_parts['where'])}" if sql_parts['where'] else ""
    group_by_clause = f"GROUP BY {', '.join(sql_parts['group_by'])}" if sql_parts['group_by'] else ""
    order_by_clause = f"ORDER BY {', '.join(sql_parts['order_by'])}" if sql_parts['order_by'] else ""
    
    # Combine clauses into the final SQL query
    sql_query = f"SELECT {select_clause} {from_clause} {where_clause} {group_by_clause} {order_by_clause};"
    return sql_query.strip()

# Apply the SQL query building function to each row in the dataset
df['generated_sql'] = df.apply(build_sql_query, axis=1)

# Display a sample of the generated SQL queries to verify output
output_sample = df[['question_processed_tokens', 'generated_sql']].head()
print(output_sample)

# Save output to a CSV file
df[['question_processed_tokens', 'generated_sql']].to_csv('generated_sql_output.csv', index=False)
print("Output saved to 'generated_sql_output.csv'")
