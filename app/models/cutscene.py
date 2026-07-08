from dataclasses import dataclass, field
import pygame

@dataclass
class Cutscene:
    
    script: list

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
