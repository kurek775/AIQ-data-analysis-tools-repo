from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import export_graphviz
import graphviz
from sklearn.tree import _tree
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Your data
data_ = {
    'lambda': np.random.uniform(0, 1, 100),
    'alpha': np.random.uniform(0, 1, 100),
    'epsilon': np.random.uniform(0.01, 0.03, 100),
    'gamma': np.random.uniform(0.6, 0.8, 100),
    'AIQ': np.random.randint(50, 70, 100)
}

# Convert the dataset into a pandas DataFrame
df = pd.DataFrame(data_)

# Discretize the continuous data into bins
df['lambda'] = pd.qcut(df['lambda'], q=4, labels=False)
df['alpha'] = pd.qcut(df['alpha'], q=4, labels=False)
df['epsilon'] = pd.qcut(df['epsilon'], q=4, labels=False)
df['gamma'] = pd.qcut(df['gamma'], q=4, labels=False)
df['AIQ'] = pd.qcut(df['AIQ'], q=4, labels=False)

# Convert DataFrame into list of lists for TransactionEncoder
transactions = df.values.tolist()

# Apply TransactionEncoder
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

# Apply apriori to find frequent itemsets
frequent_itemsets = apriori(df, min_support=0.6, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print(rules)


# Create a sample dataset
data = {
    'lambda': np.random.uniform(0, 1, 100),
    'alpha': np.random.uniform(0, 1, 100),
    'epsilon': np.random.uniform(0.01, 0.03, 100),
    'gamma': np.random.uniform(0.6, 0.8, 100),
    'AIQ': np.random.randint(50, 70, 100)
}

# Convert the dataset into a pandas DataFrame
df = pd.DataFrame(data)

# Split the dataset into features and labels
X = df[['lambda', 'alpha', 'epsilon', 'gamma']]
y = df['AIQ']

# Create an instance of the DecisionTreeRegressor
reg = tree.DecisionTreeRegressor(max_depth=3)

# Fit the regressor to the data
reg = reg.fit(X, y)

# Plot the decision tree
plt.figure(figsize=(12, 8))
tree.plot_tree(reg, feature_names=X.columns, filled=True)
plt.show()
# Export the decision tree to a dot file
dot_data = tree.export_graphviz(reg, out_file=None, 
                                max_depth=3,
                                feature_names=X.columns,  
                                filled=True)

# Use graphviz to create a graph from the dot file
graph = graphviz.Source(dot_data)

# Save the graph to a PDF file (you can also save it to a PNG or other image file)
graph.render("decision_tree", format='png')

def tree_to_rules(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    # Open the file in write mode
    with open('rules.txt', 'w') as f:
        def recurse(node, previous_rules):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                recurse(tree_.children_left[node], previous_rules + [f"{name} <= {threshold}"])
                recurse(tree_.children_right[node], previous_rules + [f"{name} > {threshold}"])
            else:
                # Write the rule to the file instead of printing
                f.write(" AND ".join(previous_rules) + f" THEN AIQ = {tree_.value[node]}\n")

        recurse(0, [])

# Call the function
tree_to_rules(reg, X.columns)