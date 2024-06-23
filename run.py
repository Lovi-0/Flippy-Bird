import pygame
from Src.Class.bird import Player
from Src.Class.pipe import Tube
from Src.Class.back import background_image
from Src.constant import WINDOW_HEIGHT, WINDOW_WIDTH, FPS


# Global variables
max_score = []
game_quit = True
int_try = 0
v_delta = 200
x_velocity = 0


# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flippy Bird')
font = pygame.font.Font(None, 36)


def load_screen():
    """Load background images onto the screen."""
    screen.blit(background_image, (0, 0))
    screen.blit(background_image, (288, 0)) 


def handle_command(player: Player):
    """Handle user input events.
    
    Args:
        - player (Player): The player object controlled by user input.
    
    Returns:
        bool: True if the game is still running, False if the user quits.
    """
    is_alive = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_alive = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.flap_up()
            if event.key == pygame.K_1:
                pygame.quit()
    return is_alive


def get_collidate(player: Player, tube_list: list[Tube], tube_index: int):
    """Check collision between player and tubes.
    
    Args:
        - player (Player): The player object.
        - tube_list (list[Tube]): List of Tube objects.
        - tube_index (int): Index of the current tube in the list.
    
    Returns:
        bool: True if collision occurs, False otherwise.
    """
    player_rect = player.get_rect()
    tube_rect = tube_list[tube_index].get_rect()
    tube_rectreverse = tube_list[tube_index].get_rect_reverse()

    if player_rect.colliderect(tube_rect) or player_rect.colliderect(tube_rectreverse):
        return True
    
    return False


def update(dt, player: Player, tube_list: list[Tube]):
    """Update game entities based on delta time.
    
    Args:
        - dt (float): Time elapsed since the last update.
        - player (Player): The player object.
        - tube_list (list[Tube]): List of Tube objects.
    """
    player.update(dt)

    for tube in tube_list:
        if not tube.offscreen():
            tube.update(dt)


def collidate_player(player: Player, tube_list: list[Tube], tube_index: int):
    """Check if player collides with any tubes.
    
    Args:
        - player (Player): The player object.
        - tube_list (list[Tube]): List of Tube objects.
        - tube_index (int): Index of the current tube in the list.
    
    Returns:
        bool: True if player collides, False otherwise.
    """
    is_alive = True

    if get_collidate(player, tube_list, tube_index-1):
        max_score.append(tube_index)
        is_alive = False

    if tube_index > 2:
        if get_collidate(player, tube_list, tube_index-2):
            max_score.append(tube_index)
            is_alive = False

    return is_alive


def update_text_screen(score):
    """Update and display text on the screen.
    
    Args:
        score (int): Current score of the game.
    """
    try_text = font.render(f'Try: {int_try}', True, (255, 255, 255))
    screen.blit(try_text, (10, 10)) 

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 35)) 

    if len(max_score) > 0:
        max_score_text = font.render(f'Max Score: {max(max_score)}', True, (255, 255, 255))
        screen.blit(max_score_text, (10, 60)) 


def run():
    global game_quit, v_delta, x_velocity

    score = 0
    tube_index = 0
    tube_list = [Tube(v_delta, x_velocity)]
    player = Player()
    is_alive = True

    while is_alive:
        dt = clock.tick(FPS) / 100
        is_alive = handle_command(player)

        load_screen()

        update(dt, player, tube_list)

        if player.position[0] > tube_list[score].position[0] + Tube.size[0] : 
            score += 1

        if tube_list[-1].position[0] < 400:
            tube_list.append(Tube(v_delta, x_velocity))
            tube_index += 1

        player.draw(screen)
        for tube in tube_list:
            if not tube.offscreen():
                tube.draw(screen)

        is_alive = collidate_player(player, tube_list, tube_index)

        update_text_screen(score)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    while game_quit:
        int_try += 1
        v_delta = 200
        x_velocity = 0
        run()
