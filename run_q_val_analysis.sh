mkdir -p log-agent-interactions/plots

find log-agent-interactions -type f | while read soubor; do 
  python q_value_analysis.py "$soubor"
done