class Ability:
    def __init__(self, name:str, level:int=0):
        self.__name = name;
        self.__level = level;

    @property
    def level(self):
        return self.__level;

    @level.setter
    def level(self, new_value:int):
        if type(new_value)!=int:
            return;
        self.__level = new_value;

    def increment(self, increment:int):
        self.__level = min(self.__level+increment, 18);

    def activate(self)->dict:
        pass;

    def pack(self)->dict:
        return {
            "name":self.__name,
            "level":self.__level
        }