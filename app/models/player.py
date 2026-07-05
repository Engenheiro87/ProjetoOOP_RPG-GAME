from uuid import uuid4;
from app.models.character import PlayerCharacter

class Player:
    def __init__(self, id:str=None):
        self.__id = id or str(uuid4());
        self.__character = None;
    
    @property
    def id(self):
        return self.__id;

    @property
    def character(self):
        return self.__character;
    
    def set_character(self, character:PlayerCharacter):
        print(f"New character being set for player \"{self.id}\" = {character}");
        self.__character = character;

    def pack(self)->dict:
        character:PlayerCharacter = self.__character;
        if not character:
            return {};
        return {
            "power":character.power,
            "evidences":[evidence.pack() for evidence in character.evidences],
            "intelligence":character.intelligence,
        }