import json
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.integrate import simps
import numpy as np
import argparse
from io import StringIO
# Nastavení argumentů příkazového řádku
parser = argparse.ArgumentParser(description='Analyzovat Q_value a E_trace z JSON souboru.')
parser.add_argument('filename', type=str, help='Název JSON souboru s daty.')
args = parser.parse_args()

# Kontrola, zda je soubor validní JSON
def is_valid_json_partial(file_path, num_lines=600002):
    try:
        with open(file_path, 'r') as file:
            lines = ''.join([next(file) for _ in range(num_lines)])
        # Find the last occurrence of the end of JSON array ']'
        end_index = lines.rfind(']')
        if end_index != -1:
            json_part = lines[:end_index+1]
            json.load(StringIO(json_part))  # Use StringIO to mimic a file object
            return True
        return False
    except (ValueError, StopIteration):
        return False


# Use the modified function in your script
if not is_valid_json_partial(args.filename):
    print(f"Soubor {args.filename} není validní JSON nebo neobsahuje dostatek řádků. Přeskakuji...")
    exit(1)

with open(args.filename, 'r') as file:
    data = json.load(file)

# Načtení dat ze souboru
with open(args.filename, 'r') as file:
    data = json.load(file)

# Uspořádání dat podle kombinací state a action
data_by_state_action = defaultdict(lambda: {"Q_value": [], "E_trace": []})

for entry in data:
    state_action = (entry["state"], entry["action"])
    data_by_state_action[state_action]["Q_value"].append(entry["Q_value"])
    data_by_state_action[state_action]["E_trace"].append(entry["E_trace"])

# Proměnné pro sledování největšího povrchu pod křivkou
max_auc = -float('inf')
max_state_action = None

# Proměnné pro sledování konvergence
convergence_results = {}

# Vytvoření grafů pro každou kombinaci state a action
for (state, action), values in data_by_state_action.items():
    q_values = values["Q_value"]
    num_steps = len(q_values)
    if num_steps <= 10:
        print(f'Přeskakuji graf pro state {state} a action {action} kvůli nedostatečnému počtu datových bodů.')
        continue
    
    start_index = int(0.5 * num_steps)
    end_index = int(0.85 * num_steps)
    if start_index < end_index:
        range_50_85 = q_values[start_index:end_index]
        if max(range_50_85) - min(range_50_85) > max(range_50_85) * 0.02:
            print(f'Špatná konfigurace pro state {state} a action {action} kvůli rozdílu mezi extrémy v rozsahu 50%-85%')
            continue
    
    plt.figure(figsize=(12, 6))

    # Graf pro Q_value
    plt.subplot(1, 2, 1)
    plt.plot(q_values, marker='o', label='Q_value')

    plt.title(f'Q_value pro state {state} a action {action}')
    plt.xlabel('Krok')
    plt.ylabel('Q_value')
    plt.legend()

    # Vypočítání plochy pod křivkou pro Q_value
    auc = simps(q_values, dx=1)
    if auc > max_auc:
        max_auc = auc
        max_state_action = (state, action)

    # Graf pro E_trace
    plt.subplot(1, 2, 2)
    plt.plot(values["E_trace"], marker='o', color='orange')
    plt.title(f'E_trace pro state {state} a action {action}')
    plt.xlabel('Krok')
    plt.ylabel('E_trace')

    # Uložení grafu do souboru
    plt.tight_layout()
    dir = 'log-agent-interactions/plots/' + args.filename.split('/')[1]
    plt.savefig(f'{dir}_plot_state_{state}_action_{action}.png')
    plt.close()

print("Grafy byly vytvořeny a uloženy jako PNG soubory.")

if max_state_action is not None:
    print(f'Největší plocha pod křivkou Q_value je {max_auc} pro kombinaci state {max_state_action[0]} a action {max_state_action[1]}')
else:
    print('Žádná konfigurace nesplňuje podmínky pro vytvoření grafu.')
