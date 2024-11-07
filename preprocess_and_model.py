import pandas as pd

# Load the Excel file
file_path = 'Major_project_dataset.xlsx'  # Ensure this path is correct
df = pd.read_excel(file_path)

# Preview the first few rows
print(df.head())
print("DataFrame Shape:", df.shape)  # Outputs (number of rows, number of columns)
