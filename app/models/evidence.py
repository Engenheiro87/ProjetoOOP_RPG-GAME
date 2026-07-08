from dataclasses import dataclass, field;
from uuid import uuid4;

@dataclass
class Evidence:
    __name:str;
    __required_ability:str = field(default_factory=lambda:None);
    __required_level:int = field(default_factory=lambda:None);

    __read:bool = field(init=False, default_factory=lambda:False);
    __id:str = field(init=False, default_factory=lambda:str(uuid4()));
    #^^^ verificar necessidade
    
    # attributes
    @property
    def name(self)->str:
        return self.__name;

    @property
    def required_ability(self)->str:
        return self.__required_ability;

    @property
    def required_level(self)->int:
        return self.__required_level;

    @property
    def id(self)->str:
        return self.__id;

    # methods
    def pack(self)->dict:
        return {
            "name":self.__name,
            "required_ability":self.__required_ability,
            "required_level":self.__required_level
        };

    def is_visible(self, abilities:list)->bool:
        for ability in abilities:
            name = ability.name;
            level = ability.level;
            if name == self.required_ability and level == self.required_level:
                return True;
        return False;
