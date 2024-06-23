import os
import pygame
from PIL import Image


# Variable
from ..constant import WINDOW_HEIGHT, WINDOW_WIDTH
BIRD_DIRECTORY = os.path.join('.', 'Src', 'flappy', 'bird')
BIRD_FILENAMES = ['bird0.png', 'bird1.png', 'bird2.png', 'bird3.png']
BIRD_IMAGES = [os.path.join(BIRD_DIRECTORY, filename) for filename in BIRD_FILENAMES]
bird_size = Image.open(BIRD_IMAGES[0]).size
bird_images = [pygame.image.load(image) for image in BIRD_IMAGES]

class Player:
    """
    A class representing the player (bird) in the Flappy Bird game.
    """

    def __init__(self):
        """
        Initialize the player (bird) object with default attributes.
        """
        self.x_velocity = 0
        self.image_index = 0
        self.size = bird_size
        self.position = [(WINDOW_WIDTH - self.size[0]) // 2, WINDOW_HEIGHT // 4]
        self.velocity_y = 5 + self.x_velocity
        self.jump_strength = -40
        self.gravity = 15
        self.is_ground = False

    def flap_up(self):
        """
        Make the bird flap upward.
        """
        self.velocity_y = self.jump_strength

    def get_rect(self):
        """
        Get the rectangular area occupied by the bird.

        Returns:
            pygame.Rect: A pygame Rect object representing the bird's position and size.
        """
        return pygame.Rect(self.position, (self.size[0], self.size[1]))

    def draw(self, screen):
        """
        Draw the bird onto the screen.

        Args:
            screen (pygame.Surface): The surface to draw the bird on.
        """
        player_rect = self.get_rect()
        current_image = bird_images[self.image_index]
        screen.blit(current_image, player_rect)
        self.image_index = (self.image_index + 1) % len(bird_images)

    def update(self, dt):
        """
        Update the position and state of the bird.

        Args:
            dt (float): Time delta since the last update.
        """
        y = self.position[1]

        # Check lower border and ground condition
        if y < WINDOW_HEIGHT - self.size[1] or self.is_ground:
            if not self.is_ground:
                self.position[1] += self.velocity_y * dt
                self.velocity_y += self.gravity * dt
            else:
                self.is_ground = False
                self.flap_up()
                self.gravity = 15
                self.position[1] += self.velocity_y * dt
                self.velocity_y += self.gravity * dt
        else:
            self.position[1] = WINDOW_HEIGHT - self.size[1]
            self.velocity_y = 0
            self.gravity = 0
            self.is_ground = True

        # Check upper border
        if self.position[1] < 0:
            self.position[1] = 0
            self.velocity_y = 0
