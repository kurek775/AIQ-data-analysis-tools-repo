# analytic tool to count area under curve for a given dataset of results 
# in .csv format mentioned in README.md

import matplotlib.pyplot as plt
from scipy.integrate import simps
import getopt, sys, os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import auc
import numpy as np
from scipy.integrate import simpson
def main():
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["default=", "el="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        df = pd.read_csv(arg)
        df = df.sort_values(by=['Ep'])
        plt.plot(df['Ep'], df['AIQ'], label='AIQ')
        plt.show()
        print(df.head)
        print(simpson(df['Ep'], df['AIQ']))
        print(auc(df['Ep'], df['AIQ']))


if __name__ == "__main__":
    main()