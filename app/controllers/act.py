from dataclasses import dataclass, field;
from app.models.location import Location;
from app.models.furniture import Furniture;
from app.controllers.data_record import StaticData;
from app.models.character import NPC;
from app.models.cutscene import Cutscene;

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

    @property
    def default_data(self)->StaticData:
        return self.__default_data;


    #############################################


    def load(self):
        self.__loaded_locations = {
            loc_name:self.load_location(loc_name)
            for loc_name in self.__dependencies['get_game_def']().read_data('locations')
        };
        self.__load_connections();
        self.__current_location = self.__loaded_locations[self.__default_data.read_data("starting_location")];
    
    def load_location(self, loc_id:str)->Location:
        # location data
        loc_data = self.__dependencies['get_loc_data'](loc_id);
        act_location_data = self.__default_data.read_data("locations").get(loc_id, {});

        # npc data
        location_npc_list = act_location_data.get("npcs", []);
        npc_data = {
            char_name:self.__dependencies['get_char_data'](char_name)
            for char_name in location_npc_list
        };

        # furniture data
        default_location_furniture = loc_data['furniture']; # list de nomes de móveis apenas DO LOCAL
        location_evidence_dict = act_location_data.get("evidences", {}); # dicionário furniture-id : [evidence_id]
        default_furniture_data:dict = self.__dependencies["get_game_def"]().read_data("furniture"); # dicionário furniture-id : {default furniture data}
        furniture_data = {
            name:{ # <- furniture data
                "default_data":default_furniture_data.get(name), # <- furniture data still
                "evidence_data":{ # <- evidences data
                    evidence_name:self.__dependencies["get_evidence_data"](evidence_name)
                    for evidence_name in location_evidence_dict.get(name, [])
                }
            }
            for name in default_location_furniture # name = wooden-desk
        };

        return Location(loc_data, npc_data, furniture_data);

    def __load_connections(self):
        for loc_name, location in self.__loaded_locations.items():
            for connected_name in self.__dependencies['get_loc_data'](loc_name)['connections']:
                other_location:Location = self.__loaded_locations.get(connected_name);
                if other_location:
                    location.connect_to(other_location);

    def start(self, layer:int=0):
        self.load();
        self.progress_story();

    def destroy(self):
        print("asked to destroy act.");

    def talk_to_npc(self, char_id:str):
        npc = self.__current_location.get_character(char_id);
        if not npc:
            return False, "missing npc";

        cutscene = self.get_cutscene(char_id, self.__current_layer) or {};
        self.__dependencies['play_cutscene'](
            Cutscene(self.parse_lines(cutscene.get("lines", [f"{char_id}/..."])))
        );

        if cutscene.get("moveto"):
            self.teleport(npc, self.__loaded_locations[cutscene['moveto']]);
        if cutscene.get("progress"):
            self.progress_story();
    
    def parse_lines(self, lines:list[str])->list:
        char_tags = self.__dependencies['get_char_tags']();
        def parse_line(line:str)->tuple:
            tag, line = line.strip().split("/");
            return char_tags.get(tag, "???"), line
        return [
            parse_line(line)
            for line in lines
        ];
    
    def get_cutscene(self, char_id:str, layer:int)->dict|None:
        char_data = self.__default_data.read_data("characters").get(char_id);
        if not char_data or not char_data.get("dialogues"):
            return;
        dialogues = char_data['dialogues'];
        return dialogues.get(str(layer));
    
    def teleport(self, npc:NPC, location:Location):
        print(f"Teleporting \"{npc.name}\" to \"{location.name}\"");
        self.__current_location.move_character_from(npc);
        location.move_character_to(npc);

    def travel_to(self, loc_name:str)->tuple[bool, str|dict]:
        target:Location = self.__loaded_locations.get(loc_name);
        if not target:
            return False, "Location does not exist.";
        if target.blocked:
            self.__dependencies["play_cutscene"](
                Cutscene(self.parse_lines(["nar/This path is blocked."]))
            );
            return False, "blocked";
        elif target.required_key:
            key = target.required_key;
            if not self.__dependencies['get_player_evidence'](key):
                self.__dependencies["play_cutscene"](
                    Cutscene(self.parse_lines([f"nar/You need \"{key}\" to unlock this place."]))
                );
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

    def inspect(self, furniture_name:str)->tuple[bool, str]|dict:
        furniture = self.__current_location.get_furniture(furniture_name);
        if not furniture:
            return False, "not found";
        stats = self.__dependencies["get_player_stats"]();
        result = furniture.inspect(stats);
        return result;

    def grab_evidence(self, furniture_name:str, evidence_name:str)->dict:
        pass;

    def on_event(self, action:str, params:dict):
        pass;

    def progress_story(self, increment:int=1):
        self.__current_layer+=increment;
        layer_now = self.__current_layer;

        layer_data = self.__default_data.read_data("layers").get(str(layer_now));
        if not layer_data:
            return;
        cutscene = layer_data.get("cutscene");
        if cutscene:
            self.__dependencies["play_cutscene"](
                Cutscene(self.parse_lines(cutscene))
            );


    def get_flag(self, flag_name:str):
        return self.__flags.get(flag_name);

    def add_flag(self, flag_name:str, default_value:bool=True):
        self.__flags[flag_name] = default_value;

    def change_flag(self, flag_name:str, new_value:bool):
        self.__flags[flag_name] = new_value;

    def get_travel_options(self):
        location_options = {
            loc_id:location
            for loc_id, location in self.__loaded_locations.items()
            if location in self.__current_location.connections
        };
        return {
            48+i:{
                "display":f"{i} - Travel to {self.__loaded_locations[key].name}",
                "action":lambda k=key: self.travel_to(k),
                "key":key
            }
            for i, key in enumerate(location_options, start=1)
        };

    def get_dialogue_options(self):
        dialogue_options = {
            char_id:character
            for char_id, character in self.__current_location.npcs.items()
            # if self.get_cutscene(char_id, self.__current_layer)
        };
        return {
            48+i:{
                "display":f"{i} - Talk to {self.__current_location.npcs[key].name}",
                "action":lambda k=key: self.talk_to_npc(k),
                "key":key
            }
            for i, key in enumerate(dialogue_options, start=1)
        };
