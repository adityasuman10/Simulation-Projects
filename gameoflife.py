import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):

    return np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):

    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider

def addGosperGliderGun(i, j, grid):

    gun = np.zeros((11, 38))
    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i:i + 11, j:j + 38] = gun

def update(frameNum, img, grid, N):

    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)

            if grid[i, j] == ON:
                if total < 2 or total > 3:
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def run_simulation():

    root = tk.Tk()
    root.title("playground")

    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

  
    usable_width = int(screen_width * 0.8)
    usable_height = int(screen_height * 0.8)


    cell_size = 10


    N_width = usable_width // cell_size
    N_height = usable_height // cell_size
    N = min(N_width, N_height)

   
    grid = randomGrid(N)


    fig, ax = plt.subplots(figsize=(usable_width / 100, usable_height / 100))
    ax.set_title("")
    img = ax.imshow(grid, interpolation='nearest', cmap='gray')

   
    ax.grid(True, color='purple', linewidth=0.5)
    ax.set_xticks(np.arange(-0.5, N, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, N, 1), minor=True)
    ax.set_xlim(-0.5, N - 0.5)
    ax.set_ylim(N - 0.5, -0.5)

   
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

 
    running = [False]  

    def start_animation():
        if not running[0]:
            running[0] = True
            ani.event_source.start()
            start_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)

    def stop_animation():
        if running[0]:
            running[0] = False
            ani.event_source.stop()
            start_button.config(state=tk.NORMAL)
            stop_button.config(state=tk.DISABLED)

    def select_pattern(event):
        if not running[0]:
            pattern = pattern_var.get()
            grid.fill(OFF) 
            if pattern == "Random":
                grid[:] = randomGrid(N)
            elif pattern == "Glider":
                addGlider(1, 1, grid)
            elif pattern == "Gosper Glider Gun":
                addGosperGliderGun(5, 5, grid)

            img.set_data(grid)
            canvas.draw()

    
    control_frame = ttk.Frame(root)
    control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    pattern_var = tk.StringVar(value="Random")
    pattern_menu = ttk.OptionMenu(control_frame, pattern_var, "Random", "Random", "Glider", "Gosper Glider Gun", command=select_pattern)
    pattern_menu.pack(side=tk.LEFT, padx=5, pady=5)

    start_button = ttk.Button(control_frame, text="Start", command=start_animation)
    start_button.pack(side=tk.LEFT, padx=5, pady=5)

    stop_button = ttk.Button(control_frame, text="Stop", command=stop_animation)
    stop_button.pack(side=tk.LEFT, padx=5, pady=5)
    stop_button.config(state=tk.DISABLED)

    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N), interval=100, blit=False)

    root.mainloop()

if __name__ == '__main__':
    run_simulation()
