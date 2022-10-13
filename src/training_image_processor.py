import os, shutil
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.elements.ui_image import UIImage
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

    def image_rect(self):
        s = self.size/2
        rect = Rect((self.location[0]-s, self.location[1]-s), (self.size, self.size))
        rect.move_ip(0, -ui_bar_height)
        scale = image.get_size()[0]/scaled_image.get_size()[0]
        rect = Rect((rect.left*scale, rect.top*scale), (rect.width*scale, rect.height*scale))
        return rect

def ProcessedImage():
    rect = selection_box.image_rect()
    pimage = pygame.Surface((rect.width, rect.height))
    global image
    pimage.blit(image, (0,0), area=rect)
    pimage = pygame.transform.smoothscale(pimage, (512,512))
    return pimage

def ClickImage():
    processed_image = ProcessedImage()
    output_path = os.path.join(open_folder, 'outputs')
    originals_path = os.path.join(open_folder, 'originals')

    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass
    try:
        os.mkdir(originals_path)
    except FileExistsError:
        pass
    
    pygame.image.save(processed_image, os.path.join(output_path, files[0]))
    shutil.move(os.path.join(open_folder, files[0]), os.path.join(originals_path, files[0]))
    files.pop(0)
    LoadImage()

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
ui_row_height = 25
ui_bar_height = 50

#Initialize UI elements
button_rect = Rect(0, 0, 150, ui_bar_height)
button_rect.topright = (0,0)
open_folder_label = pygame_gui.elements.ui_label.UILabel(Rect(150, 0, 800 - 150, ui_row_height),
                                                         "", manager)

folder_selection_button = UIButton(relative_rect=Rect(0, 0, 150, ui_row_height),
                                   manager=manager, text='Open Folder')

clockwise_button = UIButton(Rect(0,ui_row_height,ui_row_height,ui_row_height), text='', manager=manager)
clockwise_icon = pygame.image.load(os.path.join(project_folder, 'assets', 'object-rotate-right-symbolic.svg'))
clockwise_button_image = UIImage(Rect(0,ui_row_height,ui_row_height,ui_row_height).inflate(-8,-8), clockwise_icon, manager)

cclockwise_button = UIButton(Rect(ui_row_height,ui_row_height,ui_row_height,ui_row_height), text='', manager=manager)
cclockwise_icon = pygame.image.load(os.path.join(project_folder, 'assets', 'object-rotate-left-symbolic.svg'))
cclockwise_button_image = UIImage(Rect(ui_row_height,ui_row_height,ui_row_height,ui_row_height).inflate(-8,-8), cclockwise_icon, manager)

fliph_button = UIButton(Rect(ui_row_height*2,ui_row_height,ui_row_height,ui_row_height), text='', manager=manager)
fliph_icon = pygame.image.load(os.path.join(project_folder, 'assets', 'object-flip-horizontal-symbolic.svg'))
fliph_button_image = UIImage(Rect(ui_row_height*2,ui_row_height,ui_row_height,ui_row_height).inflate(-8,-8), fliph_icon, manager)

flipv_button = UIButton(Rect(ui_row_height*3,ui_row_height,ui_row_height,ui_row_height), text='', manager=manager)
flipv_icon = pygame.image.load(os.path.join(project_folder, 'assets', 'object-flip-vertical-symbolic.svg'))
flipv_button_image = UIImage(Rect(ui_row_height*3,ui_row_height,ui_row_height,ui_row_height).inflate(-8,-8), flipv_icon, manager)

next_button = UIButton(Rect(ui_row_height*4,ui_row_height,ui_row_height,ui_row_height), text='', manager=manager)
next_icon = pygame.image.load(os.path.join(project_folder, 'assets', 'go-next-symbolic.svg'))
next_button_image = UIImage(Rect(ui_row_height*4,ui_row_height,ui_row_height,ui_row_height).inflate(-8,-8), next_icon, manager)

image_rect = Rect(0, ui_bar_height, 800, 600-ui_bar_height)
image_button = UIButton(image_rect, '', manager)
placeholder_image = pygame.Surface((1,1))
placeholder_image.fill((0,0,0))
image_element = UIImage(image_rect, placeholder_image, manager)

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
    h -= ui_bar_height
    iw, ih = image.get_size()
    scale = min(w/iw, h/ih)
    scaled_size = (iw*scale,ih*scale)
    global scaled_image
    scaled_image = pygame.transform.smoothscale(image, scaled_size)
    image_element.set_image(scaled_image)
    image_rect = Rect((0, ui_bar_height),scaled_size)
    image_button.set_dimensions(image_rect.size)
    image_element.set_dimensions(image_rect.size)


def LoadImage():
    loaded = False
    while not loaded:
        if files:
            try:
                global image
                image = pygame.image.load(os.path.join(open_folder, files[0])).convert().convert_alpha()
                ScaleImage()
                selection_box.size = min(scaled_image.get_size())
                loaded = True
                image_button.show()
            except pygame.error as e:
                if str(e) != "Unsupported image format":
                    raise Exception().with_traceback(e.__traceback__)
                files.pop(0)
        else:
            image = None
            image_element.set_image(placeholder_image)
            image_button.hide()
            break

def Draw():
    manager.update(time_delta)
    screen.fill((0,0,0))
    manager.draw_ui(screen)
    if image:
        selection_box.draw()
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
            open_folder_label.set_dimensions((w-150,ui_row_height))
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
            elif event.ui_element == clockwise_button:
                if image:
                    image = pygame.transform.rotate(image, -90)
                    ScaleImage()
            elif event.ui_element == cclockwise_button:
                if image:
                    image = pygame.transform.rotate(image, 90)
                    ScaleImage()
            elif event.ui_element == fliph_button:
                if image:
                    image = pygame.transform.flip(image, True, False)
                    ScaleImage()
            elif event.ui_element == flipv_button:
                if image:
                    image = pygame.transform.flip(image, False, True)
                    ScaleImage()
            elif event.ui_element == image_button:
                if image:
                    ClickImage()
            elif event.ui_element == next_button:
                if files:
                    files.pop(0)
                    LoadImage()
        elif event.type == pygame.MOUSEMOTION:
            if image:
                selection_box.location[0] = event.pos[0]
                selection_box.location[1] = event.pos[1]
                image_rect = Rect((0,ui_bar_height), scaled_image.get_size())
                selection_box.clamp(image_rect)

        elif event.type == pygame.MOUSEWHEEL:
            if image:
                pos = pygame.mouse.get_pos()
                w,h = scaled_image.get_size()
                selection_box.size = clamp(selection_box.size + scroll_handler.scroll(event.y), 100, min(w,h))
                selection_box.location[0] = pos[0]
                selection_box.location[1] = pos[1]
                image_rect = Rect((0,ui_bar_height), (w,h))
                selection_box.clamp(image_rect)


        manager.process_events(event)

    Draw()