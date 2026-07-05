from dataclasses import dataclass, field;
from app.models.furniture import Furniture;
from app.models.character import NPC

class Location:
    def __init__(self, data:dict):
        self.__name:str = data['display_name'];
        self.__furnitures:list[Furniture] = [Furniture(data) for data in data['furniture']];
        self.__npcs:dict[str:NPC] = {npc_name:NPC(**ndata) for npc_name, ndata in data['npcs'].items()}
        self.__connections:list[Location] = [];
        self.__description:str = data.get("description");
        self.__required_key:str|None = data.get("key", None);
        self.__blocked = data.get("blocked", False);
    
    @property
    def name(self):
        return self.__name;

    @property
    def connections(self):
        return self.__connections;

    def is_connected_to(self, location:Location)->bool:
        return location!= self and location in self.__connections;

    def connect_to(self, location:Location):
        if not self.is_connected_to(location):
            self.__connections.append(location);

    def move_character_to(self, character:NPC):
        if not character in self.__npcs:
            self.__npcs.append(character);
    
    def get_character(self, char_name:str)->NPC|None:
        for character in self.__npcs:
            if character.name == char_name:
                return character;

    def move_character_from(self, character:NPC):
        if character in self.__npcs:
            self.__npcs.remove(character);

    def get_furniture(self, furniture_name:str)->Furniture|None:
        for furniture in self.__furnitures:
            if furniture.name == furniture_name:
                return furniture;