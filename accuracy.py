import pandas as pd
import numpy as np

# Load the Excel files
final_output = pd.read_excel('final_output.xlsx')
output_file = pd.read_excel('Output File.xlsx')

# Ensure both DataFrames have the same columns, ignoring the order
final_output = final_output.sort_index(axis=1)
output_file = output_file.sort_index(axis=1)

# Reindex both DataFrames to have the same columns and indices
all_columns = final_output.columns.union(output_file.columns)
all_indices = final_output.index.union(output_file.index)

final_output = final_output.reindex(index=all_indices, columns=all_columns)
output_file = output_file.reindex(index=all_indices, columns=all_columns)

# Fill missing values with NaN
final_output = final_output.fillna(np.nan)
output_file = output_file.fillna(np.nan)

# Standardize text data by stripping whitespace and converting to lowercase
for col in final_output.columns:
    if final_output[col].dtype == object:
        final_output[col] = final_output[col].str.strip().str.lower()
    if output_file[col].dtype == object:
        output_file[col] = output_file[col].str.strip().str.lower()

# Handle data type consistency carefully
for col in final_output.columns:
    if final_output[col].dtype != output_file[col].dtype:
        try:
            if pd.api.types.is_numeric_dtype(final_output[col]) and pd.api.types.is_numeric_dtype(output_file[col]):
                final_output[col] = pd.to_numeric(final_output[col], errors='coerce')
                output_file[col] = pd.to_numeric(output_file[col], errors='coerce')
            elif pd.api.types.is_string_dtype(final_output[col]) and pd.api.types.is_string_dtype(output_file[col]):
                final_output[col] = final_output[col].astype(str)
                output_file[col] = output_file[col].astype(str)
        except ValueError as e:
            print(f"Error converting column '{col}': {e}")
            continue

# Compare the dataframes
comparison = final_output == output_file

# Calculate accuracy
correct_matches = comparison.values.sum()
total_values = comparison.size
accuracy = correct_matches / total_values

# Summary of differences
differences = final_output[~comparison].combine_first(output_file[~comparison])

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Number of differences: {total_values - correct_matches}")
print("Differences found (if any):")
print(differences)

# Save differences to a new Excel file if needed
differences.to_excel('differences.xlsx', index=False)
print("Differences have been saved to 'differences.xlsx'.")
