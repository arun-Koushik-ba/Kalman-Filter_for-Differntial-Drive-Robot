# assets.py
import pygame
import os
from config import SCALE, SCREEN_HEIGHT

# Try to create assets directory if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

def world_to_screen(x, y):
    """Convert world coordinates to pygame screen coordinates"""
    screen_x = int(x * SCALE)
    screen_y = int(SCREEN_HEIGHT - y * SCALE)
    return screen_x, screen_y

def create_wall_corner_surface(size=50):
    """Create a wall corner texture"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Draw wall edges
    pygame.draw.line(surf, (120, 120, 120), (0, size//2), (size//2, size//2), 8)  # Horizontal wall
    pygame.draw.line(surf, (120, 120, 120), (size//2, size//2), (size//2, size), 8)  # Vertical wall
    # Draw corner highlight
    pygame.draw.circle(surf, (200, 200, 200), (size//2, size//2), 10)
    return surf

def create_pillar_surface(size=40):
    """Create a pillar/column texture"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Pillar base
    pygame.draw.circle(surf, (150, 150, 150), (size//2, size//2), size//2 - 2)
    pygame.draw.circle(surf, (180, 180, 180), (size//2, size//2), size//2 - 6)
    # Pillar details
    pygame.draw.circle(surf, (200, 200, 200), (size//2, size//2), size//4)
    # Shadow
    pygame.draw.circle(surf, (100, 100, 100, 100), (size//2 + 2, size//2 + 2), size//2 - 2)
    return surf

def create_table_surface(size=50):
    """Create a table texture"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Table top
    pygame.draw.rect(surf, (139, 69, 19), (5, 5, size-10, size-10), border_radius=5)
    pygame.draw.rect(surf, (160, 82, 45), (8, 8, size-16, size-16), border_radius=3)
    # Table legs
    leg_color = (101, 67, 33)
    leg_width = 6
    # Four legs at corners
    pygame.draw.rect(surf, leg_color, (10, 10, leg_width, leg_width))
    pygame.draw.rect(surf, leg_color, (size-16, 10, leg_width, leg_width))
    pygame.draw.rect(surf, leg_color, (10, size-16, leg_width, leg_width))
    pygame.draw.rect(surf, leg_color, (size-16, size-16, leg_width, leg_width))
    return surf

def create_cabinet_surface(size=60):
    """Create a cabinet texture"""
    surf = pygame.Surface((size, size//2), pygame.SRCALPHA)  # Cabinet is wider than tall
    # Cabinet body
    pygame.draw.rect(surf, (74, 49, 39), (0, 0, size, size//2), border_radius=3)
    pygame.draw.rect(surf, (101, 67, 33), (2, 2, size-4, size//2-4), border_radius=2)
    # Cabinet doors
    pygame.draw.line(surf, (50, 50, 50), (size//2, 5), (size//2, size//2-5), 2)
    # Handles
    pygame.draw.circle(surf, (200, 200, 200), (size//4, size//4), 3)
    pygame.draw.circle(surf, (200, 200, 200), (3*size//4, size//4), 3)
    return surf

def create_window_surface(size=50):
    """Create a window texture (for wall corners)"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Window frame
    pygame.draw.rect(surf, (100, 100, 100), (5, 5, size-10, size-10), 3)
    # Glass
    pygame.draw.rect(surf, (135, 206, 235, 100), (8, 8, size-16, size-16))
    # Window cross
    pygame.draw.line(surf, (100, 100, 100), (size//2, 8), (size//2, size-8), 2)
    pygame.draw.line(surf, (100, 100, 100), (8, size//2), (size-8, size//2), 2)
    return surf

def create_room_background(width, height):
    """Create a room background with walls and floor"""
    surf = pygame.Surface((width, height))
    
    # Floor color (light beige)
    surf.fill((240, 235, 220))
    
    # Draw floor tiles/pattern
    tile_size = 40
    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            if (x//tile_size + y//tile_size) % 2 == 0:
                tile_color = (230, 225, 210)
            else:
                tile_color = (235, 230, 215)
            pygame.draw.rect(surf, tile_color, (x, y, tile_size, tile_size), 1)
    
    # Draw walls around edges
    wall_thickness = 20
    wall_color = (180, 180, 180)
    # Top wall
    pygame.draw.rect(surf, wall_color, (0, 0, width, wall_thickness))
    # Bottom wall
    pygame.draw.rect(surf, wall_color, (0, height-wall_thickness, width, wall_thickness))
    # Left wall
    pygame.draw.rect(surf, wall_color, (0, 0, wall_thickness, height))
    # Right wall
    pygame.draw.rect(surf, wall_color, (width-wall_thickness, 0, wall_thickness, height))
    
    # Add some texture to walls
    for i in range(0, width, 30):
        pygame.draw.line(surf, (160, 160, 160), (i, wall_thickness//2), (i+15, wall_thickness//2), 2)
    
    return surf

def draw_legend(screen, font):
    """Draw an improved legend with color swatches"""
    legend_x = 10
    legend_y = 10
    swatch_size = 20
    spacing = 5
    text_spacing = 25
    
    # Legend background
    legend_bg = pygame.Surface((250, 200), pygame.SRCALPHA)
    legend_bg.fill((255, 255, 255, 200))
    pygame.draw.rect(legend_bg, (0, 0, 0), legend_bg.get_rect(), 2)
    screen.blit(legend_bg, (legend_x-5, legend_y-5))
    
    # Title
    title = font.render("EKF-SLAM Legend", True, (0, 0, 0))
    screen.blit(title, (legend_x, legend_y))
    
    # Robot poses
    items = [
        ((30, 144, 255), "True Pose (Blue)"),
        ((255, 165, 0), "Odometry (Orange)"),
        ((0, 200, 0), "EKF Estimate (Green)"),
        ((220, 20, 60), "True Landmarks"),
        ((160, 32, 240), "Estimated Landmarks"),
        ((200, 200, 200), "Sensor Range"),
    ]
    
    for i, (color, text) in enumerate(items):
        y_pos = legend_y + 30 + i * text_spacing
        
        # Draw color swatch
        pygame.draw.rect(screen, color, (legend_x, y_pos, swatch_size, swatch_size))
        pygame.draw.rect(screen, (0, 0, 0), (legend_x, y_pos, swatch_size, swatch_size), 1)
        
        # Draw text
        label = font.render(text, True, (0, 0, 0))
        screen.blit(label, (legend_x + swatch_size + spacing, y_pos))
    
    # Landmark descriptions
    desc_y = legend_y + 30 + len(items) * text_spacing + 10
    desc_title = font.render("Landmark Types:", True, (0, 0, 0))
    screen.blit(desc_title, (legend_x, desc_y))
    
    landmark_desc = [
        "A: Wall Corner (0,0)",
        "B: Wall Corner (10,0)",
        "C: Pillar (4,3)",
        "D: Table Corner (8,5)",
        "E: Cabinet Edge (2,7)"
    ]
    
    for i, desc in enumerate(landmark_desc):
        y_pos = desc_y + 20 + i * 20
        label = font.render(desc, True, (50, 50, 50))
        screen.blit(label, (legend_x + 10, y_pos))