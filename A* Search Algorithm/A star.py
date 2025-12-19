import pygame
import sys
import heapq

# --- 1. SETTINGS & THEME ---
WIDTH, HEIGHT = 700, 700
ROWS, COLS = 25, 25 
CELL_SIZE = WIDTH // COLS
FPS = 60 

# Colors
COLOR_DIRTY = (100, 100, 100)  # Dusty grey
COLOR_CLEAN = (236, 240, 241)  # Shiny off-white
COLOR_WALL  = (44, 62, 80)     # Furniture
COLOR_ROBOT = (46, 204, 113)   # Green
WHITE       = (255, 255, 255)

# --- 2. A* FOR NAVIGATION ---
def astar_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    def h(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    while open_list:
        current = heapq.heappop(open_list)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1: continue
                
                temp_g = g_score[current] + 1
                if neighbor not in g_score or temp_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g
                    f_score = temp_g + h(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor))
    return None

# --- 3. SYSTEMATIC COVERAGE LOGIC ---
def generate_systematic_path(grid, start):
    """Generates a lawnmower-style path, using A* to bypass obstacles."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    full_path = []
    current_pos = start
    
    # Identify all reachable floor tiles
    to_clean = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    
    while len(visited) < len(to_clean):
        # 1. Find the nearest uncleaned tile (using Manhattan for speed)
        unvisited = [p for p in to_clean if p not in visited]
        if not unvisited: break
        
        # Sort by distance to maintain a "lawnmower" flow
        unvisited.sort(key=lambda p: abs(p[0]-current_pos[0]) + abs(p[1]-current_pos[1]))
        target = unvisited[0]
        
        # 2. Use A* to find the path to that tile
        segment = astar_search(grid, current_pos, target)
        
        if segment:
            for step in segment:
                full_path.append(step)
                visited.add(step)
            current_pos = target
        else:
            # If unreachable, remove from list
            visited.add(target) 
            
    return full_path

# --- 4. MAP DESIGN ---
def create_room(grid):
    # Walls
    for r in range(ROWS): grid[r][0] = grid[r][COLS-1] = 1
    for c in range(COLS): grid[0][c] = grid[ROWS-1][c] = 1
    
    # Furniture blocks
    def add_obj(r, c, h, w):
        for i in range(h):
            for j in range(w):
                if 0 <= r+i < ROWS and 0 <= c+j < COLS: grid[r+i][c+j] = 1

    add_obj(4, 4, 4, 4)   # Table 1
    add_obj(15, 5, 2, 8)  # Sofa
    add_obj(5, 15, 10, 2) # Wall divider
    add_obj(18, 18, 3, 3) # Cabinet

# --- 5. MAIN EXECUTION ---
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Systematic A* Cleaning Robot")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20, bold=True)

    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    create_room(grid)
    
    start_pos = (1, 1)
    print("Planning systematic coverage...")
    path = generate_systematic_path(grid, start_pos)
    
    path_idx = 0
    cleaned = {start_pos}
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False

        if path_idx < len(path):
            curr_pos = path[path_idx]
            cleaned.add(curr_pos)
            path_idx += 1
        else:
            curr_pos = path[-1]

        # DRAWING
        win.fill(COLOR_DIRTY) # The "Dusty" Floor
        
        for r in range(ROWS):
            for c in range(COLS):
                rect = (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # 1. Draw Cleaned Areas
                if (r, c) in cleaned:
                    pygame.draw.rect(win, COLOR_CLEAN, rect)
                    pygame.draw.rect(win, (220, 220, 220), rect, 1) # Floor tile border
                
                # 2. Draw Obstacles
                if grid[r][c] == 1:
                    pygame.draw.rect(win, COLOR_WALL, rect)
        
        # 3. Draw Robot
        rx, ry = curr_pos[1] * CELL_SIZE, curr_pos[0] * CELL_SIZE
        pygame.draw.circle(win, COLOR_ROBOT, (rx + CELL_SIZE//2, ry + CELL_SIZE//2), CELL_SIZE//2 - 2)

        # Header UI
        pygame.draw.rect(win, COLOR_WALL, (0, 0, WIDTH, 40))
        floor_tiles = sum(row.count(0) for row in grid)
        progress = (len(cleaned) / floor_tiles) * 100
        txt = font.render(f"CLEANING PROGRESS: {progress:.1f}%", True, WHITE)
        win.blit(txt, (20, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()