
from typing import List, Dict, AnyStr
import requests
from services.base.llm_client import LLMClientBase
import time
import random
import httpx 
import asyncio

class AzureAIClient(LLMClientBase):
    def __init__(self, api:str, base_url:str, deployment_name:str, api_version:str, response_manager=None):
        super().__init__(api, base_url, response_manager=response_manager)
        self.api_version = api_version
        self.deployment_name = deployment_name
        self.max_retries=5
        self.base_delay=1.0

        # Headers
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api
        }

    def api_call(self, **kwargs) -> Dict:
        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.uri, headers=self.headers, json=kwargs["payload"])
                if response.status_code == 200:
                    return response.json()  # Return response if successful
                
                elif response.status_code == 429:
                        # Compute exponential backoff with jitter
                        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                        print(f"Rate limited (429). Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                else:
                    response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise ValueError(f"Request failed: {response.status_code} - {response.text}") from e
            

    async def async_api_call(self, **kwargs) -> Dict:
        async with httpx.AsyncClient() as client:  # Ensures proper connection management
            for attempt in range(self.max_retries):
                try:
                    response = await client.post(self.uri, headers=self.headers, json=kwargs["payload"])
                    
                    if response.status_code == 200:
                        return response.json()  # ✅ Successful response
                    
                    elif response.status_code == 429:
                        # Exponential backoff with jitter
                        delay = self.base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                        print(f"Rate limited (429). Retrying in {delay:.2f} seconds...")
                        await asyncio.sleep(delay)
                    else:
                        response.raise_for_status()  # Raise error for other status codes

                except httpx.HTTPStatusError as e:
                    raise ValueError(f"Request failed: {e.response.status_code} - {e.response.text}") from e
               
    
    
    

class GPTCompletionClient(AzureAIClient):

    def __init__(self, api, base_url, deployment_name, api_version, response_manager=None):
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

    async def call_async(self, **kwargs):
        payload = self.prepare_payload(**kwargs)
        return await self.async_api_call(payload=payload)
    
        
    def parse_response(self, response:Dict) -> List:
        msgs = []
        for choice in response["choices"]:
            msgs.append(choice["text"])
        return msgs

class GPTChatCompletionClient(AzureAIClient):
    def __init__(self, api, base_url, deployment_name, api_version, response_manager=None):
        super().__init__(api, base_url, api_version=api_version, deployment_name=deployment_name, response_manager=response_manager)
        self.uri = f"{self.base_url}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
       
        
    def prepare_payload(self, messages:List[Dict[str,str]],response_format:Dict = None, max_tokens:int = 300, choices:int = 1, temparture:float = 0.7, ):
        return {
            "messages": messages,
            "max_tokens": max_tokens,
            "n": choices,
            "temperature": temparture,
            "response_format": response_format

        }

    def call(self,**kwargs) -> Dict:
        if "messages" not in kwargs:
            raise ValueError("Missing required parameter: 'messages'")
        payload = self.prepare_payload(**kwargs)
        return self.api_call(payload=payload)
    
    async def call_async(self, **kwargs):
        payload = self.prepare_payload(**kwargs)
        return await self.async_api_call(payload=payload)


    def parse_response(self, response:Dict) -> List:
        msgs = []
        for choice in response["choices"]:
            msgs.append(choice["message"]["content"])
        return msgs
    