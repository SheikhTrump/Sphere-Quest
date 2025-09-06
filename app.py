
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time, sys, random

# ---------------------------
# Window settings
# ---------------------------
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
ASPECT = WINDOW_WIDTH / WINDOW_HEIGHT

# ---------------------------
# Game physics
# ---------------------------
gravity = -500.0
jump_strength = 250.0
max_jump_duration = 0.35

# ---------------------------
# Ball properties
# ---------------------------
ball_radius = 15.0
ball_pos = [0.0, 0.0, ball_radius]
ball_vel = [0.0, 0.0, 0.0]
jumping = False
jump_start_time = 0.0

# ---------------------------
# Game state
# ---------------------------
score = 0
lives = 3
game_over = False
game_won = False
last_tile = None
time_on_tile = 0.0
max_tile_time = 5
show_timer = False
time_last = time.time()
move_keys = {"a": False, "d": False, "w": False, "s": False}
space_pressed = False
difficulty_timer = None
difficulty_mode = False
camera_distance = 500.0
camera_angle = 45
camera_height = 300.0
wall_height = 80.0

# ---------------------------
# Grid settings
# ---------------------------
grid_size_x = 30
grid_size_y = 20
tile_size = 60
half_size_x = grid_size_x * tile_size / 2
half_size_y = grid_size_y * tile_size / 2

# ---------------------------
# Themes
# ---------------------------
themes = ["default", "dark", "desert", "ice", "space", "lava", "forest", "neon", "sunset", "ocean"]
theme = "default"
theme_colors = {
    "default": {"floor1": (0.302, 0.471, 0.388), "floor2": (0.8, 0.8, 0.8), "wall": (0.2, 0.2, 0.8), "hole": (0.0, 0.0, 0.0)},
    "dark": {"floor1": (0.1, 0.1, 0.1), "floor2": (0.3, 0.3, 0.3), "wall": (0.2, 0.2, 0.8), "hole": (0.5, 0.0, 0.0)},
    "desert": {"floor1": (0.761, 0.698, 0.502), "floor2": (0.9, 0.8, 0.6), "wall": (0.8, 0.7, 0.5), "hole": (0.4, 0.3, 0.1)},
    "ice": {"floor1": (0.8, 0.9, 1.0), "floor2": (0.9, 0.95, 1.0), "wall": (0.7, 0.8, 1.0), "hole": (0.2, 0.5, 0.8)},
    "space": {"floor1": (0.1, 0.1, 0.2), "floor2": (0.2, 0.2, 0.3), "wall": (0.1, 0.1, 0.3), "hole": (0.0, 0.0, 0.3)},
    "lava": {"floor1": (0.8, 0.2, 0.1), "floor2": (0.9, 0.4, 0.2), "wall": (0.8, 0.3, 0.1), "hole": (0.5, 0.0, 0.0)},
    "forest": {"floor1": (0.2, 0.5, 0.2), "floor2": (0.3, 0.6, 0.3), "wall": (0.3, 0.6, 0.3), "hole": (0.1, 0.3, 0.1)},
    "neon": {"floor1": (0.1, 0.8, 0.8), "floor2": (0.8, 0.1, 0.8), "wall": (0.1, 0.8, 0.8), "hole": (0.8, 0.1, 0.8)},
    "sunset": {"floor1": (0.9, 0.5, 0.2), "floor2": (0.8, 0.4, 0.1), "wall": (0.8, 0.4, 0.1), "hole": (0.4, 0.2, 0.1)},
    "ocean": {"floor1": (0.2, 0.4, 0.8), "floor2": (0.3, 0.5, 0.9), "wall": (0.2, 0.4, 0.8), "hole": (0.1, 0.2, 0.4)}
}

# ---------------------------
# Game objects
# ---------------------------
obstacles = []
collectibles = []
special_points = []
holes = set()
speed_multiplier = 1.0

# ---------------------------
# Power-ups
# ---------------------------
shields = [{'pos': [200, 200, 15], 'collected': False}, {'pos': [-200, -200, 15], 'collected': False}]
shield_active = False
shield_time = 0

