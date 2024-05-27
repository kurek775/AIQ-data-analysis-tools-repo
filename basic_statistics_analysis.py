import getopt, sys, os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        df = pd.read_csv(arg)
        df['Ep'] = df['Ep'].astype(int)
        df['Config'] = df['q'].astype(str) + '_' + df['lambda'].astype(str) + '_' + df['alpha'].astype(str) + '_' + df['epsilon'].astype(str) + '_' + df['gamma'].astype(str)
        input_file_name = os.path.splitext(os.path.basename(arg))[0]
        bins = [0, 1000, 3000, 10000, 30000, 100000]
        labels = ['1k', '3k', '10k', '30k', '100k']
        df['Ep'] = pd.cut(df['Ep'], bins=bins, labels=labels)

        # Melt the dataframe
        df_melt = df.melt(id_vars=['Alg', 'Config', 'Ep'], value_vars=['AIQ', 'HCI', 'SD'])

        # Create a new column that combines 'variable' and 'Ep'
        df_melt['var_ep'] = df_melt['variable'] + df_melt['Ep'].astype(str)

        # Pivot the dataframe to the desired format
        df_pivot = df_melt.pivot_table(index=['Alg', 'Config'], columns='var_ep', values='value').reset_index()

        # Reorder the columns
        cols_order = ['Alg', 'Config', 'AIQ1k', 'HCI1k', 'SD1k', 'AIQ3k', 'HCI3k', 'SD3k', 'AIQ10k', 'HCI10k', 'SD10k', 'AIQ30k', 'HCI30k', 'SD30k', 'AIQ100k', 'HCI100k', 'SD100k']
        df_pivot = df_pivot.reindex(columns=cols_order)
        df_pivot = df_pivot.round(3) 
        df_pivot.to_csv('reshaped_output_default.csv', index=False)

        # Select only the columns 'Alg', 'Config', and those starting with 'AIQ'
        df_grouped = df_pivot[[col for col in df_pivot.columns if col.startswith('AIQ') or col in ['Alg']]]
        df_mean_algs = df_grouped.groupby('Alg').mean().reset_index()
        for row in df_mean_algs.iterrows():
            alg = row[1]['Alg']
            df_desc = df_grouped[df_grouped['Alg'] == row[1]['Alg']].describe()
            df_desc = df_desc.loc[df_desc.index.difference(['count'])]
            df_desc = df_desc.rename(columns={'AIQ1k': '1 000', 'AIQ3k': '3 000', 'AIQ10k': '10 000', 'AIQ30k': '30 000', 'AIQ100k': '100 000'})
            df_desc = df_desc.rename(index={'25%': 'První kvartil', '50%': 'Medián', '75%': 'Třetí kvartil', 'min': 'Minimum', 'max': 'Maximum', 'mean': 'Průměr', 'std': 'Směrodatná odchylka'})
            df_desc.reset_index(inplace=True)
            df_desc = df_desc.rename(columns={'index': 'Míra'})
            df_desc = df_desc.round(3) 
            df_desc.to_csv(f'{alg}_{input_file_name}_desc.csv')


if __name__ == "__main__":
    main()