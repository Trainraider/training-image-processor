import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame_gui.elements.ui_button import UIButton
from pygame.rect import Rect

class SelectionBox:
    def __init__(self):
        self.location = [0,0]
        self.size = 512

    def draw(self):
        s = self.size/2
        rect1 = Rect((self.location[0]-s, self.location[1]-s), (self.size, self.size))
        rect2 = Rect((self.location[0]-s-1, self.location[1]-s-1), (self.size+2, self.size+2))
        black = (0,0,0)
        white = (255,255,255)
        pygame.draw.rect(screen, black, rect1, width=1)
        pygame.draw.rect(screen, white, rect2, width=1)

    def clamp(self, rect: Rect):
        s = self.size/2
        min_x = rect.left + s
        max_x = rect.right - s
        min_y = rect.top + s
        max_y = rect.bottom - s
        self.location[0] = clamp(self.location[0], min_x, max_x)
        self.location[1] = clamp(self.location[1], min_y, max_y)

class ScrollHandler:
    def __init__(self):
        self.frames_scrolled = 0
        self.y = 0
        self.rate = 0

    def start_frame(self):
        if self.y == 0:
            self.rate = 0
            self.frames_scrolled = 0
        self.y = 0
    def scroll(self, scroll_y):
        self.y = scroll_y
        self.frames_scrolled += 1
        self.rate += pow(self.frames_scrolled, 2) * scroll_y * (1/3)
        return self.rate

def clamp(x, _min, _max):
    return max(min(x,_max),_min)


# Initialize program
pygame.init()
if not pygame.image.get_extended():
    print("Warning: You are using a version of pygame with limited image format support.")
project_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
icon = pygame.image.load(os.path.join(project_folder, "assets", "emblem-photos-symbolic.svg"))
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Training Image Processor')
manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()
files = []
image = None
scaled_image = None
scroll_handler = ScrollHandler()
ui_bar_height = 25

#Initialize UI elements
button_rect = Rect(0, 0, 150, ui_bar_height)
button_rect.topright = (0,0)
open_folder_label = pygame_gui.elements.ui_label.UILabel(Rect(150, 0, 800 - 150, ui_bar_height),
                                                         "", manager)

folder_selection_button = UIButton(relative_rect=Rect(0, 0, 150, ui_bar_height),
                                   manager=manager, text='Open Folder')
selection_box = SelectionBox()

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

def ScaleImage():
    w, h = pygame.display.get_surface().get_size()
    h -= 25
    iw, ih = image.get_size()
    scale = min(w/iw, h/ih)
    scaled_size = (iw*scale,ih*scale)
    global scaled_image
    scaled_image = pygame.transform.smoothscale(image, scaled_size)


def LoadImage():
    loaded = False
    while not loaded:
        if files:
            try:
                global image
                image = pygame.image.load(os.path.join(open_folder, files[0])).convert().convert_alpha()
                ScaleImage()
                loaded = True
            except pygame.error as e:
                if str(e) != "Unsupported image format":
                    raise Exception().with_traceback(e.__traceback__)
                files.pop(0)
        else:
            break

def Draw():
    manager.update(time_delta)
    screen.fill((0,0,0))
    if image:
        screen.blit(scaled_image, (0, ui_bar_height))
    if image:
        selection_box.draw()
    manager.draw_ui(screen)
    pygame.display.update()


folder_selection = FolderSelection()
open_folder = ""


#Main loop
while True:
    time_delta = clock.tick(60) / 1000.0
    scroll_handler.start_frame()

    #Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.VIDEORESIZE:
            #Resize UI Elements
            w, h = pygame.display.get_surface().get_size()
            open_folder_label.set_dimensions((w-150,ui_bar_height))
            if image:
                ScaleImage()
            screen.fill((0,0,0))
            
            #Update Manager
            manager.set_window_resolution((w,h))

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == folder_selection_button:
                folder_selection.show()
            elif event.ui_element == folder_selection.ok_button:
                open_folder_label.set_text(folder_selection.current_directory_path)
                open_folder = folder_selection.current_directory_path
                files = [f for f in os.listdir(open_folder) if os.path.isfile(os.path.join(open_folder, f))]
                folder_selection.hide()
                LoadImage()
            elif event.ui_element == folder_selection.parent_directory_button:
                folder_selection.ok_button.enable()
            elif event.ui_element == folder_selection.home_button:
                folder_selection.ok_button.enable()
            elif event.ui_element == folder_selection.close_window_button or \
                 event.ui_element == folder_selection.cancel_button:
                    folder_selection = FolderSelection()

        elif event.type == pygame.MOUSEMOTION:
            if image:
                selection_box.location[0] = event.pos[0]
                selection_box.location[1] = event.pos[1]
                image_rect = Rect((0,ui_bar_height), scaled_image.get_size())
                selection_box.clamp(image_rect)

        elif event.type == pygame.MOUSEWHEEL:
            if image:
                w,h = scaled_image.get_size()
                selection_box.size = clamp(selection_box.size + scroll_handler.scroll(event.y), 100, min(w,h))
                image_rect = Rect((0,ui_bar_height), (w,h))
                selection_box.clamp(image_rect)

        manager.process_events(event)

    Draw()