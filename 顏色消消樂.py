import pygame
import sys
import subprocess
import webbrowser

# Initialize Pygame
pygame.init()

# Load the image with the correct path
image_path = r'/Users/daren/Desktop/pygame/mnt/data/picture.png'
try:
    image = pygame.image.load(image_path)
except pygame.error as e:
    print(f"Cannot load image: {image_path}")
    print(e)
    pygame.quit()
    sys.exit()

# Set up display
screen = pygame.display.set_mode((image.get_width(), image.get_height()))
pygame.display.set_caption("顏色消消樂")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define fonts
font_medium = pygame.font.Font(None, 64)  

# Define text
easy_text = "易"
medium_text = "中"
hard_text = "難"
rules_text = "規則說明"
title_text = "標題"

# Define positions (adjust these positions to match the background image)
rules_pos = (408, 408)  
easy_pos = (650, 580)   
medium_pos = (650, 640) 
hard_pos = (650, 740)   
title_pos = (650, 400)

# Define button sizes (matching the size of the buttons in the background)
button_width = 100  # Adjusted button width
button_height = 60  # Adjusted button height

# Render text surfaces to get their sizes
easy_surface = font_medium.render(easy_text, True, WHITE)
medium_surface = font_medium.render(medium_text, True, WHITE)
hard_surface = font_medium.render(hard_text, True, WHITE)
rules_surface = font_medium.render(rules_text, True, WHITE)
title_surface = font_medium.render(title_text, True, WHITE)

# Define button areas based on text sizes
rules_rect = pygame.Rect(rules_pos[0], rules_pos[1], button_width, button_height)
easy_rect = pygame.Rect(easy_pos[0], easy_pos[1], button_width, button_height)
medium_rect = pygame.Rect(medium_pos[0], medium_pos[1], button_width, button_height)
hard_rect = pygame.Rect(hard_pos[0], hard_pos[1], button_width, button_height)
title_rect = pygame.Rect(title_pos[0], title_pos[1], button_width, button_height)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if rules_rect.collidepoint(event.pos):
                    webbrowser.open('www.google.com')
                elif easy_rect.collidepoint(event.pos):
                    subprocess.Popen(["python", "易.py"])
                elif medium_rect.collidepoint(event.pos):
                    subprocess.Popen(["python", "中.py"])
                elif hard_rect.collidepoint(event.pos):
                    subprocess.Popen(["python", "難.py"])
                elif title_rect.collidepoint(event.pos):
                    webbrowser.open('https://github.com/jiayang0718/pygame1')

    # Draw everything
    screen.fill(WHITE)
    screen.blit(image, (0, 0))

    # Draw buttons (text)
    screen.blit(rules_surface, rules_pos)
    screen.blit(easy_surface, easy_pos)
    screen.blit(medium_surface, medium_pos)
    screen.blit(hard_surface, hard_pos)
    screen.blit(title_surface, title_pos)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
