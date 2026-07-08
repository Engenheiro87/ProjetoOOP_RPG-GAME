from dataclasses import dataclass, field;

@dataclass
class ScreenData:
    location:str;
    background:str;

    character:str = field(default_factory=str);
    dialogue:str = field(default_factory=str);
    actions: dict = field(default_factory=dict);
    location_description: str = field(default_factory=str);
