import pandas as pd
import getopt, sys, os

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        data = []
        with open(arg, 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.replace('"', '')
                if len(line.split(',')) > 7:
                    firstHalf = line.split(',')[0:7]
                    secondHalf = line.split(',')[7:]
                    
                    if len(secondHalf) > 1:
                        secondHalf = '_'.join(secondHalf)
                    else:
                        secondHalf = secondHalf[0]
                    completeLine = firstHalf + [secondHalf]
                    data.append(completeLine)
                else:
                    line = line + ',Config'
                    data.append(line.split(','))

        df = pd.DataFrame(data[1:], columns=data[0])
        df = df.rename(columns={'AGNT+AGNTconf': 'Alg'})
        df.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()