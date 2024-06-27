import argparse
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='The name of the CSV file to read')
    parser.add_argument('episode_length', type=int, help='The episode length')
    args = parser.parse_args()
    df = pd.read_csv(args.file_name)
    el = args.episode_length

    df[['lambda', 'alpha', 'epsilon', 'gamma']] = df['Config'].str.split('_', expand=True).iloc[:, 1:]

    for col in ['lambda', 'alpha', 'epsilon', 'gamma']:
        df[col] = pd.to_numeric(df[col])

    df['AIQ'] = df[f'AIQ{el}k']

    # Příprava dat pro TransactionEncoder
    transactions = df.apply(lambda row: [f'{col}={row[col]}' for col in ['lambda', 'alpha', 'epsilon', 'gamma', 'AIQ']], axis=1).tolist()

    # Encode the transactions into a one-hot encoded DataFrame
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

    # Use the apriori algorithm to find frequent itemsets
    frequent_itemsets = apriori(df_encoded, min_support=0.01, use_colnames=True)

    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

    # Print the generated rules
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

if __name__ == "__main__":
    main()
