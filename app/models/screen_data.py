from dataclasses import dataclass, field;

@dataclass
class ScreenData:
    location:str;
    background:str;

    announcement:str = field(default_factory=str);
    character:str = field(default_factory=str);
    dialogue:str = field(default_factory=str);
    actions: tuple = field(default_factory=tuple);
    location_description: str = field(default_factory=str);
    hint:str = field(default_factory=str);
