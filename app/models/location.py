from dataclasses import dataclass, field;
from app.models.furniture import Furniture;
from app.models.character import NPC
from app.models.evidence import Evidence;

class Location:
    def __init__(self, loc_id:str, location_data:dict, npc_data:dict={}, furniture_data:dict={}):
        self.__location_id = loc_id;
        self.__fear_level = location_data.get("fear", 3);
        self.__name:str = location_data['display_name'];
        self.__furnitures:list[Furniture] = {
            furniture_name:Furniture(
                fur_data['default_data']["display_name"],
                [ # list of evidences
                    Evidence(
                        evidence_data['display_name'],
                        evidence_data.get("required_ability"),
                        evidence_data.get("required_level")
                    )
                    for evidence_name, evidence_data in fur_data['evidence_data'].items()
                ],
                fur_data['default_data'].get('damages', False)
                #missing blocked location
            )
            for furniture_name, fur_data in furniture_data.items()
        };
        # self.__furnitures:list[Furniture] = [Furniture(data) for data in location_data['furniture']];
        self.__npcs:dict[str:NPC] = {npc_name:NPC(**ndata) for npc_name, ndata in npc_data.items()};
        self.__connections:list[Location] = [];
        self.__description:str = location_data.get("description");
        self.__required_key:str|None = location_data.get("key", None);
        self.__blocked = location_data.get("blocked", False);

    @property
    def npcs(self):
        return self.__npcs;
    
    @property
    def name(self):
        return self.__name;

    @property
    def id(self):
        return self.__location_id;

    @property
    def connections(self):
        return self.__connections;

    @property
    def description(self):
        return self.__description;

    @property
    def blocked(self):
        return self.__blocked;

    @property
    def required_key(self):
        return self.__required_key;

    @property
    def furnitures(self):
        return self.__furnitures;

    @property
    def fear_level(self):
        return self.__fear_level;

    def is_connected_to(self, location:Location)->bool:
        return location!= self and location in self.__connections;

    def connect_to(self, location:Location):
        if not self.is_connected_to(location):
            self.__connections.append(location);

    def move_character_to(self, character:NPC):
        if not character in self.__npcs.values():
            self.__npcs[character.id] = character;
    
    def get_character(self, id:str)->NPC|None:
        return self.__npcs.get(id);

    def move_character_from(self, character:NPC):
        char_id = character.id;
        if self.__npcs.get(char_id):
            self.__npcs.pop(char_id);
    
    def get_furniture(self, furniture_name:str)->Furniture|None:
        return self.__furnitures.get(furniture_name);
        
