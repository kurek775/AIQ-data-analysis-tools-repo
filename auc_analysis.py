import matplotlib.pyplot as plt
import getopt, sys
import pandas as pd
from sklearn.metrics import auc
from scipy.integrate import simpson

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
            df = df.sort_values('EL')
            df_max = df.loc[df[df['EL'] == 100000].groupby('Alg')['AIQ'].idxmax()]
            df = df[df.apply(lambda row: row['Config'] == df_max.loc[df_max['Alg'] == row['Alg'], 'Config'].values[0], axis=1)]
            file_list.append(df)


        df = pd.concat(file_list)
        results = []
        for alg in df['Alg'].unique():
            subset = df[df['Alg'] == alg]
            plt.plot(subset['EL'], subset['AIQ'], label=f"{alg}")
            simps_value = simpson(subset['AIQ'], subset['EL']/1000)
            results.append({
            'Algorithm': alg,
            'Config': subset['Config'].iloc[0],
            'AUC': simps_value.round(2)
            })

        results_df = pd.DataFrame(results)
        results_df.to_csv('auc_results.csv', index=False)
        plt.xlabel('EL')
        plt.ylabel('AIQ')
        plt.legend()
        plt.savefig('best_configs_plot.png', dpi=300) 
        plt.show()

if __name__ == "__main__":
    main()