import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque

def bidirectional_visualized(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    
    # Forward search
    q_f = deque([start])
    visited_f = {start: None} 
    
    # Backward search
    q_b = deque([goal])
    visited_b = {goal: None} 
    
    states = []
    directions = [
    (-1, 0),   
    (0, 1),    
    (1, 0),    
    (1, 1),    
    (0, -1),   
    (-1, -1)   
]

    intersect_node = None
    final_path = []

    while q_f and q_b:
        # --- Step Forward ---
        curr_f = q_f.popleft()
        for dr, dc in directions:
            nr, nc = curr_f[0] + dr, curr_f[1] + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                grid[nr][nc] != 1 and (nr, nc) not in visited_f):
                visited_f[(nr, nc)] = curr_f
                q_f.append((nr, nc))
                if (nr, nc) in visited_b:
                    intersect_node = (nr, nc)
                    break
        if intersect_node: break
        
        # --- Step Backward ---
        curr_b = q_b.popleft()
        for dr, dc in directions:
            nr, nc = curr_b[0] + dr, curr_b[1] + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                grid[nr][nc] != 1 and (nr, nc) not in visited_b):
                visited_b[(nr, nc)] = curr_b
                q_b.append((nr, nc))
                if (nr, nc) in visited_f:
                    intersect_node = (nr, nc)
                    break
                    
        states.append({
            'forward_visited': set(visited_f.keys()),
            'backward_visited': set(visited_b.keys()),
            'current_f': curr_f,
            'current_b': curr_b,
            'intersect': intersect_node,
            'path': []
        })
        if intersect_node: break

    # --- Reconstruct Path ---
    if intersect_node:
        # Trace back to start
        path_f = []
        curr = intersect_node
        while curr is not None:
            path_f.append(curr)
            curr = visited_f[curr]
        path_f.reverse()

        # Trace back to goal
        path_b = []
        curr = visited_b[intersect_node] # Start from parent of intersect in backward search
        while curr is not None:
            path_b.append(curr)
            curr = visited_b[curr]
        
        final_path = path_f + path_b
        
        # Add final state with path
        states.append({
            'forward_visited': set(visited_f.keys()),
            'backward_visited': set(visited_b.keys()),
            'current_f': None,
            'current_b': None,
            'intersect': intersect_node,
            'path': final_path
        })
            
    return states

def visualize_bidirectional(grid, start, goal):
    states = bidirectional_visualized(grid, start, goal)
    rows, cols = len(grid), len(grid[0])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(right=0.7)

    def draw_grid(state_idx):
        ax.clear()
        active_idx = min(state_idx, len(states) - 1)
        curr_state = states[active_idx]
        path_cells = curr_state.get('path', [])

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1: color = 'black'
                elif (i, j) == start: color = 'green'
                elif (i, j) == goal: color = 'purple'
                elif (i, j) in path_cells: color = 'magenta'
                elif curr_state['intersect'] and (i, j) == curr_state['intersect']: color = 'red'
                elif (i, j) in curr_state['forward_visited']: color = 'lightblue'
                elif (i, j) in curr_state['backward_visited']: color = 'lightpink'
                else: color = 'white'
                
                rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                         linewidth=1, edgecolor='gray', facecolor=color)
                ax.add_patch(rect)
                ax.text(j, i, f'({i},{j})', ha='center', va='center', fontsize=8, color='darkgray')

        if path_cells:
            py, px = zip(*path_cells)
            ax.plot(px, py, color='white', linewidth=3, alpha=0.8)

        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.invert_yaxis()
        ax.set_aspect('equal')
        
        # Sidebar Info
        if path_cells:
            status_text = f"--- PATH FOUND ---\n\nIntersected at: {curr_state['intersect']}\nPath Length: {len(path_cells)}"
        elif state_idx < len(states):
            status_text = (f"--- SEARCHING ---\n\nStep: {state_idx + 1}\n\n"
                           f"Forward: {curr_state['current_f']}\n"
                           f"Backward: {curr_state['current_b']}")
        else:
            status_text = "--- COMPLETE ---"

        ax.text(cols + 0.3, rows // 2, status_text, fontsize=13, fontweight='bold', 
                va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
        
        legend_elements = [
            patches.Patch(facecolor='green', label='Start (Forward)'),
            patches.Patch(facecolor='purple', label='Goal (Backward)'),
            patches.Patch(facecolor='magenta', label='Final Path'),
            patches.Patch(facecolor='lightblue', label='Forward Visited'),
            patches.Patch(facecolor='lightpink', label='Backward Visited'),
            patches.Patch(facecolor='red', label='Intersection Point')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))

    ani = FuncAnimation(fig, draw_grid, frames=len(states), interval=400, repeat=False)
    plt.show()

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

visualize_bidirectional(grid, (0, 0), (4, 4))