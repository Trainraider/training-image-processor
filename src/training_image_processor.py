import pygame
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame_gui.elements.ui_button import UIButton
from pygame.rect import Rect

# Initialize program
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()

#Initialize UI elements
button_rect = Rect(0, 0, 150, 25)
button_rect.topright = (0,0)
open_folder_label = pygame_gui.elements.ui_label.UILabel(Rect(150, 0, 800 - 150, 25),
                                                         "", manager)

folder_selection_button = UIButton(relative_rect=Rect(0, 0, 150, 25),
                                   manager=manager, text='Open Folder')
def FolderSelection():
    dialog = UIFileDialog(rect=Rect(0, 0, 600, 400), manager=manager,
                                allow_picking_directories=True,
                                allow_existing_files_only=False,
                                visible=0)
    dialog.resizable = True
    dialog.set_display_title("Open a Directory")
    dialog.enable_close_button = False
    dialog.ok_button.enable()
    bsize = (25,25)
    dialog.parent_directory_button.set_dimensions(bsize)
    dialog.home_button.set_dimensions(bsize)
    dialog.refresh_button.set_dimensions(bsize)
    dialog.delete_button.kill()
    dialog.rebuild()
    return dialog

def Draw():
    manager.update(time_delta)
    screen.fill((0,0,0))
    manager.draw_ui(screen)
    pygame.display.update()


folder_selection = FolderSelection()
open_folder = ""


#Main loop
while True:
    time_delta = clock.tick(60) / 1000.0

    #Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.VIDEORESIZE:
            #Resize UI Elements
            w, h = pygame.display.get_surface().get_size()
            open_folder_label.set_dimensions((w-150,25))
            screen.fill((0,0,0))
            
            #Update Manager
            manager.set_window_resolution((w,h))

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == folder_selection_button:
                folder_selection.show()
            elif event.ui_element == folder_selection.ok_button:
                open_folder_label.set_text(folder_selection.current_directory_path)
                open_folder = folder_selection.current_directory_path
                folder_selection.hide()
            elif event.ui_element == folder_selection.close_window_button or \
                 event.ui_element == folder_selection.cancel_button:
                    folder_selection = FolderSelection()

        manager.process_events(event)

    Draw()