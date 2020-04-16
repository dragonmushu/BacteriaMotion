import tkinter as tk
import time
from constants import *

window = tk.Tk()
window.title("bacteria motion")
frame = tk.Canvas(window, width=FRAME_WIDTH + MAZE_WIDTH, height=FRAME_HEIGHT + MAZE_WIDTH, background="white")
frame.pack()

maze = Maze(MAZE_CELLS, MAZE_CELLS, 0, 0)
maze.make_maze()
maze.draw_maze(frame)

number_bacteria = 10
bacteria = [] #[Bacteria(10, 10, 15, FRAME_WIDTH, FRAME_HEIGHT) for i in range(0, number_bacteria)]
for bacterium in bacteria:
    bacterium.draw(frame)

delta = 0
while True:
    start_time = time.time()

    # delete objects
    for bacterium in bacteria:
        bacterium.remove(frame)
    # update bacteria
    for bacterium in bacteria:
        bacterium.update(frame, delta, maze)
    # draw  object
    for bacterium in bacteria:
        bacterium.draw(frame)

    frame.update()
    window.update()

    elapsed_time = time.time() - start_time
    # noinspection PyUnresolvedReferences
    if elapsed_time < 1/FPS:
        # noinspection PyUnresolvedReferences
        sleep_time = 1 / FPS - elapsed_time
        time.sleep(sleep_time)
    delta = time.time() - start_time
