from abc import ABC, abstractmethod
from typing import List, Dict, AnyStr, Union

class LLMResponseManager(ABC):
    """
        Add history from LLM to the manager.
        
        :role: SYSTEM, USER, ASSITANT.
    """
    @abstractmethod
    def add_response(self, role: str, content: str) -> None:
        pass
    """
        Returns history of LLMs chat
    """
    
    @abstractmethod
    def get_responses(self) -> List[str]:
        pass
    
    """
        Allow indexing into the history list to retrieve an Interaction object.
        
        :param index: The index of the desired interaction.
        :return: The Interaction object at the specified index.
    """
    @abstractmethod
    def __getitem__(self, index:int) -> Dict[str, str]:
        pass
