import matplotlib.pyplot as plt
import getopt, sys
import pandas as pd
from sklearn.metrics import auc
from scipy.integrate import simpson
import numpy as np
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
            df = df[df['Alg'].isin([' Sarsa_l', 'Q', 'Q(λ)'])]
            if not df.empty:
                if 'Config' not in df.columns:
                    df.loc[df['lambda'] == 0, 'Alg'] = df['Alg'].str.replace('_l', '')
                    df.loc[df['lambda'] != 0, 'Alg'] = df['Alg'].str.replace('_l', '(λ)')
                    df['Config'] = df['q'].astype(str) + '_' + df['lambda'].astype(str) + '_' + df['alpha'].astype(str) + '_' + df['epsilon'].astype(str) + '_' + df['gamma'].astype(str)
                df = df.sort_values('EL')

                file_list.append(df)
            param = 'HCI'
            df = pd.concat(file_list)
            for conf in df['Config'].unique():
                df_conf = df[df['Config'] == conf]
                algs = df_conf['Alg'].unique()
                if len(algs) > 1:  
                    plt.figure()
                    for alg in algs:
                        df_alg_conf = df_conf[df_conf['Alg'] == alg]
                        plt.plot(df_alg_conf['EL'], df_alg_conf[param], label=f"{alg} - {conf}")
                    plt.xlabel('EL')
                    plt.ylabel(param)
                    plt.legend()
                    plt.savefig(f'best_pair_plot_{param}_{conf}.png', dpi=300)
                    plt.show()

if __name__ == "__main__":
    main()