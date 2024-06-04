import pandas as pd
import getopt, sys, os

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        df = pd.read_fwf(arg, header=None)
        df = df[0].str.split(',', expand=True)
        # Use first row as column names
        df.columns = df.iloc[0]
        # Drop the first row
        df = df[1:]
        # Replace None with 'conf[i]'
        df.columns = ['config' + str(i) if v is None else v for i, v in enumerate(df.columns)]
        # Join all 'conf' columns into one column named 'config'
        conf_cols = [col for col in df.columns if 'config' in col]
        df.columns = df.columns.str.replace('"', '')
        df['Config'] = df[conf_cols].apply(lambda row: '_'.join([val for val in row.values.astype(str) if val != 'None']), axis=1)
        df = df.drop(columns=conf_cols)
        df.to_csv('output.csv', index=False)
        bins = [0, 1000, 3000, 10000, 30000, 100000]
        labels = ['1k', '3k', '10k', '30k', '100k']
        df['EL'] = df['EL'].astype(int)
        df['EL'] = pd.cut(df['EL'], bins=bins, labels=labels)
         # Melt the dataframe
        df_melt = df.melt(id_vars=['AGNT+AGNTconf', 'Config', 'EL'], value_vars=['AIQ', 'HCI', 'SD'])
        # Create a new column that combines 'variable' and 'Ep'
        df_melt['var_ep'] = df_melt['variable'] + df_melt['EL'].astype(str)
        df_melt['value'] = pd.to_numeric(df_melt['value'], errors='coerce')
        df_filtered = df_melt[df_melt['AGNT+AGNTconf'] == 'PPO']
        print(df_filtered)
        # Pivot the dataframe to the desired format
        df_pivot = df_melt.pivot_table(index=['AGNT+AGNTconf', 'Config'], columns='var_ep', values='value').reset_index()
        df_fil = df_pivot[df_pivot['AGNT+AGNTconf'] == 'PPO']
        print(df_fil)
        # Reorder the columns
        #cols_order = ['AGNT+AGNTconf', 'Config', 'AIQ1k', 'HCI1k', 'SD1k', 'AIQ3k', 'HCI3k', 'SD3k', 'AIQ10k', 'HCI10k', 'SD10k', 'AIQ30k', 'HCI30k', 'SD30k', 'AIQ100k', 'HCI100k', 'SD100k']
        #df_pivot = df_pivot.reindex(columns=cols_order)
        #df_pivot = df_pivot.round(3) 
        #df_pivot.to_csv('reshaped_output.csv', index=False)
        # Filter rows where 'AGNT+AGNTconf' is 'PPO'
        

        # Print the filtered dataframe
        

if __name__ == "__main__":
    main()