from app.models.character import Monster
from app.models.cutscene import Cutscene;
from app.models.dice import Dice;
from random import randint;

class Fight:
    MONSTERS = (
        {
            "type": "Zombie",
            "spectrum":"power"
        }, 
        {
            "type": "Ghost",
            "spectrum":"intelligence"
        }
    );
    def __init__(self, dependencies:dict):
        self.__dependencies = dependencies;
        self.__monster_info = Fight.get_random_monster();
        self.__monster = Monster(
            self.__monster_info['type'],
            "new_monster",
            self.__monster_info['spectrum'],
            {
                "power":Dice().roll()
            }
        );
    
    @property
    def monster(self)->Monster:
        return self.__monster;

    def attack_monster(self)->bool:
        monster = self.__monster;
        spectrum = monster.spectrum;
        player_stats = self.__dependencies['get_player_stats']();
        player_skill = player_stats[spectrum];
        monster_skill = monster.power;
        lines = None;
        sucess = False;
        if monster_skill < player_skill:
            increase = self.__dependencies['increase_stat'](
                spectrum,
                1
            );
            lines = [
                f"nar/You've defeated \"{monster.name}\"!",
                f"stat/+ {increase} \"{str.upper(spectrum)}\" "
            ];
            sucess = True;
        else:
            damage = Dice().roll();
            lines = [f"nar/You've lost! Damage taken: {damage}"];
            self.__dependencies['damage_player'](damage)

        self.__dependencies['play_cutscene'](
            Cutscene(self.__dependencies['parse_lines'](lines))
        );
        return sucess;

    @staticmethod
    def get_random_monster()->dict:
        return Fight.MONSTERS[
            randint(0, len(Fight.MONSTERS)-1)
        ];
    
