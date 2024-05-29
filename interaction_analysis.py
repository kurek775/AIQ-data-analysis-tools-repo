import getopt, sys
import pandas as pd
import matplotlib.pyplot as plt

def main():
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        with open(arg, 'r') as f:
            title = f.readline().strip()  # Read the first line as title

        df = pd.read_csv(arg, skiprows=1)  # Skip the first row as it's used as title

        fig, axs = plt.subplots(3, figsize=(10, 18))

        axs[0].plot(df.index, df.iloc[:, 0])
        axs[0].set(xlabel='Time', ylabel='Q')
        axs[0].set_title(title + ' - Q')

        axs[1].plot(df.index, df.iloc[:, 1])
        axs[1].set(xlabel='Time', ylabel='Reward')
        axs[1].set_title(title + ' - Reward')

        axs[2].plot(df.index, df.iloc[:, 2])
        axs[2].set(xlabel='Time', ylabel='Action')
        axs[2].set_title(title + ' - Action')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()