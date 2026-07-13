from dataclasses import dataclass, field;
from app.models.evidence import Evidence;

@dataclass
class Character:
    __name:str;
    __health:int; # 18
    __power:int; # 3
    __evidences:list; # list

    @property
    def evidences(self):
        return self.__evidences;

    @property
    def name(self):
        return self.__name;

    @property
    def health(self):
        return self.__health;

    @property
    def power(self):
        return self.__power;

    @power.setter
    def power(self, new_value:int):
        if new_value<3 or new_value>18:
            return;
        self.__power = new_value;

    def take_damage(self, damage:int):
        if self.__health>3:
            self.__health = max(self.__health-damage, 3);
    
    def get_evidence(self, name:str)->Evidence:
        for evidence in self.__evidences:
            if evidence.name == name:
                return evidence;

    def take_evidence(self, evidence):
        if not evidence in self.__evidences:
            self.__evidences.append(evidence);
    
    def drop_evidence(self, evidence):
        if evidence in self.__evidences:
            self.__evidences.remove(evidence);
            return evidence;

    def is_dead(self)->bool:
        return self.__health<=3;

class NPC(Character):
    roles = {
        "friend":0,
        "enemy": 1,
    }
    def __init__(self, name:str, id:str, role:str, stats:dict={}):
        super().__init__(
            name, 
            stats.get('health', 18), 
            stats.get('power', 3), 
            stats.get('evidences', [])
        );
        self.__id = id;
        self.__role = role or "neutral";

    @property
    def role(self)->str:
        return self.__role;

    @property
    def id(self)->str:
        return self.__id;

class Monster(NPC):
    def __init__(self, name, id,  spectrum:str, stats = {}):
        super().__init__(name, id, NPC.roles['enemy'], stats),
        self.__spectrum = spectrum;

    @property
    def spectrum(self):
        return self.__spectrum;


class PlayerCharacter(Character):
    def __init__(self, name:str, stats:dict, abilities:list=None):
        super().__init__(name, stats['health'], stats['power'], stats['evidences']);
        self.__intelligence = stats['intelligence'] or 3;
        self.__abilities = abilities or [];
        self.__improvements = {
            "power":self.improve_power,
            "intelligence":self.improve_intelligence
        };
    
    @property
    def intelligence(self):
        return self.__intelligence;

    def improve(self, spectrum:str, increment:int):
        print(f"asked to improve spectrum \"{spectrum}\" with increment = {increment}");
        improvement = self.__improvements.get(spectrum);
        if not improvement:
            print(f"not found function to improve spectrum \"{spectrum}\"");
            return;
        improvement(increment);
        return increment;

    def improve_power(self, increment:int):
        print("increased power.");
        self.power+=increment

    def improve_intelligence(self, increment:int):
        print("increased intelligence.");
        self.__intelligence+=increment;

    def get_ability(self, name:str):
        for ability in self.__abilities:
            if ability.name == name:
                return ability;

    def pack(self)->dict:
        return {
            "health":self.health,
            "power":self.power,
            "evidences":[evidence.pack() for evidence in self.evidences],
            "intelligence":self.intelligence,
            "abilities":[ability.pack() for ability in self.__abilities]
        };
        



