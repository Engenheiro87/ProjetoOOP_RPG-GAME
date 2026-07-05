from dataclasses import dataclass, field;
from abc import ABC, abstractmethod;
from json import load, dump;
from copy import deepcopy;
from colorama import init, Fore;

init(autoreset=True);
class DataRecord(ABC):
    root = "app/controllers/db/";
    def __init__(self, file_path:str):
        self.__file_path:str = DataRecord.root+file_path;
        self.__data:dict = None;
        self.__read();
    
    @property
    def data(self):
        return self.__data;

    @data.setter
    def data(self, new_value):
        if type(new_value)!=dict:
            return;
        self.__data = new_value;

    @property
    def file_path(self):
        return self.__file_path;

    def __read(self):
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                self.__data = load(file);
        except:
            self.read_fallback();

    @abstractmethod
    def read_fallback(self):
        pass;

    def read_data(self, index:str=None, function=None, default:any=None)->any:
        if not index:
            return self.__data;
        if not index in self.__data:
            return default;
        if function:
            return function(self.__data[index]);
        return self.__data[index];

class DynamicData(DataRecord):
    def __init__(self, file_path:str, packing_function=None):
        self.__packing_function = packing_function;
        super().__init__(file_path);

    def read_fallback(self):
        print(f"fallback for dynamic data \"{self.file_path}\"");
        self.data = {};
        self.save();

    def save(self):
        if self.__packing_function is not None:
            data = self.__packing_function();
            self.data = data;
        with open(self.file_path, "w", encoding="utf-8") as file:
            dump(self.data, file, indent=4);

    def overwrite(self, data_name:str, new_value:any):
        self.data[data_name] = new_value;

class StaticData(DataRecord):
    def __init__(self, file_path:str):
        super().__init__(file_path);

    def read_fallback(self):
        raise FileNotFoundError(f"Could not find static file \"{self.file_path}\"");

    def clone_data(self, str)->any:
        original_data = self.read_data(str);
        return deepcopy(original_data);
