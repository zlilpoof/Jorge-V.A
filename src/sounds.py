import os
import pygame

def initialize_pygame():
    pygame.init()

def bip():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    bip_mp3 = os.path.join(parent_dir, "bip.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load(bip_mp3)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()