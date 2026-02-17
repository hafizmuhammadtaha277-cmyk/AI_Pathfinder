import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import heapq

def ucs_visualized(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    # visited stores the minimum cost to reach a node
    visited = {}
    # priority_queue stores (cost, current_node)
    priority_queue = [(0, start)]
    parent = {start: None}
    states = []
    final_path = []
    
    found = False
    while priority_queue:
        cost, (r, c) = heapq.heappop(priority_queue)
        
        if (r, c) in visited and visited[(r, c)] <= cost:
            continue
            
        visited[(r, c)] = cost
        
        # Capture state for animation
        states.append({
            'current': (r, c),
            'visited': visited.copy(),
            'queue': list(priority_queue),
            'cost': cost,
            'path': []
        })

        if (r, c) == target:
            found = True
            break
            
        # Directions: Up, Right, Down, Left, and 4 diagonals
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1):
                # In this grid, each step has a cost of 1
                new_cost = cost + 1
                if (nr, nc) not in visited or new_cost < visited[(nr, nc)]:
                    parent[(nr, nc)] = (r, c)
                    heapq.heappush(priority_queue, (new_cost, (nr, nc)))
    
    if found:
        curr = target
        while curr is not None:
            final_path.append(curr)
            curr = parent.get(curr)
        final_path.reverse()
        
        # Add a final state to show the path
        states.append({
            'current': target,
            'visited': visited,
            'queue': [],
            'cost': cost,
            'path': final_path
        })
    
    return states

def visualize_ucs(grid, start, target):
    states = ucs_visualized(grid, start, target)
    rows, cols = len(grid), len(grid[0])
    
    fig, ax = plt.subplots(figsize=(14, 8))
    plt.subplots_adjust(right=0.7) 

    def draw_grid(state_idx):
        ax.clear()
        active_idx = min(state_idx, len(states) - 1)
        curr_state = states[active_idx]
        path_cells = curr_state.get('path', [])
        in_queue = [pos for cost, pos in curr_state['queue']]

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 1: color = 'black'
                elif (i, j) == start: color = 'green'
                elif (i, j) == target: color = 'orange'
                elif (i, j) in path_cells: color = 'magenta'
                elif (i, j) == curr_state['current']: color = 'red'
                elif (i, j) in in_queue: color = 'yellow'
                elif (i, j) in curr_state['visited']: color = 'lightblue'
                else: color = 'white'
                
                rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                         linewidth=1, edgecolor='gray', facecolor=color)
                ax.add_patch(rect)
                
                label = f'({i},{j})'
                if (i, j) in curr_state['visited']:
                    label += f'\nC:{curr_state["visited"][(i,j)]}'
                ax.text(j, i, label, ha='center', va='center', fontsize=7, color='darkgray')

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
            status_text = f"--- UCS SUCCESS ---\n\nPath Found!\nTotal Cost: {curr_state['cost']}"
        elif state_idx < len(states):
            status_text = (f"--- UCS STATUS ---\n\nStep: {state_idx + 1}\n"
                           f"Current Cost: {curr_state['cost']}\n"
                           f"Queue Size: {len(curr_state['queue'])}")
        else:
            status_text = "--- UCS COMPLETE ---\n\nNo Path Found"

        ax.text(cols + 0.3, rows // 2, status_text, fontsize=13, fontweight='bold', 
                va='center', bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))
        
        legend_elements = [
            patches.Patch(facecolor='green', label='Start'),
            patches.Patch(facecolor='orange', label='Target'),
            patches.Patch(facecolor='magenta', label='Final Path'),
            patches.Patch(facecolor='red', label='Current'),
            patches.Patch(facecolor='yellow', label='In Priority Queue'),
            patches.Patch(facecolor='lightblue', label='Visited'),
            patches.Patch(facecolor='black', label='Obstacle')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))

    ani = FuncAnimation(fig, draw_grid, frames=len(states), interval=300, repeat=False)
    plt.show()

grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

visualize_ucs(grid, (0, 0), (4, 4))