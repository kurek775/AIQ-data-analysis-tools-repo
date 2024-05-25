import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_json('BF(5)_1.0_100000_Sarsa_l(0.0,0.0,0.5,0.04,0.6)_2024_0524_16_33_47.log', lines=True)

# Extract Q_value and E_trace into their own columns
df[['Q_value', 'E_trace']] = pd.json_normalize(df['agent_log'])

# Convert time_stamp to datetime
df['time_stamp'] = pd.to_datetime(df['time_stamp'], format='%Y_%m%d_%H:%M:%S.%f')

# Ignore rows where both Q_value and E_trace are zero
df = df[~((df['Q_value'] == 0))]

# Plot Q_value and E_trace against time_stamp
plt.figure(figsize=(12, 6))
plt.plot(df['time_stamp'], df['Q_value'], label='Q_value')
plt.plot(df['time_stamp'], df['E_trace'], label='E_trace')
plt.xlabel('Time Stamp')
plt.ylabel('Value')
plt.title('Q_value and E_trace over time')
plt.legend()
plt.show()