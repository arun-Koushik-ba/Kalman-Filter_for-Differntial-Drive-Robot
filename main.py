# main.py
import pygame
import math
import time
import random
import numpy as np
from config import *
from utils import world_to_screen, draw_robot, normalize_angle
from assets import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Autonomous EKF-SLAM Navigation System")
clock = pygame.time.Clock()

# Fonts
header_font = pygame.font.SysFont('Arial', 20, bold=True)
font = pygame.font.SysFont('Consolas', 14)
small_font = pygame.font.SysFont('Arial', 12)
legend_font = pygame.font.SysFont('Arial', 14)

# ================= 1. SETUP =================
landmark_surfaces = {
    "A": create_wall_corner_surface(50),
    "B": create_wall_corner_surface(50),
    "C": create_pillar_surface(40),
    "D": create_table_surface(50),
    "E": create_cabinet_surface(60)
}

# ================= 2. INITIALIZATION =================
random_x = random.uniform(0.5, WORLD_WIDTH - 0.5)
random_y = random.uniform(0.5, WORLD_HEIGHT - 0.5)
random_theta = random.uniform(0, 2 * math.pi)
true_x, true_y, true_theta = random_x, random_y, random_theta
odom_x, odom_y, odom_theta = random_x, random_y, random_theta 
X = np.zeros((STATE_SIZE, 1))
X[0:3, 0] = [random_x, random_y, random_theta] 

P = np.eye(STATE_SIZE) * 1.0
P[0:3, 0:3] = 0.001
P[3:, 3:] = 1000.0

landmark_ids = ["A", "B", "C", "D", "E"]
landmark_index = {lm: 3 + 2*i for i, lm in enumerate(landmark_ids)}
landmark_seen = {lm: False for lm in landmark_ids}

true_path, odom_path, ekf_path = [], [], []
error_history = []

goals = [(0,2), (8,4), (9,7)]
goal_index = 0

landmarks = {
    "A": (0.0, 0.0), "B": (10.0, 0.0), "C": (4.0, 3.0),
    "D": (8.0, 5.0), "E": (2.0, 7.0)
}

sensor_rays = []
frame_count = 0
last_time = time.time()
running = True
show_sensor_range = True

# --- HELPER: Draw Legend (Moved to Top Right) ---
def draw_dark_legend(screen):
    # FIXED: Moved to Top Right of the Map area to avoid blocking Landmark A
    # Map ends at WORLD_WIDTH * SCALE. We subtract ~210px to fit the box inside the map.
    box_x = int(WORLD_WIDTH * SCALE) - 220 
    box_y = 10 
    width, height = 210, 200
    
    # Semi-transparent dark background
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((30, 30, 30, 200)) # Slightly more transparent
    screen.blit(s, (box_x, box_y))
    pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y, width, height), 1)
    
    # Title
    title = legend_font.render("VISUAL LEGEND", True, CYAN)
    screen.blit(title, (box_x + 10, box_y + 10))
    
    items = [
        (BLUE, "True Pose (Ground Truth)"),
        (GREEN, "EKF Estimate (SLAM)"),
        (ORANGE, "Odometry (Dead Reckoning)"),
        ((255, 255, 0), "Lidar/Sensor Rays"),
        (RED, "Target Vector / Goal"),
        (PURPLE, "Est. Landmarks")
    ]
    
    y = box_y + 40
    for color, text in items:
        pygame.draw.rect(screen, color, (box_x + 10, y, 15, 15))
        label = small_font.render(text, True, TEXT_WHITE)
        screen.blit(label, (box_x + 35, y))
        y += 25

