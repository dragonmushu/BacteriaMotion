# BacteriaMotion
Maze solving bacteria simulator

GUI Features 
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
     
  

