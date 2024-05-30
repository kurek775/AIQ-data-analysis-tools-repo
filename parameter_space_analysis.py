import getopt, sys, os
import random
def main():
 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["n="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        for i in range(int(arg)):
            l_ = round(random.uniform(0.49,0.55),2)
            a_ = round(random.uniform(0.49,0.55),2)
            e_ = round(random.uniform(0.005,0.04),3)
            g_ = round(random.uniform(0.6,0.95),2)
            print(str(a_) + " " + str(l_) + " " + str(e_) + " " + str(g_))

    #Sarsa_l,0.0,0.0,0.5,0.04,0.6 
	#Sarsa_l,0.0,0.0,0.5,0.03,0.6 
	#Sarsa_l,0.0,0.0,0.5,0.02,0.8 
	#Sarsa_l,0.0,0.0,0.5,0.01,0.9 
	#Sarsa_l,0.0,0.0,0.5,0.005,0.95
    # 0.49-0.55, 0.49-0.55, 0.005-0.04, 0.6-0.95



if __name__ == "__main__":
    main()