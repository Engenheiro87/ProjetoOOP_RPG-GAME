from dataclasses import dataclass, field;
from app.models.evidence import Evidence;

@dataclass
class Furniture:
    __name:str;
    __evidences:list[Evidence];
    __damages:bool = field(default_factory=lambda:False);
    __blocked_location:str|None = field(default_factory=lambda:None);

    __inspected:bool = field(init=False, default_factory=lambda:False);

    # attributes

    @property
    def name(self):
        return self.__name;


    @property
    def evidences(self):
        return self.__evidences;

    # methods

    def inspect(self, stats:dict)->dict:
        self.__inspected = True;
        return {
            "evidences": {
                evidence.name:evidence for evidence in self.__evidences
                if evidence.is_visible(stats["abilities"])
            },
            "damages":self.__damages and not self.__inspected
        };

    def push(self, strength:int)->dict:
        pass;

    def get_evidence(self, evidence_name:str)->Evidence|None:
        for evidence in self.__evidences:
            if evidence.name == evidence_name:
                return evidence;

    def take_evidence(self, evidence:Evidence)->Evidence|None:
        if evidence in self.__evidences:
            self.__evidences.remove(evidence);
            return evidence;
