import pygame
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame_gui.elements.ui_button import UIButton
from pygame.rect import Rect

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()

file_selection_button = UIButton(relative_rect=Rect(350, 250, 100, 100),
                                 manager=manager, text='Select File')

while 1:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == file_selection_button:
                    file_selection = UIFileDialog(rect=Rect(0, 0, 300, 300), manager=manager, allow_picking_directories=True)

                if event.ui_element == file_selection.ok_button:
                    print(file_selection.current_file_path)

        manager.process_events(event)

    manager.update(time_delta)
    screen.blit(background, (0, 0))
    manager.draw_ui(screen)

    pygame.display.update()