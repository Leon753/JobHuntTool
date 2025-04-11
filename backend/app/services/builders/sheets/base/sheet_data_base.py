from abc import ABC, abstractmethod

class SheetDataInterface(ABC):
    @abstractmethod
    def update_row(
        self, 
        start_col: str, 
        end_col: str, 
        row: int, 
        values: list
    ): ...
    
    @abstractmethod
    def update_cell(
        self, 
        col: str, 
        row: int, 
        value
    ): ...
    
    @abstractmethod
    def build(self): ...
