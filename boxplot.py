import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load the data

df = pd.read_csv('basic_config_results.csv')
df['Alg'] = df['Alg'].str.replace('H_l', 'HLQ(λ)')
df['Alg'] = df['Alg'].str.replace('_l', '(λ)')


df = df.rename(columns={'AIQ1k': '1 000', 'AIQ3k': '3 000', 'AIQ10k': '10 000', 'AIQ30k': '30 000', 'AIQ100k': '100 000'})

# Převod dat do dlouhého formátu pro Seaborn
df_long = pd.melt(df, id_vars=['Alg', 'Config'], value_vars=['1 000', '3 000', '10 000', '30 000', '100 000'],
                  var_name='Epizoda', value_name='AIQ')

# Vytvoření boxplotu
plt.figure(figsize=(14, 8))
sns.boxplot(x='Alg', y='AIQ', hue='Epizoda', data=df_long)

plt.xlabel('Agent')
plt.ylabel('AIQ')
plt.legend(title='Délka epizody')

plt.savefig('boxplot.png', dpi=300)
plt.show()