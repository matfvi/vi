#! /bin/sh
# Na vasem sistemu potrebno je da bude instaliran program 'dot'
# koji koristeci 'graphviz' moze da crta grafove iz .dot datoteka.
# Ubuntu: sudo apt-get install graphviz
# ArchLinux: sudo pacman -S graphviz
# Windows: https://graphviz.gitlab.io/download/

echo "Running skript for visualization..."
python visualize_maze.py
echo "Done! Generated the_maze.dot file for the graph."
echo "Running graphivz for drawing..."
dot -Tpng the_maze.dot -o graph.png
echo "Done! Drawn graph and saved it at 'graph.png'"
