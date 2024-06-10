import argparse
from sklearn import tree
import pandas as pd
import matplotlib.pyplot as plt
import graphviz
from sklearn.tree import _tree

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='The name of the CSV file to read')
    parser.add_argument('episode_length', type=int, help='The episode length')
    args = parser.parse_args()
    df = pd.read_csv(args.file_name)

    df[['lambda', 'alpha', 'epsilon', 'gamma']] = df['Config'].str.split('_', expand=True).iloc[:, 1:]

    for col in ['lambda', 'alpha', 'epsilon', 'gamma']:
        df[col] = pd.to_numeric(df[col])

    df['AIQ'] = df[f'AIQ{args.episode_length}k']


    # Split the dataset into features and labels
    X = df[['lambda', 'alpha', 'epsilon', 'gamma']]
    y = df['AIQ']
    print(X)
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

if __name__ == "__main__":
    main()