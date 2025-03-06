from abc import ABC, abstractmethod
from typing import List, Dict, AnyStr, Union
import requests

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

class InMemoryResponseManager(LLMResponseManager):
    def __init__(self):
        """Initialize an empty dict to store responses."""
        self.messages: List[Dict[str, str]] = []  # prompt and response pair, if multiple choices then a list  
        

    def add_response(self, **kwargs):
        role = kwargs.get("role")
        if not role in ["system", "user", "assistant"]:
            raise ValueError(f"Role in correct type: VALID TYPES: [system, user, assistant] give {role}")
        
        self.messages.append({"role": role, "content": kwargs['content']})
    
    def get_responses(self) -> List[Dict[str, str]]:
        return self.messages
    
    def __getitem__(self, index):
        """Common method to retrieve a specific item by index."""
        if 0 <= index < len(self.messages):
            return self.messages[index]
        else:
            raise IndexError("Response index out of range.")
        
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


class AzureAIClient(LLMClientBase):
    def __init__(self, api:str, base_url:str, deployment_name:str, api_version:str, response_manager=None):
        super().__init__(api, base_url, response_manager=response_manager)
        self.api_version = api_version
        self.deployment_name = deployment_name
        

        # Headers
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api
        }

    def api_call(self, **kwargs) -> Dict:
        response = requests.post(self.uri, headers=self.headers, json=kwargs["payload"])
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Request failed: {response.status_code} - {response.text}") from e
        
        return response.json()

    
    
    

class GPTCompletionClient(AzureAIClient):
    def __init__(self, api, base_url, api_version, deployment_name, response_manager=None):
        super().__init__(api, base_url, api_version, deployment_name, response_manager)
        self.uri = f"{base_url}/openai/deployments/{deployment_name}/completions?api-version={api_version}"

    def prepare_payload(self, prompt:str, max_tokens:int = 300, choices:int = 1, temparture:float = 0.7):
         # Payload for chat/completions
        return {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "n": choices,
            "temperature": temparture
        }
        
    def call(self, **kwargs):
        if "prompt" not in kwargs:
            raise ValueError("Missing required parameter: 'prompt'")
        
        payload = self.prepare_payload(**kwargs)
        return self.api_call(payload=payload)

        
    def parse_response(self, response:Dict) -> List:
        msgs = []
        for choice in response["choices"]:
            msgs.append(choice["text"])
        return msgs

class GPTChatCompletionClient(AzureAIClient):
    def __init__(self, api, base_url, api_version, deployment_name, response_manager=None):
        super().__init__(api, base_url, api_version=api_version, deployment_name=deployment_name, response_manager=response_manager)
        self.uri = f"{self.base_url}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
       
        
    def prepare_payload(self, messages:List[Dict[str,str]],json_schema:Dict = None, max_tokens:int = 300, choices:int = 1, temparture:float = 0.7, ):
        return {
            "messages": messages,
            "max_tokens": max_tokens,
            "n": choices,
            "temperature": temparture,
            # "response_format": {
            #     "type": "json_schema",
            #     "json_schema": json_schema # need to update
            # }

        }

    def call(self,**kwargs) -> Dict:
        if "messages" not in kwargs:
            raise ValueError("Missing required parameter: 'messages'")
        payload = self.prepare_payload(**kwargs)
        return self.api_call(payload=payload)
        
    
    def parse_response(self, response:Dict) -> List:
        msgs = []
        for choice in response["choices"]:
            msgs.append(choice["message"]["content"])
        return msgs
    