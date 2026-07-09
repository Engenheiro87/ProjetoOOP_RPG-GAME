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
            if event.type == pygame.KEYDOWN:
                key = event.key;
                if key in game.keybinds: 
                    routed = game.keybinds[key];
                    if routed['state']():
                        routed['action']();
                elif game.options and (key in game.options):
                    game.pick_option(key);
    
        # draw screen
        pgs.draw_screen(ScreenData(
            game.current_act and game.current_act.current_location.name,
            "dark-blue",
            character=game.current_cutscene and game.current_cutscene.character+":",
            dialogue=game.current_cutscene and game.current_cutscene.dialogue,
            location_description=game.current_act and game.current_act.current_location.description,
            actions= game.options and [
                option['display']
                for key, option in game.options.items()
            ]  or game.current_cutscene and
            ["Enter - Next"] or
            [
                "M - Move to another room",
                "T - Talk to a character"
            ]
        ));
    
        pygame.display.flip();
    
        clock.tick(30);
    
    print("pygame quit running.");
    pygame.quit();