# --- HELPER: Dashboard ---
def draw_dashboard(screen, error_val):
    # Sidebar Background
    pygame.draw.rect(screen, PANEL_COLOR, (int(WORLD_WIDTH * SCALE), 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(screen, (80,80,80), (int(WORLD_WIDTH * SCALE), 0), (int(WORLD_WIDTH * SCALE), SCREEN_HEIGHT), 2)
    
    start_x = int(WORLD_WIDTH * SCALE) + 10
    y = 10

    # Header
    title = header_font.render("SYSTEM STATUS", True, CYAN)
    screen.blit(title, (start_x, y))
    y += 30

    # Logic for Status Text
    if goal_index < len(goals):
        status = "NAVIGATING"
        col = GREEN
        wp_text = f"{goal_index + 1}/{len(goals)}"
    else:
        status = "COMPLETE"
        col = ORANGE
        wp_text = "DONE" # FIXED: Shows DONE instead of 4/3

    screen.blit(font.render(f"MODE: AUTONOMOUS", True, TEXT_WHITE), (start_x, y))
    y += 20
    screen.blit(font.render(f"TASK: {status}", True, col), (start_x, y))
    y += 20
    screen.blit(font.render(f"NEXT WP: {wp_text}", True, TEXT_GRAY), (start_x, y))
    y += 40

    # Graph
    pygame.draw.rect(screen, (20, 20, 20), (start_x, y, SIDEBAR_WIDTH-20, 100))
    pygame.draw.rect(screen, (100, 100, 100), (start_x, y, SIDEBAR_WIDTH-20, 100), 1)
    screen.blit(small_font.render("EKF ERROR (m)", True, TEXT_GRAY), (start_x + 5, y + 5))
    
    error_history.append(error_val)
    if len(error_history) > (SIDEBAR_WIDTH - 20): error_history.pop(0)
    
    if len(error_history) > 1:
        points = []
        for i, val in enumerate(error_history):
            px = start_x + i
            py = (y + 100) - min(val * 80, 98) 
            points.append((px, py))
        pygame.draw.lines(screen, RED, False, points, 2)
        screen.blit(small_font.render(f"{error_val:.3f}m", True, RED), (start_x + SIDEBAR_WIDTH - 50, y + 5))

    y += 120

    # Data
    screen.blit(header_font.render("REAL-TIME DATA", True, CYAN), (start_x, y))
    y += 25
    data = [
        f"TRUE X : {true_x:.2f}", f"TRUE Y : {true_y:.2f}",
        f"TRUE θ : {math.degrees(true_theta):.1f}°",
        "-"*20,
        f"EST  X : {X[0,0]:.2f}", f"EST  Y : {X[1,0]:.2f}",
        f"EST  θ : {math.degrees(X[2,0]):.1f}°",
        "-"*20,
        f"SENSOR RAYS: {len(sensor_rays)}"
    ]
    for line in data:
        col = BLUE if "TRUE" in line else (GREEN if "EST" in line else TEXT_WHITE)
        screen.blit(font.render(line, True, col), (start_x, y))
        y += 20

def detect_obstacles_and_avoid(true_x, true_y, true_theta, landmarks, sensor_rays):
    """
    Detect obstacles in front of the robot and compute avoidance steering
    Returns: avoidance_angle (radians)
    """
    avoidance_angle = 0.0
    closest_obstacle_dist = float('inf')
    obstacle_detected = False
    
    # Convert sensor rays to obstacle information
    for start, end in sensor_rays:
        # Calculate distance to obstacle
        dist = math.hypot(end[0] - true_x, end[1] - true_y)
        
        # Only consider obstacles in front of robot
        dx = end[0] - true_x
        dy = end[1] - true_y
        angle_to_obstacle = math.atan2(dy, dx)
        angle_diff = normalize_angle(angle_to_obstacle - true_theta)
        
        # Check if obstacle is in front (within ±90 degrees)
        if abs(angle_diff) < math.pi/2 and dist < SAFE_DISTANCE:
            obstacle_detected = True
            closest_obstacle_dist = min(closest_obstacle_dist, dist)
            
            # Calculate avoidance steering: turn away from obstacle
            # Obstacle on right -> turn left (negative), obstacle on left -> turn right (positive)
            avoidance_angle += -AVOIDANCE_GAIN * (angle_diff / abs(angle_diff)) / max(dist, 0.1)
    
    # Also check direct landmark positions (for landmarks not currently sensed)
    for lm_id, (lx, ly) in landmarks.items():
        dist = math.hypot(lx - true_x, ly - true_y)
        if dist < SAFE_DISTANCE:
            dx = lx - true_x
            dy = ly - true_y
            angle_to_obstacle = math.atan2(dy, dx)
            angle_diff = normalize_angle(angle_to_obstacle - true_theta)
            
            if abs(angle_diff) < math.pi/2:  # In front
                obstacle_detected = True
                avoidance_angle += -AVOIDANCE_GAIN * (angle_diff / abs(angle_diff)) / max(dist, 0.1)
    
    # Limit the avoidance angle
    if obstacle_detected:
        avoidance_angle = max(-MAX_AVOIDANCE_ANGLE, min(MAX_AVOIDANCE_ANGLE, avoidance_angle))
        
        # If too close, slow down or stop
        if closest_obstacle_dist < STOP_DISTANCE:
            return avoidance_angle, 0.0  # Stop but still steer
    
    return avoidance_angle, 1.0  # Normal speed

# --- MAIN LOOP ---
while running:
    clock.tick(60)
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    frame_count += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                show_sensor_range = not show_sensor_range

    est_x, est_y, est_theta = X[0,0], X[1,0], X[2,0]

        # Control Logic with Obstacle Avoidance
    if goal_index < len(goals):
        gx, gy = goals[goal_index]
        dx, dy = gx - est_x, gy - est_y
        dist = math.hypot(dx, dy)
        heading_error = normalize_angle(math.atan2(dy, dx) - est_theta)
        
        # Detect obstacles and get avoidance steering
        avoidance_angle, speed_factor = detect_obstacles_and_avoid(
            true_x, true_y, true_theta, landmarks, sensor_rays
        )
        
        if dist < GOAL_THRESHOLD:
            goal_index += 1
            v, omega = 0.0, 0.0
        else:
            # Base navigation control
            base_v = min(K_DISTANCE * dist, MAX_SPEED)
            base_omega = K_HEADING * heading_error
            
            # Combine navigation with obstacle avoidance
            if avoidance_angle != 0.0:
                # When avoiding, prioritize obstacle avoidance
                omega = avoidance_angle * 1.5  # Stronger avoidance
                v = base_v * 0.5 * speed_factor  # Slow down while avoiding
            else:
                # Normal navigation
                v = base_v
                omega = base_omega
                
            # Stop if heading error is too large (except when avoiding)
            if abs(heading_error) > 1.0 and abs(avoidance_angle) < 0.1:
                v = 0.0
    else:
        v, omega = 0.0, 0.0

    v_l = v - omega*WHEEL_BASE/2
    v_r = v + omega*WHEEL_BASE/2

    # Simulation Logic
    v_t = (v_l + v_r)/2; w_t = (v_r - v_l)/WHEEL_BASE
    true_x += v_t * math.cos(true_theta) * dt
    true_y += v_t * math.sin(true_theta) * dt
    true_theta = normalize_angle(true_theta + w_t*dt)

    v_l_n = v_l + random.gauss(0, ODOM_STD); v_r_n = v_r + random.gauss(0, ODOM_STD)
    v_o = (v_l_n + v_r_n)/2; w_o = (v_r_n - v_l_n)/WHEEL_BASE
    odom_x += v_o * math.cos(odom_theta) * dt
    odom_y += v_o * math.sin(odom_theta) * dt
    odom_theta = normalize_angle(odom_theta + w_o*dt)

    theta = X[2,0]
    X[0,0] += v_o * math.cos(theta) * dt; X[1,0] += v_o * math.sin(theta) * dt
    X[2,0] = normalize_angle(X[2,0] + w_o*dt)

    F = np.eye(STATE_SIZE); F[0,2] = -v_o * math.sin(theta) * dt; F[1,2] = v_o * math.cos(theta) * dt
    Q = np.zeros((STATE_SIZE, STATE_SIZE)); Q[0,0], Q[1,1], Q[2,2] = MOTION_NOISE
    P = F @ P @ F.T + Q

    sensor_rays.clear()
    for lm_id, (lx_t, ly_t) in landmarks.items():
        dx, dy = lx_t - true_x, ly_t - true_y
        true_dist = math.hypot(dx, dy)
        if true_dist > MAX_SENSOR_RANGE: continue
        
        sensor_rays.append(((true_x, true_y), (lx_t, ly_t)))
        true_bearing = normalize_angle(math.atan2(dy, dx) - true_theta)
        z = np.array([[true_dist + random.gauss(0, RANGE_STD)], [normalize_angle(true_bearing + random.gauss(0, BEARING_STD))]])

        idx = landmark_index[lm_id]
        if not landmark_seen[lm_id]:
            X[idx, 0] = X[0,0] + z[0,0] * math.cos(X[2,0] + z[1,0])
            X[idx+1, 0] = X[1,0] + z[0,0] * math.sin(X[2,0] + z[1,0])
            landmark_seen[lm_id] = True
            continue

        lx, ly = X[idx, 0], X[idx+1, 0]
        dx, dy = lx - X[0,0], ly - X[1,0]
        q = dx**2 + dy**2; r_pred = math.sqrt(q)
        y_res = z - np.array([[r_pred], [normalize_angle(math.atan2(dy, dx) - X[2,0])]])
        y_res[1,0] = normalize_angle(y_res[1,0])

        H = np.zeros((2, STATE_SIZE))
        H[0,0] = -dx/r_pred; H[0,1] = -dy/r_pred; H[0,2] = 0
        H[1,0] = dy/q; H[1,1] = -dx/q; H[1,2] = -1
        H[0, idx] = dx/r_pred; H[0, idx+1] = dy/r_pred
        H[1, idx] = -dy/q; H[1, idx+1] = dx/q

        S = H @ P @ H.T + MEAS_NOISE
        K = P @ H.T @ np.linalg.inv(S)
        X = X + K @ y_res; X[2,0] = normalize_angle(X[2,0])
        P = (np.eye(STATE_SIZE) - K @ H) @ P

    # --- DRAWING ---
    if frame_count % 5 == 0:
        true_path.append((true_x, true_y))
        odom_path.append((odom_x, odom_y))
        ekf_path.append((X[0,0], X[1,0]))

    screen.fill(BG_COLOR)
    # Grid
    for x in range(0, int(WORLD_WIDTH * SCALE), SCALE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, SCALE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (int(WORLD_WIDTH * SCALE), y))
    
    # Range Bubble
    if show_sensor_range:
        sp = world_to_screen(true_x, true_y)
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 10), sp, int(MAX_SENSOR_RANGE*SCALE))
        pygame.draw.circle(s, (80, 80, 80), sp, int(MAX_SENSOR_RANGE*SCALE), 1)
        screen.blit(s, (0,0))

    # TRAILS
    if len(odom_path) > 1: pygame.draw.lines(screen, ORANGE, False, [world_to_screen(*p) for p in odom_path], 2)
    if len(true_path) > 1: pygame.draw.lines(screen, (50, 80, 150), False, [world_to_screen(*p) for p in true_path], 2)
    if len(ekf_path) > 1: pygame.draw.lines(screen, GREEN, False, [world_to_screen(*p) for p in ekf_path], 3)

    # RAYS
    for start, end in sensor_rays:
        pygame.draw.line(screen, (255, 255, 0), world_to_screen(*start), world_to_screen(*end), 2)
        pygame.draw.circle(screen, CYAN, world_to_screen(*end), 4)

    # LANDMARKS
    for lm_id, (lx, ly) in landmarks.items():
        pos = world_to_screen(lx, ly)
        screen.blit(landmark_surfaces[lm_id], landmark_surfaces[lm_id].get_rect(center=pos))
        screen.blit(font.render(lm_id, True, TEXT_WHITE), (pos[0]+15, pos[1]-20))
        if landmark_seen[lm_id]:
            idx = landmark_index[lm_id]
            epos = world_to_screen(X[idx, 0], X[idx+1, 0])
            pygame.draw.line(screen, PURPLE, (epos[0]-6, epos[1]-6), (epos[0]+6, epos[1]+6), 2)
            pygame.draw.line(screen, PURPLE, (epos[0]+6, epos[1]-6), (epos[0]-6, epos[1]+6), 2)

    # ROBOTS & VECTORS
    draw_robot(screen, true_x, true_y, true_theta, BLUE)
    draw_robot(screen, X[0,0], X[1,0], X[2,0], GREEN)

    rx, ry = world_to_screen(true_x, true_y)
    hx = rx + 40 * math.cos(true_theta)
    hy = ry - 40 * math.sin(true_theta)
    pygame.draw.line(screen, (255, 255, 255), (rx, ry), (hx, hy), 2) 

    if goal_index < len(goals):
        gx, gy = goals[goal_index]
        gdx, gdy = gx - true_x, gy - true_y
        target_angle = math.atan2(gdy, gdx)
        tx = rx + 60 * math.cos(target_angle)
        ty = ry - 60 * math.sin(target_angle)
        pygame.draw.line(screen, RED, (rx, ry), (tx, ty), 1)
        pygame.draw.circle(screen, RED, world_to_screen(*goals[goal_index]), 6, 2)

    draw_dark_legend(screen)
    error = math.sqrt((true_x - X[0,0])**2 + (true_y - X[1,0])**2)
    draw_dashboard(screen, error)

    pygame.display.flip()

pygame.quit()