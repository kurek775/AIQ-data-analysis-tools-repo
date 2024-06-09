import getopt, sys, os
import pandas as pd

def main():
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        files = arg.split(',')
        file_list = []
        for file in files:
            df = pd.read_csv(file)
            df['EL'] = df['EL'].astype(int)
            if 'Config' not in df.columns:
                df.loc[df['lambda'] == 0, 'Alg'] = df['Alg'].str.replace('_l', '')
                df['Config'] = df['q'].astype(str) + '_' + df['lambda'].astype(str) + '_' + df['alpha'].astype(str) + '_' + df['epsilon'].astype(str) + '_' + df['gamma'].astype(str)
            bins = [0, 1000, 3000, 10000, 30000, 100000]
            labels = ['1k', '3k', '10k', '30k', '100k']
            df['EL'] = pd.cut(df['EL'], bins=bins, labels=labels)

            df_melt = df.melt(id_vars=['Alg', 'Config', 'EL'], value_vars=['AIQ', 'HCI', 'SD'])

            # Create a new column that combines 'variable' and 'Ep'
            df_melt['var_ep'] = df_melt['variable'] + df_melt['EL'].astype(str)

            # Pivot the dataframe to the desired format
            df_pivot = df_melt.pivot_table(index=['Alg', 'Config'], columns='var_ep', values='value').reset_index()

            # Reorder the columns
            cols_order = ['Alg', 'Config', 'AIQ1k', 'HCI1k', 'SD1k', 'AIQ3k', 'HCI3k', 'SD3k', 'AIQ10k', 'HCI10k', 'SD10k', 'AIQ30k', 'HCI30k', 'SD30k', 'AIQ100k', 'HCI100k', 'SD100k']
            df_pivot = df_pivot.reindex(columns=cols_order)
            df_pivot = df_pivot.round(2) 
            file_list.append(df_pivot)

        save_df = pd.concat(file_list)    
        save_df.to_csv('basic_config_results.csv', index=False)
        


if __name__ == "__main__":
    main()