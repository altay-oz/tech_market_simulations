# Learning in networks: An agent based simulation

Simulation code for the chapter Özaygen, Özman (2021). "LLearning in networks: An agent based simulation" in Handbook of Research Methods and Applications in Industrial Dynamics and Evolutionary Economics, ed. Uwe Cantner, Marco Guerzoni and Simone Vannuccini.


The simulation is run on python 2.7.

$ python src/main/simul_tm.py

Parameters are set on src/main/global_values.py

Output graphs are obtained with src/analyze_output/analyze_simulation_output.R You need to run R with igraph and ggplot2 libraries.

Tests are in directory src/test/ and all tests could be run with

$ python src/test/test_all.py
