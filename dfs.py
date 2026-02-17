import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def dfs_visualized(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    stack = [start]
    parent = {start: None}
    states = []
    final_path = []
    found = False

    while stack:
        row, col = stack.pop()

        if (row, col) in visited:
            continue

        visited.add((row, col))

        # Save state before expanding neighbors
        states.append({
            'current': (row, col),
            'visited': visited.copy(),
            'stack': list(stack),
            'path': []
        })

        if (row, col) == target:
            found = True
            break

        # Required clockwise order
        directions = [
            (-1, 0),   # 1. Up
            (0, 1),    # 2. Right
            (1, 0),    # 3. Bottom
            (1, 1),    # 4. Bottom-Right (Diagonal)
            (0, -1),   # 5. Left
            (-1, -1)   # 6. Top-Left (Diagonal)
        ]

        # Reverse for correct DFS expansion order
        for dr, dc in reversed(directions):
            nr, nc = row + dr, col + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and
                grid[nr][nc] != 1):

                if (nr, nc) not in parent:  # prevent parent overwrite
                    parent[(nr, nc)] = (row, col)

                stack.append((nr, nc))

    # Reconstruct path if found
    if found:
        curr = target
        while curr is not None:
            final_path.append(curr)
            curr = parent.get(curr)
        final_path.reverse()

        states.append({
            'current': target,
            'visited': visited,
            'stack': [],
            'path': final_path
        })

    return states


def visualize_dfs(grid, start, target):
    states = dfs_visualized(grid, start, target)
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
                if grid[i][j] == 1:
                    color = 'black'
                elif (i, j) == start:
                    color = 'green'
                elif (i, j) == target:
                    color = 'orange'
                elif (i, j) in path_cells:
                    color = 'magenta'
                elif (i, j) == curr_state['current']:
                    color = 'red'
                elif (i, j) in curr_state['stack']:
                    color = 'yellow'
                elif (i, j) in curr_state['visited']:
                    color = 'lightblue'
                else:
                    color = 'white'

                rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                         linewidth=1,
                                         edgecolor='gray',
                                         facecolor=color)
                ax.add_patch(rect)

                ax.text(j, i, f'({i},{j})',
                        ha='center',
                        va='center',
                        fontsize=9,
                        color='darkgray')

        # Draw final path line
        if path_cells:
            py, px = zip(*path_cells)
            ax.plot(px, py, color='white', linewidth=3, alpha=0.8)

        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.invert_yaxis()
        ax.set_aspect('equal')

        # Sidebar text
        if path_cells:
            status_text = (
                "--- DFS COMPLETE ---\n\n"
                "PATH FOUND!\n\n"
                f"Path Length: {len(path_cells)}"
            )
            title_color = 'magenta'
        elif state_idx < len(states):
            curr = curr_state['current']
            status_text = (
                f"--- DFS STATUS ---\n\n"
                f"Step: {state_idx + 1}\n\n"
                f"Exploring: ({curr[0]}, {curr[1]})\n\n"
                f"Visited: {len(curr_state['visited'])}\n"
                f"In Stack: {len(curr_state['stack'])}"
            )
            title_color = 'black'
        else:
            status_text = "--- DFS STATUS ---\n\nCOMPLETE (No Path)"
            title_color = 'red'

        ax.text(cols * 1.1,
                rows / 2,
                status_text,
                fontsize=13,
                fontweight='bold',
                va='center',
                bbox=dict(facecolor='white',
                          alpha=0.8,
                          edgecolor='black'))

        ax.set_title("Depth First Search Visualization",
                     fontsize=16,
                     pad=20,
                     color=title_color)

        legend_elements = [
            patches.Patch(facecolor='green', label='Start'),
            patches.Patch(facecolor='orange', label='Target'),
            patches.Patch(facecolor='magenta', label='Final Path'),
            patches.Patch(facecolor='red', label='Current'),
            patches.Patch(facecolor='yellow', label='In Stack'),
            patches.Patch(facecolor='lightblue', label='Visited'),
            patches.Patch(facecolor='black', label='Obstacle')
        ]

        ax.legend(handles=legend_elements,
                  loc='upper left',
                  bbox_to_anchor=(1.05, 1),
                  borderaxespad=0.)

    ani = FuncAnimation(fig,
                        draw_grid,
                        frames=len(states),
                        interval=300,
                        repeat=False)

    plt.show()


# Grid
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

visualize_dfs(grid, (0, 0), (4, 4))
