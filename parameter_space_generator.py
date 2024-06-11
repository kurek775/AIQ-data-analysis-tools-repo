import getopt, sys, os
import numpy as np

def main():
    no_l_config = set()
    l_config = set()
    with open('parameter_space_analysis.log', 'w') as f:
                l_values = np.linspace(0.4, 0.9, 3)
                a_values = np.linspace(0.1, 0.55, 3)
                e_values = np.linspace(0.005, 0.1, 3)
                g_values = np.linspace(0.6, 0.99, 3)
            
                for l_ in l_values:
                    for a_ in a_values:
                        for e_ in e_values:
                            for g_ in g_values:
                                l_config.add(f"Sarsa_l,0,{l_:.2f},{a_:.2f},{e_:.3f},{g_:.2f}")
                                no_l_config.add(f"Sarsa_l,0,0,{a_:.2f},{e_:.3f},{g_:.2f}")
            
    
                for config in no_l_config:
                    f.write(f"{config}\n")

                for config in l_config:
                    f.write(f"{config}\n")
if __name__ == "__main__":
    main()