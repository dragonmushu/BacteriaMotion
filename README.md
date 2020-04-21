# BacteriaMotion
Gui simulating bacterial motion solving mazes compared to standard algorithms.

# Motivation
The ability of an organism to solve a maze is a non-trivial way to evaluate organismal intelligence. In fact, this method has been used to evaluate and compare the intelligence of humans, monkeys, other mammals, and more. One of the areas that is currently less explored is the intelligence of bacteria in a maze-solving context; however, due to advancements in microfluidics, it now poses as an interesting way to better study their space searching and partitioning algorithms. By studying how bacteria move through a maze and explore paths, it will allow us to create search algorithms inspired by their methods for use in a variety of applications. 

# Installation

# Features

- Maze Options
    - Singlepath: the default maze generated, can persist for multiple simulations
    - Multipath: knocks down walls of a single path math to generate the maze
- Simulation Options
    - Bacteria: The following parameters are required to run the bacterial simulation
        - Run Velocity (um/s)
        - Tumble Velocity (um/s)
        - Tumble Angular Velocity (rad/s)
        - Run Time (s)
        - Tumble Time (s) 
        - Bacteria type
            - input (the user enters in values for the parameters listed above)
            - e.coli (the simulator uses values obtained from literature to serialize the parameters)
    - Random Walk
    - Left wall follow
    - Right wall follow
- BFS
    - this feature allows the user to see the shortest path distance for the solved maze
- Statistics Panel: displays the following fields of information
    - Total time (s)
    - Number of cells explored (cells)
    - Percent Exploration (%)
    - Route Distance (cells)
     
  