# ---------------------------
# Moving platforms
# ---------------------------
moving_platforms = [
    {'pos': [0, 0, 25], 'size': [80, 30, 8], 'vel': [60, 0, 0], 'limits': [-250, 250]},
    {'pos': [150, -150, 30], 'size': [50, 50, 8], 'vel': [0, 60, 0], 'limits': [-200, 200]},
]

# ---------------------------
# Teleporters
# ---------------------------
teleporters = [
    {'pos': [300, 300, 15], 'target': [-300, -300, 15]},
    {'pos': [-300, 300, 15], 'target': [300, -300, 15]},
]

# ---------------------------
# Speed boosts / slows / etc.
# ---------------------------
speed_boosts = [
    {'pos': [150, 150, 15], 'active': True, 'duration': 5.0},
    {'pos': [-150, -150, 15], 'active': True, 'duration': 5.0},
]
speed_boost_active = False
speed_boost_timer = 0.0

slow_traps = [
    {'pos': [150, -150, 15], 'active': True, 'duration': 3.0},
    {'pos': [-150, 150, 15], 'active': True, 'duration': 3.0},
]
slow_trap_active = False
slow_trap_timer = 0.0

time_bonuses = [
    {'pos': [250, 250, 15], 'active': True, 'time': 3.0},
    {'pos': [-250, -250, 15], 'active': True, 'time': 3.0},
]

life_collectibles = [
    {'pos': [300, 0, 15], 'active': True},
    {'pos': [-300, 0, 15], 'active': True},
]

multipliers = [
    {'pos': [0, 300, 15], 'active': True, 'duration': 10.0, 'factor': 2},
]
multiplier_active = False
multiplier_timer = 0.0
multiplier_factor = 1

# ---------------------------
# Level progression
# ---------------------------
level = 1
max_level = 10

# ---------------------------
# Pause, scoring, camera
# ---------------------------
paused = False
high_score = 0
camera_mode = "follow"  # "follow", "overhead", "first_person"
ball_color = [1.0, 0.2, 0.2]  # Default red
particles = []

# ---------------------------
# Lighting / Skybox
# ---------------------------
light_position = [0.0, 0.0, 500.0, 1.0]   # <-- FIX: must be length 4
light_color = [1.0, 1.0, 1.0, 1.0]
ambient_light = [0.3, 0.3, 0.3, 1.0]
skybox_size = 2000

# ---------------------------
# Game state management
# ---------------------------
game_state = "menu"  # "menu", "playing", "paused", "game_over", "win", "help"
font = GLUT_BITMAP_HELVETICA_18

