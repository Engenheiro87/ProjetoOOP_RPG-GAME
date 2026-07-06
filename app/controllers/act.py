from dataclasses import dataclass, field;
from app.models.location import Location;
from app.controllers.data_record import StaticData;
from app.models.character import NPC;

@dataclass
class Act:
    __dependencies:dict;
    __act_number:int;
    __default_data:StaticData;
    __act_data:dict = field(default_factory=dict)

    __loaded_locations:dict = field(init=False, default_factory=dict),
    __current_location:Location|None = field(init=False, default_factory=lambda: None);
    __missions:list = field(init=False, default_factory=list);
    __flags:dict = field(init=False, default_factory=dict);
    __current_layer:int = field(init=False, default_factory=lambda:-1);

    #############################################
    # attributes
    @property
    def act_number(self)->int:
        return self.__act_number;

    @property
    def current_location(self)->Location:
        return self.__current_location;


    #############################################


    def load(self):
        self.__loaded_locations = {
            loc_name:self.load_location(loc_name)
            for loc_name in self.__dependencies['get_game_def']().read_data('locations')
        };
        self.__load_connections();
        self.__current_location = self.__loaded_locations[self.__default_data.read_data("starting_location")];
        print(f"Set current location as {self.__current_location.name}");
    
    def load_location(self, loc_id:str)->Location:
        loc_data = self.__dependencies['get_loc_data'](loc_id);
        act_npc_data = self.__default_data.read_data("npcs");
        location_npc_list = act_npc_data.get(loc_id) or [];
        npc_data = {
            char_name:self.__dependencies['get_char_data'](char_name)
            for char_name in location_npc_list
        };
        return Location(loc_data, npc_data);

    def __load_connections(self):
        for loc_name, location in self.__loaded_locations.items():
            location:Location = location;
            for connected_name in self.__dependencies['get_loc_data'](loc_name)['connections']:
                other_location:Location = self.__loaded_locations.get(connected_name);
                if other_location:
                    location.connect_to(other_location);

    def start(self, layer:int=0):
        self.load();
        self.progress_story();

    def destroy(self):
        print("asked to destroy act.");

    def talk_to_npc(self, char_id:str)->tuple[bool, str]|dict:
        npc = self.__current_location.get_character(char_id);
        if not npc:
            return False, "missing npc";
        cutscene = self.get_cutscene(char_id, self.__current_layer);
        self.__dependencies["play_cutscene"](cutscene['lines']);
        if cutscene.get("moveto"):
            self.teleport(npc, self.__loaded_locations[cutscene['moveto']]);

    def get_cutscene(self, char_id:str, layer:int)->dict|None:
        char_data = self.__default_data.read_data("characters").get(char_id);
        if not char_data or not char_data.get("dialogues"):
            return;
        dialogues = char_data['dialogues'];
        if len(dialogues)<layer+1:
            return;
        return dialogues[layer];
    
    def teleport(self, npc:NPC, location:Location):
        print(f"Teleporting \"{npc.name}\" to \"{location.name}\"");
        self.__current_location.move_character_from(npc);
        location.move_character_to(npc);

    def travel_to(self, loc_name:str)->tuple[bool, str|dict]:
        target:Location = self.__loaded_locations.get(loc_name);
        if not target:
            return False, "Location does not exist.";
        if target.blocked:
            return False, "blocked";
        elif target.required_key:
            key = target.required_key;
            if not self.__dependencies['get_player_evidence'](key):
                return False, {
                    "required_key":key
                };
        current_location = self.__current_location;
        if current_location.is_connected_to(target):
            self.__current_location = target;
            return True, {
                "options":
                {
                    location.name:loc_name 
                    for loc_name, location in self.__loaded_locations.items()
                    if target.is_connected_to(location)
                },
                "description":target.description
            }; # retorna True (sucesso) e as próximas opções no formato NOME FANTASIA : ID.
        else:
            return False, f"not_connected";

    def inspect(self, furniture_name:str)->dict:
        pass;

    def grab_evidence(self, furniture_name:str, evidence_name:str)->dict:
        pass;

    def on_event(self, action:str, params:dict):
        pass;

    def progress_story(self, increment:int=1):
        self.__current_layer+=increment;
        layer_now = self.__current_layer;

        layer_data = self.__default_data.read_data("layers")[layer_now];
        cutscene = layer_data.get("cutscene");
        if cutscene:
            self.__dependencies["play_cutscene"](cutscene);


    def get_flag(self, flag_name:str):
        return self.__flags.get(flag_name);

    def add_flag(self, flag_name:str, default_value:bool=True):
        self.__flags[flag_name] = default_value;

    def change_flag(self, flag_name:str, new_value:bool):
        self.__flags[flag_name] = new_value;
