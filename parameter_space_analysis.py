import getopt, sys, os
import numpy as np
def main():
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["n="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    with open('parameter_space_analysis.log', 'w') as f:
        for opt, arg in opts:
            for i in range(int(arg)):
                l_values = np.linspace(0.4, 0.9, 3)
                a_values = np.linspace(0.1, 0.55, 3)
                e_values = np.linspace(0.005, 0.1, 3)
                g_values = np.linspace(0.6, 0.99, 3)
            
                for l_ in l_values:
                    for a_ in a_values:
                        for e_ in e_values:
                            for g_ in g_values:
                            # Write the configuration to the file
                                f.write(f"Sarsa_l,{a_:.2f},{l_:.2f},{e_:.3f},{g_:.2f}\n")

    #Sarsa_l,0.0,0.0,0.5,0.04,0.6 
	#Sarsa_l,0.0,0.0,0.5,0.03,0.6 
	#Sarsa_l,0.0,0.0,0.5,0.02,0.8 
	#Sarsa_l,0.0,0.0,0.5,0.01,0.9 
	#Sarsa_l,0.0,0.0,0.5,0.005,0.95
    # 0.49-0.55, 0.49-0.55, 0.005-0.04, 0.6-0.95



if __name__ == "__main__":
    main()