# ---------------------------
# Helpers
# ---------------------------
def generate_holes():
    global holes
    holes = set()
    num_holes = min(30 + level * 3, 150)
    while len(holes) < num_holes:
        i = random.randint(0, grid_size_x - 1)
        j = random.randint(0, grid_size_y - 1)
        # Don't place holes near the starting position
        if abs(i - grid_size_x//2) > 3 or abs(j - grid_size_y//2) > 3:
            holes.add((i, j))

def find_safe_tile():
    while True:
        i = random.randint(0, grid_size_x - 1)
        j = random.randint(0, grid_size_y - 1)
        if (i, j) not in holes:
            x = i * tile_size - half_size_x + tile_size / 2
            y = j * tile_size - half_size_y + tile_size / 2
            return (x, y)

def find_safe_start_tile():
    # Find a safe tile near the center
    center_i = grid_size_x // 2
    center_j = grid_size_y // 2
    for radius in range(0, max(grid_size_x, grid_size_y)):
        for i in range(center_i - radius, center_i + radius + 1):
            for j in range(center_j - radius, center_j + radius + 1):
                if 0 <= i < grid_size_x and 0 <= j < grid_size_y and (i, j) not in holes:
                    x = i * tile_size - half_size_x + tile_size / 2
                    y = j * tile_size - half_size_y + tile_size / 2
                    return [x, y, ball_radius]
    return [0.0, 0.0, ball_radius]

def reset_game(reset_score=True, reset_lives=True):
    global ball_pos, ball_vel, jumping, jump_start_time, score, lives, game_over, game_won
    global collectibles, time_last, obstacles, last_tile, time_on_tile, show_timer, special_points
    global difficulty_timer, difficulty_mode, speed_multiplier, level, paused, high_score
    global speed_boost_active, speed_boost_timer, slow_trap_active, slow_trap_timer
    global multiplier_active, multiplier_timer, multiplier_factor, ball_color, particles
    global shield_active, shield_time, game_state

    if score > high_score:
        high_score = score

    ball_pos[:] = find_safe_start_tile()
    ball_vel[:] = [0.0, 0.0, 0.0]
    jumping = False
    jump_start_time = 0.0

    if reset_score:
        score = 0
        generate_holes()
        collectibles = []
        for _ in range(15 + level * 2):
            x, y = find_safe_tile()
            collectibles.append({
                'type': random.choice(['cube', 'torus', 'pyramid', 'sphere', 'teapot']),
                'pos': (x, y, 15),
                'color': (random.random(), random.random(), random.random())
            })

        special_points = []
        for _ in range(5 + level):
            x, y = find_safe_tile()
            special_points.append({'pos': (x, y, 15), 'collected': False})

        # Reset power-ups
        for boost in speed_boosts:
            boost['active'] = True
        for trap in slow_traps:
            trap['active'] = True
        for bonus in time_bonuses:
            bonus['active'] = True
        for life in life_collectibles:
            life['active'] = True
        for mult in multipliers:
            mult['active'] = True
        for shield in shields:
            shield['collected'] = False

        speed_boost_active = False
        speed_boost_timer = 0.0
        slow_trap_active = False
        slow_trap_timer = 0.0
        multiplier_active = False
        multiplier_timer = 0.0
        multiplier_factor = 1
        ball_color = [1.0, 0.2, 0.2]
        shield_active = False
        shield_time = 0
        particles = []

        # Generate obstacles
        obstacles = []
        num_obstacles = min(5 + level * 2, 20)
        for _ in range(num_obstacles):
            x = random.uniform(-half_size_x + 50, half_size_x - 50)
            y = random.uniform(-half_size_y + 50, half_size_y - 50)
            obstacles.append({
                'pos': [x, y, 30],
                'size': random.uniform(15, 30),
                'type': random.choice(['sphere', 'cube', 'cone']),
                'color': (random.random() * 0.5 + 0.5, random.random() * 0.3, random.random() * 0.3)
            })

    if reset_lives:
        lives = 3

    game_over = False
    game_won = False
    time_last = time.time()
    last_tile = None
    time_on_tile = 0.0
    show_timer = False

    difficulty_timer = None
    difficulty_mode = False
    speed_multiplier = 1.0 + level * 0.1

    # Reset moving platforms
    for platform in moving_platforms:
        platform['pos'] = [platform['pos'][0], platform['pos'][1], platform['pos'][2]]

    game_state = "playing"

def setup_projection():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, ASPECT, 1.0, 3000.0)
    glMatrixMode(GL_MODELVIEW)

def reshape(w, h):
    global WINDOW_WIDTH, WINDOW_HEIGHT, ASPECT
    WINDOW_WIDTH = max(1, w)
    WINDOW_HEIGHT = max(1, h)
    ASPECT = WINDOW_WIDTH / WINDOW_HEIGHT
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    setup_projection()

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

