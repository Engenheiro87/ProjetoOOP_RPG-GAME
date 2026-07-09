import pygame;
from app.models.screen_data import ScreenData;

class PygameService:
    WINDOW_DIMENSIONS = (500,500);
    COLORS = {
        "black": (25,25, 25),
        "white": (255,255,255),
        "dark-blue":(33, 47, 82),
        "bright-blue":(111, 173, 201),
    }
    def __init__(self, window, dependencies:dict={}):
        self.__dependencies = dependencies;
        self.__window = window;

        self.__H1 = pygame.font.SysFont(
            "Georgia",
            32
        );
        self.__H2 = pygame.font.SysFont(
            "Georgia",
            16,
        );
        self.__H3 = pygame.font.SysFont(
            "Georgia",
            13,
        );
        self.__H4 = pygame.font.SysFont(
            "Georgia",
            8,
        );

    def draw_screen(self, screen:ScreenData):
        self.fill_background(screen.background);
        # Location
        self.render_text( 
            screen.location, 
            self.color_from_string("white"),
            .07
        );
        # Location description
        self.render_text(
            screen.location_description,
            self.color_from_string("white"),
            .17,
            font=self.__H2
        );

        # Character talking:
        self.render_text(
            screen.character,
            self.color_from_string("white"),
            font=self.__H3
        );
        # Dialogue:
        self.render_text(
            screen.dialogue,
            self.color_from_string("white"),
            y=.55,
            font=self.__H3
        )

        # actions
        pygame.draw.line(
            self.__window,
            self.color_from_string("bright-blue"),
            self.convert_to_offset(.2, .75),
            self.convert_to_offset(.8, .75)
        );

        actions_length = len(screen.actions);
        current = 1;

        for action in screen.actions:
            self.render_text(
                action,
                self.color_from_string("white"),
                y = .75 + .15*current/actions_length,
                x = .5,
                font = self.__H4
            );
            current+=1;

    def convert_to_offset(self, x:float, y:float)->tuple[int, int]:
        return (
            int(x*PygameService.WINDOW_DIMENSIONS[0]),
            int(y*PygameService.WINDOW_DIMENSIONS[1])
        );

    def render_text(self, text:str, color:tuple, y:float=.5, x:float=.5, font=None):
        if not font:
            font = self.__H1;
        
        text = font.render(
            text,
            True,
            color
        );

        rect:pygame.rect = text.get_rect(
            center = self.convert_to_offset(x, y)
            # center = (x if x is not None else PygameService.WINDOW_DIMENSIONS[0]//2, y)
        );

        pygame.draw.line(
            self.__window,
            self.color_from_string("white"),
            (rect.left, rect.top+rect.height+5),
            (rect.left+rect.width, rect.top+rect.height+5),
            width=1
        );

        self.__window.blit(
            text, 
            rect
        );

        return text;

    def draw_line(self):
        pass;
    
    def color_from_string(self, color_name:str, default:tuple=None)->tuple[int, int, int]|None:
        return PygameService.COLORS.get(color_name, default);

    def fill_background(self, color:str|tuple):
        if type(color) ==str:
            color = self.color_from_string(color, (25,25,25));
        self.__window.fill(color);
