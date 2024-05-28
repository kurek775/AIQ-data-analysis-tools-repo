import getopt, sys
import pandas as pd

def main():
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        df = pd.read_csv(arg)
        df_grouped = df[[col for col in df.columns if col.startswith('AIQ') or col in ['Alg']]]
        df_mean_algs = df_grouped.groupby('Alg').mean().reset_index()
        for row in df_mean_algs.iterrows():
            alg = row[1]['Alg']
            df_desc = df_grouped[df_grouped['Alg'] == row[1]['Alg']].describe()
            df_desc = df_desc.loc[df_desc.index.difference(['count'])]
            df_desc = df_desc.rename(columns={'AIQ1k': '1 000', 'AIQ3k': '3 000', 'AIQ10k': '10 000', 'AIQ30k': '30 000', 'AIQ100k': '100 000'})
            df_desc = df_desc.rename(index={'25%': '1qt', '50%': 'median', '75%': '3qt', 'min': 'min', 'max': 'max', 'mean': 'mean', 'std': 'std'})
            df_desc.reset_index(inplace=True)
            df_desc = df_desc.rename(columns={'index': 'stat'})
            df_desc = df_desc.round(3) 
            df_desc.to_csv(f'{alg}_.csv')


if __name__ == "__main__":
    main()