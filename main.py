import pygame;
from app.controllers.pygame_service import PygameService as PGS;
from app.controllers.game import Game;
from app.models.screen_data import ScreenData;

if __name__ == "__main__":
    # pygame stuff
    pygame.init();
    window = pygame.display.set_mode(PGS.WINDOW_DIMENSIONS);
    pygame.display.set_caption("Harry Potter: A Mystery at Hogwarts");
    clock = pygame.time.Clock();

    # instantiation
    pgs = PGS(window);
    game = Game();
    game.load_act(1); #<- temporarily.

    running = True;

    while running:
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.update_game_state("exit")
                running = False;
                break;
    
        # draw screen
        pgs.draw_screen(ScreenData(
            "Loading game...",
            "dark-blue",
            character="Character Name:",
            dialogue="Character dialogue here...",
            location_description="Location description",
            actions= {
                "E":"Talk to character",
                "F":"Inspect",
                "M":"Move to another Location"
            }
        ));
    
        pygame.display.flip();
    
        clock.tick(30);
    
    print("pygame quit running.");
    pygame.quit();

