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
            "player_data": DynamicData("player.json", self.__player.pack),
            "character_data" : StaticData("characters.json"),
        };
        self.__act_dependencies = {
            "get_game_def":lambda: self.__data["game_default"],
            "get_loc_data":self.get_location_data,
        };
        self.__game_state = "N/A";
        self.start();

    def start(self):
        print("starting game.");
        self.reload_character();
        return self;

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

    def get_location_data(self, location_name:str)->dict:
        return StaticData(
            f"location_data/{location_name}.json"
        ).data;
