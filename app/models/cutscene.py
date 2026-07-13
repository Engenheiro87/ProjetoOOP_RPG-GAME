from dataclasses import dataclass, field
import pygame

@dataclass
class Cutscene:
    
    __script: list[dict];
    __callable:callable|None = field(default_factory=lambda:None);

    character:str = field(init=False, default_factory=str);
    dialogue:str = field(init=False, default_factory=str);
    __iteration:int = field(init=False, default_factory=lambda: -1);

    @property
    def finished(self)->bool:
        return self.__iteration>=len(self.__script)

    def run(self, screen) -> None:
       
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 24)
        
        
        text_color = (255, 255, 255)
        bg_color = (0, 0, 0)

       
        for dialog_line in self.script:
            for character_name, text in dialog_line.items():
                
                
                display_text = f"{character_name}: {text}"
                text_surface = font.render(display_text, True, text_color, bg_color)
                
                
                screen.fill(bg_color)
                screen.blit(text_surface, (50, 250)) 
                pygame.display.flip() 
                
                
                pygame.time.delay(3000)
    
    def next(self):
        self.__iteration+=1;
        if self.finished:
            if self.__callable:
                self.__callable();
            return;
        self.character, self.dialogue = self.__script[self.__iteration];