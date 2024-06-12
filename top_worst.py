import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('basic_config_results_.csv')

# Remove leading/trailing whitespaces from column names and values
df.columns = df.columns.str.strip()
df['Alg'] = df['Alg'].str.strip()

# Split the 'Config' column into 'q', 'lambda', 'alpha', 'epsilon', and 'gamma' columns
df[['q', 'lambda', 'alpha', 'epsilon', 'gamma']] = df['Config'].str.split('_', expand=True)

# Initialize lists to store results
top_5_configs = []
bottom_5_configs = []

# For each unique algorithm, find the top 5 and bottom 5 configurations based on 'AIQ100k'
for alg in df['Alg'].unique():
    subset = df[df['Alg'] == alg]
    
    # Sort by 'AIQ100k' and select the top 5 configurations
    top_5 = subset.sort_values('AIQ100k', ascending=False).head(5)[['Alg', 'q', 'lambda', 'alpha', 'epsilon', 'gamma', 'AIQ100k']]
    top_5_configs.append(top_5)
    
    # Sort by 'AIQ100k' and select the bottom 5 configurations
    bottom_5 = subset.sort_values('AIQ100k').head(5)[['Alg', 'q', 'lambda', 'alpha', 'epsilon', 'gamma', 'AIQ100k']]
    bottom_5_configs.append(bottom_5)

# Concatenate the results into DataFrames
top_5_df = pd.concat(top_5_configs)
bottom_5_df = pd.concat(bottom_5_configs)

# Write the results to CSV files
top_5_df.to_csv('top_5_configs.csv', index=False)
bottom_5_df.to_csv('bottom_5_configs.csv', index=False)