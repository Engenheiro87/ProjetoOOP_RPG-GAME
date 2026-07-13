from dataclasses import dataclass, field;

@dataclass
class OptionTable:
    __options: dict;
    __block_escape: bool = field(default_factory=lambda:False);

    @property
    def block_escape(self):
        return self.__block_escape;

    def get_options(self)->dict:
        return self.__options;

    def get_option(self, key:int)->dict|None:
        return self.__options.get(key);
