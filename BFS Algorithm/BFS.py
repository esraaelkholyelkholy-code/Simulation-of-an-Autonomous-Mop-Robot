import pygame
import sys
from collections import deque

WIDTH, HEIGHT = 700, 700
ROWS, COLS = 25, 25 
CELL_SIZE = WIDTH // COLS
FPS = 60 

COLOR_DIRTY = (100, 100, 100)
COLOR_CLEAN = (236, 240, 241)
COLOR_WALL  = (44, 62, 80)
COLOR_ROBOT = (231, 76, 60)
WHITE       = (255, 255, 255)

def bfs_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1][1:]

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 0 and neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current
    return None

def generate_systematic_path(grid, start):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    full_path = []
    current_pos = start
    to_clean = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]
    
    while len(visited) < len(to_clean):
        unvisited = [p for p in to_clean if p not in visited]
        if not unvisited: break
        
        unvisited.sort(key=lambda p: abs(p[0]-current_pos[0]) + abs(p[1]-current_pos[1]))
        target = unvisited[0]
        
        segment = bfs_search(grid, current_pos, target)
        if segment:
            for step in segment:
                full_path.append(step)
                visited.add(step)
            current_pos = target
        else:
            visited.add(target) 
    return full_path

def create_room(grid):
    for r in range(ROWS): grid[r][0] = grid[r][COLS-1] = 1
    for c in range(COLS): grid[0][c] = grid[ROWS-1][c] = 1
    
    def add_obj(r, c, h, w):
        for i in range(h):
            for j in range(w):
                if 0 <= r+i < ROWS and 0 <= c+j < COLS: grid[r+i][c+j] = 1

    add_obj(4, 4, 4, 4)
    add_obj(15, 5, 2, 8)
    add_obj(5, 15, 10, 2)
    add_obj(18, 18, 3, 3)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Systematic BFS Cleaning Robot")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20, bold=True)

    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    create_room(grid)
    
    start_pos = (1, 1)
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

        win.fill(COLOR_DIRTY)
        for r in range(ROWS):
            for c in range(COLS):
                rect = (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (r, c) in cleaned:
                    pygame.draw.rect(win, COLOR_CLEAN, rect)
                    pygame.draw.rect(win, (220, 220, 220), rect, 1)
                if grid[r][c] == 1:
                    pygame.draw.rect(win, COLOR_WALL, rect)
        
        rx, ry = curr_pos[1] * CELL_SIZE, curr_pos[0] * CELL_SIZE
        pygame.draw.circle(win, COLOR_ROBOT, (rx + CELL_SIZE//2, ry + CELL_SIZE//2), CELL_SIZE//2 - 2)

        pygame.draw.rect(win, COLOR_WALL, (0, 0, WIDTH, 40))
        floor_tiles = sum(row.count(0) for row in grid)
        progress = (len(cleaned) / floor_tiles) * 100
        txt = font.render(f"BFS CLEANING: {progress:.1f}%", True, WHITE)
        win.blit(txt, (20, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()