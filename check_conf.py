import pandas as pd

def main():

    gen = pd.read_csv('parameter_space_analysis.csv')
    df = pd.read_csv('basic_config_results_.csv')
    if 'Config' not in gen.columns:
        gen['Config'] = gen['q'].astype(str) + '_' + gen['lambda'].astype(str) + '_' + gen['alpha'].astype(str) + '_' + gen['epsilon'].astype(str) + '_' + gen['gamma'].astype(str)

    for config in gen['Config']:
        if config not in df['Config'].values:
            print(f"Missing config: {config}")    


if __name__ == "__main__":
    main()