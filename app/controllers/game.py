from app.controllers.data_record import StaticData, DynamicData;
from app.controllers.act import Act;
from app.models.player import Player;
from app.models.character import PlayerCharacter;
from app.models.evidence import Evidence;
from app.models.ability import Ability;

class Game:
    def __init__(self):
        self.__player = Player();
        self.__current_act = None;
        self.__data = {
            "game_data" : DynamicData("game.json"),
            "game_default":StaticData("game_default.json"),
            "evidence_default":StaticData("evidence_default.json"),
            "player_data": DynamicData("player.json", self.__player.pack),
        };
        self.__act_dependencies = {
            "get_game_def":lambda: self.__data["game_default"],
            "get_loc_data":self.get_location_data,
            "get_char_data":self.get_char_data,
            "get_player_evidence":self.get_player_evidence,
            "get_player_stats":self.get_player_stats,
            "play_cutscene":self.play_cutscene,
            "get_evidence_data":self.get_evidence_data,
        };
        self.__game_state = "N/A";
        self.start();

    ##############################################################
    # attributes (for bash testing)
    @property
    def player(self):
        return self.__player;

    @property
    def act(self):
        return self.__current_act;
    ##############################################################
    
    #methods
    def start(self):
        print("starting game.");
        self.reload_character();
        return self;

    def increase_ability(self, name:str, increment:float):
        pass;

    def destroy(self):
        for dt_name, data in self.__data.items():
            if type(data) == DynamicData:
                print(f"Saving DynamicData \"{dt_name}\"");
                data.save();

    def read_game_data(self, data_name:str)->StaticData|DynamicData:
        return self.__data.get(data_name, None);

    def upload_game_data(self, data_name:str, data:StaticData|DynamicData):
        data_type = type(data);
        if data_type!=StaticData and data_type!=DynamicData:
            return;
        self.__data[data_name] = data;
    

    def save_act_data(self, act_number:int, act_data:dict):
        game_data:DynamicData = self.read_game_data("game_data");
        game_data.overwrite(f"act_{act_number}", act_data);
        print("Saving act data...");
        game_data.save();
        print("Saved!");

    def load_act(self, act_number:int):
        if self.__current_act:
            self.__current_act.destroy();
        game_data:DynamicData = self.read_game_data("game_data");
        act = Act(
            self.__act_dependencies,
            act_number,
            StaticData(f"act_data/act{act_number}.json"),
            game_data.read_data(f"act{act_number}")
        );
        self.__current_act = act;
        act.start();

    def update_game_state(self, new_state:str):
        self.__game_state = new_state;

    def translate_input(self, input:str):
        pass;

    def reload_character(self):
        player_data = self.read_game_data("player_data");
        stats = {
            "health":18,
            "power":player_data.read_data("power", int, 3),
            "evidences":[Evidence(data) for data in player_data.read_data("evidences", default=[])],
            "intelligence":player_data.read_data("intelligence", default=3)
        };
        new_character = PlayerCharacter(
            self.__player.id,
            stats,
            [Ability(data['name'], data['level']) for data in player_data.read_data("abilities", default=[])]
        );
        self.__player.set_character(new_character);
    
    def damage_player(self, damage:int):
        if not self.__player:
            raise Exception("No player instantiated to be damaged.");
        if self.__player.character.is_dead():
            print("player is already dead.");
            return;
        self.__player.character.take_damage(damage);
        if self.__player.character.is_dead():
            print("player died.");
    
    def prompt_player(self, data:dict):
        pass;

    def get_location_data(self, location_name:str)->dict:
        return StaticData(
            f"location_data/{location_name}.json"
        ).data;

    def get_char_data(self, char_id:str)->dict:
        return StaticData(
            f"character_data/{char_id}.json"
        ).data;

    def get_player_evidence(self, evidence_name:str)->Evidence:
        if not self.__player:
            raise Exception("Attempt to perform a 'player_has_evidence' check without a player instantiated.");
        return self.__player.character.get_evidence(evidence_name);

    def play_cutscene(self, script:list):
        game_default:StaticData = self.__data["game_default"];
        char_tags:dict = game_default.read_data("char_tags");
        for line in script:
            if not "/" in line:
                return print(f"No \"/\" in line to separate char_name/line\nLINE=  {line}");
            tag, line = line.strip().split("/");
            print(f"{char_tags.get(tag, "???")}: {line}")
            input();

    def get_player_stats(self)->dict:
        return self.__player.character.pack();

    def get_evidence_data(self, evidence_name:str)->dict:
        return self.__data["evidence_default"].read_data(evidence_name);
