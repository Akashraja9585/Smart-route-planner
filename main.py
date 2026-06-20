import pygame
import heapq
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Route Planner")

BG_COLOR = (30, 30, 46)
NODE_COLOR = (233, 69, 96)
EDGE_COLOR = (90, 90, 110)
VISITED_COLOR = (244, 162, 97)
PATH_COLOR = (43, 147, 72)
START_COLOR = (52, 152, 219)
END_COLOR = (155, 89, 182)
TEXT_COLOR = (255, 255, 255)

FONT = pygame.font.SysFont('segoeui', 20)
SMALL_FONT = pygame.font.SysFont('segoeui', 15)

# Cities as (name, x, y)
cities = {
    "Chennai": (650, 480),
    "Bangalore": (480, 420),
    "Coimbatore": (420, 500),
    "Madurai": (520, 560),
    "Trichy": (560, 510),
    "Hyderabad": (550, 250),
    "Mumbai": (300, 200),
    "Pune": (330, 260),
    "Delhi": (450, 60),
    "Kolkata": (750, 220),
}

# Roads as (cityA, cityB, distance in km)
roads = [
    ("Chennai", "Bangalore", 350),
    ("Chennai", "Trichy", 320),
    ("Bangalore", "Coimbatore", 365),
    ("Coimbatore", "Madurai", 220),
    ("Trichy", "Madurai", 130),
    ("Bangalore", "Hyderabad", 570),
    ("Hyderabad", "Mumbai", 710),
    ("Hyderabad", "Pune", 560),
    ("Mumbai", "Pune", 150),
    ("Mumbai", "Delhi", 1400),
    ("Pune", "Delhi", 1450),
    ("Delhi", "Kolkata", 1500),
    ("Hyderabad", "Kolkata", 1500),
    ("Chennai", "Hyderabad", 630),
]

# Build adjacency list (graph)
graph = {city: [] for city in cities}
for a, b, dist in roads:
    graph[a].append((b, dist))
    graph[b].append((a, dist))

start_node = None
end_node = None
visited_order = []
final_path = []
total_distance = 0
status_text = "Click a city to set START point"


def dijkstra(start, end):
    """Returns (visited_order, shortest_path, total_distance)"""
    distances = {city: float('inf') for city in cities}
    distances[start] = 0
    previous = {city: None for city in cities}
    visited = set()
    order = []

    pq = [(0, start)]

    while pq:
        current_dist, current_city = heapq.heappop(pq)

        if current_city in visited:
            continue

        visited.add(current_city)
        order.append(current_city)

        if current_city == end:
            break

        for neighbor, weight in graph[current_city]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_city
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    if distances[end] == float('inf'):
        return order, [], None

    return order, path, distances[end]


def get_clicked_city(pos):
    for city, (x, y) in cities.items():
        if math.hypot(pos[0] - x, pos[1] - y) < 20:
            return city
    return None


def draw():
    screen.fill(BG_COLOR)

    # Draw roads
    for a, b, dist in roads:
        x1, y1 = cities[a]
        x2, y2 = cities[b]
        pygame.draw.line(screen, EDGE_COLOR, (x1, y1), (x2, y2), 2)
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        dist_label = SMALL_FONT.render(str(dist), True, (140, 140, 160))
        screen.blit(dist_label, (mid_x, mid_y))

    # Draw path (final shortest route) on top of roads
    if final_path:
        for i in range(len(final_path) - 1):
            x1, y1 = cities[final_path[i]]
            x2, y2 = cities[final_path[i + 1]]
            pygame.draw.line(screen, PATH_COLOR, (x1, y1), (x2, y2), 5)

    # Draw cities (nodes)
    for city, (x, y) in cities.items():
        color = NODE_COLOR
        if city in visited_order and city not in final_path:
            color = VISITED_COLOR
        if city in final_path:
            color = PATH_COLOR
        if city == start_node:
            color = START_COLOR
        if city == end_node:
            color = END_COLOR

        pygame.draw.circle(screen, color, (x, y), 14)
        label = SMALL_FONT.render(city, True, TEXT_COLOR)
        screen.blit(label, (x - 25, y - 32))

    # Status bar
    title = FONT.render("Smart Route Planner — Dijkstra's Algorithm", True, TEXT_COLOR)
    screen.blit(title, (20, 15))

    status = SMALL_FONT.render(status_text, True, (200, 200, 200))
    screen.blit(status, (20, 45))

    if total_distance:
        dist_text = SMALL_FONT.render(f"Shortest distance: {total_distance} km   Path: {' -> '.join(final_path)}", True, PATH_COLOR)
        screen.blit(dist_text, (20, HEIGHT - 60))

    instructions = SMALL_FONT.render("Click START city, then click END city. Press R to reset.", True, (150, 150, 150))
    screen.blit(instructions, (20, HEIGHT - 30))

    pygame.display.update()


def reset():
    global start_node, end_node, visited_order, final_path, total_distance, status_text
    start_node = None
    end_node = None
    visited_order = []
    final_path = []
    total_distance = 0
    status_text = "Click a city to set START point"


def main():
    global start_node, end_node, visited_order, final_path, total_distance, status_text

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = get_clicked_city(event.pos)
                if clicked:
                    if start_node is None:
                        start_node = clicked
                        status_text = f"START set to {clicked}. Now click END city."
                    elif end_node is None and clicked != start_node:
                        end_node = clicked
                        status_text = f"Finding shortest path from {start_node} to {end_node}..."
                        visited_order, final_path, total_distance = dijkstra(start_node, end_node)
                        if total_distance:
                            status_text = f"Shortest path found from {start_node} to {end_node}!"
                        else:
                            status_text = f"No path exists between {start_node} and {end_node}"

        draw()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()