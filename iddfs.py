import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def dls_iteration(grid, start, target, limit, rows, cols):
    states = []
    visited_this_run = set()
    parent = {start: None} # Needed to reconstruct the path
    
    def recursive_dls(node, depth):
        if depth > limit:
            return False
        
        visited_this_run.add(node)
        row, col = node
        
        # Capture state for animation
        states.append({
            'current': node,
            'visited': visited_this_run.copy(),
            'depth': depth,
            'limit': limit,
            'path': []
        })

        if node == target:
            return True
        
        # Directions: Up, Right, Bottom, Bottom-Right, Left, Top-Left
        directions = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]
        
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and 
                grid[nr][nc] != 1 and (nr, nc) not in visited_this_run):
                parent[(nr, nc)] = node
                if recursive_dls((nr, nc), depth + 1):
                    return True
        return False

    found = recursive_dls(start, 0)
    
    final_path = []
    if found:
        # Reconstruct path by following parents back to start
        curr = target
        while curr is not None:
            final_path.append(curr)
            curr = parent.get(curr)
        final_path.reverse()
        
        # Add a final state to display the completed path
        states.append({
            'current': target,
            'visited': visited_this_run.copy(),
            'depth': limit,
            'limit': limit,
            'path': final_path
        })

    return states, found

def iddfs_visualized(grid, start, target, max_depth):
    rows, cols = len(grid), len(grid[0])
    all_animation_states = []
    
    for current_limit in range(max_depth + 1):
        iteration_results, found = dls_iteration(grid, start, target, current_limit, rows, cols)
        all_animation_states.extend(iteration_results)
        
        if found: # Found the path at the shallowest depth!
            break
            
    return all_animation_states

def visualize_iddfs(grid, start, target, max_depth):
    states = iddfs_visualized(grid, start, target, max_depth)
    rows, cols = len(grid), len(grid[0])
    
    # Using a larger width to prevent the sidebar from squashing the grid
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
                elif (i, j) in path_cells: color = 'magenta' # Final path
                elif (i, j) == curr_state['current']: color = 'red'
                elif (i, j) in curr_state['visited']: color = 'lightblue'
                else: color = 'white'
                
                rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                         linewidth=1, edgecolor='gray', facecolor=color)
                ax.add_patch(rect)
                ax.text(j, i, f'({i},{j})', ha='center', va='center', fontsize=8, color='darkgray')

        # Draw a line through the final path for clarity
        if path_cells:
            py, px = zip(*path_cells)
            ax.plot(px, py, color='white', linewidth=3, alpha=0.7)

        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.invert_yaxis()
        ax.set_aspect('equal')
        
        if path_cells:
            status_text = f"--- IDDFS SUCCESS ---\n\nPath Found at limit: {curr_state['limit']}\nLength: {len(path_cells)}"
        elif state_idx < len(states):
            status_text = (f"--- IDDFS STATUS ---\n\n"
                           f"CURRENT LIMIT: {curr_state['limit']}\n"
                           f"Step: {state_idx + 1}\n\n"
                           f"Exploring: {curr_state['current']}")
        else:
            status_text = "--- IDDFS COMPLETE ---\n\nNo path found."

        ax.text(cols + 0.3, rows // 2, status_text, fontsize=13, fontweight='bold', 
                va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
        
        legend_elements = [
            patches.Patch(facecolor='green', label='Start'),
            patches.Patch(facecolor='orange', label='Target'),
            patches.Patch(facecolor='magenta', label='Final Path'),
            patches.Patch(facecolor='red', label='Current'),
            patches.Patch(facecolor='lightblue', label='Visited (This iteration)'),
            patches.Patch(facecolor='black', label='Obstacle')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))

    ani = FuncAnimation(fig, draw_grid, frames=len(states), interval=150, repeat=False)
    plt.show()

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

visualize_iddfs(grid, (0, 0), (4, 4), max_depth=10)