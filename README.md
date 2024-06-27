# AIQ-data-analysis-tools-repo
- This repository contains the tools and scripts for data analysis and visualization of AIQ data.

## configurations_analysis
- This script turns basic _el results to working configurations for the AIQ data analysis tools.
- Each configuration of agent is one row of the output file.
- contains cols: Alg, Config, AIQ1K, SD1K, HCI1K ..... AIQ100K, SD100K, HCI100K (1,3,10,30,100)

## agent_desc_statistics
- This script generates csv descriptive statistics of each agent contained in the output file from configurations_analysis

## auc_best_configs_analysis
- This script generates csv with plot of best configurations for each agent based on the highest value at 100 000 EL. Also returns csv of AUC values of the best configs.

## same_configs_analysis
- This script pairs agents of Q, Sarsa with same configs and generates pair plot

## boxplot
- This script generates boxplot of the agents based on the output file from configurations_analysis

## reg_tree
- This script generates regression tree of the agents based on the output file from configurations_analysis

## previous_agents_formater
- This script formats the file with different structure, which was used by Ing. Ondřej Vadinský , Ph.D. to the format that can be worked with by the AIQ data analysis tools.


## parameter_space_generator
- This script generates parameter space of interval that you can configure. It basically generates all possible combinations of the parameters you want to test for agent Sarsa and SarsaLambda.