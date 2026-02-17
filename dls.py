import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def dls_visualized(grid, start, target, limit):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    states = []
    parent = {start: None}
    final_path = []

    def recursive_dls(node, depth):
        if depth > limit:
            return False
        
        visited.add(node)
        row, col = node
        
        # Log state for animation
        states.append({
            'current': node,
            'visited': visited.copy(),
            'depth': depth,
            'path': []
        })

        if node == target:
            return True
        
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
                grid[nr][nc] != 1 and (nr, nc) not in visited):
                parent[(nr, nc)] = node
                if recursive_dls((nr, nc), depth + 1):
                    return True
        return False

    found = recursive_dls(start, 0)

    if found:
        curr = target
        while curr is not None:
            final_path.append(curr)
            curr = parent.get(curr)
        final_path.reverse()
        
        # Add final state to highlight the path
        states.append({
            'current': target,
            'visited': visited,
            'depth': len(final_path) - 1,
            'path': final_path
        })
    
    return states, final_path

def visualize_dls(grid, start, target, limit):
    states, final_path = dls_visualized(grid, start, target, limit)
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
                elif (i, j) == target: color = 'orange'
                elif (i, j) in path_cells: color = 'magenta'
                elif (i, j) == curr_state['current']: color = 'red'
                elif (i, j) in curr_state['visited']: color = 'lightblue'
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
        
        if path_cells:
            status_text = f"--- DLS SUCCESS ---\n\nTarget Found!\nPath Length: {len(path_cells)-1}"
        elif state_idx < len(states):
            status_text = (f"--- DLS SEARCHING ---\n\nLimit: {limit}\n"
                           f"Step: {state_idx + 1}\n"
                           f"Depth: {curr_state['depth']}\n\n"
                           f"Current: {curr_state['current']}")
        else:
            status_text = f"--- DLS COMPLETE ---\n\nNo Path Found\nwithin limit {limit}"

        ax.text(cols + 0.3, rows // 2, status_text, fontsize=13, fontweight='bold', 
                va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
        
        legend_elements = [
            patches.Patch(facecolor='green', label='Start'),
            patches.Patch(facecolor='orange', label='Target'),
            patches.Patch(facecolor='magenta', label='Final Path'),
            patches.Patch(facecolor='red', label='Current'),
            patches.Patch(facecolor='lightblue', label='Visited'),
            patches.Patch(facecolor='black', label='Obstacle')
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

# Note: If limit is too small (e.g., 3), it won't find (4,4)
visualize_dls(grid, (0, 0), (4, 4), limit=10)