# utils.py
import math
import pygame
from config import SCALE, SCREEN_HEIGHT

def normalize_angle(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi

def world_to_screen(x, y):
    """
    Convert world coordinates (meters)
    to pygame screen coordinates (pixels)
    """
    screen_x = int(x * SCALE)
    screen_y = int(SCREEN_HEIGHT - y * SCALE)
    return screen_x, screen_y

def draw_robot(screen, x, y, theta, color):
    """
    Draw robot as a triangle
    """
    size = 0.3  # meters

    # Triangle points in robot frame
    points = [
        (size, 0),
        (-size/2, size/2),
        (-size/2, -size/2)
    ]

    transformed_points = []
    for px, py in points:
        rx = x + px * math.cos(theta) - py * math.sin(theta)
        ry = y + px * math.sin(theta) + py * math.cos(theta)
        transformed_points.append(world_to_screen(rx, ry))

    pygame.draw.polygon(screen, color, transformed_points)
    # Draw a small circle at the center
    center_pos = world_to_screen(x, y)
    pygame.draw.circle(screen, (0, 0, 0), center_pos, 2)

def create_landmark_sprite(color, size=30, shape="circle"):
    """Create a sprite for a landmark"""
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    
    if shape == "circle":
        pygame.draw.circle(sprite, color, (size//2, size//2), size//2 - 2)
        pygame.draw.circle(sprite, (0, 0, 0), (size//2, size//2), size//2 - 2, 2)
    elif shape == "square":
        pygame.draw.rect(sprite, color, (2, 2, size-4, size-4))
        pygame.draw.rect(sprite, (0, 0, 0), (2, 2, size-4, size-4), 2)
    elif shape == "triangle":
        points = [(size//2, 4), (4, size-4), (size-4, size-4)]
        pygame.draw.polygon(sprite, color, points)
        pygame.draw.polygon(sprite, (0, 0, 0), points, 2)
    
    return sprite

def load_landmark_sprites():
    """Load or create sprites for different landmark types"""
    sprites = {}
    
    # Create different sprites for different landmark types
    sprites["corner"] = create_landmark_sprite((150, 75, 0), 24, "square")  # Brown for corners
    sprites["pillar"] = create_landmark_sprite((100, 100, 100), 28, "circle")  # Gray for pillar
    sprites["table"] = create_landmark_sprite((0, 100, 0), 26, "square")  # Green for table
    sprites["cabinet"] = create_landmark_sprite((75, 0, 130), 24, "triangle")  # Purple for cabinet
    sprites["default"] = create_landmark_sprite((220, 20, 60), 24, "circle")  # Red for default
    
    return sprites

def draw_legend(screen):
    font = pygame.font.SysFont(None, 20)
    title_font = pygame.font.SysFont(None, 24, bold=True)
    
    # Draw legend background
    legend_width = 250
    legend_height = 230
    legend_x = SCREEN_WIDTH - legend_width - 10
    legend_y = 10
    
    # Semi-transparent background
    legend_bg = pygame.Surface((legend_width, legend_height), pygame.SRCALPHA)
    legend_bg.fill((255, 255, 255, 200))  # White with transparency
    pygame.draw.rect(legend_bg, (0, 0, 0, 150), (0, 0, legend_width, legend_height), 2)
    screen.blit(legend_bg, (legend_x, legend_y))
    
    # Title
    title = title_font.render("SLAM Legend", True, (0, 0, 0))
    screen.blit(title, (legend_x + 10, legend_y + 10))
    
    # Legend items with colored squares
    items = [
        ((30, 144, 255), "True Pose", "Actual robot position"),
        ((255, 165, 0), "Odometry", "Wheel encoder estimate"),
        ((0, 200, 0), "EKF Estimate", "SLAM corrected pose"),
        ((220, 20, 60), "Landmarks", "True positions"),
        ((160, 32, 240), "Estimated LM", "EKF estimated positions"),
        ((150, 75, 0), "Corners (A,B)", "Wall corners"),
        ((100, 100, 100), "Pillar (C)", "Structural pillar"),
        ((0, 100, 0), "Table (D)", "Table corner"),
        ((75, 0, 130), "Cabinet (E)", "Cabinet edge"),
        ((255, 0, 0), "Current Goal", "Navigation target")
    ]
    
    y_offset = 40
    for color, name, description in items:
        # Draw color box
        pygame.draw.rect(screen, color, (legend_x + 10, legend_y + y_offset, 15, 15))
        pygame.draw.rect(screen, (0, 0, 0), (legend_x + 10, legend_y + y_offset, 15, 15), 1)
        
        # Draw text
        name_text = font.render(name, True, (0, 0, 0))
        desc_text = font.render(description, True, (80, 80, 80))
        
        screen.blit(name_text, (legend_x + 30, legend_y + y_offset))
        screen.blit(desc_text, (legend_x + 30, legend_y + y_offset + 15))
        
        y_offset += 35