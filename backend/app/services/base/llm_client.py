from abc import ABC, abstractmethod
from typing import List, Dict, AnyStr, Union
from services.base.llm_response_manager import LLMResponseManager

class LLMClientBase(ABC):
    def __init__(self, api:str, base_url:str, response_manager:LLMResponseManager=None):
        self.api = api 
        self.base_url = base_url
        self.response_manager = response_manager


    @abstractmethod
    def prepare_payload(self, **kwargs):
        pass

    @abstractmethod
    def call(self, **kwargs):
        pass

    @abstractmethod
    def parse_response(self, **kwargs) ->List:
        pass

    def add_memory(self, **kwargs ) -> None:
        self.response_manager.add_response(**kwargs)

    
    def get_history(self) -> LLMResponseManager:
        return self.response_manager.messages