def setup_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set background color based on theme
    if theme == "space":
        glClearColor(0.0, 0.0, 0.1, 1.0)
    elif theme == "ocean":
        glClearColor(0.2, 0.4, 0.8, 1.0)
    elif theme == "sunset":
        glClearColor(0.8, 0.5, 0.2, 1.0)
    elif theme == "lava":
        glClearColor(0.5, 0.2, 0.1, 1.0)
    else:
        glClearColor(0.5, 0.8, 1.0, 1.0)

    # Camera
    if camera_mode == "follow":
        angle_rad = math.radians(camera_angle)
        eye_x = ball_pos[0] - camera_distance * math.cos(angle_rad)
        eye_y = ball_pos[1] + camera_distance * math.sin(angle_rad)
        eye_z = ball_pos[2] + camera_height
        gluLookAt(eye_x, eye_y, eye_z, ball_pos[0], ball_pos[1], ball_pos[2], 0.0, 0.0, 1.0)
    elif camera_mode == "overhead":
        gluLookAt(0, 0, 800, 0, 0, 0, 0, 1, 0)
    elif camera_mode == "first_person":
        gluLookAt(ball_pos[0], ball_pos[1], ball_pos[2] + 10,
                  ball_pos[0] + math.cos(math.radians(camera_angle)) * 10,
                  ball_pos[1] + math.sin(math.radians(camera_angle)) * 10,
                  ball_pos[2] + 10,
                  0.0, 0.0, 1.0)

    setup_lighting()

def draw_skybox():
    glDisable(GL_LIGHTING)
    glBegin(GL_QUADS)

    size = skybox_size
    # Front
    glColor3f(0.6, 0.8, 1.0)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)

    # Back
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)

    # Top - sky
    if theme == "space":
        glColor3f(0.0, 0.0, 0.2)
    elif theme == "sunset":
        glColor3f(0.9, 0.6, 0.3)
    else:
        glColor3f(0.4, 0.6, 1.0)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)

    # Bottom - ground
    glColor3f(0.3, 0.2, 0.1)
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)

    # Left
    glColor3f(0.5, 0.7, 0.9)
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, -size, size)

    # Right
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)

    glEnd()
    glEnable(GL_LIGHTING)

def draw_floor():
    colors = theme_colors[theme]
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            x = i * tile_size - half_size_x
            y = j * tile_size - half_size_y
            if (i, j) in holes:
                glColor3f(*colors["hole"])
                glBegin(GL_QUADS)
                glVertex3f(x, y, 0.0)
                glVertex3f(x + tile_size, y, 0.0)
                glVertex3f(x + tile_size, y + tile_size, 0.0)
                glVertex3f(x, y + tile_size, 0.0)
                glEnd()

                # Draw hole depth
                glColor3f(colors["hole"][0] * 0.7, colors["hole"][1] * 0.7, colors["hole"][2] * 0.7)
                glBegin(GL_QUADS)
                glVertex3f(x + 5, y + 5, -20.0)
                glVertex3f(x + tile_size - 5, y + 5, -20.0)
                glVertex3f(x + tile_size - 5, y + tile_size - 5, -20.0)
                glVertex3f(x + 5, y + tile_size - 5, -20.0)
                glEnd()
            else:
                if (i + j) % 2 == 0:
                    glColor3f(*colors["floor2"])
                else:
                    glColor3f(*colors["floor1"])
                glBegin(GL_QUADS)
                glVertex3f(x, y, 0.0)
                glVertex3f(x + tile_size, y, 0.0)
                glVertex3f(x + tile_size, y + tile_size, 0.0)
                glVertex3f(x, y + tile_size, 0.0)
                glEnd()

def draw_walls():
    colors = theme_colors[theme]
    glColor3f(*colors["wall"])
    for sx, sy in [(-half_size_x,0),(half_size_x,0),(0,half_size_y),(0,-half_size_y)]:
        glBegin(GL_QUADS)
        if sx != 0:
            x = sx
            glVertex3f(x, -half_size_y, 0)
            glVertex3f(x,  half_size_y, 0)
            glVertex3f(x,  half_size_y, wall_height)
            glVertex3f(x, -half_size_y, wall_height)
        else:
            y = sy
            glVertex3f(-half_size_x, y, 0)
            glVertex3f( half_size_x, y, 0)
            glVertex3f( half_size_x, y, wall_height)
            glVertex3f(-half_size_x, y, wall_height)
        glEnd()