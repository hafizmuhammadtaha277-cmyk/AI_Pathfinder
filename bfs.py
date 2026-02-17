import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque

def bfs_visualized(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    visited = {start}
    queue = deque([start])
    parent = {start: None}  # Track where we came from
    states = []
    final_path = []

    found = False
    while queue:
        row, col = queue.popleft()
        
        # Capture state before exploring neighbors
        states.append({
            'current': (row, col),
            'visited': visited.copy(),
            'queue': list(queue),
            'path': [] 
        })

        if (row, col) == target:
            found = True
            break

        directions = [
        (-1, 0),   
        (0, 1),    
        (1, 0),    
        (1, 1),    
        (0, -1),   
        (-1, -1)   
        ]

        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                (nr, nc) not in visited and grid[nr][nc] != 1):
                visited.add((nr, nc))
                parent[(nr, nc)] = (row, col)
                queue.append((nr, nc))

    # Reconstruct path if target was reached
    if found:
        curr = target
        while curr is not None:
            final_path.append(curr)
            curr = parent[curr]
        final_path.reverse()
        
        # Add a final state to show the path clearly
        states.append({
            'current': target,
            'visited': visited,
            'queue': [],
            'path': final_path
        })

    return states, final_path

def visualize_bfs(grid, start, target):
    states, final_path = bfs_visualized(grid, start, target)
    rows, cols = len(grid), len(grid[0])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(right=0.75)

    def draw_grid(state_idx):
        ax.clear()
        active_idx = min(state_idx, len(states) - 1)
        curr_state = states[active_idx]
        path_cells = curr_state.get('path', [])

        for i in range(rows):
            for j in range(cols):
                # Logic for coloring
                if grid[i][j] == 1: color = 'black'
                elif (i, j) == start: color = 'green'
                elif (i, j) == target: color = 'orange'
                elif (i, j) in path_cells: color = 'magenta' # Final Path color
                elif (i, j) == curr_state['current']: color = 'red'
                elif (i, j) in curr_state['queue']: color = 'yellow'
                elif (i, j) in curr_state['visited']: color = 'lightblue'
                else: color = 'white'
                
                rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                         linewidth=1, edgecolor='gray', facecolor=color)
                ax.add_patch(rect)

        # Draw the path line for better visualization at the end
        if path_cells:
            py, px = zip(*path_cells)
            ax.plot(px, py, color='white', linewidth=3, alpha=0.8)

        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.invert_yaxis()
        ax.set_aspect('equal')
        
        if path_cells:
            ax.set_title("Path Found!", fontsize=15, fontweight='bold')
        else:
            ax.set_title(f"BFS Searching... Step {state_idx}", fontsize=12)

        legend_elements = [
            patches.Patch(facecolor='green', label='Start'),
            patches.Patch(facecolor='orange', label='Target'),
            patches.Patch(facecolor='red', label='Current'),
            patches.Patch(facecolor='magenta', label='Final Path'),
            patches.Patch(facecolor='lightblue', label='Visited'),
            patches.Patch(facecolor='black', label='Obstacle')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))

    ani = FuncAnimation(fig, draw_grid, frames=len(states), interval=200, repeat=False)
    plt.show()

# Grid and execution
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

visualize_bfs(grid, (0, 0), (4, 4))