from dataclasses import dataclass, field;
from app.models.location import Location;
from app.controllers.data_record import StaticData;

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
    __current_layer:int = field(init=False, default_factory=lambda:0);

    #############################################
    # attributes for bash testing

    @property
    def current_location(self)->Location:
        return self.__current_location;

    #############################################


    def load(self):
        self.__loaded_locations = {
            loc_name:Location(self.__dependencies['get_loc_data'](loc_name))
            for loc_name in self.__dependencies['get_game_def']().read_data('locations')
        };
        self.__load_connections();
        self.__current_location = self.__loaded_locations[self.__default_data.read_data("starting_location")];
        print(f"Set current location as {self.__current_location.name}");
        

    def __load_connections(self):
        for loc_name, location in self.__loaded_locations.items():
            location:Location = location;
            for connected_name in self.__dependencies['get_loc_data'](loc_name)['connections']:
                other_location:Location = self.__loaded_locations.get(connected_name);
                if other_location:
                    location.connect_to(other_location);

    def start(self, layer:int=0):
        self.load();

    def destroy(self):
        print("asked to destroy act.");

    def talk_to_npc(self, name:str)->dict:
        pass;

    def travel_to(self, loc_name:str)->tuple[bool, str]:
        target:Location = self.__loaded_locations.get(loc_name);
        if not target:
            return False, "Location does not exist.";
        target_name = target.name;
        current_location = self.__current_location;
        if current_location.is_connected_to(target):
            self.__current_location = target;
            print(f"moved to {target_name}\nNext moves:");
            for connected in self.__current_location.connections:
                print(f"MOVE TO - \"{connected.name}\"");
            return True, f"Moved to {target_name}";
        else:
            return False, f"{target_name} isn't connected to {current_location.name}";

    def inspect(self, furniture_name:str)->dict:
        pass;

    def grab_evidence(self, furniture_name:str, evidence_name:str)->dict:
        pass;

    def on_event(self, action:str, params:dict):
        pass;

    def progress_story(self):
        pass;

    def get_flag(self, flag_name:str):
        return self.__flags.get(flag_name);

    def add_flag(self, flag_name:str, default_value:bool=True):
        self.__flags[flag_name] = default_value;

    def change_flag(self, flag_name:str, new_value:bool):
        self.__flags[flag_name] = new_value;
