import pandas as pd
import numpy as np

# Load your data
output_file = pd.read_excel('Output File.xlsx')
final_output = pd.read_excel('final_output.xlsx')

# Print the first few rows of each file to understand the structure
print("Output File Head:")
print(output_file.head(5))
print("\nFinal Output Head:")
print(final_output.head(5))

# Standardize column names
output_file.columns = output_file.columns.str.lower().str.replace(' ', '_')
final_output.columns = final_output.columns.str.lower().str.replace(' ', '_')

# Convert '-' and other missing values to NaN for both dataframes
output_file.replace('-', np.nan, inplace=True)
final_output.replace('-', np.nan, inplace=True)

# Normalize case for all text columns in both dataframes
text_columns = ['voter_full_name', 'relative\'s_name', 'relation_type', 'gender', 'house_no']

for col in text_columns:
    if col in output_file.columns:
        output_file[col] = output_file[col].astype(str).str.upper().str.strip()
    if col in final_output.columns:
        final_output[col] = final_output[col].astype(str).str.upper().str.strip()

# Convert 'epic_no' to string in both dataframes for consistent merging
output_file['epic_no'] = output_file['epic_no'].astype(str)
final_output['epic_no'] = final_output['epic_no'].astype(str)

# Merge dataframes
merged_df = output_file.merge(final_output, how='left', left_on='epic_no', right_on='epic_no', suffixes=('_output', '_final'), indicator=True)

# Find missing rows
missing_rows = merged_df.query('_merge == "left_only"').drop('_merge', axis=1)

# Print missing rows to check
print("Missing Rows:")
print(missing_rows)

# Create a comparison DataFrame to find rows with incorrect values
comparison_df = merged_df[merged_df['_merge'] == 'both'].copy()

# Compare columns and create a DataFrame with boolean results
comparison_df['match'] = True
for col in output_file.columns:
    if col != 'epic_no':  # Skip 'epic_no' since it's used for merging
        comparison_df['match'] &= comparison_df[col + '_output'].fillna(np.nan) == comparison_df[col + '_final'].fillna(np.nan)

# Find rows with mismatches
mismatch_rows = comparison_df[~comparison_df['match']].drop('match', axis=1)

# Print rows with mismatches
print("Rows with Mismatches:")
print(mismatch_rows)

# Save mismatched rows to an Excel file
mismatch_rows.to_excel('mismatched_rows.xlsx', index=False)

# Calculate accuracy
accuracy = comparison_df['match'].mean() if comparison_df.shape[0] > 0 else np.nan
print(f"Accuracy: {accuracy}")
