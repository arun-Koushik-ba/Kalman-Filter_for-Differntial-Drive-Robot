# config.py
import numpy as np

# World dimensions (meters)
WORLD_WIDTH = 10.0
WORLD_HEIGHT = 8.0

# Scaling
SCALE = 70  # Slightly smaller to fit dashboard

# UI Layout
SIDEBAR_WIDTH = 350
SCREEN_WIDTH = int(WORLD_WIDTH * SCALE) + SIDEBAR_WIDTH
SCREEN_HEIGHT = int(WORLD_HEIGHT * SCALE)

# Colors (Dark Mode Theme)
# Hex: #1e1e1e (Background), #2d2d2d (Panel)
BG_COLOR = (30, 30, 30)
PANEL_COLOR = (45, 45, 45)
GRID_COLOR = (60, 60, 60)
TEXT_WHITE = (220, 220, 220)
TEXT_GRAY = (150, 150, 150)

RED = (255, 80, 80)
BLUE = (50, 150, 255)
GREEN = (50, 205, 50)
ORANGE = (255, 165, 0)
PURPLE = (180, 80, 255)
CYAN = (0, 255, 255)

# Robot parameters
WHEEL_BASE = 0.5
MAX_SPEED = 1.0

# Odometry noise
ODOM_STD = 0.06

# Controller gains
K_DISTANCE = 1.2
K_HEADING = 3.5
GOAL_THRESHOLD = 0.2

# Sensor parameters
MAX_SENSOR_RANGE = 5.0
RANGE_STD = 0.1
BEARING_STD = 0.02

# EKF parameters
NUM_LANDMARKS = 5
STATE_SIZE = 3 + 2 * NUM_LANDMARKS
# In config.py, modify these lines:
MOTION_NOISE = [0.01, 0.01, 0.005]  # Reduced from [0.05, 0.05, 0.02]
MEAS_NOISE = np.diag([0.05**2, 0.02**2]) * 5.0  # Reduced noise

# config.py - Add these parameters
SAFE_DISTANCE = 1 # Minimum safe distance from obstacles
AVOIDANCE_GAIN = 2.0  # How strongly to avoid obstacles
MAX_AVOIDANCE_ANGLE = 0.8  # Maximum steering for avoidance
STOP_DISTANCE = 0.5  # Stop if too close to obstacle

