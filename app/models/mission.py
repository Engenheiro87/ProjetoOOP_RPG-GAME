from dataclasses import dataclass, field

@dataclass
class Mission:
    mission_id: str
    display_name: str
    desc: str
    activation_flags: list
    completion_tags: list
    mission_type: str
    params: dict
    layer: int
    completed: bool = field(default=False)
    active: bool = field(default=False)

    def try_complete(self, flags: dict) -> bool:
        
        for tag in self.completion_tags:
            
            if not flags.get(tag, False):
                return False
        
       
        self.completed = True
        self.active = False
        return True

    def check_requirements(self, flags: dict) -> bool:
       
        if self.completed or self.active:
            return False

        
        for flag in self.activation_flags:
            if not flags.get(flag, False):
                return False
        
        return True
